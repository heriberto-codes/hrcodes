# Project Brief Abuse Throttling Implementation Plan

## 1. Architecture grounding

- Keep the change inside the existing Django server-rendered request path: `apps/pages` continues to own the public project-brief form and synchronous email delivery.
- Use the existing relational database as the shared coordination boundary so throttling applies across fresh sessions, both Gunicorn workers, and future Fly Machines without adding a framework or external service.
- Preserve Django form validation, CSRF middleware, POST/Redirect/GET success behavior, environment-driven configuration, and generic failure feedback.
- Store only short-lived abuse-control metadata; do not persist inquiry content, raw client IP addresses, email addresses, or other visitor-provided values.

## 2. Approved design grounding

- No matching design workspace exists for `project_brief_abuse_throttling`, and the backlog item is a backend security hardening change rather than a new visual direction.
- Preserve the approved Start a Project form, its existing server-rendered non-field error state, accessible focus behavior, and Calendly alternative without redesigning the interface.

## 3. Tech stack detected

- Backend: Django 5.1.2, `FormView`, Django forms, sessions, messages, email, ORM, and migrations.
- Runtime: Gunicorn with two workers on Fly.io; production uses PostgreSQL and local tests use SQLite.
- Frontend: Django templates and existing vanilla JavaScript enhancement; no frontend change is required for the shared throttle.
- Testing: Django `TestCase`, request client, in-memory mail backend, settings overrides, and mocks in `apps/pages/tests/`.

## 4. Files impacted

- Modify `apps/pages/models.py` to add the short-lived project-inquiry throttle bucket.
- Add `apps/pages/migrations/0001_projectinquirythrottle.py` for the explicitly planned abuse-control schema.
- Add `apps/pages/throttling.py` to isolate client identification, opaque key derivation, atomic limit consumption, and bounded expiry cleanup.
- Modify `apps/pages/views.py` to enforce the shared throttle before synchronous email delivery while preserving current form behavior.
- Modify `hrcodes/settings.py` to add environment-driven throttle limit, window, and trusted client-IP header settings.
- Add `apps/pages/tests/test_throttling.py` and extend `apps/pages/tests/test_views.py` with focused security and integration coverage.

## 5. Data / DB changes

- Add one `apps_pages_projectinquirythrottle` table containing a unique HMAC-derived client/window key, an attempt count, and an indexed expiry timestamp.
- Use a conditional ORM update against the configured limit so concurrent workers cannot authorize more requests than the shared bucket permits.
- Remove expired records through bounded opportunistic cleanup during valid submission attempts; retain no durable inquiry or identity history.

## 6. API endpoints

- Keep the existing public `POST /` project-brief endpoint and all URL names unchanged.
- Apply the shared throttle only after server-side form and honeypot validation and before rendering or sending the email.
- Return the existing form page with a generic non-field error when the limit is reached or the throttle cannot be evaluated safely; do not expose bucket state or client identifiers.

## 7. Frontend components

- Reuse the existing non-field error container in `templates/includes/start_project.html` and its current accessible focus behavior.
- Preserve the form fields, CSRF token, valid-value retention, Calendly route, and no-JavaScript submission path.
- Do not add client-side rate-limit logic because the security decision must remain server authoritative.

## 8. Implementation approach

- Resolve a normalized client network address from an explicitly configured trusted request header in production and `REMOTE_ADDR` elsewhere; validate it with Python's IP address parser and never trust arbitrary `X-Forwarded-For` positions.
- Derive the bucket key with Django's keyed-HMAC utility from the normalized address and fixed time-window identifier so database rows cannot reveal raw IP addresses.
- Preserve the current one-submission-per-60-seconds intent as configurable defaults, replacing the session as the authoritative limiter while retaining current success and failure messages.
- Claim a bucket by creating its unique row or conditionally incrementing its count with an `F()` expression while the count is below the configured limit; treat a zero-row update as blocked.
- Consume the throttle before calling SMTP, including when delivery later fails, so repeated SMTP failures cannot be used to exhaust workers.
- Fail closed with generic feedback and server-side exception logging if shared throttle state cannot be evaluated; do not log the raw client address or submitted form values.

