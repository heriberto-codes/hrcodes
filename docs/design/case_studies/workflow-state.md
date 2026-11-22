---
feature_slug: case_studies
scope: section
status: planned
sections_confirmed: true
current_section: null
assembly_status: complete
checkpoint_status: approved
backlog_status: ready
plan_status: created
backlog_item: "- [ ] Add Turtle AI as the second founder case study while preserving the approved site design (`case_studies`)"
plan_path: docs/plans/case_studies_plan.md
---

# Design Workflow State

## Sections

| Order | Section | Status | Selected direction |
| --- | --- | --- | --- |
| 1 | section_introduction | selected | Continuity — updated project count |
| 2 | relationship_selector_and_project_index | selected | Continuity — append Turtle AI |
| 3 | case_narratives_and_evidence | selected | Continuity — Turtle AI evidence card |
| 4 | project_fit_inquiry_band | selected | Continuity — existing inquiry band |

## Decisions

- 2026-11-20: Bootstrapped the existing `case_studies` workspace through `$turtle-design-next`. It is the only design folder eligible for bootstrap; `business_focused_homepage` is already `planned` and remains unchanged.
- Inspected [audit.md](audit.md). No `design-spec.md`, `mockups/`, `checkpoint.md`, or `approved-design.md` exists in this workspace. No section selection or approval can be recovered from those artifacts.
- Proposed the four ordered design areas above from the audit's section list. All are pending and require explicit user confirmation before mockups. This bootstrap is the single transition performed by this invocation.
- User objective: add **Turtle AI as a new founder project** in `02 / Case Studies`, using [heriberto-codes/turtle_ai](https://github.com/heriberto-codes/turtle_ai) for details. This instruction establishes project inclusion; it does not select a visual direction or confirm the proposed section order.
- Preserve the surrounding Services → Case Studies → Development Process sequence, brand system, client/founder separation, existing client cases, cThink, and inquiry destination. Scope the design work to incorporating Turtle AI coherently; the earlier audit is context, not authorization to rewrite every existing case or resolve unrelated content questions.
- Confirmed founder order: **cThink → Turtle AI**, retaining the existing project's position and appending the new project. The user explicitly confirmed this order with the section list on 2026-11-20.
- The introduction, relationship label/index, and fallback explanation should accommodate **four client engagements and two founder projects**. Explore plural “Founder Projects” wording rather than retaining singular counts. This is a proposed content adjustment, not a selected design.
- The narrative/evidence area should include a Turtle AI case using the existing Understand → Build → Show structure. Preserve the current client order: Empowered Path Therapy → Rubix AI → LinkTag → Change Food For Good.
- Existing homepage Direction B is historical context. It is not an explicit selection for this new workspace, and the previous homepage approval does not approve the Turtle AI addition.
- No production code/assets, audit content, backlog, plan, checkpoint, or approval artifact was changed during bootstrap.
- 2026-11-20: The user explicitly confirmed the proposed sections and founder order. Confirmed section order: section introduction → relationship selector and project index → case narratives and evidence → project-fit inquiry band. The section table records this final order; all sections remain pending with no visual direction selected.
- Completed the section-confirmation transition only: set `sections_confirmed` to `true`, selected the first unfinished section (`section_introduction`) as `current_section`, and advanced to `section_mockup_pending`. No mockups were created in this transition.
- 2026-11-20: Created and visually inspected two introduction mockup options. The user subsequently requested removal of the A/B mockups. Removed both options, their shared stylesheet, comparison gallery, five preview images, and the specification that described only those options.
- Returned `section_introduction` to `pending` and workflow status to `section_mockup_pending` so no selection is requested for deleted artifacts. Preserved the confirmed section/founder order, Turtle AI brief, and all handoff state. No replacement mockups were created and no direction was selected or approved.

## Turtle AI source evidence and content brief

- Inspected the public repository metadata, README, and file tree on 2026-11-20. Source revision: [`04c7a3f732cac0f272eba7c9b031035cfe3eccb0`](https://github.com/heriberto-codes/turtle_ai/commit/04c7a3f732cac0f272eba7c9b031035cfe3eccb0), the observed `main` head. The [README](https://github.com/heriberto-codes/turtle_ai/blob/04c7a3f732cac0f272eba7c9b031035cfe3eccb0/README.md) identifies v1.1.0.
- Positioning supported by the README: a collection of project-local Codex skills and Markdown workflow rules for building software in small, reviewable steps while retaining engineer understanding. It is an instruction-based developer workflow, not a hosted application.
- Problem supported by the README: accepting AI-generated code without understanding how it works can make later maintenance harder. Turtle makes explaining the change part of the workflow through an engineer checkpoint.
- Deliverable supported by the README: 25 skills, an optional design-to-approval workflow, an implementation loop of execute → verify → engineer checkpoint → test → plan step update, conditional debugging, and separate design/implementation file-based state systems.
- Primary evidence candidate: the public repository and README. Supporting evidence candidates: the repository's [workflow reference](https://github.com/heriberto-codes/turtle_ai/blob/04c7a3f732cac0f272eba7c9b031035cfe3eccb0/docs/system/workflow.md) and [design workflow](https://github.com/heriberto-codes/turtle_ai/blob/04c7a3f732cac0f272eba7c9b031035cfe3eccb0/docs/system/design-workflow.md). Those supporting files were confirmed in the tree; their full remote contents were not reviewed in this bootstrap.
- Visual candidates confirmed in the source tree: `assets/turtleAI.png` (the README describes it as a workflow overview), plus logo variants under `assets/Turtleai_logo/` including PNG, SVG, and WebP. No image was downloaded, visually assessed, or copied into production. The mockup stage must inspect a candidate before choosing its treatment.
- Do not describe this as a live SaaS product, imply measured productivity gains, or promise mechanically enforced gates, bug-free code, or secure code. The README explicitly states that the workflow depends on Codex, human review, and file-based state and does not guarantee those results.
- The user's instruction establishes founder-project classification. Exact personal role wording, project dates, adoption, and measurable outcomes are not established by the inspected material. Omit unsupported metadata and claims unless the owner supplies them; qualitative descriptions of the published deliverable are sufficient.

## Next action

2026-11-20: The user explicitly invoked `$turtle-design-next` to resume the Turtle AI addition, preserving layout, colors, and case structure, retaining cThink first, and limiting review to the new project and necessary count, label, and index updates. This supersedes the earlier wait for replacement-artifact direction. The public Turtle AI README was re-read; its v1.1.0 workflow positioning remains consistent with the source brief above. No setup prompts from that README were executed.

Performed the section-mockup transition only. Created one narrow direction, **Continuity — updated project count**, for `section_introduction`: [editable mockup](mockups/section_introduction/continuity.html), [gallery](mockups/index.html), [specification](design-spec.md), and [desktop](mockups/previews/introduction_desktop.png) / [mobile](mockups/previews/introduction_mobile.png) previews. Proposed introduction count: four client engagements and two founder projects. Desktop/mobile previews were visually inspected; normal-width checks at 320/390/768/1440px and 200% text checks at 320/390/1440px found no horizontal overflow after small heading-wrapping safeguards. Reduced-motion behavior was checked.

At the end of that mockup transition, the introduction was `mockup_ready` and all other sections remained `pending`. No direction was selected and no checkpoint, approval, backlog, plan, production template, stylesheet, or asset was changed.

2026-11-21: The user invoked `$turtle-design-next` with “I approve the current introduction.” Recorded this explicit section selection as **Continuity — updated project count**, preserving the heading, layout, palette, and the copy “Four client engagements and two founder projects.” This is selection of the introduction only; it is not approval of the complete assembled design or authorization for production implementation.

Performed the section-selection transition only. Set `section_introduction` to `selected`, moved `current_section` to `relationship_selector_and_project_index`, and set workflow status to `section_mockup_pending`. All later sections remain `pending`; no mockup, specification, checkpoint, approval, backlog, plan, production code, or asset was changed in this transition.

2026-11-21: The user invoked `$turtle-design-next` again. Performed the section-mockup transition for `relationship_selector_and_project_index` only. Created one direction, **Continuity — append Turtle AI**, in [the editable project-list mockup](mockups/relationship_selector_and_project_index/continuity.html?group=founder). Updated the [gallery](mockups/index.html) and [specification](design-spec.md); created [Founder Projects desktop](mockups/previews/project_index_founder_desktop.png), [Founder Projects mobile](mockups/previews/project_index_founder_mobile.png), and [Client Work desktop](mockups/previews/project_index_client_desktop.png) previews.

The mockup preserves the selected introduction as context, the existing layout/palette/control styling, the four client entries/order, and Client Work as the default. It proposes the plural **Founder Projects** tab/index label, **01 cThink → 02 Turtle AI**, the new `#case-turtle-ai` anchor, and plural no-script wording. A clearly labelled review guide supplies navigation destination markers only; it is not proposed website UI and contains no new card narrative or imagery. This addresses the user's earlier confusion about incomplete introduction-only previews without advancing the case-narrative stage.

Visually inspected all three preview images. Chromium checks passed at 320/390/768/1440px and 200% root text at 320/390/1440px without horizontal overflow. Verified click/keyboard tab behavior, inactive indexes/panels, native Turtle AI anchor navigation, founder hash selection, reduced motion, and no-JavaScript access to all six entries. Safari/device and screen-reader checks remain unperformed. No production code/assets, selected introduction artifact, audit, checkpoint, approval, backlog, or plan was changed.

At the end of that mockup transition, workflow status was `section_selection_pending` and `relationship_selector_and_project_index` was `mockup_ready`. The introduction stayed `selected`, later sections stayed `pending`, and assembly stayed `pending`.

2026-11-21: The user invoked `$turtle-design-next` with “I approve the project list.” Recorded this explicit section selection as **Continuity — append Turtle AI**: preserve Client Work as the default and the existing four client entries/order; use the plural **Founder Projects** label and **01 cThink → 02 Turtle AI** founder index. Preserve the existing layout, colors, and selected introduction. This selects the project list only and does not approve the complete assembled design or authorize production implementation.

Performed the section-selection transition only. Set `relationship_selector_and_project_index` to `selected`, moved `current_section` to `case_narratives_and_evidence`, and set workflow status to `section_mockup_pending`. The introduction remains selected; the case narratives and inquiry band remain pending. Assembly, checkpoint, backlog, and plan state are unchanged. No mockup, specification, production code, or asset was changed in this transition.

2026-11-21: The user invoked `$turtle-design-next` again. Performed the section-mockup transition for `case_narratives_and_evidence` only. Created one narrow direction, **Continuity — Turtle AI evidence card**, in [the editable case preview](mockups/case_narratives_and_evidence/continuity.html?group=founder#case-turtle-ai). Updated the [gallery](mockups/index.html) and [design specification](design-spec.md), and created [desktop](mockups/previews/turtle_ai_card_desktop.png), [mobile](mockups/previews/turtle_ai_card_mobile.png), and [founder context](mockups/previews/founder_cases_desktop.png) previews.

The preview appends Turtle AI after cThink with the existing identity/image/Understand → Build → Show/evidence-disclosure structure and surrounding palette. Its new copy describes project-local Codex skills, review/understanding/testing steps, and human-reviewed file-based progress. Read the public README, workflow/design references, and license through the GitHub connector at the recorded revision. Inspected the original 1254 × 1254 workflow overview before selecting it; copied the unmodified image and license into mockup assets. A square full-frame treatment prevents cropping workflow blocks. Omitted unsupported dates, personal role, adoption, measured gains, hosted-app claims, and guaranteed enforcement.

All five existing case article HTML blocks are preserved apart from local image URLs, with read-only image copies so the preview is independent of Django. The selected introduction/index files remain unchanged. The scope banner is review-only; the pending inquiry band is not included. New artifact titles and cream-surface focus reuse deep navy; broader audit redesigns remain deferred. A 14px gap separates only the new card’s mobile evidence actions from their descriptions.

Rendered and visually inspected desktop/mobile/new-card and complete founder-context previews. Chromium checks at 320/390/768/1440px and 200% root text at 320/390/1440px found no horizontal overflow. Verified all six images decode, client default, founder selection/order, new hash navigation, keyboard disclosure/focus, and no-JavaScript access to all six articles. Real Safari/device, screen-reader, and true browser-zoom verification remain unperformed. Source artwork delivery optimization remains an implementation consideration. No production code/assets, audit, checkpoint, approval, backlog, or plan was changed.

At the end of that mockup transition, status was `section_selection_pending` and `case_narratives_and_evidence` was `mockup_ready`. Introduction and project list remained selected, inquiry band remained pending, and assembly remained pending. No selection or complete-page approval was inferred.

2026-11-21: The user invoked `$turtle-design-next` with “approved.” in direct response to the Turtle AI card approval prompt. Recorded the explicit selection as **Continuity — Turtle AI evidence card**: append Turtle AI after cThink, preserve the existing case structure and palette, and use the reviewed full-frame workflow overview, Understand → Build → Show narrative, and repository/workflow/design evidence links. The introduction and project-list selections remain unchanged. This selects the case narrative and evidence direction only; it does not approve the complete assembled design or authorize production implementation.

Performed the section-selection transition only. Set `case_narratives_and_evidence` to `selected`, moved `current_section` to `project_fit_inquiry_band`, and set workflow status to `section_mockup_pending`. The inquiry band remains `pending`; assembly, checkpoint, backlog, and plan state are unchanged. Only this state file changed; no mockup, specification, production code, or asset was changed.

2026-11-21: The user invoked `$turtle-design-next` alone. Performed the section-mockup transition for `project_fit_inquiry_band` only. Created **Continuity — existing inquiry band** in [the editable closing-band preview](mockups/project_fit_inquiry_band/continuity.html). Updated the [gallery](mockups/index.html) and [specification](design-spec.md), and created [desktop](mockups/previews/inquiry_band_desktop.png) and [mobile](mockups/previews/inquiry_band_mobile.png) preview images.

The direction preserves the authored closing band’s visible wording, palette, layout, responsive stack, and `#start-a-project` destination. Remove only the mismatched overriding action `aria-label` so its accessible name follows “Discuss Your Project”; the arrow stays decorative. Broader form/call copy changes remain deferred. The standalone preview includes visibly labelled review guidance and a test destination, not a working form. These are not application UI. No full-page assembly was performed.

Visually inspected desktop/mobile previews. Chromium checks at 320/390/768/1440px at normal and 200% root text found no document or band overflow. Verified exact visible accessible name, peach keyboard focus, cream hover, Enter activation, return link, and JavaScript-disabled native anchor operation. SHA-256 checks confirmed all three selected editable artifacts unchanged. Safari/device, screen-reader, and true browser-zoom checks remain unperformed. No production code/assets, audit, checkpoint, approval, backlog, or plan changed.

At the end of that mockup transition, status was `section_selection_pending` and `project_fit_inquiry_band` was `mockup_ready`. All earlier sections remained selected; assembly remained pending. No direction selection or complete-page approval was inferred.

2026-11-21: The user invoked `$turtle-design-next` with “I approve the closing section”. Recorded the explicit selection as **Continuity — existing inquiry band**, preserving the visible wording, palette, responsive composition, and `#start-a-project` destination, with the reviewed removal of the mismatched action `aria-label`. All three earlier section selections remain unchanged.

Performed the section-selection transition only. All four confirmed sections are now `selected`; cleared `current_section` and set workflow status to `assembly_pending`. Assembly remains `pending`; checkpoint, backlog, and plan state are unchanged. Only this state file changed. No assembly, mockup revision, specification update, complete-page approval, or production implementation was performed.

2026-11-21: The user invoked `$turtle-design-next` alone. Performed the full-page assembly transition through the mockup contract. Combined the four selected directions as **Continuity — Turtle AI addition** in [the complete editable preview](mockups/assembled/continuity.html?group=founder). Updated the [gallery](mockups/index.html) and [specification](design-spec.md), and rendered [Founder Projects desktop](mockups/previews/assembled_founder_desktop.png), [phone](mockups/previews/assembled_founder_mobile.png), and [Client Work desktop](mockups/previews/assembled_client_desktop.png) images.

Preserved introduction → selector/index → cases/evidence → inquiry band, existing palette/layout, default Client Work and four client cases/order, and cThink → Turtle AI. The closing band occurs once outside both relationship panels. The assembly contains real content for all six cases and a separately labelled review-only inquiry destination. All four selected source artifacts remain unchanged; six article blocks and the selected closing band match their sources exactly. No material continuity conflict or new section direction was introduced. The production sticky rail and real inquiry form remain implementation boundaries, not redesigns authorized by this preview.

Visually inspected desktop/phone/full-client previews. Both relationship views passed Chromium layout checks at 320/390/768/1440px with normal and 200% root text without document/band horizontal overflow. Verified keyboard tabs/focus, anchors and direct hash selection, disclosure controls, inquiry accessible name and native destination, image decode, reduced motion, and JavaScript-disabled access to all six cases. Real Safari/device, screen-reader, and true browser-zoom checks remain unperformed. Verification details and deferred audit/image-delivery questions are recorded in the specification.

All four sections stay `selected`; `current_section` stays null. Set `assembly_status` to `complete` and workflow status to `checkpoint_pending`. Checkpoint remains `not_started`; backlog and plan remain unchanged. No checkpoint questions, final approval, approval artifact, production implementation, or audit changes were performed.

2026-11-21: The user invoked `$turtle-design-next` alone. Began the feature-level checkpoint through the checkpoint specialist contract and created [checkpoint.md](checkpoint.md). Confirmed the only active workspace is `case_studies`, every section has an explicit selected direction, and assembly is complete. Reviewed the saved audit, specification, assembled HTML, gallery, and existing verification record; no new browser verification was performed in this transition.

Presented the sole assembled direction, **Continuity — Turtle AI addition**. Recorded the user's existing scope, preservation requirements, founder order, and all four section selections without asking those decisions again. The remaining question is whether the user approves the complete desktop and phone composition for planning. Individual section approvals and this bare invocation do not establish complete-design approval.

Set `checkpoint_status` to `under_review`; workflow status remains `checkpoint_pending`. Preserved confirmed order, selected directions, `current_section: null`, complete assembly, and all backlog/plan fields. No mockups, specification, audit, production code/assets, backlog, or plan changed. No approval artifact was created.

2026-11-21: The user compared the working site and preview and asked about the sticky desktop heading/index rail. Clarified that this is existing production behavior which the specification requires preserving; the static preview does not authorize removing it. No revision or production change was requested or made.

2026-11-21: The user invoked `$turtle-design-next` with “I approve Continuity — Turtle AI addition for planning.” Performed the feature-level checkpoint approval transition only. Updated [checkpoint.md](checkpoint.md) to `approved`, recording the explicit named complete-design approval, desktop/mobile acceptance in response to the outstanding question, and sticky-sidebar preservation. Created [approved-design.md](approved-design.md) with approved scope, content, order, tokens, assets, responsive and interaction requirements, accepted design tradeoffs, verification limits, and implementation questions.

Set workflow and checkpoint status to `approved`. Preserved all four selected sections/directions, confirmed order, complete assembly, `current_section: null`, and unchanged backlog/plan fields. No audit, specification, mockups, production application code/assets, backlog, or plan changed. Approval authorizes planning only.

2026-11-21: The user invoked `$turtle-design-next` alone. Performed the approved-design-to-backlog transition through the `turtle-backlog` contract. Verified that [checkpoint.md](checkpoint.md) records `approved` and [approved-design.md](approved-design.md) explicitly authorizes planning. Compared the approved goal and `case_studies` slug against the existing backlog; no equivalent item exists. Appended one unchecked Features item to [the backlog](../../backlog.md):

- [ ] Add Turtle AI as the second founder case study while preserving the approved site design (`case_studies`)

The item inherits the approved scope: cThink first, Turtle AI second, existing layout/colors/case structure and desktop sticky rail preserved, with necessary count, label, index, fallback, evidence, and approved inquiry accessible-name updates. Preserved all existing backlog items/statuses, four selected sections/directions, confirmed order, complete assembly, checkpoint approval, and plan fields. Set `backlog_status` to `ready`, recorded the exact item, and advanced workflow status to `plan_pending`. No plan or production implementation was created.

2026-11-21: The user invoked `$turtle-design-next` alone. Performed the backlog-to-plan transition through the `turtle-plan` contract using the exact recorded backlog item and `case_studies` slug. Reconfirmed checkpoint/design approval, the sole active workspace, and the matching unchecked backlog item. Created [the implementation plan](../../plans/case_studies_plan.md) with two unchecked atomic steps: prepare the approved artwork/license, then integrate the complete coordinated case/navigation/presentation change with regression coverage in its TEST phase.

The plan preserves the existing desktop sticky rail, brand and cases, records the actual cThink-only hash handling that must be extended, avoids overwriting the different existing Turtle AI image used elsewhere, and acknowledges the implemented FormView boundary where foundation documentation is stale. It includes scoped browser and Django verification, asset delivery assessment, accepted tradeoffs, and remaining verification limits.

Set workflow status to `planned`, `plan_status` to `created`, and `plan_path` to `docs/plans/case_studies_plan.md`. Preserved all selected sections/directions, confirmed order, complete assembly, checkpoint approval, exact backlog reference, and backlog status. No backlog item was completed, no plan step was checked, and no production code/assets or specialist design artifacts changed.

Next action: design automation is complete. Implementation begins only when the user explicitly invokes `$turtle-engineer-execute`; it will act on the first unchecked step in `docs/plans/case_studies_plan.md`.
