# Accessible Inquiry Throttling Guidance Plan

Selected backlog item (exact text): Add accessible inquiry-throttling guidance with the scheduling alternative

Feature slug: `accessible_inquiry_throttling_guidance`

## 1. Architecture grounding

`architecture.md` establishes server-rendered Django pages, reusable template includes, lightweight JavaScript, and app-owned persistence. Public routes are anonymous; Django authentication protects admin, and sessions support public interactions. SQLite is local and PostgreSQL is production. Preserve Django's test runner, Fly.io/Gunicorn, WhiteNoise, environment configuration, and security middleware. No public API, frontend framework, worker, or service layer is needed.

Code supersedes stale architecture descriptions: `HomePageView` is now a `FormView` that validates project briefs and sends synchronous email, rather than a template view selecting two recent posts. It selects configured published insight channels. `apps/pages/throttling.py` and `ProjectInquiryThrottle` enforce a shared database limit before delivery; sessions no longer authorize submissions. Keep these implemented boundaries.

## 2. Approved design grounding

No matching `docs/design/accessible_inquiry_throttling_guidance/` workspace exists; standalone planning applies. Reuse the existing brief builder, form-wide alert, scheduling destination, responsive layout, and focus behavior. This is a targeted recovery-state improvement within the existing interface.

## 3. Tech stack detected and confirmed

Django 5.1.2 is pinned in `requirements.txt` and present locally. The implementation uses Django forms/templates, authored CSS, and vanilla JavaScript.

Context7's [official Django forms guidance](https://github.com/django/django/blob/main/docs/ref/forms/api.md) confirms that `add_error(None, ValidationError(..., code=...))` creates a coded non-field error and `has_error(NON_FIELD_ERRORS, code)` can identify it. Installed Django's `django/forms/forms.py` confirms these APIs. Use this existing form mechanism instead of matching message text or retaining request state in a session.

## 4. Files impacted

- `apps/pages/views.py`: identify an actual throttle denial with a coded error and expose a boolean template context value.
- `templates/includes/start_project.html`: render recovery guidance and a scheduling link inside the existing form-wide error only when throttled.
- `static/pages/home.css`: scoped link readability, wrapping, and focus styling within the error panel.
- `apps/pages/tests/test_views.py`: targeted behavior and semantic-markup coverage during each step's TEST phase.
- Read-only contracts: `apps/pages/throttling.py`, `apps/pages/forms.py`, `static/pages/home.js`, and existing throttle/privacy tests.

## 5. Data / DB changes

None. The new context value exists only while rendering a response. Preserve throttle records, attempt consumption, expiry, success timestamps, and submitted-field handling. No migrations or stored inquiry data.

## 6. API endpoints

Preserve `GET /` and `POST /` under the `home` URL name. Throttled submissions continue to render HTTP 200 with a bound form; successful delivery still redirects to `/#start-a-project`. No new endpoint, status-code policy, or retry header.

## 7. Frontend components

Keep the existing `.home-form-wide-error` wrapper, `role="alert"`, `tabindex="-1"`, and `data-home-form-wide-error` focus hook. Its added paragraph should say that this submission was not sent and offer retrying later or booking a call. Add a real anchor labeled “Book a call instead” using `https://calendly.com/heriberto_codes/coffee_chat`, with the existing new-tab convention: `target="_blank"`, `rel="noopener noreferrer"`, and accessible new-tab text.

Keep the sidebar's scheduling link. The recovery link must be adjacent to the throttle explanation, keyboard reachable, underlined, and readable against the alert background. Use existing color tokens and a contrasting local focus outline. It must render without JavaScript and remain outside the builder's individually hidden step panels.

## 8. Implementation approach

When the limiter returns false, keep the existing “Please wait a moment before sending another project brief.” text and attach error code `inquiry_throttled` through `ValidationError`. In `get_context_data`, derive `project_inquiry_throttled` from the bound form using `has_error(NON_FIELD_ERRORS, 'inquiry_throttled')`; default to false for the initial form and other outcomes.

