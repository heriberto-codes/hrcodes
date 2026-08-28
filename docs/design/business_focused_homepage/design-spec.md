# Business-Focused Homepage — Hero Design Specification

## Status and scope

This specification covers the selected, founder-forward homepage Hero direction requested after the business-focused homepage audit. Review it from [`mockups/index.html`](./mockups/index.html), then open [`Version A`](./mockups/hero/direction-a.html) from the section-specific `mockups/hero/` workspace for the responsive, editable view. These are design artifacts, not production-ready code, and they do not modify or depend on the production Django templates.

Version A is selected for continued revision and feedback; it is not approved for implementation. No checkpoint exists for this design workspace.

## Version A — Founder-led business clarity

### Intent and rationale

The Hero should make Hroman Codes read as a software business within the first screen while preserving Heriberto Roman as the source of trust. The hierarchy therefore begins with the client constraint, names Hroman Codes as the partner, shows the founder alongside the promise, and offers one high-intent action plus one evaluation action.

This responds directly to the audit’s primary tension: the current Hero has useful business language, but the surrounding résumé cues and founder-first headline leave the commercial identity ambiguous. The proposed direction keeps the personality and existing visual system without leading with a name, job title, or “I build for the web.”

### Structure and visual hierarchy

1. A compact header uses the official Hroman Codes wordmark and buyer-oriented navigation: Services, Case Studies, Process, About, Contact, and Start a project.
2. One semantic H1 connects the client’s business constraint to a concrete delivery outcome: “From business problem to working software.” The word “software” carries the peach emphasis and hand-drawn underline.
3. User-supplied supporting copy introduces Heriberto as Principal Software Engineer and founder of HROMAN CODES, LLC, then connects ideas and inefficient workflows to digital products, practical automation, and scalable software for small businesses, startups, and growing organizations.
4. “Book A Call,” paired with a calendar icon, is the primary action; “Review case studies” supports prospects who want to evaluate relevant client problems, responsibilities, approaches, and delivered results before scheduling.
5. A founder portrait and proof card establish direct collaboration and end-to-end ownership, use “Founder + Principal Software Engineer,” and provide the Hero-level About destination.
6. A capability rail presents the product-development progression `idea → prototype → MVP → product → iterate` as an operating signal.

### Existing elements preserved

- Colors derived from production tokens: navy `#192A51`, cream `#F9E9D5`, peach `#F29576`, white, and a lightened supporting grey.
- IBM Plex Mono across headlines, navigation, body copy, controls, labels, and proof content to create one consistent brand voice. Hierarchy comes from weight, scale, spacing, and color rather than a second typeface.
- The exact production `hr.svg` wordmark used by the current desktop navbar and the existing `aboutMeImage.png` founder portrait, both referenced read-only from `static/pages/images/`. The earlier improvised `H.svg` plus text lockup was removed after review feedback.
- Rounded CTA borders, subtle rules, numbered labels, dark surfaces, orange accents, and full-width mobile actions.
- Founder-led credibility and a five-stage product-development narrative.

### Proposed components

- Business-oriented brand lockup and navigation labels.
- Client-problem H1 with a restrained hand-drawn underline accent.
- Scheduling CTA with an inline calendar icon as the primary conversion action.
- Founder proof composition combining portrait, role, availability state, and two operating promises.
- Five-stage capability rail.
- Native `<details>` mobile navigation that does not depend on third-party JavaScript.

### Tokens and assets

- `--navy` and `--navy-deep` provide the primary and layered dark surfaces.
- `--cream` is the main text color; `--peach` is reserved for emphasis and action.
- The production grey is lightened in the mockup to protect readability for normal-size copy. Production implementation should confirm exact contrast values before selecting a final token.
- IBM Plex Mono uses its available 700 weight, slightly relaxed display tracking, and fluid `clamp()` sizing for headlines; supporting copy retains a lighter monospaced cadence.
- The portrait area uses CSS grid lines and gradients rather than a new decorative asset.

### Responsive behavior

- Desktop uses a two-column Hero: message first, founder proof second.
- Below 860 px, the Hero becomes a single-column sequence with message and CTAs before the portrait.
- Desktop navigation changes to a native mobile menu at the same breakpoint.
- Below 480 px, actions become full width, the headline scales fluidly, proof facts stack, and the capability rail moves to a two-column layout.
- Essential content is not duplicated between breakpoints, preserving one logical heading hierarchy.

