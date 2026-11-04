# Security Regression Coverage

Feature slug: `security_regression_coverage`

Completed: 2026-11-04

Backlog item: Add security regression coverage for inquiry throttling, like mutations, and draft exposure

## Summary

- Added regression coverage for inquiry middleware and throttling, stale like forms, and publication withdrawal across public read surfaces.
- All three plan steps and the matching backlog item are complete. EXECUTE reconciled existing guards as already satisfied; VERIFY and ENGINEER CHECKPOINT passed, TEST completed, and PLAN STEP UPDATE marked each step complete. No runtime defect required DEBUG.
- SECURITY found no issues within the feature scope. PERFORMANCE found no introduced regression; the existing listing-query improvement was accepted as an optional follow-up.

## Architecture Impact

- Changes are confined to existing owning-app tests and workflow documentation. Production views, models, templates, routes, dependencies, and configuration are unchanged.
- No API, database schema, migration, or frontend changes. Existing publication, CSRF, session, and throttle contracts remain intact.

## Decisions

- Exercise CSRF with enforced test clients, tokens from rendered forms, cookies, and explicit origins. Preserve positive controls so middleware rejection cannot conceal application behavior.
- Capture like forms before changing article publication or slug. Check missing/existing Like rows and previously liked sessions, comparing complete stored row and session snapshots after rejection.
- Revisit public surfaces with the same client after changing a published post to draft. Assert context and rendered content, direct-detail 404 responses, and preservation of published companions and fallbacks.
- Reuse existing fixture builders, parsers, throttle/model coverage, and Django test tools. Use synthetic inquiry data, in-memory email, a fixed throttle clock, and an empty Sentry DSN during validation.

## Test Impact

- `apps/pages/tests/test_views.py`: strengthened inquiry CSRF rejection against seeded throttle/session state for missing cookies, missing or malformed tokens, and untrusted origins. Valid rendered-token submissions confirm that fresh sessions sharing an address share quota, while a different address remains eligible.
- `apps/blog/tests/test_like_views.py`: added stale-form rejection after unpublishing and slug changes. Rejected requests return 404 without Like/session mutations; a newly rendered canonical form remains the positive control after renaming.
- `apps/blog/tests/test_blog_views.py`: added published-to-draft transitions across index, category, direct detail, and Guardrails related signals, checking context, content, and links.
- `apps/pages/tests/test_views.py`: added homepage publication withdrawal and extended existing form-redisplay coverage to limiter exceptions. Assertions preserve published insights and generic feedback, exclude draft content and raw exception text, and prevent email delivery.
- Four new test methods plus extensions to existing tests; no coverage-percentage claim is made.
- Recorded TEST validation passed: **3 targeted tests**, **76 publication-focused tests**, and the **136-test full explicit suite**. The full suite used all nine module labels listed in `docs/plans/security_regression_coverage_plan.md`.
- Django configuration validation and whitespace checks passed. The existing `ckeditor.W001` warning remains. Tests were not rerun during documentation.

## Deployment Notes

- No deployment, production data changes, new environment variables, or migration steps were required or performed.

## Follow-ups / Accepted Risks

- Default test discovery remains a separate issue; continue using explicit module labels and confirm a nonzero test count.
- Category queries in blog listings remain an optional backlog improvement. With an expected maximum of about 20 posts and no measured slowdown, revisit category prefetching if listings slow down or content grows substantially. Pagination is not required for this feature; no production benchmark was performed.
- Existing SQLite concurrency coverage does not establish arbitrary PostgreSQL scheduling behavior. No concurrency guarantee was expanded.
- Foundational architecture/map descriptions remain stale in places; executable code governs current homepage, publication, and like behavior. Their refresh and the existing rich-text authoring follow-up remain separate work.
