# Published Post Filtering Plan

Selected backlog item (exact text): Centralize published-post filtering across public blog and homepage queries

Feature slug: `published_post_filtering`

## 1. Architecture grounding

`architecture.md` establishes a server-rendered Django application with app-owned views, template composition, and ORM persistence. Blog data belongs in `apps/blog`; homepage composition belongs in `apps/pages`. Public routes are anonymous; Django authentication and staff permissions protect admin. SQLite is local, PostgreSQL is production, and session state tracks likes. Tests use Django's test runner. Fly.io/Gunicorn and WhiteNoise remain unchanged.

Code supersedes stale architecture descriptions: the homepage is now a `FormView` selecting three configured insight channels, rather than a `TemplateView` selecting two newest posts. Detail and like routes already require exact published posts, and likes use CSRF-protected POST. Preserve these implemented contracts. No service layer, frontend framework, public JSON API, or deployment changes are needed.

## 2. Approved design grounding

No matching `docs/design/published_post_filtering/` workspace exists; standalone planning applies. Preserve existing templates, insight channel hierarchy, fallback copy, and responsive presentation. This work changes which posts reach public rendering, without a visual redesign.

## 3. Tech stack detected and confirmed

- Django 5.1.2, Django ORM, Django templates, Bootstrap/custom CSS, and lightweight JavaScript; confirmed against `requirements.txt`, installed Django, and application code.
- Use a chainable custom `QuerySet` exposed through `as_manager()`. Context7's [official Django manager guidance](https://github.com/django/django/blob/main/docs/topics/db/managers.txt) supports this approach and cautions against filtering the default manager. Installed Django 5.1.2 confirms the method and unfiltered manager behavior; no newer-only API is required.
- Existing publication contract: exactly `status=1` is published; default `status=0` is draft. Retain the integer field and choices.

## 4. Files impacted

- `apps/blog/models.py`: shared publication scope on the post queryset.
- `apps/blog/views.py`: index, category, detail, related insight, and like lookups.
- `apps/pages/views.py`: featured homepage insight selection.
- `apps/blog/tests/test_blog_model.py`, `apps/blog/tests/test_blog_views.py`, `apps/blog/tests/test_like_views.py`, and `apps/pages/tests/test_views.py`: targeted coverage during each step's TEST stage, extending existing cases where sufficient.
- Inspect `apps/blog/admin.py`, `apps/blog/urls.py`, `apps/pages/urls.py`, and existing templates as contracts; no edits are planned.

## 5. Data / DB changes

No schema or stored-data changes. Add `PostQuerySet.published()` in `apps/blog/models.py`, returning a queryset restricted to `status=1`, and expose it through `Post.objects = PostQuerySet.as_manager()`. Keep `objects.all()`, default/base manager access, and admin access unfiltered. Do not enable migration serialization or modify migration history. Confirm migration drift remains absent with a dry-run check during implementation validation.

## 6. API endpoints

Preserve route names and matching semantics:

- `GET /` (`home`): configured published insight channels only, including on form redisplay.
- `GET /blog/` (`blog_index`) and `GET /blog/<category>/` (`blog_category`): published posts only, newest first; preserve the category name `contains` lookup.
- `GET /blog/<pk>/<slug>` (`blog_detail`): exact published identity, retaining standard/Guardrails template selection and published related channels.
- `POST /blog/liked/<pk>/<slug>` (`like_post`): exact published identity before reading or mutating session/like state. Preserve CSRF, method restrictions, once-per-session behavior, and redirect feedback.

No new endpoints or authentication requirements.

## 7. Frontend components

Keep existing view context names, category prefetching on detail/homepage/related queries, and configured channel ordering. The blog index currently hides drafts inside its template; it will receive a published-only queryset instead. A draft-only index will consequently use its existing single empty-state message. The category template currently renders all supplied posts and requires filtering at the view boundary. Retain template guards and like forms; no CSS, JavaScript, or template cleanup is necessary.

## 8. Implementation approach

Define the publication predicate once on the model's queryset, without overriding default manager filtering or adding global ordering. Apply `Post.objects.published()` explicitly at all six public query sites: index, category, detail, Guardrails related posts, likes, and homepage insights. Replace duplicated status predicates; preserve each site's existing additional filters, prefetches, ordering, and context construction.

Use the scoped queryset as the first argument to `get_object_or_404` for detail and like resolution, retaining both `pk` and `slug`. Keep list queries lazy until their existing evaluation point. Do not change category matching, add pagination, fix unrelated model methods, alter like counting, or broaden into the next security-regression backlog item.

## 9. Risks & edge cases

