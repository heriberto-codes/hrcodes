# Like Form Success Feedback Plan

Selected backlog item (exact text): Replace like links with secure no-JavaScript form controls and success feedback

Feature slug: `like_form_success_feedback`

## 1. Architecture grounding

`architecture.md` establishes server-rendered Django HTML routes, reusable template includes, authored CSS, and app-owned ORM persistence. Anonymous public interactions use sessions; Django authentication protects admin. Preserve SQLite locally, PostgreSQL in production, Django's test runner, Gunicorn/Fly.io, WhiteNoise, and environment-driven security configuration. No API layer, frontend framework, worker, or build tool is needed.

Repository code supersedes stale architecture descriptions: Likes already require CSRF-protected POST requests for an exact published post, rather than GET mutations. `HomePageView` is now a project-inquiry `FormView` selecting configured published insight channels, rather than a template view selecting two recent posts. The current homepage does not render the legacy blog include. Preserve these implemented boundaries; updating foundation documents is outside this plan.

## 2. Approved design grounding

No matching `docs/design/like_form_success_feedback/` workspace exists; standalone planning applies. Preserve the existing blog layout, native Like buttons, and Guardrails transcript design. Add concise feedback within the existing article presentation without introducing a new Like control on the Guardrails transcript.

## 3. Tech stack detected and confirmed

Django 5.1.2 is pinned in `requirements.txt`. Existing code uses Django templates, `@require_POST`, `CsrfViewMiddleware`, `HttpResponseRedirect`, and `request.session['liked_posts']`. The shared Like form already renders an internal POST action, CSRF token, native submit button, escaped article-specific accessible name, and decorative icon. Submission needs no JavaScript.

Context7's official Django documentation confirms [internal POST forms use the CSRF template tag](https://github.com/django/django/blob/main/docs/howto/csrf.txt), and [sessions are normally saved when modified](https://github.com/django/django/blob/main/docs/topics/http/sessions.txt). Keep feedback reads free of assignments or deletions to session data. No Django upgrade or middleware changes are required.

## 4. Files impacted

- `apps/blog/views.py`: derive a session-backed feedback boolean for both article template branches.
- `templates/blog/includes/like_feedback.html`: new shared conditional success text.
- `templates/blog/blog_detail.html`: include feedback near the existing Like control and count.
- `templates/blog/insight_detail.html`: include feedback near the article title for Likes submitted from the blog index.
- `static/blog/blog.css`: scoped feedback spacing, text color, and wrapping for standard articles.
- `static/blog/insight_detail.css`: scoped feedback styling using the existing transcript palette.
- `apps/blog/tests/test_blog_views.py` and `apps/blog/tests/test_like_views.py`: behavior and rendered-feedback coverage during the corresponding TEST phases.
- Read-only contracts: `templates/blog/includes/like_form.html`, `templates/blog/blog_index.html`, `templates/includes/blog_home_page.html`, `apps/blog/urls.py`, and `apps/blog/models.py`.

## 5. Data / DB changes

None. Reuse the existing `liked_posts` session list and Like records. Keep article GET/HEAD requests read-only and retain the standard article's existing count lookup and zero fallback. Do not add a Like lookup or count display to the Guardrails template. No migrations or new session keys.

## 6. API endpoints

Preserve the `like_post` and `blog_detail` URL names and routes. Accepted POSTs and sequential repeats continue to redirect with HTTP 302 to the resolved post's canonical detail URL plus `?liked=true`. Preserve 403 CSRF rejection, 405 method rejection, and 404 exact-publication/identity rejection. No new endpoint, redirect parameter, or redirect destination.

## 7. Frontend components

Retain the working native POST form and its visible Like label, accessible article-specific name, decorative icon, keyboard operation, and existing focus outline. Retain standard article counts.

The shared feedback include renders one paragraph only when `post_was_liked` is true, with text “You liked this post. Thank you!” and `role="status"`. Place it beside the standard article's Like controls and near the Guardrails article title, outside decorative `aria-hidden` content. Text must remain visible with JavaScript and icon resources unavailable, wrap on narrow screens, and use the appropriate existing color tokens on each background. A repeated accepted submission uses the same acknowledgment without claiming another increment.

## 8. Implementation approach

The prior `blog_like_security` feature already replaced all known Like anchors with secure forms. Preserve that implementation and address the remaining textual success feedback.

After resolving the exact published post in `blog_detail`, derive `post_was_liked` from both `request.GET.get('liked') == 'true'` and membership of that post's integer primary key in `request.session.get('liked_posts', [])`. Short-circuit on the query flag so ordinary article views do not need a new session read. Pass this boolean into both the standard and Guardrails template contexts; the Guardrails early return currently omits it. A query flag alone must not produce an acknowledgment.

Keep `like_post`, counters, session writes, and redirects unchanged. Include the same conditional feedback partial on both article destinations. Reuse existing CSS tokens and add only scoped feedback rules required for readability and wrapping. Do not add JavaScript, flash-message infrastructure, disabled-button behavior, or new controls to other surfaces.

## 9. Risks & edge cases

