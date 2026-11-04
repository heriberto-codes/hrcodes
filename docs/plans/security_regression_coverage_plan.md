# Security Regression Coverage Plan

Selected backlog item (exact text): Add security regression coverage for inquiry throttling, like mutations, and draft exposure

Feature slug: `security_regression_coverage`

## 1. Architecture grounding

`architecture.md` establishes server-rendered Django views and templates, app-owned ORM persistence, anonymous public routes, and Django authentication/permissions for admin. Local development uses SQLite; production uses PostgreSQL behind Fly.io/Gunicorn, with WhiteNoise static delivery and Sentry monitoring. Preserve CSRF middleware, sessions, environment-driven configuration, and existing app boundaries. Use the existing Django test runner without a new framework or build tool.

Executable code supersedes stale architecture descriptions: the homepage is a project-brief `FormView` with three configured insight channels; `ProjectInquiryThrottle` persists opaque expiring counters; likes require CSRF-protected POST; public queries explicitly use `Post.objects.published()`. Preserve these contracts rather than implementing the already-resolved risks listed in the architecture document. `repo_map.md` also predates the inquiry model, throttling helper, and tests packages.

## 2. Approved design grounding

No matching `docs/design/security_regression_coverage/` workspace exists; standalone planning applies. This item validates existing behavior and requires no visual design decisions. The homepage design workspace belongs to the completed homepage feature.

## 3. Tech stack detected and confirmed