- Filtering the default manager globally could hide drafts from admin and internal operations; publication must remain opt-in.
- Index templates can conceal an unfiltered queryset, so rendered HTML alone is insufficient evidence. Assert the returned context as well.
- Category drafts currently expose title/snippet/link content. Cover drafts sharing a category with published posts and categories containing drafts only.
- Preserve newest-first list ordering and configured homepage/related channel ordering; they are different contracts.
- Treat unsupported non-published integer statuses as excluded, rather than using a truthiness or nonzero test.
- Preserve empty/partial channel fallbacks and category prefetch behavior. No new per-post queries or eager list conversion should be introduced.

## 10. Security concerns

Publication filtering belongs at the ORM boundary before template rendering or like mutation. Draft title, snippet, body, and article/like links must not leak through public query results. Valid CSRF tokens must not permit liking drafts or mismatched identities. Preserve anonymous reading, admin draft management, secure cookies, HTTPS, and existing middleware. No inquiry data, telemetry, credentials, infrastructure, or production data changes are in scope.

## 11. Testing strategy

Tests are added or extended during the corresponding step's TEST stage after VERIFY and ENGINEER CHECKPOINT; they are not separate implementation steps.

- Queryset: published, draft, and unsupported-status fixtures; scope composition before/after another filter and ordering; unfiltered `objects`, default/base manager, and registered `PostAdmin.get_queryset()` still expose drafts. Avoid altering existing image fixtures or unrelated tests.
- Listings: mixed published/draft fixtures in matching categories; assert exact context post identities and newest-first order, absence of draft title/snippet/URLs in HTML, and HTTP 200/template preservation. Cover no posts and draft-only results; assert the index empty-state message appears once.
- Detail/related/likes: reuse existing exact identity, draft 404, POST/CSRF, read-only GET/HEAD, session preservation, and related channel ordering tests. Extend only gaps, including exclusion of non-published statuses and draft Guardrails rendering; require rejected mutations to leave Like rows and session state unchanged.
- Homepage: reuse complete/partial/empty insight tests, including exclusion of unconfigured published notes and drafts. Assert published-only `posts` and `insight_signals`, retained channel order/count/missing names, category prefetches, and unchanged form redisplay behavior.
- Focused runs, as appropriate to each step: `DEBUG=True venv/bin/python manage.py test apps.blog.tests.test_blog_model`, then `DEBUG=True venv/bin/python manage.py test apps.blog.tests.test_blog_views apps.blog.tests.test_like_views`, then `DEBUG=True venv/bin/python manage.py test apps.pages.tests.test_views`.
- After focused checks, run the full repository suite via explicit module labels: `DEBUG=True venv/bin/python manage.py test apps.blog.tests.test_blog_model apps.blog.tests.test_blog_views apps.blog.tests.test_like_views apps.pages.tests.test_forms apps.pages.tests.test_models apps.pages.tests.test_sentry_privacy apps.pages.tests.test_throttling apps.pages.tests.test_views apps.archive.tests.test_archive_views`. Existing feature plans report default discovery finding zero tests and app-label discovery failing with the `apps` namespace; verify a nonzero count and do not treat an empty run as success.
- Run `DEBUG=True venv/bin/python manage.py check` and `DEBUG=True venv/bin/python manage.py makemigrations --check --dry-run`. Use isolated test data and no outbound Sentry transport. Existing CKEditor warnings and test-discovery repairs remain outside scope.

## 12. Assumptions and unresolved questions

- Auto-selected the first unchecked backlog item; this plan is new and has no completed steps to preserve.
- `status=1` remains the complete publication rule; scheduling, author previews, and new statuses are outside scope. No blocking product questions remain.
- Architecture documentation is stale about homepage selection, inquiry persistence, and like behavior. Existing executable behavior governs this plan; refreshing foundational documentation is separate work.
- Admin draft access must remain available without adding a second filtered manager or changing related-object behavior.
- No tests or production commands are run as part of planning. Execute each step through the repository's required implementation loop; only `turtle-plan-step-update` may change step completion state.

## 13. Step-by-step plan

- [x] Add `PostQuerySet.published()` and expose it on the unfiltered `Post.objects` manager in `apps/blog/models.py`; during TEST, cover scope composition and preserved internal/admin draft access in `apps/blog/tests/test_blog_model.py`.
- [x] Apply the shared published scope to `blog_index` and `blog_category` in `apps/blog/views.py`, preserving list ordering and category matching; during TEST, cover published-only context, draft-content exclusion, and empty/draft-only responses in `apps/blog/tests/test_blog_views.py`.
- [x] Replace duplicated publication predicates in `blog_detail`, its related insight query, and `like_post` in `apps/blog/views.py` with the shared scope, preserving exact identity and mutation guards; during TEST, reuse and extend `apps/blog/tests/test_blog_views.py` and `apps/blog/tests/test_like_views.py` for publication rejection and unchanged published behavior.
- [x] Use the shared published scope for featured insight selection in `apps/pages/views.py`, preserving configured channels, prefetches, and context contracts; during TEST, reuse and extend `apps/pages/tests/test_views.py` for complete, partial, empty, and form-redisplay insight behavior, then run the full regression suite and configuration/migration checks.
