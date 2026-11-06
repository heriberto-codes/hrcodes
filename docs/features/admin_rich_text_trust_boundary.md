# Admin Rich-Text Trust Boundary

## Summary

- Added body/snippet guidance to the existing Django post admin: content is rendered as trusted HTML, pasted markup and link destinations require review, and post-writing permissions belong only to trusted authors.
- Both steps in [the implementation plan](../plans/admin_rich_text_trust_boundary_plan.md) and the exact matching [backlog item](../backlog.md) are checked complete.
- Security review found no new blockers under the trusted-author policy. Static performance review found no introduced performance concerns.

## Architecture Impact

- Runtime changes are confined to `PostAdmin.formfield_for_dbfield()` in `apps/blog/admin.py`.
- Django still constructs form fields and enforces active-staff access, model permissions, and CSRF protection. Public visitors have no post-authoring endpoint.
- No routes, database schema, migrations, dependencies, settings, or public templates changed. Guidance adds bounded string operations without additional queries or network calls.

## Decisions

- Retain inherited Django authorization rather than introduce a role system or require superuser status. Staff with the appropriate add/change permissions remain authorized authors.
- Append guidance to individual form fields, preserving CKEditor, existing snippet instructions, field order, and requiredness without mutating shared model fields.
- Preserve legitimate trusted HTML rendering. Help text documents the trust policy; it does not sanitize content or validate URL schemes.
- Add a source comment requiring server-side HTML sanitization and allowed URL schemes before expanding to less-trusted authors, imports, or visitor content.

## Test Impact

- Added `apps/blog/tests/test_admin.py` covering unauthorized writes with valid CSRF tokens and unchanged post/category state, view-only draft access, independent add/change permissions, authorized writes, and missing/invalid CSRF rejection.
- Admin form tests cover guidance on add/change and invalid submissions, retained snippet instructions and CKEditor, stable field behavior, and unchanged shared model help text.
- Extended `apps/blog/tests/test_blog_views.py` to preserve trusted article/snippet markup on existing rendering surfaces and Guardrails introduction/chapter HTML.
- Tests were inspected, not rerun, during security review and documentation. No benchmark or coverage-percentage claim is made.

## Deployment Notes

- No new environment variables or feature-specific migration steps are required. No deployment or production data/permission changes were performed during finalization.

## Follow-ups / Accepted Risks

- Existing body/snippet HTML and extracted payload links remain trusted. A malicious or compromised authorized author can publish executable HTML or unsafe URL schemes. Keep writing permissions restricted; production assignments were not inspected.
- Before broadening input sources, separately implement HTML sanitization and URL-scheme allowlists across body HTML, snippets, and extracted payload links. Attribute escaping alone does not validate URL schemes.
- The existing CKEditor maintenance issue and stale foundation-document descriptions remain separate work.
- Completion of the earlier implementation loop is taken from the checked plan state. Detailed prior gate transcripts and test execution counts were unavailable in this documentation session.