Condition the added guidance/link on that boolean inside the existing non-field-error block. Keep strings escaped and links in the template. Reuse the existing JavaScript behavior that selects step three and focuses the form-wide error; no JavaScript changes are planned. Add only local CSS needed for the recovery link's readability and focus state.

## 9. Risks & edge cases

- Shared addresses and fixed windows can block a legitimate visitor. Offer a useful alternative without claiming an exact wait duration or showing attempt counts.
- Throttle-evaluation exceptions and SMTP failures are different from a known limit denial. Preserve their existing generic feedback; do not label them as throttled.
- Every submitted value must remain bound after denial, including choices and consent. A blocked submission must not show success feedback or send another email.
- Alert announcements vary by browser and assistive technology on navigation. Verify actual focus, reading order, and link access rather than assuming `role="alert"` alone is sufficient.
- A yellow global focus ring may be weak on the light alert background; use a scoped contrasting token and verify visually. Check narrow screens and zoom for wrapping and clipping.

## 10. Security concerns

Preserve CSRF, honeypot validation, the shared limiter, fail-closed behavior, SMTP ordering, and Sentry privacy filtering. Expose no address, bucket key, counter, expiry, configuration value, or exception detail. Use a fixed scheduling URL without inquiry content in its query string. Do not move submission enforcement into the browser or introduce new telemetry.

## 11. Testing strategy

For step one, extend existing view tests to prove the error code and context flag appear only on a real denial. Reuse current cross-session enforcement, preserved values, no-email, and no-success assertions. Check initial GET, field/honeypot errors, successful submission, SMTP failures, and throttle exceptions do not receive the throttled marker.

For step two, inspect rendered HTML using the existing `HTMLParser` approach: assert the recovery anchor is inside the same focusable alert as the throttle text, has the exact destination and accessible label/new-tab disclosure, and is absent from that panel on other outcomes. Assert the bound values remain rendered. Existing sidebar links alone must not satisfy the recovery assertion. Keep tests focused on behavior, without adding source-string snapshots for CSS or JavaScript.

Run `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.pages.tests.test_views` first, then the default full suite and `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py check`. Prior feature records report incomplete default/app-label discovery: verify the discovered count and, if needed, run all current modules explicitly: `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.pages.tests.test_forms apps.pages.tests.test_models apps.pages.tests.test_sentry_privacy apps.pages.tests.test_throttling apps.pages.tests.test_views apps.blog.tests.test_blog_model apps.blog.tests.test_blog_views apps.blog.tests.test_admin apps.blog.tests.test_like_views apps.archive.tests.test_archive_views`.

During UI validation, use local test data and a local email backend to reproduce a denied submission. Verify desktop/mobile presentation, keyboard focus and tab order, screen-reader announcement/reading, zoom, and JavaScript-disabled rendering. Check that following the scheduling link needs no form resubmission; no real booking is required. Automated markup tests alone do not establish the accessibility outcome.

## 12. Assumptions and unresolved questions

The existing scheduling URL and new-tab behavior remain intentional. Generic retry wording is sufficient; countdowns, exact retry times, disabling submission, or changing throttle policy are outside this item. Existing error text remains unchanged so established behavioral tests can continue to assert it.

No blocking implementation questions remain. Manual assistive-technology validation is still required during implementation. Preserve the already requested removal of the optional category-query backlog item; planning makes no further backlog edits.

## 13. Step-by-step plan

- [x] In `apps/pages/views.py`, add the `inquiry_throttled` code to the existing limit-denial non-field error and derive `project_inquiry_throttled` in template context from that code, retaining the current message, bound form, status, delivery, and failure behavior; cover the response-state distinction in `apps/pages/tests/test_views.py` during this step's TEST phase.
- [x] In `templates/includes/start_project.html`, add throttle-only recovery guidance and the scheduling anchor inside the existing focusable form-wide alert; style the link locally in `static/pages/home.css` for readable wrapping, underlining, and contrasting focus, retaining the existing JavaScript/no-JavaScript flow; cover rendered semantics in `apps/pages/tests/test_views.py` and perform keyboard, assistive-technology, and responsive validation during this step's TEST phase.
