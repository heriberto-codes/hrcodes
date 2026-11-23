# About Profile Refresh — Design Specification

Date: 2026-11-22
Feature: `about_profile_refresh`
Current section: `about_profile_and_resume`
Direction: **Continuity — current studies**
Status: section direction selected; responsive assembly complete; final design checkpoint pending. No final approval has occurred.

## Preview and rationale

- [Review gallery](mockups/index.html)
- [Assembled responsive About preview](mockups/assembled/continuity.html#about)
- [Assembled desktop](mockups/previews/assembled_desktop.jpg)
- [Assembled mobile](mockups/previews/assembled_mobile.jpg)
- [Editable About preview](mockups/about_profile_and_resume/continuity.html#about)
- [Desktop section](mockups/previews/desktop.jpg)
- [Desktop portrait detail](mockups/previews/portrait_desktop.jpg)
- [Mobile portrait detail](mockups/previews/portrait_mobile.jpg)
- Local assembled preview: <http://127.0.0.1:8765/assembled/continuity.html#about> while the preview server runs.

Provide one narrow continuity direction because the user requested a small caption/link refinement and confirmed the single-section scope. Alternatives differing only in decoration would not clarify a meaningful decision. The existing About section is the visual context; the isolated preview is not a full-homepage assembly or production-ready implementation.

## Proposed content and hierarchy

Preserve the framed portrait and existing identity in this order:

1. Founder + Principal Software Engineer
2. Heriberto Roman
3. A fine divider, followed by **Current student · Boston University**
4. **Master’s in Software Engineering for Artificial Intelligence**

The education statement explicitly describes current study. Do not imply a completed degree or add graduation dates, program abbreviations, university branding, or unsupported credentials. Institution and program wording come from the user. The education statement sits below the name inside the existing caption, in normal reading order. The two paragraphs separate student status/institution from the long program title without competing with the name.

The existing **View résumé** action uses exactly:

<https://hroman-codes.s3.us-east-2.amazonaws.com/HRomandevresume_November_2026.pdf>

Keep its label, decorative arrow, new-tab announcement, `target="_blank"`, and `rel="noopener noreferrer"`. This destination is specified by the user, rather than a visual choice.

## Existing components and assets preserved

- All About story paragraphs, section number, headline, skillset/diagram, video, and consultation action.
- Portrait image, framing, crop, professional role/name, caption's outer divider, desktop sticky behavior, and mobile sequence.
- Existing navy/cream/peach palette, IBM Plex Mono, section spacing, profile footer, and button styling.
- `mockups/assets/aboutMeImage.png` is an unchanged copy of the authored portrait; `mockups/assets/home_context.css` is an unchanged snapshot of `static/pages/home.css`. They make the preview independent of Django and do not modify production sources.
- `mockups/assets/base.css` reproduces only the relevant existing browser/Bootstrap/global defaults: heading weight/margins, body line height, paragraph color, image alignment, and peach strong text. The preview uses the same Google Fonts family/weights as the site. There is no new JavaScript, framework, or font family.

## Proposed styling

Only the education block is proposed product styling in `mockups/styles.css`:

| Element | Treatment |
| --- | --- |
| Education group | Existing `--line-dark` divider; 11px top margin and 16px top padding |
| Student/institution text | `--navy-deep`; 0.75rem; weight 600; line-height 1.6 |
| Program title | `--ink`; 0.875rem; line-height 1.65; 8px separation |
| Long program text | Natural wrapping, with an overflow-wrap fallback; no truncation or fixed height |

All colors and the font are reused homepage tokens. The source's generic caption span treatment remains confined to the existing role; the new paragraphs retain readable sentence case.

## Responsive behavior

- Preserve the existing two-column About layout and sticky portrait above 760px.
- Preserve the source's one-column mobile order below that breakpoint: section label → headline → portrait/caption → story → skillset → video → profile actions.
- The education group follows the portrait-column width, expanding vertically as needed; no forced line breaks or independent breakpoint are introduced.
- Existing tablet column sizing and action stacking remain unchanged.
- The sticky column becomes taller with the education addition. Content remains part of the normal scroll layout; this direction does not add a fixed overlay or hide caption content.

## Interaction and accessibility

- The added text is noninteractive and needs no hover, loading, error, or selected state.
- The existing outbound résumé action remains a native keyboard-accessible link with the original new-tab announcement and decorative arrow semantics.
- New text uses navy/ink on cream. Preserve readable wrapping and document order with enlarged text.
- Existing skill anchors, hover behavior, reduced-motion styles, and iframe are retained as context, not redesigned or newly endorsed by this scope.
- The navy review header, gallery, skip link, résumé-destination notes, and their navigation are visibly identified as review UI. Do not implement them in the website.

## Verification performed

- Rendered and visually inspected the full desktop About section at 1440px and the portrait/caption at 390px; saved the linked desktop and mobile previews. The program title is fully visible and wraps beneath the institution line.
- Chromium layout checks at 320, 390, 768, 1000, and 1440px: the new education group fits its column and viewport. Normal-size document width matches viewport width at all five sizes.
- Repeated those checks at 200% root font size: the new education group remains within its column/viewport with no internal overflow at every width. This simulates enlarged text, not true browser zoom.
- The unchanged headline causes document overflow at enlarged text on 320/390px; an additional small context overflow occurs at 768px. These inherited context limitations are not caused by the new caption and were not silently redesigned. Do not describe the entire existing page as passing 200% text checks. Address separately if broader accessibility scope is requested.
- Verified that the preview has exactly the supplied November résumé destination and no April résumé links, its original new-tab/security attributes, and a visible computed focus outline when focused. The local portrait decodes at its original 1200px natural width.
- Used reduced-motion mode for screenshots. The only observed console error was a missing local favicon; it does not affect the design.
- Did not request the external PDF, verify its contents/availability, activate external actions, or validate third-party video playback. Real-device Safari, screen-reader, actual browser zoom, and complete inherited interaction testing remain unperformed.

## Implementation implications and boundaries

- Once selected, assembled, and approved for planning, carry the education content and styling into the existing Django About template/style boundary. Reuse application sources; do not import preview code or its CSS snapshot into the app.
- The user also requested every old résumé link be updated. Audit evidence identifies the live About action, its regression expectation, and the historical About mockup's clickable destination. Plan the historical mockup destination-only change deliberately; preserve its prior design and approval. Update the regression expectation during the engineering TEST phase.
- Other service/company/architecture PDFs are outside résumé replacement scope. Generated `staticfiles/`, database content, credentials, routing, and deployment are untouched.
- The initial mockup transition created section mockups/specification only. The user subsequently selected the direction, and the assembly transition below prepares the complete selected scope. Checkpoint approval, backlog, and planning remain later distinct transitions; the live site is unchanged.

## Responsive assembly — 2026-11-22

The sole confirmed review section, `about_profile_and_resume`, is selected as **Continuity — current studies**. Its complete About section now appears in `mockups/assembled/continuity.html`. Because this is a section-scoped refinement, assembly covers the complete About experience; it does not introduce or redesign unrelated homepage sections.

Assembly order preserves the existing portrait/caption column beside the story column on desktop. The story column retains section label → headline → story → skillset → video → résumé/consultation actions. At widths below 760px, the existing flex ordering places the portrait and selected student caption between the headline and story. The résumé action remains at the end of the complete About experience. All elements use the existing shared tokens and selected education styling described above. There are no cross-section layout conflicts or new visual decisions to resolve.

The selected source file is unchanged, with SHA-256 `cfcf2976ae618e02dab50afde2db49e2151869c5df3801611a90e3dd57889de6`. The assembled About HTML matches the selected About HTML exactly; only the surrounding review-page title/guidance identifies it as assembled. Updated the gallery to prioritize the assembly and retain the selected section preview as a reference. Existing assets/styles were reused without revision.

Rendered and visually inspected the complete assembly at 1440px desktop and 390px phone widths. Chromium checks at 320/390/768/1440px confirm normal document width equals viewport width, the new education group stays within its column, and the portrait is static on mobile and sticky on desktop. Verified one About section and one education group, decoded portrait, no April résumé links in the assembly, the exact November destination, original new-tab/security attributes, computed focus visibility, and the gallery's assembly link. Screenshot capture used reduced motion.

The earlier enlarged-text context limitations remain documented; no broader accessibility redesign was introduced. External PDF availability/content, third-party video playback, screen readers, real devices, and actual browser zoom remain unverified. No production files, original selected section artifacts, audit, checkpoint, approval, backlog, or plan were changed. The final design checkpoint is ready to begin on the next controller invocation; it was not started during assembly.
