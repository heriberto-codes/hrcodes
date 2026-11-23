# Product Backlog

## Features

- [x] Implement the approved business-focused homepage and Guardrails Insights article experience (`business_focused_homepage`)
- [x] Protect project-brief submissions with session-independent abuse throttling
- [x] Secure blog likes with CSRF-protected POST actions limited to exact published posts
- [x] Prevent project-brief data and client identifiers from reaching Sentry (`project_brief_sentry_privacy`)
- [x] Add Turtle AI as the second founder case study while preserving the approved site design (`case_studies`)
- [x] Refresh résumé links and add current Boston University study beneath the About portrait using the approved design (`about_profile_refresh`)

## Architecture Improvements

- [x] Centralize published-post filtering across public blog and homepage queries
- [x] Add security regression coverage for inquiry throttling, like mutations, and draft exposure
- [x] Preserve the admin-only rich-text trust boundary and validate external URL schemes if authoring expands

## Client Improvements

- [x] Add accessible inquiry-throttling guidance with the scheduling alternative
- [x] Replace like links with secure no-JavaScript form controls and success feedback
