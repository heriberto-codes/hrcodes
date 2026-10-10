# Project Brief Sentry Privacy Implementation Plan

Selected item: Prevent project-brief data and client identifiers from reaching Sentry

## 1. Architecture grounding

- Keep Django server rendering, synchronous inquiry email delivery, and the existing Sentry integration. Place the outbound event policy beside project configuration; add no framework, service, or storage.
- Preserve form validation, CSRF, shared database throttling, generic failure feedback, and success redirects.
- `architecture.md` describes a template-only homepage; executable code now uses `HomePageView(FormView)` with inquiry submission. Use that implemented request boundary for this plan.

## 2. Approved design grounding

- No matching `docs/design/project_brief_sentry_privacy/` workspace exists. This remediation changes telemetry behavior and needs no visual design.

## 3. Tech stack detected

- Django 5.1.2; Python standard-library logging and URL parsing; Sentry Python SDK 2.18.0.
- Existing `sentry_sdk.init()` in `hrcodes/settings.py`; `logger.exception()` in the throttle and SMTP failure branches of `apps/pages/views.py`.
- Django `SimpleTestCase`/`TestCase`, request clients, settings overrides, and `unittest.mock`; local SQLite and production PostgreSQL remain unchanged.

## 4. Files impacted

- Add `hrcodes/sentry_privacy.py` for a pure, startup-safe `before_send` callback and its scoped event classification.
- Modify `hrcodes/settings.py` only to import and register the callback in the existing Sentry initialization.
- Add `apps/pages/tests/test_sentry_privacy.py` for callback, registration, and SDK transport regression coverage during the TEST phases.
- Inspect `apps/pages/views.py`, `apps/pages/urls.py`, and existing inquiry tests as behavior contracts; no form, view, template, or throttle logic change is planned.

## 5. Data / DB changes

- No model, migration, or database change. The SDK may send only sanitized diagnostic events for inquiry failures, containing no submitted values or client identifiers.

## 6. API endpoints

- Keep public `POST /` and URL name `home`. It is an intentionally anonymous form protected by CSRF, validation, and throttling.
- Treat error events associated with that submission as private regardless of whether the error is caught by the view or captured by Django.

## 7. Frontend components

- No frontend changes. Preserve bound-form value retention, existing accessible errors, and the scheduling alternative.

## 8. Implementation approach