- The blog index can submit Likes for the Guardrails post, whose distinct destination currently has no feedback. Cover this path without adding a new transcript Like form.
- A manually supplied `?liked=true` must not imply success in a fresh session or a session containing only another post. The same-session flag confirms prior participation, not a newly incremented count.
- Refreshes and sequential repeat POSTs can retain the acknowledgment. Its wording must remain accurate when the count does not change.
- Session loss prevents feedback confirmation; it does not justify new persistence, identity tracking, or additional writes on article reads.
- Existing nonunique Like rows and read/modify/save increments have concurrency limitations. Schema uniqueness, atomic increments, cross-session abuse controls, and unlike behavior remain separate scope.
- `role="status"` on a newly navigated document does not guarantee an automatic announcement in every screen reader. Validate discoverability and actual reading behavior without adding unplanned script-driven focus.
- Global button and text styles can affect contrast and layout. Preserve the existing control focus treatment and inspect both article palettes at narrow widths and 200% zoom.

## 10. Security concerns

Preserve CSRF protection, POST-only mutation, exact published-post resolution before session/counter handling, canonical internal redirects, and template escaping. Never trust submitted alternate identifiers or redirect destinations. Render fixed feedback text without raw user content. Feedback is presentation only and must not authorize or perform a Like mutation. Preserve admin-only rich-text authoring and existing publication filtering.

## 11. Testing strategy

For step one, extend view tests for both standard and Guardrails articles: accepted POST followed by its redirect yields a true flag; missing/wrong query flags, fresh sessions with `?liked=true`, and sessions containing only another post yield false. Exercise repeated GET/HEAD with snapshots of Like rows and session dictionaries to confirm no mutation. Preserve existing standard zero/count rendering and transcript/category/related-post behavior.

For step two, assert exactly one visible success paragraph with status semantics after accepted submissions, and its absence on ordinary or unconfirmed requests, on both article destinations. Use real rendered forms and enforced CSRF clients to follow index-to-Guardrails and standard-detail submissions. Confirm repeat submissions preserve counts and session state while retaining accurate text. Reuse existing form/parser checks for internal POST actions, CSRF tokens, escaped accessible names, and absence of mutation anchors; retain rejected-method, invalid-CSRF, draft, missing-post, and wrong-slug regressions. Keep existing index and legacy-include forms covered without changing those callers unnecessarily.

Run `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.blog.tests.test_like_views apps.blog.tests.test_blog_views` first, then the full suite and Django configuration check. Default test discovery previously found zero tests; if still incomplete, use the explicit full set: `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.pages.tests.test_forms apps.pages.tests.test_models apps.pages.tests.test_sentry_privacy apps.pages.tests.test_throttling apps.pages.tests.test_views apps.blog.tests.test_blog_model apps.blog.tests.test_blog_views apps.blog.tests.test_admin apps.blog.tests.test_like_views apps.archive.tests.test_archive_views`. Run `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py check` and a whitespace check. Record existing CKEditor warnings separately from feature results.

During UI validation, use synthetic published posts and an isolated local database. With JavaScript disabled, verify keyboard Tab focus and Enter/Space submission from the index and standard detail, correct destination feedback including Guardrails, accurate count/repeat behavior, readable wrapping at 320/390px and 200% zoom, and accessible text discoverability. Check the message remains understandable without icons. Automated semantic assertions do not establish visual or screen-reader behavior.

## 12. Assumptions and unresolved questions

- Auto-selection chose the first unchecked backlog item. Its form-control requirement is already delivered; this feature preserves and revalidates it while completing success feedback.
- Use the existing redirect flag together with session membership, rather than a new one-time message system. A previously liked post can show its acknowledgment again when the flag is present.
- Guardrails receives acknowledgment for index-originated Likes but retains its existing lack of a Like form and count. The current homepage and category listing receive no new controls.
- No blocking product question was found. The acknowledgment wording above is a proposed implementation detail for review.
- PLAN creates only this plan. Implementation, validation gates, test changes, backlog completion, and final feature records remain separate workflow operations.

## 13. Step-by-step plan

- [x] In `apps/blog/views.py`, derive `post_was_liked` after exact published-post resolution from the existing redirect query flag and the resolved post's membership in `liked_posts`, expose it to both standard and Guardrails detail contexts, and preserve all mutation/redirect behavior; during this step's TEST phase extend `apps/blog/tests/test_blog_views.py` and `apps/blog/tests/test_like_views.py` for confirmed and unconfirmed state on both destinations and unchanged Like/session snapshots on GET/HEAD.
- [x] Add the conditional acknowledgment partial in `templates/blog/includes/like_feedback.html`, include it near the existing controls in `templates/blog/blog_detail.html` and title in `templates/blog/insight_detail.html`, and add scoped readable/wrapping styles in `static/blog/blog.css` and `static/blog/insight_detail.css`; during this step's TEST phase extend `apps/blog/tests/test_blog_views.py` and `apps/blog/tests/test_like_views.py` for actual rendered feedback, absence on unconfirmed requests, index-to-Guardrails submission, secure form contracts, and repeat behavior, then complete JavaScript-disabled keyboard, viewport/zoom, and assistive-technology validation.
