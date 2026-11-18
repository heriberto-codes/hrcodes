# Accessible Inquiry Throttling Guidance

## Summary

- A throttled project brief now explains that the submission was not sent and offers retrying later or booking a call.
- Both steps in [the implementation plan](../plans/accessible_inquiry_throttling_guidance_plan.md) completed EXECUTE, VERIFY, ENGINEER CHECKPOINT, TEST, and PLAN STEP UPDATE. The matching backlog item is checked. SECURITY and PERFORMANCE reviews passed.

## Architecture Impact

- `apps/pages/views.py` attaches the `inquiry_throttled` error code to an actual limit denial and derives the response-only `project_inquiry_throttled` flag from the form.
- `templates/includes/start_project.html` renders recovery guidance inside the existing focusable form-wide alert, outside the individually hidden step panels. It works with JavaScript disabled and reuses the existing focus behavior without JavaScript changes.
- `static/pages/home.css` adds scoped wrapping, underlining, and a contrasting focus outline using the existing navy token. No database queries, automatic network requests, dependencies, or persistence were added.

## Decisions

- Identify throttling by the Django non-field error code rather than matching message text. Initial forms, field errors, honeypot rejection, throttle-evaluation exceptions, and delivery failures do not receive the throttle recovery guidance.
- Preserve the original wait message, submitted values and consent, shared database limiter, CSRF protection, and delivery ordering. A denied submission sends no additional email and shows no success feedback.
- Offer a fixed `https://calendly.com/heriberto_codes/coffee_chat` anchor labeled “Book a call instead,” with `target="_blank"`, `rel="noopener noreferrer"`, and accessible text announcing the new tab. No submitted information is included in the URL; the existing sidebar link remains available.
- Give general retry guidance without exposing counters or claiming an exact wait time.

## API Changes

- No new endpoint. `GET /` and `POST /` retain their existing behavior: denied submissions render HTTP 200 with the bound form, and successful delivery redirects to `/#start-a-project`.

## Database Changes

- None. Throttle records, limits, expiry, and schema are unchanged; no migration is required.

## Test Impact

- Extended existing tests in `apps/pages/tests/test_views.py` with coded-error and context-flag assertions, rendered alert/link semantics, retained field values and consent, and absence of recovery guidance for other outcomes. A scoped HTML parser distinguishes the recovery link from the sidebar link.
- Recorded TEST results: 46 view tests passed; the full run using the ten explicit module labels in the plan passed all 144 tests. Default discovery found zero tests and was not counted as full-suite validation.
- Django configuration checks passed with the existing `ckeditor.W001` warning. Whitespace checks passed.
- Local browser checks covered focus on the alert, Tab access to the underlined link, its focus outline and accessible name, wrapping at 1440/390/320-pixel widths, and JavaScript-disabled rendering with submitted values retained. Keyboard activation opened the expected new tab without another form POST; the destination was intercepted for that check.
- The user confirmed readability at actual 200% Chrome zoom, VoiceOver reading the message, and announcing the recovery link with its new-tab disclosure.
- Browser validation used synthetic submissions, an isolated in-memory database, and local email delivery. No real booking was made.
- Read-only SECURITY and PERFORMANCE reviews identified no feature findings. Performance conclusions came from code review, without benchmarks.

## Deployment Notes

- No deployment was performed. This feature requires no new environment variables, dependencies, or database migrations. The changed template, view, and authored CSS use the existing deployment and static-asset pipeline.

## Follow-ups / Accepted Risks

- Shared-address and fixed-window limitations of the existing throttle remain; the scheduling alternative provides another contact path without changing enforcement.
- Accessibility validation covers the tested Chrome/VoiceOver setup and viewport checks, rather than every browser and assistive-technology combination.
- Existing test-discovery limitations and the CKEditor warning remain outside this feature's scope. No feature-specific follow-up is required by the completed reviews.