## 9. Risks & edge cases

- Shared office, school, carrier-grade NAT, or VPN addresses can group legitimate visitors; keep the default window short and thresholds environment-configurable.
- Missing or invalid proxy headers must not allow attackers to choose arbitrary bucket identities or collapse every visitor into an unsafe shared value.
- Concurrent first requests for the same bucket can race; the unique key and conditional count update must make the limit deterministic across workers.
- SMTP failures consume capacity intentionally; the short window and scheduling alternative limit user impact while protecting the synchronous mail boundary.
- Expired rows can accumulate during long idle periods; indexed, bounded cleanup must avoid an unbounded delete on a public request.
- Secret-key rotation changes derived bucket keys, but prior opaque rows expire and contain no reusable identity data.

## 10. Security concerns

- Trust `Fly-Client-IP` only when configured for the deployed Fly proxy boundary; do not treat `X-Forwarded-For` as authoritative without an explicit trusted-proxy design.
- Validate and normalize IPv4 and IPv6 values before key derivation, and use constant-size HMAC output as the database key.
- Preserve CSRF protection, the honeypot, length validation, fixed mail recipient and subject, secure cookies, and HTTPS enforcement.
- Keep throttle responses generic and identical across client identities; do not disclose remaining attempts, stored keys, raw addresses, or internal failures.
- Ensure the database-backed decision is atomic and authoritative rather than falling back to the existing bypassable session check.

## 11. Testing strategy

- Unit-test client-address selection and validation, stable HMAC key derivation without raw-address storage, allowed and blocked bucket claims, expiry rollover, bounded cleanup, invalid configuration, and conditional count behavior.
- Prove that two clients with fresh sessions but the same trusted client address share a limit and that distinct addresses do not share a bucket.
- Verify blocked and throttle-error submissions send no email, preserve entered values, expose only generic feedback, and retain the scheduling alternative.
- Verify valid submissions still send exactly one email and redirect, invalid forms and honeypots do not consume throttle capacity, and SMTP failure attempts do consume capacity.
- Run `DEBUG=True venv/bin/python manage.py test apps.pages.tests.test_throttling apps.pages.tests.test_views`, then `DEBUG=True venv/bin/python manage.py test apps.pages apps.blog`, the full Django suite, and `DEBUG=True venv/bin/python manage.py check`.

## 12. Assumptions and unresolved questions

- The production request path currently reaches Django through Fly Proxy without another reverse proxy. Fly documents `Fly-Client-IP` as the client address from its proxy perspective and notes that another upstream proxy changes that meaning; adding Cloudflare or another proxy requires revisiting the trusted-header setting.
- Django's local-memory cache is per-process, so it is not sufficient for the current two-worker Gunicorn runtime; the database-backed bucket avoids introducing Redis or Memcached.
- The existing `PROJECT_INQUIRY_COOLDOWN_SECONDS=60` behavior defines the default window intent. The production owner may tune the new environment-driven limit and window after observing legitimate traffic.
- This follow-up deliberately adds ephemeral abuse-control metadata even though the homepage plan avoided inquiry persistence; no inquiry content or directly identifying value is stored.
- Edge-level filtering can still complement this application control later, but deploying or configuring external infrastructure remains outside this backlog item.

## 13. Step-by-step plan

- [x] Add the opaque, expiring throttle bucket model in `apps/pages/models.py` and its explicit schema migration in `apps/pages/migrations/0001_projectinquirythrottle.py`.
- [x] Add environment-driven throttle settings in `hrcodes/settings.py` and implement trusted client-address resolution, HMAC bucket derivation, atomic bucket consumption, and bounded expiry cleanup in `apps/pages/throttling.py`.
- [x] Integrate the shared limiter into `apps/pages/views.py` before email delivery, remove the session as the authoritative throttle boundary, and preserve generic server-rendered failure and success behavior.
- [x] Add focused unit and integration coverage in `apps/pages/tests/test_throttling.py` and `apps/pages/tests/test_views.py` for cross-session enforcement, concurrency-safe limits, expiry, proxy-header handling, delivery failures, and legitimate submissions.
