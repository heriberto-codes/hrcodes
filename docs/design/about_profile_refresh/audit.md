# About Profile Refresh — Design Audit

Date: 2026-11-22
Feature slug: `about_profile_refresh`

## Objective and audience

Help prospective clients, collaborators, and employers see Heriberto Roman's current professional and educational profile. The user requests the November 2026 résumé destination wherever an older résumé is linked, plus current Boston University student information beneath the About portrait. Preserve the established site design and existing founder/principal engineer identity.

User-supplied destination:

<https://hroman-codes.s3.us-east-2.amazonaws.com/HRomandevresume_November_2026.pdf>

User-supplied education facts: current student at **Boston University**, pursuing the **Master’s in Software Engineering for Artificial Intelligence**. These establish student status, not a completed degree. No graduation date, abbreviation, university logo, or additional credentials were supplied.

## Evidence inspected

- `AGENTS.md`, `architecture.md`, `repo_map.md`, and `docs/system/design-workflow.md`.
- Both existing design workspace state files: `business_focused_homepage` and `case_studies` are `planned`. Neither is reopened by this request; this is a new, focused workspace.
- `templates/home.html` and `templates/includes/about.html`: About composition, portrait caption, and résumé action.
- `static/pages/home.css`: About tokens, caption styling, desktop sticky portrait, and responsive reordering. `static/style.css`: global brand tokens.
- `apps/pages/tests/test_views.py`: the About regression contract explicitly expects the April résumé filename around line 1951.
- Repository text searches for résumé/resume terms, filenames, and PDF links, excluding generated static output and virtual environments.
- Live homepage at `http://127.0.0.1:8000/#about`: inspected rendered content and screenshots at desktop 1440 × 1100 and phone 390 × 844 viewports. Temporary browser evidence is stored outside the repository in `/tmp/hrcodes-about-profile-audit-20261122-browser/`: desktop `element-2026-11-22T16-06-45-281Z.jpeg` and phone `element-2026-11-22T16-07-22-770Z.jpeg`. These local captures are inspection evidence, not durable design deliverables.

## Current design inventory

- `05 / About Heriberto Roman` uses a cream surface, navy type, peach accents, IBM Plex Mono, and a framed portrait.
- Beneath the portrait, the role precedes the name: “Founder + Principal Software Engineer” → “Heriberto Roman.” The current caption ends with a fine divider and has no education information.
- Desktop uses a sticky portrait column beside the story, skillset, video, and actions. Below 760px, the portrait/caption appears after the heading and before the story, without sticky positioning.
- The profile footer contains “View résumé” and “Meet Heriberto.” The résumé is a normal outbound link with `target="_blank"`, `rel="noopener noreferrer"`, a decorative arrow, and hidden new-tab text.

## Strengths to preserve

- Recognizable portrait framing, existing role/name hierarchy, palette, typography, and fine rules.
- Clear résumé action and existing external-link accessibility/security behavior.
- Established desktop sticky behavior and mobile reading order.
- Story, skillset, video, consultation destination, and surrounding sections; no broader redesign is requested.

## Findings, ordered by impact

1. **The live résumé action points to April 2026.** Source and rendered DOM both identify `https://hromancodes.s3.us-east-1.amazonaws.com/static/pages/HRomandevresume_April_2026.pdf`. Visitors receive an older document than the owner intends. Replace the destination with the exact supplied November URL when implementation is authorized. The search found one live application résumé link; the change includes a different bucket, region, and path, not only a filename change.
2. **Current study is absent from the portrait caption.** Source and screenshots show only the professional role and name. Visitors cannot discover the education detail where the user wants it. Explore a subordinate education treatment beneath the existing identity that clearly communicates current enrollment and retains the supplied program title. Exact wording and presentation remain a user choice.
3. **The full program title introduces a wrapping consideration.** The desktop portrait column is narrower than the story; the phone caption occupies the available portrait width. The existing generic caption span style is small and uppercase. Reusing that treatment blindly for a long degree title could make the detail hard to scan. Review readable wrapping, spacing, and hierarchy in the mockup, including narrow widths and enlarged text. This is a design consideration, not an observed defect in the current two-line caption.
4. **The old destination also exists outside the live template.** The regression expectation in `apps/pages/tests/test_views.py` will need to follow the authorized URL change during the engineering TEST phase. The historical homepage mockup `docs/design/business_focused_homepage/mockups/about/direction-a.html` has a clickable April résumé link as well. Carry that link into the later plan as a destination-only update to satisfy “any other link,” preserving its historical design and approval record. This audit does not modify that completed workspace. Other inspected PDFs are service, company, and architecture documents; they are not résumé replacements.

## Existing components, tokens, and assets to reuse

- About portrait and its current image, framing, caption container, and divider.
- Existing résumé action and new-tab announcement.
- Homepage tokens `--navy-deep`, `--ink`, `--cream`, `--peach`, `--line-dark`, and `--mono`, consistent with global brand variables.
- Existing responsive widths and stacking rules. No new framework, font, image, or university branding asset is needed for this scope.

## Responsive and accessibility considerations

- Retain role/name text and introduce explicit student-status wording without implying a completed master's degree.
- Allow the institution and complete program title to wrap naturally at phone and intermediate desktop widths; avoid fixed-height captions or truncation.
- Review contrast and readable size for any new secondary text rather than assuming the current small role label is suitable for the entire education statement.
- Keep the caption in the normal reading order under the portrait, and preserve the mobile sequence.
- Preserve the résumé link's visible label, keyboard access, decorative-arrow treatment, and new-tab announcement. A university link or badge is not required by this request.

## Constraints, assumptions, and missing evidence

- Foundation documents exist. Some architecture descriptions predate the current homepage; executable templates/styles control this audit's findings.
- Education facts and the new résumé URL are supplied by the owner. The PDF contents, external availability, and official program naming have not been independently verified; no degree dates or additional claims are inferred.
- Screenshots show the current interface only; no proposed caption has been rendered yet. Screen-reader, real-device, enlarged-text, and proposed-layout validation remain for later stages.
- Search covers authored repository text and the rendered homepage, not database-managed blog content, third-party sites, or generated `staticfiles/`. No additional live résumé destination was found in the inspected sources.
- Audit-only transition: no production code/assets, older workspace artifacts, backlog items, plan steps, mockups, or approvals are changed.

## Prioritized opportunities for turtle-design-mockup

1. Explore a restrained education addition beneath the existing portrait identity, using the supplied current-student facts and full program name.
2. Show the November résumé destination in the existing action, with the rest of the About section as context.
3. Check the added caption at desktop/mobile widths and enlarged text, preserving brand and surrounding content.

## Proposed design sections in recommended page order

| Order | Section | Rationale |
| --- | --- | --- |
| 1 | `about_profile_and_resume` | Review the portrait education detail and existing résumé action together inside the single affected About section. All other content is contextual, keeping this small request to one design review area. |

The résumé destination is an explicit user requirement, not a separate visual direction to choose. The proposed section list requires confirmation before mockups.
