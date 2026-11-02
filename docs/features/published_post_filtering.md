# Published Post Filtering

Feature slug: `published_post_filtering`

Completed: 2026-11-01

Backlog item: Centralize published-post filtering across public blog and homepage queries

## Summary

- Public post queries now share one publication rule: exactly `status=1` is published. Drafts and unsupported status values are excluded before rendering or like mutation.
- Blog index and category contexts now contain only published posts, preventing category draft exposure and preserving the index's empty-state fallback.
- All four plan steps and the matching backlog item are complete. EXECUTE, VERIFY, ENGINEER CHECKPOINT, TEST, and PLAN STEP UPDATE completed; DEBUG was not needed. SECURITY and PERFORMANCE reviews passed for this feature's scope.

## Architecture Impact

- `apps/blog/models.py` defines the chainable `PostQuerySet.published()` method and exposes it through `Post.objects = PostQuerySet.as_manager()`.
- `apps/blog/views.py` applies the scope to index, category, detail, related insight, and like queries. `apps/pages/views.py` applies it to featured homepage insights.
- Existing Django view/template boundaries, template context names, and frontend assets are preserved.

## Decisions

- Keep publication filtering opt-in. Ordinary, default, and base managers remain unfiltered, preserving internal and admin draft access.
- Keep the existing integer status field and exact equality rule; no scheduling or draft-preview behavior was added.
- Preserve newest-first listing order and category-name `contains` matching. Homepage and related insights retain their configured channel order.
- Preserve category prefetches on detail, related insight, and homepage queries. The shared method adds a lazy database filter without an extra query.
- Resolve both `pk` and `slug` within the published scope before reading or mutating like/session state. Existing POST, CSRF, and sequential per-session repeat protections remain intact.
- Preserve complete, partial, and empty homepage insight states, including redisplay after invalid, failed-delivery, or throttled form submissions.

## API Changes

- No new endpoints, route names, or authentication requirements.
- Blog index and category responses exclude unpublished posts from both context and rendered content.
- Detail and CSRF-valid like requests for unpublished posts continue to return HTTP 404; rejected likes leave stored counts and session state unchanged.

## Database Changes

- No schema changes, migrations, or stored-data changes.
- Migration drift check reported `No changes detected`.

## Test Impact

- `apps/blog/tests/test_blog_model.py`: added coverage for exact publication status, filter/order composition, empty scopes, unchanged stored statuses, and unfiltered manager/admin access.
- `apps/blog/tests/test_blog_views.py`: added published-only listing contexts, newest-first ordering, category matching, draft-content/link exclusion, empty/draft-only results, and standard/Guardrails rejection of non-published statuses. Extended related insight and category-prefetch coverage.
- `apps/blog/tests/test_like_views.py`: extended existing CSRF-enforced rejection checks to unsupported status values, preserving full Like-row and session snapshots.
- `apps/pages/tests/test_views.py`: strengthened complete, partial, and empty insight coverage; added form-redisplay coverage for invalid input, delivery failure, and throttling. Assertions check order, context counts, missing channels, draft exclusion, fallbacks, and category reads requiring no additional queries.
- Recorded validation: focused homepage module **45 tests passed**; full explicit suite across all nine blog, pages, and archive test modules **132 tests passed**. Module labels are listed in `docs/plans/published_post_filtering_plan.md`.
- Test runs used `DEBUG=True SENTRY_DSN='' DATABASE_URL='sqlite:///:memory:'` with isolated test data. Django `check`, `makemigrations --check --dry-run`, and whitespace validation passed; the existing `ckeditor.W001` warning remains.

## Deployment Notes

- Release the model queryset method and its view callers together.
- No new dependencies, environment variables, migration requirements, or production configuration changes.
- No deployment was performed during this workflow.

## Follow-ups / Accepted Risks

- Future public post queries must explicitly use `.published()`; the default manager deliberately does not enforce publication globally.
- PERFORMANCE identified an existing low-impact category-query-per-post pattern in index/category listings. A separate follow-up can add `prefetch_related('categories')`; pagination or new indexes should follow measurements. No production benchmark was performed.
- Existing test-discovery limitations remain outside scope; validation used explicit module labels rather than treating an empty discovery run as success.
- Foundational architecture documentation still contains older homepage and GET-like descriptions. Executable code and this feature record describe the completed behavior; refreshing those documents remains separate work.
