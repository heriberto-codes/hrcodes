# Blog Like Security

Feature slug: `blog_like_security`

Completed: 2026-10-13

Backlog item: Secure blog likes with CSRF-protected POST actions limited to exact published posts

## Summary

- Likes now require a CSRF-protected POST for the exact published post identified by the URL's `pk` and `slug`.
- Opening a standard article reads its existing Like record and displays zero when none exists, without creating a record or changing its count.
- Native Like forms work without JavaScript and retain the existing redirect/icon feedback and sequential per-session repeat suppression.
- Both implementation-plan steps and the matching backlog item are complete. VERIFY, ENGINEER CHECKPOINT, TEST, SECURITY, and PERFORMANCE passed; DEBUG was not needed.

## Architecture Impact

- `apps/blog/views.py` owns post resolution, method enforcement, Like persistence, and session deduplication within the existing Django request boundary.
- `templates/blog/includes/like_form.html` provides the shared internal POST form for article detail, blog index, and the legacy homepage blog include. The legacy include remains unused by the current homepage.
- `static/blog/blog.css` scopes the form/button layout, disables inherited button animation and hover shadows, and supplies a visible orange focus outline.
- The Guardrails transcript retains its existing template and related-post behavior, with no Like form.

## Decisions

- Apply `@require_POST` and retain the enabled `CsrfViewMiddleware` without a CSRF exemption.
- Resolve `pk`, `slug`, and `status=1` before reading or changing Like/session state, including when the session already lists the post as liked.
- Build redirects from the resolved post's `get_absolute_url()`; submitted post identifiers and redirect destinations do not control the action.
- Preserve anonymous Likes and the existing `liked_posts` session list. A sequential repeat redirects without incrementing again.
- Use `.filter(post=post).first()` for standard article reads and the template's `default:"0"` fallback. The `?liked=true` flag changes presentation only.
- Give the submit button an escaped article-specific accessible name and hide its decorative icon from assistive technology. Native keyboard activation and form submission require no added JavaScript.

## API Changes

The `like_post` URL name and `/blog/liked/<pk>/<slug>` route are preserved.

| Request | Outcome |
| --- | --- |
| Valid-CSRF POST matching an exact published post | Increment once per session; redirect with HTTP 302 to its canonical detail URL plus `?liked=true`. |
| Sequential repeat in the same session | Same redirect; count and session remain unchanged. |
| GET or HEAD to the Like action | HTTP 405 with `Allow: POST`; no Like/session mutation. |
| CSRF-valid PUT, PATCH, or DELETE | HTTP 405; no Like/session mutation. |
| POST with missing/invalid CSRF protection or an untrusted Origin | HTTP 403; no Like/session mutation. |
| Valid-CSRF POST for a missing ID, wrong slug, or draft | HTTP 404; no Like/session mutation. |

CSRF middleware can reject unsupported unsafe methods before the method decorator runs. Standard article GET/HEAD reads retain their existing route and publication checks.

## Database Changes

- No schema changes or migrations. Existing Like counts are preserved.
- Like records are created or incremented only by accepted Like POSTs; article reads perform a read-only lookup.

## Test Impact

- `apps/blog/tests/test_like_views.py` covers exact-post rejection, canonical redirects, first/existing counts, and repeat suppression using clients with CSRF enforcement and tokens extracted from real rendered forms.
- Rejected-request coverage includes 16 missing-cookie/token, mismatched-token, and untrusted-Origin subcases plus 10 non-POST method subcases. Assertions preserve full Like row snapshots and session dictionaries.
- `apps/blog/tests/test_blog_views.py` checks 18 article reads across missing, zero, and positive counts, repeated GET/HEAD, and feedback flags; validates working token-bearing forms in all three callers, escaped accessible labels, absence of Like anchors/draft controls, and unchanged Guardrails behavior.
- A fresh-session form POST follows the canonical redirect, shows count/feedback, ignores alternate submitted identifiers/destinations, and preserves state on a repeat.
- Focused blog modules: **23 tests passed**. Full explicit suite across pages, blog, and archive: **120 tests passed**. Runs used `PYTHONDONTWRITEBYTECODE=1 DEBUG=True SENTRY_DSN=''` with `venv/bin/python manage.py test` and the explicit labels listed in the completed plan.
- Django `check` and `git diff --check` passed; the existing `ckeditor.W001` warning remains.
- Chrome validation with JavaScript disabled confirmed Tab focus, a visible 2px orange outline with a 3px offset, stable hover dimensions, native Enter/Space POST submission, and unchanged counts on sequential repeats. Validation used synthetic data in an isolated temporary database; the server was stopped and the database removed afterward.

## Deployment Notes

- Release the view, shared form, caller templates, and authored CSS together so rendered controls match the endpoint's POST contract.
- No new environment variables or migration requirements. Existing production HTTPS and secure-cookie settings remain in place.
- No deployment was performed during this feature workflow.

## Follow-ups / Accepted Risks

- SECURITY passed for this repair's scope. Fresh sessions can still Like again; session deduplication is not unique-person identity or abuse throttling. Stronger abuse controls remain separate work.
- The existing Like foreign key is nonunique and increments use read/modify/save. Concurrent requests can produce duplicate rows or lost increments; this feature guarantees only sequential repeat suppression. Uniqueness and atomic increments need separate scope.
- PERFORMANCE passed by static review. The existing blog index still loads all posts and queries categories per rendered post; pagination and category prefetching are follow-ups as the archive grows. No production load benchmark was performed.
- Broader published-query consistency and category draft exposure remain separate backlog work. Richer Like success feedback remains a separate client backlog item; this feature preserves the existing flag/icon feedback.
- `architecture.md` still contains older homepage and GET-Like descriptions; executable code and this feature record describe the completed behavior.
