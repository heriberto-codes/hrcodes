# Product Backlog

## Features

- [x] Implement the approved business-focused homepage and Guardrails Insights article experience (`business_focused_homepage`)
- [x] Protect project-brief submissions with session-independent abuse throttling
- [ ] Secure blog likes with CSRF-protected POST actions limited to exact published posts
- [x] Prevent project-brief data and client identifiers from reaching Sentry (`project_brief_sentry_privacy`)

## Architecture Improvements

- [ ] Centralize published-post filtering across public blog and homepage queries
- [ ] Add security regression coverage for inquiry throttling, like mutations, and draft exposure
- [ ] Preserve the admin-only rich-text trust boundary and validate external URL schemes if authoring expands

## Client Improvements

- [ ] Add accessible inquiry-throttling guidance with the scheduling alternative
- [ ] Replace like links with secure no-JavaScript form controls and success feedback
