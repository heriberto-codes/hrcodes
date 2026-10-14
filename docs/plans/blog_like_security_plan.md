# Blog Like Security Implementation Plan

Selected backlog item: Secure blog likes with CSRF-protected POST actions limited to exact published posts

Feature slug: `blog_like_security`

## 1. Architecture grounding

- Keep anonymous HTML actions in the existing Django function-based blog views, ORM, templates, and session boundary. Preserve SQLite locally, PostgreSQL in production, and WhiteNoise asset delivery.
- Keep the public `like_post` URL name and route identifiers. Use the existing CSRF middleware, secure cookies, and HTTPS settings without configuration changes.
- `architecture.md` still describes a template-only homepage and leaves publication filtering unresolved. Executable code now has a project-brief FormView and strict published article-detail lookup; preserve those implemented contracts.

## 2. Approved design grounding

- No `docs/design/blog_like_security/` workspace exists. This is a targeted security change with a necessary form-control replacement, not a new visual direction.
- Preserve the existing Like label, icon, count placement, article layouts, and redirect feedback. Use native forms that work without JavaScript.

## 3. Tech stack detected

- Django 5.1.2, synchronous function views, `Post`/`Like`, database-backed sessions, Django templates, and authored CSS.
- Existing tests use Django `TestCase`, `Client`, `reverse`, and explicit module labels. CSRF tests must use `Client(enforce_csrf_checks=True)`.
- Context7 official Django documentation and the installed decorator implementation confirm `require_POST`; version-matched [method documentation](https://docs.djangoproject.com/en/5.1/topics/http/decorators/) and [CSRF documentation](https://docs.djangoproject.com/en/5.1/ref/csrf/) confirm the method and token contracts.

## 4. Files impacted

- Modify `apps/blog/views.py`: exact published lookup, canonical redirect, POST restriction, and read-only Like lookup during article rendering.
- Add `templates/blog/includes/like_form.html`; use it in `templates/blog/blog_detail.html`, `templates/blog/blog_index.html`, and `templates/includes/blog_home_page.html`.
- Modify `static/blog/blog.css` only for the new form/button classes and visible keyboard focus.
- Add `apps/blog/tests/test_like_views.py` during the applicable TEST phases; extend `apps/blog/tests/test_blog_views.py` where existing detail and template contracts are affected.
- Inspect `apps/blog/models.py`, `apps/blog/urls.py`, `templates/blog/insight_detail.html`, and `hrcodes/settings.py` as unchanged contracts.

## 5. Data / DB changes

- No schema change or migration. Retain the existing Like count and sequential per-session deduplication using `liked_posts`.
- Create or increment Like rows only inside an accepted like POST. Article GET requests must read existing counts and display zero when no row exists, without creating a row.

## 6. API endpoints

- Preserve `/blog/liked/<pk>/<slug>` and `like_post`; require POST for mutation.
- GET/HEAD to the action return HTTP 405 with POST allowed and no Like/session mutation. Other non-POST methods cannot mutate; CSRF middleware may reject unsafe requests before method validation.
- Missing/invalid CSRF protection returns HTTP 403 before mutation. A CSRF-valid POST for a missing post, mismatched slug, or unpublished post returns HTTP 404 without changing Like rows or `liked_posts`.
- An accepted POST redirects to the resolved post's canonical detail URL with the existing `?liked=true` feedback. A sequential repeat in the same session redirects without another increment.

## 7. Frontend components

- Replace all three existing like anchors with a shared internal POST form containing a CSRF token and a native submit button with an article-specific accessible name.
- Scope styles to the new classes, preserve the surrounding count markup, and override inherited button animation/outline suppression to provide stable controls and visible focus.
- The legacy homepage blog include is currently unused but contains a like action; update its control consistently. Do not add a like control to the Guardrails transcript, which has none today.

## 8. Implementation approach

- First require `pk`, `slug`, and `status=1` together in the like lookup, before reading/updating deduplication state or creating/incrementing Like rows. Build redirects from the resolved post rather than submitted destinations.
- Then change the method contract and all its template callers together: apply `require_POST`, retain `CsrfViewMiddleware` without exemptions, and submit same-origin CSRF-bearing forms. Add no JavaScript request layer.
- Remove `Like.objects.get_or_create()` from standard article rendering. Preserve the `like` context contract with an existing row or an empty value; render the missing count as zero.
- Preserve existing sequential duplicate behavior, standard article rendering, and Guardrails template selection. Do not alter publication filtering in blog index/category queries, redesign feedback, or introduce authentication, rate limiting, count-concurrency guarantees, or new persistence.

## 9. Risks & edge cases

- A draft, a forged slug, or a missing ID must fail before any count or session change. Validate identifiers even when the session already lists that post as liked.
- Default Django clients bypass CSRF enforcement; ordinary POST tests alone cannot prove this repair. Test denied requests against both absent and pre-existing Like rows.
- Removing GET row creation must preserve first-visit zero counts and existing counts. Requests with `?liked=true` are presentation only and must never authorize mutation.
- The existing Like foreign key is not unique, and increments use read/modify/save. Concurrent first likes, overlapping session requests, and lost count updates are existing limitations; this plan makes no concurrency or exactly-once guarantee.
- Fresh sessions can still like again. Session deduplication and CSRF are not abuse throttling or a unique-person identity scheme.

## 10. Security concerns

- Method validation, CSRF checks, and exact published-object selection are separate requirements. None may be substituted for another.
- Use only the post selected by the URL lookup; ignore any submitted post identity or redirect target. Keep all token-bearing form actions internal and keep session/CSRF cookies and HTTPS protections intact.
- Safe page requests must not create Like rows or increase counts. Test the action and article-rendering paths, including rejected identifiers and duplicate submissions.
- Existing category draft visibility and broader published-query consistency remain separate backlog concerns. This feature protects the like mutation boundary and retains strict article-detail filtering.

## 11. Testing strategy

- Step 1 TEST: cover a matching published post, mismatched slug, draft, missing ID, and a draft/mismatch already represented in `liked_posts`. Assert unchanged rows/counts and deduplication state on rejection; verify canonical redirect and sequential duplicate behavior.
- Step 2 TEST: with real CSRF enforcement, reject POSTs with missing cookie, missing token, invalid token, and an untrusted Origin; accept a valid same-origin form POST. GET/HEAD to the action must return 405, advertise POST, and leave database/session state unchanged. A CSRF-valid unsupported unsafe method must also return 405 without mutation.
- Assert standard article GET/HEAD reads do not create Like rows, missing counts display zero, and existing counts are retained. Verify GET feedback flags do not increment counts.
- Render index/detail controls with real request context; assert POST actions, tokens, native submit buttons, and absence of like anchors. Exercise the legacy include with request context and ensure draft index entries produce no like control.
- Follow an actual rendered form through a CSRF-valid POST and redirect to prove a count of one, feedback, and repeat suppression. Retain Guardrails template/related-post and standard article routing regressions.
- Run focused modules `apps.blog.tests.test_like_views` and `apps.blog.tests.test_blog_views`, then the full explicit set: `apps.pages.tests.test_forms`, `apps.pages.tests.test_models`, `apps.pages.tests.test_sentry_privacy`, `apps.pages.tests.test_throttling`, `apps.pages.tests.test_views`, `apps.blog.tests.test_blog_model`, `apps.blog.tests.test_blog_views`, `apps.blog.tests.test_like_views`, and `apps.archive.tests.test_archive_views`. Use `PYTHONDONTWRITEBYTECODE=1 DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test` with those labels, followed by Django `check` with the same environment.
- Existing default discovery previously found zero tests; do not report that as success. Preserve the existing CKEditor warning as a separate concern. During UI validation, check keyboard focus and submit behavior with JavaScript disabled.

## 12. Assumptions and unresolved questions

- Auto-selection uses the first unchecked feature item in `docs/backlog.md`; the derived concise slug is `blog_like_security`.
- Anonymous likes and sequential per-session suppression remain the product contract. Stronger deduplication, counter concurrency, schema uniqueness, and abuse controls need separate scope.
- Preserve the existing redirect flag/icon feedback; a richer feedback redesign remains a separate client backlog item. The necessary POST form replacement is part of this method transition, without marking that separate item complete.
- The first step tightens object selection while retaining the existing method temporarily. Full CSRF/method protection is delivered by the second step; do not claim the feature secure after the first step alone.
- No implementation, test changes, backlog updates, or feature finalization are performed during PLAN. Each step receives its own required execution and validation loop.

## 13. Step-by-step plan

- [x] Tighten `like_post` in `apps/blog/views.py` to resolve the exact published `pk`/`slug` before any Like or session handling and redirect through the resolved post's canonical URL, preserving sequential duplicate behavior; add rejection, no-mutation, canonical-redirect, and repeat regressions in `apps/blog/tests/test_like_views.py` during this step's TEST phase.
- [x] Complete the POST/CSRF transition in `apps/blog/views.py`, make standard article Like reads side-effect-free, add `templates/blog/includes/like_form.html`, replace like anchors in `templates/blog/blog_detail.html`, `templates/blog/blog_index.html`, and `templates/includes/blog_home_page.html`, and add scoped control/focus styles in `static/blog/blog.css`; during this step's TEST phase extend `apps/blog/tests/test_like_views.py` and `apps/blog/tests/test_blog_views.py` for enforced CSRF, rejected methods without mutation, read-only article requests, zero/existing counts, token-bearing forms, sequential duplicates, and existing article-template behavior.
