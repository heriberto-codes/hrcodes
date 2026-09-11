# Business-Focused Homepage Implementation Plan

## 1. Architecture grounding

- Keep the feature inside the existing Django 5.1 server-rendered architecture: `apps/pages` owns homepage composition and inquiry handling, while `apps/blog` owns post retrieval and article rendering.
- Preserve the root homepage and existing blog URL boundaries, Django templates, ORM-backed blog content, session support, CSRF middleware, and WhiteNoise-served authored static assets.
- Use reusable template includes and scoped vanilla CSS/JavaScript; do not introduce a frontend framework, build pipeline, public JSON API, background worker, or new persistence layer.
- Treat `hrcodes/settings.py` as high impact and limit changes to environment-driven mail configuration required by the inquiry workflow.

## 2. Approved design grounding

- Implement the confirmed sequence: Hero → Services → Case Studies → Development Process → Insights → About → Start a Project → Footer.
- Use [the approved design](../design/business_focused_homepage/approved-design.md) as the source of truth for hierarchy, copy intent, responsive behavior, components, assets, motion, accessibility fallbacks, and accepted tradeoffs.
- Preserve Hero C, Services B, Case Studies B, Development Process D, Insights C, About A, Start a Project B, and Footer B.
- Keep Insights Article B exclusive to the approved Guardrails post; other posts retain the standard article template.
- Do not invent client outcomes, testimonials, metrics, responsibilities, pricing, response promises, or qualification rules.

## 3. Tech stack detected

- Backend: Django 5.1.2, class- and function-based HTML views, Django forms, sessions, messages, CSRF, and the Django ORM.
- Frontend: Django templates, authored CSS, Bootstrap-era global styles, and lightweight JavaScript without a build step.
- Data: `Post`, `Category`, and `Like` models in SQLite locally and PostgreSQL in production.
- Static delivery: WhiteNoise with compressed manifest storage.
- Runtime: Gunicorn on Fly.io, configured through environment variables and deployed by GitHub Actions.

## 4. Files impacted

- Modify `templates/base.html` and `templates/home.html` to add page metadata/body/asset extension points and compose the approved section order.
- Modify `templates/includes/navbar.html`, `templates/includes/hero.html`, `templates/includes/about.html`, and `templates/includes/footer.html`.
- Add `templates/includes/services.html`, `templates/includes/case_studies.html`, `templates/includes/development_process.html`, `templates/includes/insights.html`, and `templates/includes/start_project.html`.
- Add `static/pages/home.css` and `static/pages/home.js`; add approved mockup-only source images to `static/pages/images/` with production-safe names while reusing existing production assets where available.
- Add `apps/pages/forms.py` and `templates/email/project_inquiry.txt`; modify `apps/pages/views.py` and `hrcodes/settings.py` for validated inquiry delivery.
- Add `templates/blog/insight_detail.html` and `static/blog/insight_detail.css`; modify `apps/blog/views.py` and `apps/blog/models.py` for the Guardrails-only template and correct canonical detail URLs.
- Extend `apps/pages/tests/test_views.py`; add `apps/pages/tests/test_forms.py`; update `apps/blog/tests/test_blog_views.py` and `apps/blog/tests/test_blog_model.py`.

## 5. Data / DB changes

- No model-field or database migration is planned.
- Continue sourcing Insights from published `Post` records and categories.
- Do not persist project inquiries in the database; validate them server-side, deliver them through configured email, and retain only the existing short-lived session state used for feedback and submission throttling.

## 6. API endpoints

- No JSON API is added.
- Keep `GET /` for homepage rendering and accept CSRF-protected `POST /` for the project brief, using redirect-after-success to `/#start-a-project`.
- Preserve `GET /blog/<pk>/<slug>` and select the Signal Transcript template only when both the requested post and approved Guardrails slug match.

## 7. Frontend components

