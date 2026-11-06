# Admin Rich-Text Trust Boundary Plan

Selected backlog item (exact text): Preserve the admin-only rich-text trust boundary and validate external URL schemes if authoring expands

Feature slug: `admin_rich_text_trust_boundary`

## 1. Architecture grounding

Keep the server-rendered Django view/template boundary, blog-owned ORM persistence, and Django admin authentication and model permissions. Public visitors can read published posts and submit likes; they cannot author posts. SQLite is used locally and PostgreSQL in production behind Fly.io/Gunicorn, with WhiteNoise static delivery. Preserve sessions, CSRF middleware, HTTPS settings, and existing runtime configuration.

`architecture.md` correctly identifies admin as the content-management surface, but its homepage, GET-like, and publication-filtering descriptions are stale. Current code uses a project-brief `FormView`, CSRF-protected POST likes, and explicit `Post.objects.published()` queries. Preserve executable behavior. `repo_map.md` also predates the current tests packages and inquiry implementation. Refreshing foundation documents is separate work.

## 2. Approved design grounding

No matching `docs/design/admin_rich_text_trust_boundary/` workspace exists; standalone planning applies. No public design change is required. Any new guidance belongs in the existing Django admin form.

## 3. Tech stack detected and confirmed

- Django 5.1.2 and django-ckeditor 6.7.1 are pinned in `requirements.txt`. `Post.body` is a CKEditor `RichTextField`; `Post.snippet` is a character field.
- `PostAdmin` inherits Django's standard permissions without overrides. Installed Django source confirms that admin-site access requires active staff status and post creation/editing requires the respective model permission. Authorized staff need not be superusers.
- Context7's [official Django admin reference](https://github.com/django/django/blob/main/docs/ref/contrib/admin/index.txt) describes model permissions and admin form customization. Confirm version-sensitive details against installed 5.1.2 source rather than relying on newer examples.
- The [official template reference](https://github.com/django/django/blob/main/docs/ref/templates/builtins.txt) defines `safe` as bypassing HTML escaping. It provides no sanitization guarantee. The [URL validator reference](https://github.com/django/django/blob/main/docs/ref/validators.txt) documents configurable schemes; default URL validation is not an HTTP/HTTPS-only policy or an HTML sanitizer.

## 4. Files impacted

- `apps/blog/admin.py`: scoped author guidance for the existing body and snippet form fields, preserving model permissions and widgets.
- `apps/blog/tests/test_admin.py`: new owning-app test module, created only during TEST, for admin authorization, CSRF, successful writes, and form guidance.
- `apps/blog/tests/test_blog_views.py`: extend only missing behavioral coverage for preservation of existing trusted article/snippet rendering during the second step's TEST phase.
- Read-only contracts: `apps/blog/models.py`, `apps/blog/forms.py`, `apps/blog/views.py`, `apps/blog/urls.py`, `hrcodes/urls.py`, `hrcodes/settings.py`, `templates/blog/blog_detail.html`, `templates/blog/insight_detail.html`, `templates/blog/blog_index.html`, `templates/blog/blog_category.html`, and `templates/includes/blog_home_page.html`.

## 5. Data / DB changes

None. Preserve existing HTML, publication statuses, categories, permissions, and migration history. Use isolated test users and posts. Add help text at the admin form boundary rather than changing model fields or generating a migration. Do not inspect or rewrite live content or user permissions.

## 6. API endpoints

No new routes or API. Exercise `admin:blog_post_add`, `admin:blog_post_change`, and `admin:blog_post_changelist` through the registered admin site. Anonymous/non-staff requests follow the existing admin login redirect; active staff lacking the required model permission receive permission denial. View-only staff may view existing posts but cannot save them.

Preserve all public blog routes, canonical identities, publication filtering, and like behavior. The unused `CommentForm` is not an authoring endpoint and must not be wired into one.

## 7. Frontend components

Keep CKEditor, existing snippet help text, field order, and all public templates unchanged. Add concise admin guidance that body/snippet content is rendered as trusted HTML, pasted markup and destinations require review, and post add/change permissions must be restricted to trusted site authors. Guidance describes the policy; permissions enforce access. It must not claim that CKEditor or the application sanitizes stored HTML.

## 8. Implementation approach

Preserve the current authoring boundary rather than adding a new role system or duplicating Django's permission checks. First reconcile registered admin behavior and establish meaningful request-level permission coverage during TEST. EXECUTE may report `already_satisfied` for this reconciliation step; it must not add tests or force runtime changes.

Then add field-specific guidance through `PostAdmin` form-field customization, delegating field construction to Django. Limit customization to body/snippet, preserve CKEditor's widget and current snippet instructions, and avoid mutating shared form base fields. Add a short source comment at that customization identifying the trusted-author assumption and the requirement to reassess it before broadening input sources.

This feature does not expand authoring. The backlog's URL-validation clause is conditional and remains a prerequisite for any future expansion. Before accepting less-trusted authors, imports, or visitor HTML, separately plan server-side HTML sanitization and explicit allowed schemes at every rendered URL sink. Include ordinary body links and snippet HTML as well as extracted Guardrails payloads; validating only `payload.href` cannot secure HTML rendered with `safe`. Do not implement a partial sanitizer, URL rewriting, or a new dependency here.

## 9. Risks & edge cases

- Active staff status alone does not authorize writing posts. Test model permissions separately; retain successful add-only and change-only controls without granting superuser access.
- CSRF rejection can conceal a missing permission check. Use valid CSRF for authenticated permission-denial cases and separate missing/invalid-token cases for authorized writers.
- Verify rejected writes preserve the complete post state and category relationships and create no new post. An invalid form submission alone is insufficient proof of authorization.
- Trusted authors can publish executable HTML or unsafe links today. Admin guidance and access tests preserve the accepted trust assumption; they do not eliminate stored-XSS risk from a compromised or malicious trusted account.
- Keep nullable/blank bodies, drafts, and existing rich markup working. Reuse current Guardrails chapter/payload tests rather than modifying its parser or fallback behavior.
- The existing CKEditor warning and unsupported editor remain separate maintenance work. No editor upgrade or production permission audit is included.

## 10. Security concerns

Do not broaden access, require superusers instead of currently authorized staff, weaken CSRF, or accept public post fields. Treat both post body and snippet as trusted because public templates render both through `safe`. Guardrails fragments retain that same trust assumption; extracted payload attributes are escaped but not scheme-validated. Do not present attribute escaping as URL scheme validation. Keep external-link `rel` protections and publication checks intact.

## 11. Testing strategy

- During step 1 TEST, create `apps/blog/tests/test_admin.py` with real admin requests for anonymous, inactive/non-staff, staff without post permissions, view-only staff, and authorized add/change users. Assert expected redirects/denials and unchanged stored content for rejected writes, including attempts to publish. Use valid forms and tokens where necessary to prove permissions caused rejection. Include authorized create/edit positive controls and independent CSRF rejection for authorized users with `Client(enforce_csrf_checks=True)`.
- During step 2 TEST, extend that module to check guidance on actual add/change forms, retained snippet instructions, CKEditor widget preservation, and unchanged successful saves. Reuse existing article/payload tests; add only missing representative checks that legitimate trusted body markup and snippets still render through existing public templates.
- Start with `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.blog.tests.test_admin`, then the relevant blog view/model modules. No tests are written or run during planning or EXECUTE.
- After focused tests pass, run the full explicit suite including the new module: `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py test apps.blog.tests.test_admin apps.blog.tests.test_blog_model apps.blog.tests.test_blog_views apps.blog.tests.test_like_views apps.pages.tests.test_forms apps.pages.tests.test_models apps.pages.tests.test_sentry_privacy apps.pages.tests.test_throttling apps.pages.tests.test_views apps.archive.tests.test_archive_views`.
- Run `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py check`, `DEBUG=True SENTRY_DSN='' venv/bin/python manage.py makemigrations --check --dry-run`, and `git diff --check` during validation. Confirm a nonzero test count; previous feature records identify default test-discovery limitations.
- Use synthetic fixtures and an isolated test database; disable outbound Sentry and keep email in memory where relevant. No production database access, static collection, or deployment is required.

## 12. Assumptions and unresolved questions

- Auto-selected the first unchecked backlog item. Its conditional wording does not authorize broader authoring or a general HTML-sanitization project.
- Trusted authors include active staff deliberately granted post add/change permissions, not only superusers. Django permissions are the existing enforcement mechanism; no custom author role is needed.
- Acceptance for the current item is preserved admin-only authoring, explicit author guidance, and permission regression evidence. URL scheme enforcement is deferred because authoring is not expanding; this plan does not claim URL validation has been implemented.
- No blocking product question remains under that scope. A request for less-trusted authoring or URL hardening now requires an explicitly revised scope before execution.
- No application code, tests, backlog state, or existing plan state changes are made during planning. Unrelated workflow/skill edits in the working tree remain outside this feature.

## 13. Step-by-step plan

- [x] Reconcile the registered `PostAdmin` authoring boundary in `apps/blog/admin.py` against existing Django admin/model permissions without changing access policy; during TEST, create `apps/blog/tests/test_admin.py` covering denied add/change requests without post mutations, view-only access, authorized staff create/edit positive controls, and enforced CSRF for authorized writers.
- [x] Add field-specific trusted-HTML author guidance and the future-authoring prerequisite comment in `apps/blog/admin.py`, preserving CKEditor, snippet instructions, and inherited permissions; during TEST, extend `apps/blog/tests/test_admin.py` for rendered guidance and unchanged form behavior, reuse or minimally extend `apps/blog/tests/test_blog_views.py` for legitimate rich-content rendering, then run the full explicit suite and configuration/migration checks.
