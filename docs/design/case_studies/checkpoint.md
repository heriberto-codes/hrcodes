# Case Studies design checkpoint

- Feature: `case_studies`
- Review started: 2026-11-21
- Status: `approved`
- Approval date: 2026-11-21
- Assembled direction reviewed: **Continuity — Turtle AI addition**
- Selected complete-page direction: **Continuity — Turtle AI addition**, explicitly approved for planning.
- References: [audit](audit.md), [specification](design-spec.md), [assembled editable preview](mockups/assembled/continuity.html?group=founder), [review gallery](mockups/index.html), [controller state](workflow-state.md).

## Directions reviewed

One continuity direction is available because the user explicitly requested preserving the existing design while adding Turtle AI. The complete Case Studies section combines these previously selected directions:

| Section | User-selected direction |
| --- | --- |
| Introduction | Continuity — updated project count |
| Relationship selector and project index | Continuity — append Turtle AI |
| Case narratives and evidence | Continuity — Turtle AI evidence card |
| Project-fit inquiry band | Continuity — existing inquiry band |

All confirmed sections are selected and assembly is complete. This checkpoint concerns the assembled section, not unrelated homepage sections. Prior section approvals establish the decisions below; the explicit complete-design approval is recorded separately below.

## Resolved decisions

- Preserve the existing layout, navy/cream/peach palette, typography, and Understand → Build → Show case structure. Keep Client Work as the default and preserve its four cases and their order.
- Keep cThink first and append Turtle AI as the second founder project. Update the introduction count to four client engagements and two founder projects, use the plural Founder Projects label, and include the new numbered index link and fallback wording.
- Use the selected Turtle AI overview graphic in full, the reviewed narrative about project-local Codex skills and human-reviewed development, and repository/workflow/design evidence links. Omit unsupported dates, role wording, adoption, quantified gains, hosted-app claims, and enforcement guarantees.
- Preserve the selected closing inquiry band and its existing destination; align the accessible action name with the visible Discuss Your Project text.
- Preserve the working site's sticky desktop sidebar: the heading and project index stay visible while cases scroll. The user compared the full site and preview and asked about this behavior; it was clarified before final approval that the static mockup does not authorize removing production stickiness. Retain the existing non-sticky stacked behavior at 1080px and below.
- Keep this review focused on the new project and required supporting changes. The audit's broader typography, other case content, chronology, and navigation redesign proposals remain deferred under the user's scope.

## Assembly review against the brief and audit

The assembly retains the introduction → selector/index → case narrative/evidence → inquiry sequence. The existing five cases remain present and Turtle AI follows cThink. One closing band sits outside both filtered panels. No material conflict between selected sections is recorded in the specification.

Desktop uses the existing two-column proportions; on smaller screens the rail moves above the cases and card content stacks. Both relationship groups, case anchors, disclosures, keyboard tabs, and no-JavaScript access are represented. These support inspecting the new founder project while preserving the existing evaluation path. The user approved the complete direction in response to the desktop/mobile approval question, with production sticky-sidebar preservation clarified beforehand.

Review evidence: [Founder Projects desktop](mockups/previews/assembled_founder_desktop.png), [phone](mockups/previews/assembled_founder_mobile.png), and [Client Work desktop](mockups/previews/assembled_client_desktop.png). The specification records prior visual checks and Chromium checks at 320/390/768/1440px, normal and enlarged root text, keyboard navigation, and no-JavaScript behavior. This invocation inspected the saved artifacts; it did not rerun browser tests.

## Requested revisions

None outstanding. The sticky-sidebar question was a clarification of the existing preservation requirement, not a request to redesign or revise the assembled sections.

## Accepted design tradeoffs and verification limits

- Prior selections preserve the current small-copy hierarchy and use a taller square Turtle AI image to avoid cropping its workflow blocks. Broader audit remediation remains deferred.
- Image delivery optimization remains an implementation question. The existing production sticky rail and real inquiry form must be preserved; static review guidance, the demo script, and the labelled destination marker are preview tools only.
- Real Safari/device, screen-reader, and true browser-zoom checks remain unperformed. Chromium root-text enlargement does not establish those checks or full accessibility conformance. Approval of the design does not certify unperformed checks.

## Explicit approval

On 2026-11-21 the user invoked `$turtle-design-next` with:

> I approve Continuity — Turtle AI addition for planning.

This resolves the final complete-design approval question. Created [approved-design.md](approved-design.md) as the planning handoff. Approval authorizes planning through `turtle-plan` only; it does not authorize production implementation.

## Remaining questions

None for design approval. Image delivery optimization and implementation verification remain technical planning concerns. Continue with `$turtle-design-next` to create or reuse the matching backlog item in a separate transition.
