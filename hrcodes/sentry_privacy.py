"""Limit inquiry error events to fixed diagnostics at the Sentry boundary."""

from datetime import datetime
from logging import LogRecord
import re
from urllib.parse import urlsplit


INQUIRY_LOGGER = 'apps.pages.views'
INQUIRY_LOG_CATEGORIES = {
    'Project inquiry throttle evaluation failed.': 'throttle',
    'Project inquiry email delivery failed.': 'email_delivery',
}
APPROVED_LEVELS = frozenset({
    'debug', 'info', 'warning', 'error', 'critical', 'fatal',
})
EVENT_ID_PATTERN = re.compile(r'[0-9a-fA-F]{32}')
TIMESTAMP_PATTERN = re.compile(
    r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}'
    r'(?:\.[0-9]{1,6})?Z'
)


def _log_category(logger, message):
    if (
        type(logger) is str
        and logger == INQUIRY_LOGGER
        and type(message) is str
    ):
        return INQUIRY_LOG_CATEGORIES.get(message)
    return None


def _inquiry_log_category(event, hint):
    logger = event.get('logger')
    category = _log_category(logger, event.get('message'))
    if category:
        return category

    logentry = event.get('logentry')
    if type(logentry) is dict:
        for field in ('message', 'formatted'):
            category = _log_category(logger, logentry.get(field))
            if category:
                return category

    if type(hint) is dict:
        record = hint.get('log_record')
        if isinstance(record, LogRecord):
            # Use the original constant message, never render logging args.
            return _log_category(record.name, record.msg)
    return None


def _is_inquiry_request(event):
    request = event.get('request')
    if type(request) is not dict:
        return False

    method = request.get('method')
    url = request.get('url')
    if type(method) is not str or method.upper() != 'POST':
        return False
    if type(url) is not str:
        return False

    # Let before_send drop POST events whose URL cannot be safely classified.
    return urlsplit(url).path == '/'


def _safe_timestamp(value):
    if type(value) is not str or not TIMESTAMP_PATTERN.fullmatch(value):
        return None
    try:
        datetime.fromisoformat(value.replace('Z', '+00:00'))
    except ValueError:
        return None
    return value


def before_send(event, hint):
    """Sanitize inquiry errors without mutating event or hint; pass others on.

    The SDK supplies serialized events here, including a generated event ID.
    An invalid ID or unsafe hint drops a recognized event instead of returning
    its original data. Attachments travel outside the event payload in SDK
    2.18.0, so inquiry events with hint attachments must be dropped entirely.
    """
    if type(event) is not dict:
        return None

    try:
        request = event.get('request')
        if (
            event.get('logger') == 'django.security.DisallowedHost'
            and type(request) is dict
            and type(request.get('method')) is str
            and request['method'].upper() == 'POST'
        ):
            # An invalid Host can change the SDK URL's apparent path.
            # Drop these POSTs before trusting that URL to establish scope.
            return None

        category = _inquiry_log_category(event, hint)
        if category is None and not _is_inquiry_request(event):
            return event

        if hint is not None:
            if type(hint) is not dict:
                return None
            attachments = hint.get('attachments')
            if attachments is not None and (
                type(attachments) not in (list, tuple) or attachments
            ):
                return None

        event_id = event.get('event_id')
        if (
            type(event_id) is not str
            or not EVENT_ID_PATTERN.fullmatch(event_id)
        ):
            return None

        category = category or 'other'
        level = event.get('level')
        if type(level) is not str or level not in APPROVED_LEVELS:
            level = 'error'

        diagnostic = {
            'event_id': event_id,
            'level': level,
            'message': 'Project inquiry failed.',
            'tags': {'project_inquiry_failure': category},
            'fingerprint': ['project-inquiry', category],
        }
        timestamp = _safe_timestamp(event.get('timestamp'))
        if timestamp is not None:
            diagnostic['timestamp'] = timestamp
        return diagnostic
    except Exception:
        # Do not log, inspect exceptions, or fall back to the original payload.
        return None
