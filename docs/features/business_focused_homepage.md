# Business-Focused Homepage

## Summary

- Present Hroman Codes as a founder-led software business through the approved sequence: Hero, Services, Case Studies, Development Process, Insights, About, Start a Project, and Footer.
- Implement the approved mosaic hero, service ledger, client/founder evidence views, five-stage process, Insights tuner, founder profile, three-step brief builder, and closing route board.
- Provide the dedicated Signal Transcript presentation for the published Guardrails article, with standard article rendering retained for other posts.
- All twelve steps in `docs/plans/business_focused_homepage_plan.md` are checked following the previously completed execution flow. The matching backlog item is checked.

## Architecture Impact

- Preserve Django server rendering, reusable template includes, and the existing `apps/pages` and `apps/blog` ownership boundaries.
- `templates/base.html` supplies page-specific metadata, body classes, asset blocks, and a content-wrapper extension. Homepage styling and enhancements live in `static/pages/home.css` and `static/pages/home.js`; the curated article has its own template and stylesheet.
- `HomePageView` now uses `FormView` to compose published Insights and handle validated inquiry submissions. Email remains synchronous and environment-configured.
- No frontend framework, build pipeline, public JSON API, background worker, or third-party analytics integration was introduced.

## Decisions

- Keep navigation and content semantic, with one homepage H1, consistent section anchors, external-link protections, visible focus styles, responsive rules, and reduced-motion treatments.
- Use native mobile navigation with Escape/outside-pointer closing and focus return. Case-study tabs support keyboard selection; both evidence views remain available without JavaScript. The Insights tuner uses native radio controls with CSS selection and fallback content.
- Select Guardrails, Constraints, and Revival posts by explicit stable slugs, require published status, preserve their editorial order, and prefetch categories. Missing posts produce partial or empty states rather than fabricated content.
- Require matching primary key, slug, and published status for article detail. `Post.get_absolute_url()` now includes both route identifiers.
- Build the Guardrails transcript from its existing CMS body and expected headings. Extract its three payload destinations when their structure matches; otherwise preserve the appendix HTML. Related signals include only the selected published posts.
- Preserve the trusted-admin rich-text boundary. The curated template does not authorize visitor HTML or generalize the presentation to all CMS posts.
- Validate inquiry choices, required consent, lengths, normalized email, and honeypot on the server. The brief builder enhances the same submit-capable form with staged validation, live summary, error focus, and confirmation.
- Use a fixed mail subject and configured recipient, with validated email as Reply-To. Delivery exceptions or a zero-delivery result show generic errors and preserve values; success uses messages and POST/Redirect/GET.

## API Changes

- `GET /` renders the redesigned homepage; CSRF-protected `POST /` processes project briefs and redirects successful delivery to `/#start-a-project`.
- Existing blog detail routes now reject mismatched slugs and drafts with HTTP 404. Guardrails uses `templates/blog/insight_detail.html`; other published posts retain `templates/blog/blog_detail.html`.

## Database Changes

- The homepage feature adds no model fields, migrations, or inquiry-record storage. Existing posts/categories supply Insights and article content.
- The later `project_brief_abuse_throttling` remediation adds ephemeral opaque throttle metadata and replaces the original session-based limit. Its migration and deployment requirements are documented in `docs/features/project_brief_abuse_throttling.md`.

## Test Impact

- Form tests cover valid/optional values, email normalization, required fields, invalid choices/formats, length boundaries, and honeypot rejection.
- Homepage tests cover published Insight selection/order and missing-post states, section/anchor/heading continuity, scoped assets, template contracts, inquiry delivery and failures, retained values, CSRF, and subsequent shared-throttle behavior.
- Blog tests cover canonical URLs, strict published detail lookup, Guardrails-only template selection, transcript mapping/payload fallback, ordered published related signals, and archive fallback.
- The latest recorded full run after the remediation work passed 109 tests using eight explicit module labels. Django checks exited successfully with the existing `ckeditor.W001` warning. The reproducible command and discovery limitations are recorded in `docs/features/project_brief_sentry_privacy.md`.
- These automated assertions cover server behavior and markup/source contracts; they do not establish real-device rendering performance or assistive-technology behavior.

## Deployment Notes

- No deployment was performed during this finalization. Production inquiry delivery requires working SMTP configuration, sender, and recipient through the existing environment-based mail settings.
- Publish the selected Insight slugs to populate all tuner channels. The transcript's curated structure depends on the Guardrails CMS body and expected headings.
- Ship the authored static assets through the existing static collection/deployment process. Do not substitute design mockups or edit generated `staticfiles/` by hand.
- Include the completed shared-throttle migration and Sentry callback when releasing the current inquiry flow. `docs/features/project_brief_sentry_privacy.md` records the outgoing error-event privacy policy, malformed-Host repairs, and transport regressions.

## Follow-ups / Accepted Risks

- The later throttling and Sentry privacy features supersede the original plan's session-only limit and protect inquiry error telemetry; the current implementation is authoritative.
- The long page, imagery, motion, and lazy YouTube embed retain the approved rendering, network, third-party privacy, and availability tradeoffs. Real-device and assistive-technology validation results are not available in the retained finalization context and are not claimed here.
- Client evidence permissions, commercial wording, scheduling expectations, and production mail operation remain business-owner launch considerations identified by the plan.
- Featured-slug changes or substantially different Guardrails headings require reviewing the curated selection/presentation contracts. This feature does not change blog index/category publication filtering or the existing like action.
- Existing test-discovery limitations and the CKEditor warning remain outside this feature's scope.
