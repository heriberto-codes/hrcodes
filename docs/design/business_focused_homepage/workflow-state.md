---
feature_slug: business_focused_homepage
scope: page
status: planned
sections_confirmed: true
current_section: null
assembly_status: complete
checkpoint_status: approved
backlog_status: ready
plan_status: created
backlog_item: "- [ ] Implement the approved business-focused homepage and Guardrails Insights article experience (`business_focused_homepage`)"
plan_path: docs/plans/business_focused_homepage_plan.md
---

# Design Workflow State

## Sections

| Order | Section | Status | Selected direction |
| --- | --- | --- | --- |
| 1 | hero | selected | Direction C — Kinetic mosaic |
| 2 | services | selected | Direction B — Editorial service ledger |
| 3 | case_studies | selected | Direction B — Evidence trail |
| 4 | development_process | selected | Direction D — The working canvas |
| 5 | insights | selected | Direction C — Signal tuner |
| 6 | about | selected | Direction A — Founder profile |
| 7 | start_a_project | selected | Direction B — Three-step brief builder |
| 8 | footer | selected | Direction B — Closing signal |

## Decisions

- Bootstrapped controller state from the existing audit, design specification, mockup workspace, approved checkpoint, and approved-design artifact.
- The user explicitly confirmed the homepage section order as Hero → Services → Case Studies → Development Process → Insights → About → Start a Project → Footer on 2026-09-08.
- Preserved the eight selected directions because `checkpoint.md` and `approved-design.md` explicitly name the same direction set.
- Preserved completed assembly and approved checkpoint evidence because `approved-design.md` calls the homepage an assembled direction set, `checkpoint.md` records `approved`, and `approved-design.md` exists.
- Insights Article Direction B is a separate article-detail experience and is not part of the homepage section list.
- No matching backlog item or implementation plan was found during bootstrap.
- Added the approved design to `docs/backlog.md` as one feature item covering the homepage and its approved Guardrails Insights article experience.
- Created `docs/plans/business_focused_homepage_plan.md` from the recorded backlog item, approved design, and repository architecture; design automation is complete and production implementation remains gated behind an explicit `/turtle-execute` invocation.
