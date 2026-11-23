# About Profile Refresh Implementation Plan

Feature slug: `about_profile_refresh`

Selected backlog item: Refresh résumé links and add current Boston University study beneath the About portrait using the approved design (`about_profile_refresh`)

## 1. Architecture grounding

Keep Django server rendering, homepage includes, authored static CSS, and native outbound links. No API, model, query, session, authentication, or routing change is required. Local SQLite, production PostgreSQL, WhiteNoise/Gunicorn delivery, and environment-driven deployment remain unchanged.

`architecture.md` describes a template view loading recent posts; current `HomePageView(FormView)` handles project inquiries and curated published insight channels. Preserve the executable view/context contract and inquiry security controls. This content/style change needs no view modification. Leave configuration, migrations, generated `staticfiles/`, virtual environments, and deployment paths alone.

## 2. Approved design grounding

The [approved design](../design/about_profile_refresh/approved-design.md) and [checkpoint](../design/about_profile_refresh/checkpoint.md), dated 2026-11-22, approve **Continuity — current studies** for planning. Use the [specification](../design/about_profile_refresh/design-spec.md) and [assembled preview](../design/about_profile_refresh/mockups/assembled/continuity.html#about) for visual detail; the approval artifacts supersede the specification's earlier pending-checkpoint wording.

Preserve role → name, then add a fine divider and two paragraphs: **Current student · Boston University** and **Master’s in Software Engineering for Artificial Intelligence**. Keep the portrait, About content/actions, brand, desktop sticky column, and mobile order. Update all identified old résumé links to the exact November URL. The approved scope includes a destination-only change in the historical About mockup without reopening its design approval.

## 3. Tech stack detected

Django templates/static tags, existing `static/pages/home.css` tokens, IBM Plex Mono, and Django `TestCase` view tests. No JavaScript change or new dependency is needed. Planning relies on inspected local template/style/test contracts; no new third-party API behavior is assumed.

## 4. Files impacted

| Path | Change |
| --- | --- |
| `templates/includes/about.html` | November résumé destination and approved education caption |
| `static/pages/home.css` | Scoped education group styling beside existing portrait-caption rules |
| `templates/home.html` | Refresh the existing homepage CSS query version alongside the stylesheet change |
| `docs/design/business_focused_homepage/mockups/about/direction-a.html` | Replace only the old résumé href; preserve historical download attributes, content, and design |
| `apps/pages/tests/test_views.py` | Update affected URL/cache expectations and education assertions during the applicable step's TEST phase |

No new asset or application file is required. Re-search authored sources during implementation; any additional actual old résumé link falls within destination replacement scope, while historical prose/evidence describing the old state stays intact.

## 5. Data / DB changes

None. Education text and résumé links are authored template content. Database-managed blog content is outside the audited repository-link scope; no production data access or migration is required.

## 6. API endpoints

None. Reuse the existing homepage and external PDF link without changing URL names or context.

## 7. Frontend components

Extend the existing portrait caption with a noninteractive education group in normal reading order. Use separate paragraph hooks for status/institution and the full program title. Preserve the existing résumé link's visible label, decorative arrow, hidden new-tab announcement, `target="_blank"`, and `rel="noopener noreferrer"`.

## 8. Implementation approach

First replace the live and historical clickable résumé hrefs with `https://hroman-codes.s3.us-east-2.amazonaws.com/HRomandevresume_November_2026.pdf`. The bucket, region, and path all differ; replace the complete destination. Preserve each link's existing behavior, including the historical mockup's download attribute. Do not rewrite unrelated service/company/architecture PDFs or historical audit evidence.

Then add the approved education group beneath the existing name inside the caption. Reuse `--line-dark` for the divider, 11px top margin and 16px top padding. Status text uses `--navy-deep`, 0.75rem, weight 600, and line-height 1.6. Program text uses `--ink`, 0.875rem, line-height 1.65, and 8px separation. Reset paragraph margins within this group and allow natural wrapping with `overflow-wrap: anywhere`. Preserve existing caption flex spacing, outer divider, role span, name, and responsive rules. Implement from the approved design in application sources; do not import preview markup/assets or review UI.

Update only the CSS query version in `templates/home.html`, currently `20261122-case-studies-2`, to a new feature-specific value when changing CSS. Keep the JavaScript query version unchanged.

## 9. Risks and edge cases

The full program title increases caption height and wraps differently across portrait-column widths. Avoid fixed heights, truncation, forced line breaks, or new breakpoints. Preserve desktop sticky behavior above 760px and mobile order below it; check intermediate widths and short viewport scrolling.

The mockup's education block fits enlarged text, but inherited headline/context overflow was observed at narrow enlarged-text widths. Record those existing limits separately from any new caption regression; broader accessibility redesign is outside the approved scope. Search results in approval/audit records are historical evidence rather than active links to replace indiscriminately.

## 10. Security concerns

Use the exact supplied HTTPS destination and preserve outbound-link attributes and keyboard semantics. Add plain text only; do not introduce embeds, university branding, credentials, remote scripts, or request-handling changes. Preserve CSRF, inquiry throttling, Sentry privacy, admin boundaries, and production settings.

## 11. Testing strategy

During step 1's TEST phase, update `TestViews.test_home_renders_about_a_semantic_and_destination_contract` to expect the complete November URL, preserve link semantics, and reject the old résumé destination in rendered About HTML. Check the historical mockup's href manually and inspect its destination-only diff; no new automated test for that static preview is necessary.

During step 2's TEST phase, extend the same rendered-HTML contract to verify both exact education statements appear once within the portrait caption after the preserved role/name. Update the CSS-version expectation in `TestViews.test_home_uses_page_scoped_foundation`. Keep existing About interaction/responsive coverage; verify actual wrapping/layout in the browser rather than adding source-string tests mirroring new CSS declarations.

For each step, run the affected `apps.pages.tests.test_views.TestViews` methods first, then the `apps.pages.tests.test_views` module, using `DEBUG=True venv/bin/python manage.py test` with the relevant labels. Run the full Django suite before feature completion and `DEBUG=True venv/bin/python manage.py check` separately. Prior plans record default discovery limitations: if default discovery finds zero tests, use the explicit existing module labels `apps.pages.tests.test_views`, `apps.pages.tests.test_forms`, `apps.pages.tests.test_models`, `apps.pages.tests.test_throttling`, `apps.pages.tests.test_sentry_privacy`, `apps.blog.tests.test_blog_views`, `apps.blog.tests.test_blog_model`, `apps.blog.tests.test_admin`, `apps.blog.tests.test_like_views`, and `apps.archive.tests.test_archive_views`. Zero discovered tests do not establish a pass.

Inspect the actual Django homepage at 320, 390, 768, 1000, and 1440px. Compare the caption with approved desktop/mobile previews; check portrait decoding, text order, full program visibility, group/document overflow, desktop stickiness, mobile stacking, unchanged surrounding content, and résumé keyboard focus/new-tab announcement. Check enlarged text and actual browser zoom where tooling permits, recording unavailable checks explicitly. Do not count preview-only checks as application validation or assert remote PDF availability/content without separately checking it.

## 12. Assumptions and unresolved questions

The user supplies enrollment facts, program wording, and the résumé destination. No graduation date or completed-degree claim is authorized. There are no unresolved design decisions. External PDF availability/content, real-device/screen-reader checks, and actual browser zoom remain unverified; report verification limits accurately. No production deployment or external form submission is part of validation.

Each unchecked step must pass EXECUTE → VERIFY → ENGINEER CHECKPOINT → TEST, with DEBUG if needed, before `turtle-engineer-plan-step-update` may mark it complete. Test changes belong to TEST, not EXECUTE.

## 13. Step-by-step plan

- [x] Update the résumé href in `templates/includes/about.html` and the historical clickable href in `docs/design/business_focused_homepage/mockups/about/direction-a.html` to the exact supplied November URL, rechecking authored sources for additional old résumé destinations while preserving existing link semantics, unrelated PDFs, and historical design/evidence.
- [x] Add the approved current-student/institution and full program paragraphs beneath the preserved role/name in `templates/includes/about.html`, implement the scoped education styling in `static/pages/home.css`, and refresh only the CSS query version in `templates/home.html`, preserving the existing desktop/mobile composition and all surrounding About content.