### Interaction and content states

- Hover states distinguish both CTA priorities without introducing attention-heavy animation.
- All links and the mobile-menu summary have a high-visibility keyboard focus state.
- The mobile menu works through native HTML and exposes the same navigation choices as desktop.
- Anchor destinations are illustrative because this mockup covers only the Hero. Services and About point to visible Hero content; Case Studies, Process, and Contact retain nonvisual targets for future section mockups without displaying prototype boundary labels.
- “Book A Call” points to the illustrative Contact target. Production implementation still needs a confirmed scheduling destination, meeting length, availability, timezone handling, and concise expectations for what the call covers.
- The mockup demonstrates the pre-scheduling state only. External scheduling, loading, error, confirmation, privacy, and follow-up states remain outside this Hero artifact.
- Reduced-motion preferences disable smooth scrolling and transitions.

### Accessibility considerations

- The Hero uses one H1 and a logical H2 for founder identity.
- The official wordmark has a concise accessible name inside the home link; the founder portrait has meaningful alternative text.
- Navigation landmarks are separately labeled for desktop and mobile.
- Focus treatment does not rely on color alone, actions meet comfortable touch-target sizing, and copy remains understandable without imagery or motion.
- The final palette requires a formal contrast check before production implementation.

### Assumptions and items requiring confirmation

- The primary conversion should begin with a scheduled call rather than a project brief or email. The scheduling provider and destination still require confirmation.
- Heriberto can promise one accountable partner from strategy through delivery.

The user-supplied audience statement, Principal Software Engineer title, product-development stages, all-IBM-Plex-Mono typography, and “Accepting select projects” label are treated as confirmed for this mockup. The remaining assumptions must be settled before implementation.

### Tradeoffs and implementation implications

- Leading with the business problem improves commercial clarity but reduces the immediate prominence of Heriberto’s name. The portrait and founder card intentionally restore that trust signal within the same screen.
- The portrait increases visual warmth and differentiation, but production should optimize the source image and crop for responsive delivery.
- The header is included to show the Hero’s real first-screen context. A future implementation must reconcile its labels and mobile behavior with the global navbar rather than introduce a second navigation component.
- A direct scheduling CTA reduces friction but collects less qualification context than a project brief. Planning should decide what fit guidance appears before booking and confirm the scheduling workflow before implementation.
- The design can map to the existing server-rendered Hero include and global CSS conventions; it does not require a new frontend framework.

## Preview and verification

Version A was revised after browser feedback to replace the improvised header lockup with the exact `hr.svg` production wordmark. Later feedback removed the temporary prototype banner, added About and Contact to both navigation variants, renamed Selected work to Case Studies, removed the numbered founder-led eyebrow and expectation microcopy, replaced the introduction with user-supplied founder copy, and confirmed the availability label without a marker. The latest revisions remove the visible future-section boundary, set the headline to “From business problem to working software.” with orange underlined emphasis on “software,” replace the project-brief action with “Book A Call” and a calendar icon, increase navigation text, establish Principal Software Engineer as the founder title, change the capability rail to Idea, Prototype, MVP, Product, and Iterate, and use IBM Plex Mono for all mockup text.

- [`Version A desktop preview`](./mockups/hero/previews/hero-a-desktop.jpg) rendered at **1440 × 1168**.
- [`Version A mobile preview`](./mockups/hero/previews/hero-a-mobile.jpg) captured at **390 × 1363**. The editable HTML remains the complete mobile source of truth, including the capability rail and future-section boundary below the preview crop.

The editable HTML remains the source of truth. The saved preview images document the preceding navigation revision and were not refreshed after the latest Case Studies, eyebrow, introduction, title, availability, microcopy, headline, CTA, boundary, typography, and capability-stage changes because browser automation was blocked from loading the local `file://` mockup. Static verification confirmed that the current HTML contains one H1, uses the user-supplied Principal Software Engineer wording, removes the eyebrow, expectation microcopy, and visible future-section boundary, uses Case Studies consistently, exposes six matching desktop and mobile destinations, includes the calendar icon within the “Book A Call” action, presents the five requested product stages, and loads IBM Plex Mono as its only text typeface. Open the editable mockup to review the current visual.

## Next step

Continue collecting feedback on Version A. Once revisions are complete, run `turtle-design-checkpoint` to review the Hero’s primary positioning and conversion choice one decision at a time. This mockup does not approve itself or authorize implementation.
