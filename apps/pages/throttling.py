from datetime import datetime, timezone as datetime_timezone
from ipaddress import ip_address

from django.conf import settings
from django.db.models import F
from django.utils import timezone
from django.utils.crypto import salted_hmac

from apps.pages.models import ProjectInquiryThrottle


THROTTLE_KEY_SALT = "apps.pages.project-inquiry-throttle"
EXPIRED_BUCKET_CLEANUP_LIMIT = 100


class ProjectInquiryThrottleError(Exception):
    """Raised when a project-inquiry throttle decision cannot be made."""


def _positive_int_setting(name):
    value = getattr(settings, name, None)
    if type(value) is not int or value <= 0:
        raise ProjectInquiryThrottleError(
            f"{name} must be configured as a positive integer."
        )
    return value


def _normalize_client_address(value):
    if not isinstance(value, str) or not value.strip():
        raise ProjectInquiryThrottleError(
            "A valid client network address is required."
        )

    try:
        normalized_address = ip_address(value.strip())
    except ValueError:
        raise ProjectInquiryThrottleError(
            "A valid client network address is required."
        ) from None

    return str(normalized_address)


def resolve_client_address(request):
    trusted_header = getattr(
        settings,
        "PROJECT_INQUIRY_TRUSTED_IP_HEADER",
        "",
    )
    if not isinstance(trusted_header, str):
        raise ProjectInquiryThrottleError(
            "PROJECT_INQUIRY_TRUSTED_IP_HEADER must be a string."
        )

    trusted_header = trusted_header.strip()
    if trusted_header:
        raw_address = request.headers.get(trusted_header)
    elif settings.DEBUG:
        raw_address = request.META.get("REMOTE_ADDR")
    else:
        raise ProjectInquiryThrottleError(
            "A trusted client IP header must be configured in production."
        )

    return _normalize_client_address(raw_address)


def derive_bucket_key(client_address, window_id):
    normalized_address = _normalize_client_address(client_address)
    if type(window_id) is not int:
        raise ProjectInquiryThrottleError(
            "The throttle window identifier must be an integer."
        )

    bucket_value = f"{normalized_address}|{window_id}"
    return salted_hmac(
        THROTTLE_KEY_SALT,
        bucket_value,
        algorithm="sha256",
    ).hexdigest()


def _window_context(current_time, window_seconds):
    if (
        not isinstance(current_time, datetime)
        or timezone.is_naive(current_time)
    ):
        raise ProjectInquiryThrottleError(
            "The throttle clock must provide an aware datetime."
        )

    window_id = int(current_time.timestamp()) // window_seconds
    expires_at = datetime.fromtimestamp(
        (window_id + 1) * window_seconds,
        tz=datetime_timezone.utc,
    )
    return window_id, expires_at


def cleanup_expired_buckets(current_time):
    expired_bucket_ids = list(
        ProjectInquiryThrottle.objects.filter(
            expires_at__lte=current_time,
        )
        .order_by("expires_at")
        .values_list("pk", flat=True)[:EXPIRED_BUCKET_CLEANUP_LIMIT]
    )
    if expired_bucket_ids:
        ProjectInquiryThrottle.objects.filter(
            pk__in=expired_bucket_ids,
        ).delete()

    return len(expired_bucket_ids)


def consume_project_inquiry_throttle(request, *, now=None):
    limit = _positive_int_setting("PROJECT_INQUIRY_THROTTLE_LIMIT")
    window_seconds = _positive_int_setting(
        "PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS"
    )
    current_time = now if now is not None else timezone.now()
    window_id, expires_at = _window_context(current_time, window_seconds)
    client_address = resolve_client_address(request)
    bucket_key = derive_bucket_key(client_address, window_id)

    cleanup_expired_buckets(current_time)

    _, created = ProjectInquiryThrottle.objects.get_or_create(
        bucket_key=bucket_key,
        defaults={"expires_at": expires_at},
    )
    if created:
        return True

    updated = ProjectInquiryThrottle.objects.filter(
        bucket_key=bucket_key,
        expires_at__gt=current_time,
        attempt_count__lt=limit,
    ).update(attempt_count=F("attempt_count") + 1)
    return updated == 1
