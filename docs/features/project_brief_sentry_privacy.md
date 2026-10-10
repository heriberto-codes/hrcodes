# Project Brief Sentry Privacy

## Summary

- Protect outgoing Sentry error events for project-brief submissions to `POST /` and the known inquiry failure logs.
- Ordinary inquiry failures retain fixed diagnostics without submitted values or client identifiers. Unsafe events are dropped before transport.
- All four steps in `docs/plans/project_brief_sentry_privacy_plan.md` completed the required implementation and validation loop; the matching backlog item is checked. SECURITY and PERFORMANCE reviews passed.

## Architecture Impact

- `hrcodes/sentry_privacy.py` provides a pure `before_send` callback registered by the existing Sentry initialization in `hrcodes/settings.py`.
- The callback uses standard-library code without database queries, disk access, networking, Django imports, or logging recursion.
- Existing Django form handling, CSRF protection, shared throttling, synchronous email delivery, and frontend behavior are preserved. This feature adds no endpoint, model, migration, or dependency.

## Decisions

- Recognize inquiry events by POST method and URL path `/`, or by the existing throttle/email failure messages from `apps.pages.views`, including log-record hints when request metadata is absent.
- Construct a new allowlist payload containing a validated event ID, an approved level, the constant message `Project inquiry failed.`, and fixed category tags/fingerprint (`throttle`, `email_delivery`, or `other`). Include a timestamp only when valid.
- Exclude original request data, URLs, headers, cookies, user/session data, exceptions, stacks, locals, breadcrumbs, extras, contexts, and arbitrary event fields. Do not mutate the input event or hint.
- Drop recognized events with invalid identity, unsafe hints, or attachments. Attachments travel outside the event payload, so sanitizing that payload alone is insufficient.
- Let malformed POST URL parsing reach the outer fail-closed handler, which returns `None` instead of forwarding the original event.
- Drop POST events from the exact `django.security.DisallowedHost` logger before parsing their URLs. SDK 2.18.0 builds these URLs using an unvalidated Host; delimiter-bearing hosts can produce parseable URLs with misleading paths.
- Preserve ordinary reporting for homepage GET errors, GET DisallowedHost events, parseable valid-host unrelated POSTs, and unrelated logs.

## Test Impact

- Added `apps/pages/tests/test_sentry_privacy.py` with direct callback, registration, and final serialized-envelope coverage. Direct tests check input immutability, excluded private channels, metadata validation, and unaffected reporting.
- Real `WSGIHandler` requests with Hosts `[`, `testserver/blog`, `testserver?`, and `testserver#` return HTTP 400 and emit zero envelopes for POSTs, with PII collection both disabled and enabled. Tests confirm a synthetic private brief marker reaches the callback before filtering. Corresponding GETs retain normal diagnostics.
- Throttle, SMTP, and unexpected inquiry errors produce approved diagnostics with no synthetic private markers in the final serialized envelope. Inquiry attachments drop the entire envelope.
- Recorded validation: 25 focused privacy tests and 109 repository tests passed. Django configuration checks exited successfully with the existing `ckeditor.W001` warning. SECURITY and the static PERFORMANCE review found no blocking issues.
- Validation used Django 5.1.2, Sentry SDK 2.18.0, an empty application DSN, synthetic data, and an isolated in-memory transport; no remote Sentry requests were made.
- Default test discovery previously found zero tests. The successful full run used eight explicit module labels:

```sh
PYTHONDONTWRITEBYTECODE=1 DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.pages.tests.test_forms apps.pages.tests.test_models apps.pages.tests.test_sentry_privacy apps.pages.tests.test_throttling apps.pages.tests.test_views apps.blog.tests.test_blog_model apps.blog.tests.test_blog_views apps.archive.tests.test_archive_views --verbosity 1
```

## Deployment Notes

- No deployment was performed. The callback is registered during application startup using the existing environment-configured `SENTRY_DSN`; no additional environment variables or migrations are required for this feature.

## Follow-ups / Accepted Risks

- Inquiry diagnostics intentionally omit exception detail. Invalid-host POSTs on any route and unparseable POST URLs are dropped because their inquiry scope cannot be established safely.
- The callback protects the covered outgoing error-event boundary. Historical Sentry data, retention, production proxy behavior, and remote configuration were not inspected or changed.
- Reassess classification when inquiry routes change and regression coverage when the SDK changes. Separate transaction, profiling, or SDK log channels require their own privacy review before enablement.
- Existing test-discovery limitations and the CKEditor warning remain outside this feature's scope.