- Native desktop/mobile navigation with reliable menu, Escape, outside-pointer, focus-return, anchor, and reduced-motion behavior.
- Kinetic-mosaic hero with semantic heading hierarchy and Book A Call / Review Services routes.
- Editorial service ledger, evidence-trail case-study tabs, and five-stage development-process canvas.
- Three-channel Insights tuner backed by three explicit published posts, with written empty/fallback states and full-card article routes.
- Founder profile, interactive-but-nonessential skillset visualization, lazy YouTube embed, résumé route, and conversation route.
- Progressive three-step project brief with server-compatible field names, accessible validation, preserved invalid values, live summary, confirmation, and direct scheduling alternative.
- Closing signal footer with route board, verified social links, copyright, founder credit, and return-to-top action.

## 8. Implementation approach

- Add page-specific template blocks to `base.html` so the redesign can load scoped assets without destabilizing archive and standard blog pages.
- Replace only homepage composition and the four reusable includes it already owns; leave legacy includes unused until the redesign is verified, avoiding destructive cleanup during feature delivery.
- Adapt the approved mockup markup and styles into semantic Django templates, consolidating shared tokens and responsive rules in `static/pages/home.css` rather than linking mockup files into production.
- Keep enhancement JavaScript in `static/pages/home.js`; essential content, navigation, article access, and form completion must remain understandable without animation and usable with JavaScript unavailable.
- Use a `FormView`-compatible homepage flow, Django form validation, a honeypot and per-session cooldown, plain-text email rendering, messages, and POST/Redirect/GET. Report delivery failures without showing a false success state.
- Configure mail entirely through environment variables; tests use Django's in-memory backend. No secret values or production credentials enter the repository.
- Select the approved three Insight posts by stable slugs in view code, require `status=1`, prefetch categories, preserve approved order, and render a clear fallback if one is unavailable.
- Tighten blog detail lookup to matching `pk`, `slug`, and published status, then render the dedicated Signal Transcript template only for the approved Guardrails slug. The CMS body remains the article source; the template supplies its approved presentation and supporting related-post routes.

## 9. Risks & edge cases

- Missing or renamed featured Insight slugs can leave fewer than three tuner channels; the UI must degrade without broken controls or fabricated content.
- The selected Guardrails article is identified by slug, not database ID, because IDs differ across environments.
- Existing project evidence wording and image permissions must be confirmed before production deployment; unverifiable claims must remain omitted.
- Motion, layered imagery, tabs, the skillset chart, iframe, and long page can increase rendering cost and must be checked on representative mobile hardware.
- JavaScript failure must expose usable navigation, all essential section content, direct article links, and a submit-capable form.
- SMTP outage, duplicate submission, invalid input, missing configuration, and mail-header injection must produce safe feedback without losing valid user input or claiming delivery.
- Current blog tests contain stale assumptions, including a nonexistent `Comment` import and a mismatched `get_absolute_url` contract; related test maintenance is required as part of changing article behavior.

## 10. Security concerns

- Keep CSRF protection on the inquiry POST and validate every field server-side regardless of browser validation.
- Limit field lengths, normalize email input, reject honeypot submissions, avoid reflecting sensitive data, and warn users not to submit passwords or private customer information.
- Build mail subjects and bodies from validated values without treating user input as headers; keep recipients and SMTP credentials environment-controlled.
- Add a modest session-based repeat-submission cooldown and document that production edge-level abuse protection remains necessary for stronger rate limiting.
- Render CMS article content through the repository's existing trusted-admin rich-text boundary; do not broaden authoring permissions or introduce raw visitor HTML.
- Preserve secure cookies, HTTPS redirects, external-link `rel` protection, visible focus, and safe iframe attributes.

## 11. Testing strategy

- Form unit tests cover required fields, length limits, email validation, honeypot rejection, and optional values.
- Homepage view tests cover GET context, the exact three published Insight selections and order, draft/missing-post fallbacks, invalid POST rendering, successful email delivery and redirect, delivery failure, and repeat-submission cooldown.
- Template assertions cover approved section order, one logical H1, navigation anchors, CSRF markup, accessible form labels/errors, external-link protections, and page-specific asset loading.
- Blog view tests cover strict `pk`/`slug` matching, draft rejection, Guardrails-only Signal Transcript selection, standard-template behavior for other posts, related published posts, and canonical URLs.
- Run `DEBUG=True venv/bin/python manage.py test apps.pages apps.blog`, then `DEBUG=True venv/bin/python manage.py test`, followed by `DEBUG=True venv/bin/python manage.py check`.
- Manually verify desktop, tablet, and phone layouts; keyboard-only navigation; screen-reader announcements; no-script behavior; reduced motion; horizontal overflow; form failure/success focus; external destinations; and representative mobile performance.

