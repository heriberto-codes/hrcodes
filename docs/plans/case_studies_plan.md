# Turtle AI Case Studies Implementation Plan

Feature slug: `case_studies`

Selected backlog item: Add Turtle AI as the second founder case study while preserving the approved site design (`case_studies`)

## 1. Architecture grounding

Keep Django server rendering and the homepage include boundary. Case content is static HTML in `templates/includes/case_studies.html`; styling and progressive enhancement live in `static/pages/home.css` and `static/pages/home.js`. No new service, framework, build system, or persistence is needed.

`architecture.md` describes the homepage as a template view adding recent posts; executable code now uses `HomePageView(FormView)` with inquiry handling and shared database throttling. Preserve that implemented boundary and its security controls. This feature needs no view change. Keep existing URL names, context, blog/admin authentication, session behavior, WhiteNoise/Gunicorn deployment, and environment configuration.

## 2. Approved design grounding

The [approved design](../design/case_studies/approved-design.md) and [approved checkpoint](../design/case_studies/checkpoint.md), dated 2026-11-21, select **Continuity — Turtle AI addition**. Use these for design intent, the [specification](../design/case_studies/design-spec.md) for detail, and the [assembled preview](../design/case_studies/mockups/assembled/continuity.html?group=founder) as a visual reference. Reimplement in existing authored files; do not import the standalone mockup or its script.

Preserve the four default client cases/order, cThink first, existing article structure, palette, typography, navigation IDs, and Services → Case Studies → Development Process sequence. Append **02 / Founder project — Turtle AI**, using the approved Understand → Build → Show text, descriptor, full-square artwork, alt text, three evidence links, and initially open native disclosure. Coordinate the introduction count, Founder Projects tab/index label, numbered link, and no-script explanation with inclusion.

Preserve desktop `.home-case-rail` stickiness at `top: 32px`, with the existing stacked, static rail at 1080px and below. The static preview does not replace this behavior. Retain one closing band outside both panels, its visible copy and `#start-a-project` destination; remove only its mismatched overriding action `aria-label`.

## 3. Tech stack detected

Django 5.1.2, Django templates/static tags, existing homepage CSS variables and IBM Plex Mono, plain deferred JavaScript, native links/disclosures, and Django's existing test runner. SQLite remains local and PostgreSQL production. Existing test coverage resides in `apps/pages/tests/test_views.py`; browser checks are needed for actual layout, focus, and navigation behavior. Planning relies on inspected repository behavior rather than new third-party API assumptions.

## 4. Files impacted

| Path | Intended change |
| --- | --- |
| `static/pages/images/turtle-ai-overview.png` | New delivery asset derived from the approved 1254 × 1254 overview |
| `static/pages/images/turtle-ai-LICENSE.txt` | Preserve the source MIT notice beside the derived asset |
| `templates/includes/case_studies.html` | New case plus coordinated count, labels, index, fallback, wrapping hook, and inquiry accessible name |
| `static/pages/home.css` | Scoped square image, wrapping, new-card evidence/focus/spacing, and dark-surface focus rules |
| `static/pages/home.js` | Select the appropriate existing panel from either founder case hash |
| `templates/home.html` | Refresh existing CSS/JavaScript query-version values for changed assets |
| `apps/pages/tests/test_views.py` | Update affected case contracts during the implementation step's TEST phase |

The approved source image and notice are under `docs/design/case_studies/mockups/assets/`. Read these as source assets, without importing mockup HTML/CSS/JavaScript. Leave `staticfiles/`, unrelated assets, configuration, migrations, and other plans unchanged.

## 5. Data / DB changes

None. The new case is authored content; no migration, model, CMS, query, or session change is required.

## 6. API endpoints

None. Reuse the homepage and native `#case-turtle-ai` / `#start-a-project` anchors. Preserve inquiry POST behavior and all current routes.

## 7. Frontend components

Extend the existing founder panel and index without renaming their `*-product` IDs. Keep the new article's identity → image → three narrative steps → evidence disclosure structure. Preserve all five existing article bodies, links, images, and initial disclosure states. The new evidence links use the public repository and the two approved documents pinned to `04c7a3f732cac0f272eba7c9b031035cfe3eccb0`.

## 8. Implementation approach

Prepare the image and license first as an independent, non-visible change. Compare lossless PNG optimization with the approved original, preserve resolution and all artwork, and use a smaller result only when fidelity is preserved. If available tooling cannot improve delivery safely, retain the approved original and record its size; do not introduce a dependency just to optimize it. Keep lazy loading and explicit image dimensions.

Then integrate the complete feature in one coordinated change so the new count and index never precede the real card. Add only the approved wrapping safeguards and narrowly scoped CSS: full-frame square image with `object-fit: contain` that wins over narrow-screen fixed-height rules; new-card navy evidence titles/focus and 14px mobile action gap; existing peach focus for the relevant dark controls. Preserve tokens, default card styling, and sticky breakpoints. Group “trail.” without losing the production decorative period/pixel markup.

The specification suggests current hash handling is generic, but `home.js` actually special-cases only `#case-cthink`. Extend this existing helper to resolve either founder article to its containing panel and associated tab, retaining the current Client Work default for empty/unrelated hashes. Preserve click/arrow/Home/End behavior, roving focus, hidden indexes/panels, and viewport correction. Do not add the preview-only `?group=founder` behavior or replace the enhancement script.