- Classify inquiry error events using request method `POST` and the parsed URL path `/`; ignore query strings when matching. Also recognize the existing `apps.pages.views` inquiry error messages when request metadata is absent, using event data or the SDK's log-record hint.
- Reduce recognized events to a newly constructed allowlist payload. Retain validated SDK event identity/time and fixed diagnostic fields: an approved level, a constant message, and a bounded failure category/fingerprint for throttle, email delivery, or other inquiry failures.
- Do not copy arbitrary event fields. Exclude request bodies, URLs and query values, headers, user/session data, exception text and stacks, locals, breadcrumbs, attachments, extras, contexts, and original tags or fingerprints. Do not serialize the original hint, request, form, or exception into diagnostics.
- Keep a useful sanitized event for ordinary recognized failures. Return `None` if a recognized event cannot be safely reduced; never fall back to its original payload. Handle absent or malformed optional metadata without raising from the callback.
- Return unrelated events unchanged. Match request scope and known inquiry logs rather than globally disabling Sentry or sanitizing every homepage GET.
- For POST events not identified by a known inquiry log, let URL parsing errors reach `before_send`'s existing fail-closed handler and return `None`; an unparseable URL must not be treated as evidence that the request is unrelated.
- Before URL classification or unrelated-event passthrough, drop POST error events from the exact `django.security.DisallowedHost` logger. SDK 2.18.0 constructs its URL from the unvalidated Host, so successful URL parsing cannot establish the original route for these events. Do not inspect private values or add Django imports, host allowlists, or route resolution to the callback.
- Register the callback through `before_send`; keep it free of Django model imports, URL resolution during settings import, database queries, networking, and logging recursion.
- This boundary follows [Sentry's filtering contract](https://docs.sentry.io/platforms/python/configuration/filtering/). Installed SDK 2.18.0 confirms it runs after request enrichment, scrubbing, and serialization, and applies to error events rather than transactions. Use installed behavior instead of newer SDK-only configuration options.

## 9. Risks & edge cases

- Missing request metadata must not bypass protection for either existing inquiry log message. Invalid URL/method/header shapes must not cause callback failures.
- Sensitive values can occur anywhere in an event, including exception messages, breadcrumb text, nested extras, tags, and a rendered email body in frame locals; removing only form data is insufficient.
- Broad matching could suppress unrelated blog/admin errors or homepage GET diagnostics. Cover both protected and unaffected cases.
- Dropping unparseable POST URLs also suppresses diagnostics for unrelated POST routes whose path cannot be established. Preserve unchanged handling of parseable unrelated requests and non-POST requests.
- The DisallowedHost POST guard intentionally also drops invalid-host POST diagnostics for blog/admin routes, even when the SDK URL parses. Preserve normal reporting for GET errors, valid-host unrelated POSTs, and unrelated logs; preserve fixed diagnostics for ordinary inquiry failures.
- Sanitization deliberately reduces inquiry debugging detail; retain only static failure classification and SDK event identity. Future submission route changes require updating the classifier.
- `before_send` does not sanitize separate transaction, profiling, or SDK log pipelines. Reassess privacy before enabling those channels; no such enablement is part of this work.

## 10. Security concerns

- Diagnosis captured two synthetic events in memory: throttle and SMTP failures both retained inquiry fields and `Fly-Client-IP`; the SMTP event also retained inquiry text in stack locals. No production events were accessed or transmitted.
- Default `send_default_pii=False` is insufficient for these fields in installed SDK 2.18.0. A constant log message does not prevent attached data from reaching the transport.
- Security review reproduced `POST /` with Hosts `testserver/blog`, `testserver?`, and `testserver#` through real `WSGIHandler`: each returned HTTP 400 and produced one in-memory envelope containing a synthetic private brief marker with `send_default_pii=False`. The bracket-host fix still produced zero envelopes. Treat invalid-host POST events as private before trusting their reconstructed URL.
- Use fixed diagnostics rather than value-based redaction, which cannot reliably recognize every free-text inquiry value. Preserve CSRF, secure cookies, HTTPS, and the shared throttle.
- Use synthetic markers and an in-memory transport for validation; never use actual inquiry data, credentials, production DSNs, or remote Sentry requests.

## 11. Testing strategy

- During the first step's TEST phase, add `SimpleTestCase` coverage in `apps/pages/tests/test_sentry_privacy.py` for POST-root matching, both known log messages without request metadata, query-bearing URLs, safe handling of incomplete metadata, and unchanged unrelated events.
- Seed protected events with distinct markers in all excluded channels, including nested data, IP headers, exception text, locals, breadcrumbs, tags, and extras. Assert marker absence throughout the resulting serialized payload, while verifying useful static diagnostics remain and input event/hint data is not mutated.
- During the second step's TEST phase, verify actual Sentry initialization registers the callback. With an isolated SDK client and in-memory transport, exercise real `HomePageView.form_valid` throttle and SMTP failure branches, including the existing malformed trusted-header path, and inspect final transport payloads after SDK/Django enrichment.
- Include a Django-captured unexpected POST-root error and an unrelated error event so logger-only filtering and blanket event suppression cannot pass. Keep SDK scopes and patched log handlers isolated and restored after each test.
- During the remediation step's TEST phase, correct the malformed POST URL passthrough expectation and add direct cases for `http://[/` and a query-bearing variant, asserting `None` without input mutation. Reuse the in-memory transport and real `WSGIHandler` to submit a synthetic private brief to `POST /` with `Host: [`, require HTTP 400 and zero outgoing envelopes, and preserve ordinary inquiry diagnostics plus unrelated-event coverage. Use an empty application DSN and the isolated synthetic SDK client; make no remote Sentry requests.
- During the Host delimiter remediation step's TEST phase, add direct POST DisallowedHost cases whose SDK URLs parse as a non-root path or an empty path, asserting `None` and input immutability. Extend the existing real WSGI/in-memory transport regression across Hosts `[`, `testserver/blog`, `testserver?`, and `testserver#`, with PII collection disabled and enabled; require HTTP 400, SDK capture of the synthetic private brief before filtering, and zero outgoing envelopes. Cover the intentional drop of non-root POST DisallowedHost events and preserve GET DisallowedHost reporting, valid-host blog/admin POST reporting, unrelated logs, and ordinary inquiry diagnostics. Keep the application DSN empty and reuse existing fixtures.
- Reuse existing inquiry assertions for generic feedback, bound values, email count, and throttle capacity; add no duplicate behavioral suite. Focused validation: `DEBUG=True venv/bin/python manage.py test apps.pages.tests.test_sentry_privacy apps.pages.tests.test_throttling apps.pages.tests.test_views`.
- Then run all repository test modules via explicit labels, including the new privacy module, followed by `DEBUG=True venv/bin/python manage.py check`. Prior default discovery found zero tests and app-label discovery failed on the `apps` namespace; document those existing runner limitations rather than treating zero discovered tests as success. Repairing discovery and CKEditor warnings is outside this plan.

## 12. Assumptions and unresolved questions

- The item is manually selected by the user and is not currently persisted in `docs/backlog.md`; this skill creates the remediation plan only.
- The scope is outgoing Sentry error events for the current project-brief endpoint and known inquiry logs. Historical Sentry data, retention policy, server-side scrubbing, production configuration, and unrelated telemetry are not inspected or changed.
- Current SDK versions and route ownership are confirmed in repository code. The settings change is explicitly planned because initialization owns the outgoing event boundary.
- The completed abuse-throttling plan remains the baseline. Privacy tests are implemented within each step's required TEST stage; there is no separate test-only EXECUTE step.
- The bracket-host parsing repair and its regression coverage completed the required loop; preserve all three checked steps. The Host delimiter bypass is a newly diagnosed implementation defect, and its guard and regression coverage are not yet implemented. The appended step must pass EXECUTE (DEBUG FIX), VERIFY, ENGINEER CHECKPOINT, and TEST before PLAN STEP UPDATE; rerun the feature security review afterward.

## 13. Step-by-step plan

- [x] Implement the scoped, startup-safe inquiry event classifier and fail-closed diagnostic allowlist callback in `hrcodes/sentry_privacy.py`, with direct privacy and unaffected-event coverage added in `apps/pages/tests/test_sentry_privacy.py` during this step's TEST phase.
- [x] Register the callback in the existing `sentry_sdk.init()` in `hrcodes/settings.py`, with registration and final SDK transport coverage for inquiry failures and unrelated events added in `apps/pages/tests/test_sentry_privacy.py` during this step's TEST phase.
- [x] Reconcile the fail-closed malformed-POST-URL repair in `hrcodes/sentry_privacy.py` so parsing errors cannot return an unsanitized event, with corrected direct expectations and a synthetic `POST /` with `Host: [` regression through real `WSGIHandler` and an in-memory Sentry transport in `apps/pages/tests/test_sentry_privacy.py` during this step's TEST phase; require HTTP 400, zero outgoing envelopes, input immutability, and preserved ordinary inquiry diagnostics and unrelated-event behavior.
- [x] Add a fail-closed POST `django.security.DisallowedHost` guard in `hrcodes/sentry_privacy.py` before URL classification so Host delimiters cannot cause original-event passthrough, with direct immutability checks and real WSGI/in-memory transport regressions in `apps/pages/tests/test_sentry_privacy.py` during this step's TEST phase for Hosts `[`, `testserver/blog`, `testserver?`, and `testserver#` with PII collection disabled and enabled; require HTTP 400, zero outgoing envelopes, intentional dropping of invalid-host POSTs on any route, and preserved GET reporting, valid-host unrelated POSTs, unrelated logs, and ordinary inquiry diagnostics.