## 12. Assumptions and unresolved questions

- The three approved homepage Insight posts remain the Guardrails, Constraints, and Revival slugs shown in the approved mockups; changing that editorial selection later requires an explicit content-management decision.
- Signal Transcript remains Guardrails-only. Generalizing it across arbitrary rich-text posts is outside this approved scope.
- The project brief sends plain-text email and stores no inquiry record. Production SMTP host, credentials, sender, recipient, and operational owner must be supplied through environment variables before deployment.
- A per-session cooldown and honeypot are baseline safeguards, not a substitute for production edge rate limiting or a managed anti-abuse service.
- No analytics provider exists in the inspected repository. The implementation may expose stable semantic event hooks, but adding third-party tracking requires a separate privacy and provider decision.
- Final service wording, case-study permissions, Calendly expectations, privacy language, and any response-time promise require business-owner validation before launch.

## 13. Step-by-step plan

- [x] Add page-scoped metadata, body, stylesheet, and script extension points in `templates/base.html`; replace `templates/home.html` composition with the approved semantic section order and establish shared responsive tokens in `static/pages/home.css`.
- [ ] Rebuild `templates/includes/navbar.html` and `templates/includes/hero.html` as the approved native navigation and Hero C mosaic, add the approved working-photo asset under `static/pages/images/`, and implement menu/mosaic/reduced-motion behavior in `static/pages/home.js`.
- [ ] Add `templates/includes/services.html` with the approved Services B editorial ledger, five verified service categories, progressive disclosure where specified, and internal Start a Project routing.
- [ ] Add `templates/includes/case_studies.html`, promote the approved evidence assets into `static/pages/images/`, and implement Case Studies B with semantic Client Work / Founder Product views, verified artifact links, and a no-script content fallback.
- [ ] Add `templates/includes/development_process.html` with Development Process D's five ordered stages, illustrative working canvas, reduced-motion-safe card treatment, and internal project-inquiry route.
- [ ] Update `apps/pages/views.py` to retrieve the three approved published Insight posts by stable slug with prefetched categories and fallback context, then add `templates/includes/insights.html` with the responsive Insights C tuner and dynamic internal article/archive routes.
- [ ] Tighten the canonical post contract in `apps/blog/models.py` and `apps/blog/views.py`, add `templates/blog/insight_detail.html` and `static/blog/insight_detail.css`, and render Signal Transcript only for the approved Guardrails slug while preserving the standard template for every other published post.
- [ ] Rebuild `templates/includes/about.html` as About A using the approved founder content, existing portrait and wordmark, semantic five-part skillset visualization, lazy Watch Me Build embed, and verified résumé/conversation destinations.
- [ ] Add the validated project-brief contract in `apps/pages/forms.py`, plain-text notification template in `templates/email/project_inquiry.txt`, environment-driven mail settings in `hrcodes/settings.py`, and CSRF-protected POST/Redirect/GET handling with safe failure feedback and session cooldown in `apps/pages/views.py`.
- [ ] Add `templates/includes/start_project.html` and progressive brief-builder behavior in `static/pages/home.js`, preserving server-rendered errors and values while implementing accessible steps, live summary, focus management, success messaging, no-script completion, and the direct Calendly alternative.
- [ ] Rebuild `templates/includes/footer.html` as Footer B and complete cross-section anchor, numbering, route-board, external-link, heading-hierarchy, reduced-motion, and responsive-continuity reconciliation across `templates/home.html` and `static/pages/home.css`.
- [ ] Add and repair focused coverage in `apps/pages/tests/test_forms.py`, `apps/pages/tests/test_views.py`, `apps/blog/tests/test_blog_views.py`, and `apps/blog/tests/test_blog_model.py` for the approved data, routing, form, email, security, template-selection, and regression contracts.