Update the existing homepage asset query versions alongside CSS/JavaScript changes so browsers request the changed files. Do not change cache infrastructure or the color system.

## 9. Risks & edge cases

The 2.46 MiB source artwork is larger than a normal screenshot; assess size and inspect text legibility after optimization. An existing `static/pages/images/turtleAI.png` has different bytes and is referenced by the blog and legacy work includes; do not overwrite it or substitute it for the approved overview.

Direct loading of `#case-turtle-ai`, later hash changes, and keyboard index activation must reveal the founder panel and reach the actual card. Avoid throwing on unknown hashes. Client anchors and cThink must continue working. Verify scrolling after the target panel is revealed, not just its selected state.

Long descriptors, plural labels, evidence actions, and enlarged text may overflow. Scope fixes to this approved section/new content. The square image must remain uncropped at all breakpoints. Test sticky behavior on the full homepage; the existing short-window sticky limitation and broader audit issues remain deferred. No-JavaScript users must see both labelled indexes and all six articles.

## 10. Security concerns

Use the reviewed HTTPS evidence destinations and existing `target="_blank" rel="noopener noreferrer"` pattern. No remote script, installation command, embed, or new request-handling surface is needed. Preserve the source license and existing CSRF, throttling, sessions, Sentry privacy controls, and real inquiry form. Browser validation should navigate the inquiry anchor without sending a real submission.

## 11. Testing strategy

For the asset step, inspect the rendered image at desktop/phone sizes, confirm 1254 × 1254 dimensions, full artwork and legible text, compare delivery size, and verify the copied license. No new test file is necessary for a static asset preparation step.

During the integration step's TEST phase, update the existing `TestViews` case-study contracts in `apps/pages/tests/test_views.py` for six cases, six narrative sequences/disclosures, three initially open disclosures, founder order, new asset and three evidence URLs, plural wording, and the visible inquiry action name. Replace the assertion requiring the old cThink-only hash expression with coverage aligned to the revised behavior. Prefer semantic rendered-HTML assertions over adding more source-string assertions; source checks do not establish browser behavior.

Run the focused affected `apps.pages.tests.test_views.TestViews` methods, then the full `apps.pages.tests.test_views` module. Run the complete repository suite with explicit existing module labels: `apps.pages.tests.test_views`, `apps.pages.tests.test_forms`, `apps.pages.tests.test_models`, `apps.pages.tests.test_throttling`, `apps.pages.tests.test_sentry_privacy`, `apps.blog.tests.test_blog_views`, `apps.blog.tests.test_blog_model`, `apps.blog.tests.test_admin`, `apps.blog.tests.test_like_views`, and `apps.archive.tests.test_archive_views`. Use `DEBUG=True venv/bin/python manage.py test` with these labels; previous plans record default discovery limitations, so do not count zero discovered tests as a pass. Run `DEBUG=True venv/bin/python manage.py check` separately.

On the full Django homepage, check both groups at 320, 390, 768, and 1440px; enlarged text and actual browser zoom; default Client Work; founder order; click/arrow/Home/End selection and focus; direct initial hashes and subsequent hash navigation for cThink/Turtle AI/client cases; visible index targets; native disclosure keyboard activation; and correct focus colors. Verify the desktop rail stays in place while the right column scrolls, becomes static at 1080px and below, and the inquiry band remains once outside both panels with its exact visible accessible name and working native form anchor. Check full artwork decoding, overflow, existing cases, reduced motion, and JavaScript-disabled access to all six cases. Use Chromium plus Safari/WebKit when available; distinguish WebKit automation from real Safari/device verification, and explicitly record any unavailable browser, screen-reader, or zoom checks.

## 12. Assumptions and unresolved questions

Design approval is complete; there are no new design questions. Image optimization outcome and actual browser/tool availability are implementation verification concerns. Keep the supplied pinned source claims rather than refreshing remote project content during implementation. Unsupported role/date, adoption, productivity, hosted-app, and guaranteed-enforcement claims remain excluded.

Known documentation differences are resolved conservatively above: retain the implemented FormView architecture and extend the actual cThink-only hash helper rather than assuming a generic one already exists. Historical stage prompts in the specification do not override the current approved design/checkpoint. Neither planning nor the preview authorizes deployment.

All steps start unchecked. Each requires EXECUTE → VERIFY → ENGINEER CHECKPOINT → TEST → DEBUG if needed → PLAN STEP UPDATE. Tests belong to each step's TEST phase; only the plan-step-update skill may mark completion.

## 13. Step-by-step plan

- [x] Prepare `static/pages/images/turtle-ai-overview.png` from the approved overview source, assess lossless optimization while preserving its complete 1254 × 1254 artwork, and preserve the source MIT notice in `static/pages/images/turtle-ai-LICENSE.txt`; keep the older `static/pages/images/turtleAI.png` and its consumers unchanged.
- [x] Integrate the approved Turtle AI addition in `templates/includes/case_studies.html`, coordinated with count/label/index/fallback updates and the inquiry action's visible accessible name; add scoped presentation and wrapping rules in `static/pages/home.css`, extend founder hash selection in `static/pages/home.js`, and refresh affected asset query versions in `templates/home.html`, preserving existing cases, palette, sticky rail, keyboard behavior, real form, and no-JavaScript access; update affected coverage in `apps/pages/tests/test_views.py` during this step's TEST phase.
