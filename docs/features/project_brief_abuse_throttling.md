# Project Brief Abuse Throttling

## Summary

- Replace session-based submission throttling with a database-backed limit shared across fresh sessions and application workers.
- Valid project briefs consume capacity before email delivery. Blocked requests preserve entered values and show generic feedback with the scheduling alternative.
- All four steps in `docs/plans/project_brief_abuse_throttling_plan.md` are complete following the previously completed execution flow. The matching backlog item is checked.

## Architecture Impact

- `apps/pages/throttling.py` owns client-address resolution, opaque bucket keys, atomic attempt consumption, and bounded expiry cleanup.
- `HomePageView.form_valid()` invokes the limiter after form/honeypot validation and before rendering or sending the notification email.
- Coordination uses the existing relational database rather than per-process memory or sessions. No external service, framework, frontend change, or new dependency was introduced.
- The existing success timestamp remains in the session, but it no longer authorizes throttle decisions. CSRF protection, form validation, email delivery, and success redirects are preserved.

## Decisions

- Normalize IPv4/IPv6 addresses from `PROJECT_INQUIRY_TRUSTED_IP_HEADER`. Production requires a configured trusted header; missing or invalid values fail closed. With no configured header, `REMOTE_ADDR` is used only in DEBUG mode. Arbitrary `X-Forwarded-For` values cannot override the selected address.
- Derive a 64-character SHA-256 HMAC key from the normalized address and fixed time-window identifier using Django's secret. Store no raw address, email address, or submitted brief content in throttle rows.
- Use a unique bucket key with `get_or_create()` for the first attempt and a conditional database update with `F()` for subsequent attempts. The update succeeds only while capacity remains and the bucket has not expired.
- Defaults allow one attempt per fixed 60-second window. Positive integer limit/window settings are validated before database writes.
- Email failures consume capacity intentionally. Throttle evaluation failures send no email and return generic bound-form feedback; there is no session fallback.
- Remove at most 100 expired buckets per evaluated submission, oldest first. Cleanup is opportunistic rather than a background job.
- The later `project_brief_sentry_privacy` remediation protects inquiry failure telemetry, including throttle exceptions. See `docs/features/project_brief_sentry_privacy.md` for its completed policy and regression results.

## API Changes

- The existing `POST /` endpoint and URL names remain. Successful delivery redirects to `/#start-a-project`; blocked or failed submissions render the form with HTTP 200 and a non-field error.

## Database Changes

- Added `ProjectInquiryThrottle` and migration `apps/pages/migrations/0001_projectinquirythrottle.py`.
- Table `apps_pages_projectinquirythrottle` contains a unique `bucket_key`, an `attempt_count` defaulting to one, and indexed `expires_at`, plus Django's primary key.

## Test Impact

- `apps/pages/tests/test_throttling.py` covers address selection/normalization, trusted-header failures, opaque keys, capacity, window rollover, invalid settings/clocks, and bounded cleanup.
- Concurrent claim tests use separate SQLite connections and synchronized stale reads to exercise unique first-bucket creation and competition for the last available attempt.
- `apps/pages/tests/test_views.py` covers fresh-session enforcement, distinct-address independence, forwarded-header bypass attempts, generic failure feedback, preserved values, invalid forms/honeypots without capacity consumption, successful delivery, and SMTP failures consuming capacity.
- The latest recorded full validation, after the Sentry remediation, passed 109 tests across eight explicit module labels, including these throttle and view modules. Django checks exited successfully with the existing `ckeditor.W001` warning.
- Default/app-label discovery limitations required explicit module labels; see the reproducible full-suite command in `docs/features/project_brief_sentry_privacy.md`.

## Deployment Notes

- Apply the new migration before serving submissions. The existing Fly release configuration runs Django migrations; no deployment or production migration was performed during this finalization.
- `PROJECT_INQUIRY_THROTTLE_LIMIT` defaults to `1`. `PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS` defaults to `PROJECT_INQUIRY_COOLDOWN_SECONDS`, whose default is `60`.
- `PROJECT_INQUIRY_TRUSTED_IP_HEADER` defaults to `Fly-Client-IP` outside DEBUG and an empty string in DEBUG. Its trust depends on the actual ingress proxy supplying an authoritative address.

## Follow-ups / Accepted Risks

- Shared NAT/VPN addresses share capacity. Fixed windows permit attempts on either side of a boundary; this is not a rolling minimum interval between submissions.
- Address rotation can evade an address-based limit. Additional proxy layers require reassessing which header is authoritative; live production ingress was not validated here.
- Secret rotation changes bucket keys. Expired rows may remain during idle periods until later submissions perform cleanup.
- Concurrency coverage exercised local SQLite behavior; it does not constitute a live multi-worker PostgreSQL deployment test.
- Existing test-discovery limitations and the CKEditor warning remain outside this feature's scope.
