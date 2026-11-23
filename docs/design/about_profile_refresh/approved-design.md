# About Profile Refresh — Approved Design

Feature: `about_profile_refresh`  
Direction: **Continuity — current studies**  
Approval date: 2026-11-22  
Scope: the complete assembled About section, `about_profile_and_resume`.

The user explicitly stated: “I approve Continuity — current studies for planning.” This approval authorizes implementation planning through `turtle-plan` only. Implementation requires a later explicit engineering invocation.

## Approved goals and structure

Refresh the résumé destination and communicate current Boston University study beneath the existing portrait identity while preserving the established About design.

Keep the caption in this order:

1. Founder + Principal Software Engineer
2. Heriberto Roman
3. A fine divider, then **Current student · Boston University**
4. **Master’s in Software Engineering for Artificial Intelligence**

Use the exact user-supplied résumé destination:

<https://hroman-codes.s3.us-east-2.amazonaws.com/HRomandevresume_November_2026.pdf>

Preserve “View résumé,” its decorative arrow and hidden new-tab announcement, `target="_blank"`, and `rel="noopener noreferrer"`. Update other old résumé links identified by the audit, including the historical About mockup's destination only. Preserve that mockup's historical design and approval. Carry the matching application regression expectation into the engineering TEST phase. Other PDF documents remain outside this scope.

## Required components, tokens, and assets

Add a subordinate education group containing separate status/institution and program-title paragraphs inside the existing portrait caption. Use normal reading order and current-student language; do not imply a completed degree or introduce dates, abbreviations, or university branding.

Reuse the existing portrait, framing, IBM Plex Mono, navy/cream/peach palette, and homepage tokens. The education group uses the existing `--line-dark` divider, 11px top margin, and 16px top padding. Status text uses `--navy-deep`, 0.75rem, weight 600, and line-height 1.6. The program uses `--ink`, 0.875rem, line-height 1.65, and 8px top separation, with natural wrapping and an overflow-wrap fallback.

Preserve the About headline, story, skillset, video, consultation action, and surrounding content. Implement within the existing Django template and authored stylesheet boundary; reuse application assets rather than importing preview HTML, CSS snapshots, or review navigation into the site. No new framework, JavaScript, font, or image is required.

## Responsive behavior and interactions

Retain the existing desktop two-column layout and sticky portrait above 760px. Preserve mobile order below that breakpoint: section label, headline, portrait/caption, story, skillset, video, and actions. Allow education text to wrap and increase caption height without truncation, fixed heights, forced line breaks, or an additional breakpoint.

The education detail is noninteractive. Preserve native keyboard access, visible focus, and existing external-link semantics for the résumé action.

## Accepted tradeoffs and implementation questions

The user approved the assembled caption hierarchy, added vertical height, and desktop/mobile presentation. The narrow change retains the surrounding design and existing responsive behavior.

Mockup verification found normal-width fit and new-caption fit with enlarged root text. Inherited headline/context overflow at enlarged text remains documented; approval does not assert a full-page accessibility pass or expand scope to redesign those elements. External PDF availability/content, third-party playback, real devices, screen readers, and actual browser zoom remain unverified. Validate the application rendering and relevant regression behavior during the engineering workflow; preview evidence is not application validation.

No design questions remain for planning. Search authored sources again during implementation for additional old résumé destinations, preserving unrelated document links and avoiding generated files. No database, routing, deployment, or infrastructure change is required by this design.

## Design references

- [Audit](audit.md)
- [Design specification](design-spec.md), retaining its pre-approval assembly-stage record
- [Selected editable mockup](mockups/about_profile_and_resume/continuity.html#about)
- [Complete assembled About preview](mockups/assembled/continuity.html#about)
- [Desktop preview](mockups/previews/assembled_desktop.jpg)
- [Mobile preview](mockups/previews/assembled_mobile.jpg)
- [Approved checkpoint record](checkpoint.md)

The approved checkpoint and this artifact establish final approval; the earlier specification's pending-checkpoint wording records the stage at which it was authored.
