# Turtle AI Case Study

## Summary

- Added Turtle AI after cThink in Founder Projects, bringing Case Studies to four client engagements and two founder projects. The introduction, tab label, numbered index, and no-JavaScript explanation now agree with the displayed content.
- The new card includes the approved artwork, Understand → Build → Show narrative, and three evidence links. Existing cases, their order, and the default Client Work panel are preserved.
- Both steps in [the implementation plan](../plans/case_studies_plan.md) completed EXECUTE, VERIFY, ENGINEER CHECKPOINT, TEST, DEBUG where needed, and PLAN STEP UPDATE. The matching [backlog item](../backlog.md) is checked.

## Architecture Impact

- Implementation stays in `templates/includes/case_studies.html`, `static/pages/home.css`, and `static/pages/home.js`, composed by the existing Django homepage.
- No endpoints, database changes, queries, dependencies, or framework changes were added. The existing `HomePageView(FormView)` and inquiry validation, CSRF protection, throttling, sessions, and Sentry privacy controls are unchanged.

## Decisions

- Followed the approved [Continuity design](../design/case_studies/approved-design.md), preserving the palette, typography, production IDs, desktop sticky rail, and static rail at 1080px and below.
- Kept the full 1254 × 1254 artwork in `static/pages/images/turtle-ai-overview.png`, with its MIT notice alongside it. The optimization assessment retained the approved original; the older `turtleAI.png` and its consumers are unchanged. Explicit dimensions, lazy loading, and a square contained presentation preserve the complete artwork.
- Used the public GitHub repository and two documentation links pinned to revision `04c7a3f732cac0f272eba7c9b031035cfe3eccb0`, with `noopener noreferrer` on new-tab links. No remote scripts or embeds were added.
- Hash handling finds the target's containing panel and associated tab, reveals that panel and index, then scrolls on the next animation frame. Initial loads and hash changes support both founder cards and client cases; empty or unrelated hashes retain the Client Work default.
- Preserved keyboard tab controls and native disclosures. Without JavaScript, both indexes and all six cases remain available. The single closing band stays outside both panels; its inquiry link now takes its accessible name from the visible “Discuss Your Project” text.
- Added section wrapping and focus rules. After enlarged-text validation exposed legacy mobile descriptor overflow, the DEBUG repair allowed all descriptors to wrap at 760px and below. Above that breakpoint, legacy descriptors retain their existing single-line behavior; Turtle AI can wrap at every width.

## Test Impact

- Updated four affected tests in `apps/pages/tests/test_views.py`. Semantic HTML coverage checks six ordered cards and narrative sequences, disclosures, index targets, founder relationships, artwork, evidence destinations and link protections, no-JavaScript markup, and the closing action. Updated asset-version expectations and removed obsolete source assertions for cThink-only hash handling and exact sticky-rule serialization.
- Recorded final TEST results: 4 focused tests, 46 homepage tests, and 146 repository tests passed. The full run used the ten explicit module labels listed in the plan because default discovery has a known limitation. Django configuration checks succeeded with the existing CKEditor warning; whitespace checks passed.
- Chromium validation covered both groups at 320, 390, 760, 761, 768, and 1440px with normal and 200% root text size. The section stayed within the viewport; descriptors fit their headers without title overlap or artwork overlap. Artwork decoded at its original dimensions and remained square and uncropped.
- Browser checks also covered initial and changed founder/client hashes, keyboard tab navigation, native disclosures, focus styling, reduced motion, desktop sticky behavior, and the inquiry anchor without submitting a real inquiry. JavaScript-disabled checks confirmed access to all six cases and both indexes.
- VERIFY and ENGINEER CHECKPOINT passed after the DEBUG repair, followed by a passing TEST rerun. Security review found no issues in scope; performance review recorded the nonblocking artwork cost below. These results were recorded from the completed workflow, not rerun during documentation.

## Deployment Notes

- No deployment or migration was performed; no new environment variables are required.
- Homepage CSS and JavaScript query versions were refreshed in `templates/home.html`. Generated `staticfiles/` output was not edited.

## Follow-ups / Accepted Risks

- **Medium, nonblocking performance risk:** the artwork is 2,577,088 bytes (2.46 MiB), with the same file used at phone and desktop widths. The plan permits retaining it after the optimization assessment. A follow-up may compare smaller delivery formats while preserving artwork and text legibility; production load timings were not measured.
- Native browser zoom, Safari/WebKit, and screen-reader checks remain unverified. The 200% root text checks establish text-enlargement behavior, not native zoom or assistive-technology conformance.
- Broader typography/contrast audit findings, the existing sticky limitation in short windows, test discovery, and the CKEditor warning remain outside this feature's scope.