- Django 5.1.2 from `requirements.txt`, Django ORM/templates, Python `unittest.mock`, and existing `TestCase`/`TransactionTestCase` coverage.
- Context7's [official Django CSRF testing guidance](https://github.com/django/django/blob/main/docs/howto/csrf.txt) requires `Client(enforce_csrf_checks=True)` when validating CSRF. The installed Django test-client source confirms support; use existing APIs rather than newer-version examples.
- Follow [Django's explicit dotted test-label support](https://github.com/django/django/blob/main/docs/topics/testing/overview.txt) and existing repository validation practice. No additional test libraries are needed.

## 4. Files impacted

- `apps/pages/tests/test_views.py`: inquiry middleware/limiter integration and homepage publication-transition coverage.
- `apps/blog/tests/test_like_views.py`: valid rendered forms submitted after publication or identity changes.
- `apps/blog/tests/test_blog_views.py`: publication transitions across public read surfaces.
- Read-only implementation contracts: `apps/pages/views.py`, `apps/pages/throttling.py`, `apps/pages/models.py`, `apps/pages/forms.py`, `apps/blog/models.py`, `apps/blog/views.py`, app URL modules, and existing templates.
- Reuse coverage in `apps/pages/tests/test_throttling.py` and `apps/blog/tests/test_blog_model.py`; changes are unnecessary unless TEST review identifies a concrete gap within the active step.

## 5. Data / DB changes

None. Use isolated test databases and synthetic fixtures for existing `Post`, `Category`, `Like`, and `ProjectInquiryThrottle` models. Preserve production data, migration history, default/admin draft visibility, and current session keys. Snapshot existing rows and relevant session state when checking rejected requests.

## 6. API endpoints

No new endpoints. Exercise the existing named routes:

- `GET /` and `POST /` (`home`): published configured insights; inquiry validation, CSRF, shared throttling, and email behavior.
- `GET /blog/` (`blog_index`) and `GET /blog/<category>/` (`blog_category`): published-only lists.
- `GET /blog/<pk>/<slug>` (`blog_detail`): exact published identity, standard/Guardrails templates, and published related signals.
- `POST /blog/liked/<pk>/<slug>` (`like_post`): exact published identity checked before like/session mutation, followed by the existing canonical redirect.

Preserve current response contracts: CSRF rejection is 403, invalid article identity/publication is 404, non-POST like methods are 405, and inquiry throttling redisplays the bound form with HTTP 200.

## 7. Frontend components

No frontend edits. Obtain CSRF tokens through rendered forms and cookies. Keep the inquiry form, scheduling link, success feedback, shared like form, insight fallbacks, and existing template/context contracts. Assert public content and destinations rather than adding CSS/JavaScript implementation-string checks.

## 8. Implementation approach

Extend existing owning-app tests only where current coverage lacks a meaningful combined request path or state transition. Reuse fixture builders and `LikeFormParser`; avoid a cross-app helper layer, duplicate suites, broad test reorganization, or a coverage-percentage target.

Existing tests already cover cross-session/address throttling, forwarded-header spoofing, fixed-window expiry, atomic counter claims, SMTP failures consuming quota, fail-closed limiter errors, like method/CSRF rejection, exact identity, once-per-session counts, static draft exclusion, and unfiltered admin managers. Keep those tests as evidence.

Target these remaining gaps:

- Inquiry CSRF rejection with an existing bucket and seeded unrelated session state: missing/malformed token and untrusted origin must not send email, change bucket state, or record success. Include a rendered-token positive control that actually reaches the limiter and a fresh-session same-address retry that is blocked with valid CSRF. Existing missing-cookie coverage can be extended rather than duplicated.
- Stale like forms: render a valid form for a published article, then unpublish it or change its slug before POST. Exercise missing/existing Like rows and a session already containing the target post, proving identity/publication resolution still precedes repeat-like handling. Rejection must preserve all Like rows and session entries. A newly rendered canonical form remains the positive control after a slug change.
- Publication transitions: request a published configured insight, change it to draft, then revisit affected public surfaces with the same client. Check homepage, index, matching category, direct detail, and a published Guardrails article's related signals where applicable. Require absence from context and HTML, 404 for direct access, and preserved published companions/fallbacks. Extend homepage form-redisplay coverage to a limiter exception, ensuring generic inquiry feedback cannot reintroduce draft content. Existing status-2 tests remain the unsupported-status evidence.

Workflow routing: this is test-only work. For each step, EXECUTE should reconcile the named existing production guards and report `already_satisfied` when appropriate, without adding tests or changing runtime logic. VERIFY reviews those guards; ENGINEER CHECKPOINT remains required; TEST mode A selects the missing cases and mode B implements them. Only PLAN STEP UPDATE may mark the step complete after validation. A newly exposed runtime defect requires explicit DEBUG routing and a plan adjustment if its fix exceeds this test-only scope.

## 9. Risks & edge cases

- A CSRF-disabled client can make a security test pass without exercising middleware. Obtain genuine form tokens, use a trusted origin for positive controls, and distinguish middleware rejection from application rejection.
- Rejected requests may still read session data through templates. Assert stored values and domain side effects, not session-access flags or cookie byte equality.
- Freeze the throttle clock and explicitly configure the trusted client header, limit, window, and local email backend. Distinct clients must use the same authoritative address for shared-quota assertions.
- A stale-form test must capture its token/action before changing the article. Refreshing the form first would miss the regression.
- Use distinctive title/snippet/body markers and check only fields the surface can expose. Inspect context as well as HTML because template guards can conceal unfiltered queries.
- Existing concurrency tests deliberately synchronize stale reads and order writes to avoid SQLite lock noise. Retain them without claiming they prove arbitrary PostgreSQL scheduling behavior.
- Previous validation records report zero tests under default discovery and failures under broad app labels. Use explicit module labels and verify a nonzero test count; discovery repair is separate work.

## 10. Security concerns

Preserve inquiry abuse limits independently of cookies and submitted identity. Rejected requests must not deliver email, mutate likes, alter throttle counters, or mark success except where an allowed inquiry attempt intentionally consumes quota before delivery. Keep exact `status=1` publication semantics, canonical article identity, and anonymous read behavior. Do not broaden likes into global deduplication or concurrency hardening. Do not expose credentials, raw client identifiers, or real inquiry content in fixtures, output, or remote telemetry.

## 11. Testing strategy

- During each step's TEST review, map existing tests to the named invariants, reuse complete cases, and add only the gaps listed above. Do not write tests during planning or EXECUTE.
- Inquiry focused run: `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.pages.tests.test_views apps.pages.tests.test_throttling`.
- Like focused run: `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.blog.tests.test_like_views`.
- Publication focused run: `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.blog.tests.test_blog_views apps.blog.tests.test_blog_model apps.pages.tests.test_views`.
- After focused checks pass, run the full suite with all nine explicit module labels: `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.blog.tests.test_blog_model apps.blog.tests.test_blog_views apps.blog.tests.test_like_views apps.pages.tests.test_forms apps.pages.tests.test_models apps.pages.tests.test_sentry_privacy apps.pages.tests.test_throttling apps.pages.tests.test_views apps.archive.tests.test_archive_views`.
- Run `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py check` and `git diff --check`. Configuration validation supplements behavioral tests. No static collection, production migration, or deployment is required.
- Keep email in memory, use synthetic addresses, disable outbound Sentry with the empty DSN, and retain the existing privacy suite's in-memory transport. Do not load production databases. The existing CKEditor warning is outside this item.

## 12. Assumptions and unresolved questions

- Auto-selected the first unchecked backlog item and generated a concise snake_case slug. There is no existing matching plan or design approval gate.
- No blocking product questions remain. Scope is additive regression coverage of implemented security contracts, with no runtime or UI behavior change.
- Existing feature records establish broad prior coverage but do not prove newly proposed cases pass. No behavioral tests have been run during planning.
- Foundational architecture/map refresh, default discovery repair, rich-text authoring policy, inquiry accessibility improvements, and further like UX changes remain separate backlog/workflow work.

## 13. Step-by-step plan

- [x] Reconcile existing inquiry CSRF and shared-throttle guards in `apps/pages/views.py` and `apps/pages/throttling.py`; during TEST, extend `apps/pages/tests/test_views.py` with side-effect-free CSRF rejection against seeded state and a rendered-token submission followed by a valid-CSRF same-address fresh-session throttle rejection, reusing `apps/pages/tests/test_throttling.py` as existing limiter evidence.
- [x] Reconcile exact published-identity resolution before like/session mutation in `apps/blog/views.py`; during TEST, extend `apps/blog/tests/test_like_views.py` for valid stale forms submitted after unpublishing or slug changes, including pre-liked sessions, unchanged rejected state, and a canonical positive control.
- [x] Reconcile published-only public queries in `apps/blog/views.py` and `apps/pages/views.py`; during TEST, extend `apps/blog/tests/test_blog_views.py` and `apps/pages/tests/test_views.py` for same-client publication transitions across affected read surfaces and draft exclusion during limiter-exception form redisplay, then run focused checks, the full explicit suite, configuration validation, and whitespace checks.
