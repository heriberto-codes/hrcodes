# Approved Case Studies design

- Feature slug: `case_studies`
- Scope: existing homepage Case Studies section only.
- Status: `approved`
- Approval date: 2026-11-21
- Selected direction: **Continuity — Turtle AI addition**
- User approval: “I approve Continuity — Turtle AI addition for planning.”
- Authorization: planning only, including the `turtle-plan` handoff. Production implementation requires a later explicit `$turtle-engineer-execute` invocation.

## Approved goal and structure

Append Turtle AI as a founder project while preserving the existing website design and case structure. Keep the surrounding Services → Case Studies → Development Process order. Within the section retain introduction → relationship selector/project index → case narratives/evidence → inquiry band.

Keep Client Work as the default, with Empowered Path Therapy → Rubix AI → LinkTag → Change Food For Good unchanged. Founder Projects contains **01 cThink → 02 Turtle AI**. Update the introduction to four client engagements and two founder projects, plural relationship/index labels, the new numbered project anchor, and the no-JavaScript explanation together with project inclusion.

Keep the existing desktop sticky heading/index rail while the case cards scroll. The isolated preview's static rail is not a replacement for production behavior. At 1080px and below retain the existing stacked, non-sticky rail. Preserve existing case content, IDs, links, disclosures, and context contracts except the specifically approved supporting changes.

## Required new project content and assets

Use the existing cream card, identity/image/Understand → Build → Show sequence, and native evidence disclosure. Turtle AI is **02 / Founder project**, with descriptor **Codex skills + development workflow**.

| Step | Heading | Narrative |
| --- | --- | --- |
| Understand | Keep understanding the code you build | Accepting AI-generated code without knowing how it works can make a project harder to maintain. |
| Build | Small changes, deliberate checkpoints | Organize Codex work with project-local skills, Markdown rules, and a step-by-step loop for implementation, review, understanding, and testing. |
| Show | A published workflow to inspect | The public repository documents the skills, optional design path, and file-based progress tracking. People review the work and decide when to continue. |

Use the selected [workflow overview artwork](mockups/assets/turtle-ai-overview.png), [MIT notice](mockups/assets/turtle-ai-LICENSE.txt), and descriptive alt text from the selected mockup. Display the square artwork in full without cropping. The three evidence links are the public repository, implementation workflow reference, and design workflow reference, with labels and destinations from the selected card. Supporting document URLs are pinned to inspected revision `04c7a3f732cac0f272eba7c9b031035cfe3eccb0`; source details are recorded in the specification. Do not add unsupported dates, personal role, adoption, measured gains, hosted-app claims, or guaranteed enforcement.

## Presentation, interaction, and accessibility

Preserve IBM Plex Mono, deep navy `#101D3B`, cream `#F9E9D5`, peach `#F29576`, grey `#AEB7CA`, existing supporting/line tokens, 1320px maximum, gutters, spacing, and desktop column proportions. Green/purple remain within the supplied artwork. Preserve selected heading wrapping safeguards, the new card's navy evidence titles/focus treatment, and mobile evidence-action spacing as detailed in the specification.

Retain existing responsive transitions: stacked rail at 1080px; single-column card narrative, evidence, and closing band at 760px; narrow-phone gutters/padding. Allow text wrapping and preserve reduced-motion behavior. Retain keyboard tab selection, roving focus, native case/hash links and disclosures, and access to all six cases without JavaScript.

Keep one existing closing inquiry band outside both filtered panels, its visible copy, and `#start-a-project` destination. Remove its overriding mismatched `aria-label` so its accessible name follows Discuss Your Project. Preserve the real homepage form. Review banners, gallery, destination marker, and standalone demo script are not website implementation requirements.

## Accepted scope and implementation questions

The selected continuity direction retains existing small-copy styling and a taller square Turtle AI image. Broader audit findings about other cases, chronology, navigation, and typography remain deferred. Preserve the existing sticky rail; its short-window limitation is not redesigned by this approval.

Assess optimized delivery of the approximately 2.46 MiB source artwork while retaining fidelity and licensing. Repository architecture controls technical decisions: reuse the Django include, authored CSS/assets, and existing JavaScript behavior without introducing a framework, database, or route change. Do not import the standalone mockup as application code.

Recorded checks cover Chromium layouts, enlarged root text, keyboard controls, no-JavaScript access, and reduced motion. Real Safari/device, screen-reader, and true browser-zoom checks remain unperformed; design approval is not a certification of those checks. Production integration must verify the preserved sticky sidebar and coordinated project content/navigation changes.

## Source artifacts

- [Checkpoint and explicit approval](checkpoint.md)
- [Design specification and verification evidence](design-spec.md)
- [Audit; broader findings deferred under the approved scope](audit.md)
- [Selected complete editable mockup](mockups/assembled/continuity.html?group=founder)
- [Desktop preview](mockups/previews/assembled_founder_desktop.png) · [phone preview](mockups/previews/assembled_founder_mobile.png) · [Client Work preview](mockups/previews/assembled_client_desktop.png)
- [Workflow state](workflow-state.md)
