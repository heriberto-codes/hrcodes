# Business-Focused Homepage — Hero, Services, and Case Studies Design Specification

## Status and scope

This specification covers the selected, founder-forward homepage Hero, the selected Services Direction B, and the completed Case Studies Direction B mockup. Review the workspace from [`mockups/index.html`](./mockups/index.html), open the preserved [`Hero Version A`](./mockups/hero/direction-a.html) and [`Services Direction B`](./mockups/services/direction-b.html), then review [`Case Studies Direction B`](./mockups/case-studies/direction-b.html). These are design artifacts, not production-ready code, and they do not modify or depend on the production Django templates.

Hero Version A and Services Direction B are preserved in the comparison workspace as completed mockup sections. No Hero or Services source or preview file was changed during the Case Study pass. Case Studies Direction B is the sole remaining direction and is marked completed on the mockup workspace at the user’s request. This mockup-completion status is not approval for planning or implementation. No checkpoint exists for this design workspace.

## Version A — Founder-led business clarity

### Intent and rationale

The Hero should make Hroman Codes read as a software business within the first screen while preserving Heriberto Roman as the source of trust. The hierarchy therefore begins with the client constraint, names Hroman Codes as the partner, shows the founder alongside the promise, and offers one high-intent action plus one evaluation action.

This responds directly to the audit’s primary tension: the current Hero has useful business language, but the surrounding résumé cues and founder-first headline leave the commercial identity ambiguous. The proposed direction keeps the personality and existing visual system without leading with a name, job title, or “I build for the web.”

### Structure and visual hierarchy

1. A compact header uses the official Hroman Codes wordmark and buyer-oriented navigation: Services, Case Studies, Development Process, About, and Start a project. The scheduling action remains the primary contact path.
2. One semantic H1 connects the client’s business constraint to a concrete delivery outcome: “From business problem to working software.” The word “software” carries the peach emphasis and hand-drawn underline.
3. User-supplied supporting copy introduces Heriberto as Principal Software Engineer and founder of HROMAN CODES, LLC, then connects ideas and inefficient workflows to digital products, practical automation, and scalable software for small businesses, startups, and growing organizations.
4. “Book A Call,” paired with a calendar icon, is the primary action; “Review case studies” supports prospects who want to evaluate relevant client problems, responsibilities, approaches, and delivered results before scheduling.
5. A founder portrait and proof card establish direct collaboration and end-to-end ownership, use “Founder + Principal Software Engineer,” and provide the Hero-level About destination.
6. A “Development Process” rail presents the product-development progression `idea → prototype → MVP → product → iterate` as an operating signal.

### Existing elements preserved

- Colors derived from production tokens: navy `#192A51`, cream `#F9E9D5`, peach `#F29576`, white, and a lightened supporting grey.
- IBM Plex Mono across headlines, navigation, body copy, controls, labels, and proof content to create one consistent brand voice. Hierarchy comes from weight, scale, spacing, and color rather than a second typeface.
- The exact production `hr.svg` wordmark used by the current desktop navbar and the existing `aboutMeImage.png` founder portrait, both referenced read-only from `static/pages/images/`. The earlier improvised `H.svg` plus text lockup was removed after review feedback.
- Rounded CTA borders, subtle rules, numbered labels, dark surfaces, orange accents, full-width mobile actions, the original Hero underline’s playful straightening behavior, and its luminous endpoint detail adapted to the headline period.
- Founder-led credibility and a five-stage product-development narrative.

### Proposed components

- Business-oriented brand lockup and navigation labels.
- Client-problem H1 with a restrained hand-drawn underline accent.
- Scheduling CTA with an inline calendar icon as the primary conversion action.
- Founder proof composition combining portrait, role, availability state, the accountable-partner promise, and the focus on digital products and practical automation. The two proof statements use 0.75rem type with 1.45 line height so the credibility details remain readable rather than behaving like decorative microcopy.
- Five-stage Development Process rail.
- Native `<details>` mobile navigation that does not depend on third-party JavaScript.

### Tokens and assets

- `--navy` and `--navy-deep` provide the primary and layered dark surfaces.
- `--cream` is the main text color; `--peach` is reserved for emphasis and action.
- The production grey is lightened in the mockup to protect readability for normal-size copy. Production implementation should confirm exact contrast values before selecting a final token.
- IBM Plex Mono uses its available 700 weight, slightly relaxed display tracking, and fluid `clamp()` sizing for headlines; supporting copy retains a lighter monospaced cadence. An additional 8 pixels separates the headline and introduction at desktop and mobile sizes.
- The portrait area uses CSS grid lines and gradients rather than a new decorative asset.

### Responsive behavior

- Desktop uses a two-column Hero: message first, founder proof second.
- Below 860 px, the Hero becomes a single-column sequence with message and CTAs before the portrait.
- Desktop navigation changes to a native mobile menu at the same breakpoint.
- Below 480 px, actions become full width, the headline scales fluidly, proof facts stack, and the capability rail moves to a two-column layout.
- Essential content is not duplicated between breakpoints, preserving one logical heading hierarchy.

### Interaction and content states

- Hover states distinguish both Hero CTA priorities, while the header’s Start a project action uses the same peach fill and restrained two-pixel lift for consistent conversion affordance.
- Hovering the emphasized word “software” eases its underline from a two-degree tilt to straight over 200 milliseconds. The refined motion preserves the original portfolio interaction without shifting or resizing the line.
- The period after “software” carries a slow 2.4-second peach-and-cream glow pulse adapted from the current portfolio’s luminous orb. On pointer-hover devices, hovering the period makes the glyph disappear into an eight-pixel radial burst; it returns when the pointer leaves. Touch-only devices retain the glow without a hover-dependent effect, while reduced-motion preferences replace both animations with a static, restrained glow.
- Moving a fine pointer through the portrait applies a restrained position-driven translate, skew, color shift, and local highlight. Updates are limited to one per animation frame; touch and reduced-motion users receive the static portrait.
- All links and the mobile-menu summary have a high-visibility keyboard focus state.
- The mobile menu works through native HTML and exposes the same navigation choices as desktop.
- Anchor destinations are illustrative because this mockup covers only the Hero. Services and About point to visible Hero content; Case Studies, Development Process, and Contact retain nonvisual targets for future section mockups without displaying prototype boundary labels.
- “Book A Call” opens the confirmed `https://calendly.com/heriberto_codes/coffee_chat` scheduling destination in a new tab. Production implementation still needs confirmation of the meeting length, availability, timezone handling, and concise expectations for what the call covers.
- The mockup demonstrates the pre-scheduling state only. External scheduling, loading, error, confirmation, privacy, and follow-up states remain outside this Hero artifact.
- Reduced-motion preferences disable smooth scrolling, transitions, CTA lift transforms, the period pulse, and the pixel burst.

### Accessibility considerations

- The Hero uses one H1 and a logical H2 for founder identity.
- The official wordmark has a concise accessible name inside the home link; the founder portrait has meaningful alternative text.
- Navigation landmarks are separately labeled for desktop and mobile.
- Focus treatment does not rely on color alone, actions meet comfortable touch-target sizing, and copy remains understandable without imagery or motion.
- The final palette requires a formal contrast check before production implementation.

### Assumptions and items requiring confirmation

- The primary conversion begins with a scheduled call through the user-confirmed Calendly `coffee_chat` destination rather than a project brief or email.
- Heriberto can promise one accountable partner.

The user-supplied audience statement, Principal Software Engineer title, product-development stages, all-IBM-Plex-Mono typography, and “Accepting select projects” label are treated as confirmed for this mockup. The remaining assumptions must be settled before implementation.

### Tradeoffs and implementation implications

- Leading with the business problem improves commercial clarity but reduces the immediate prominence of Heriberto’s name. The portrait and founder card intentionally restore that trust signal within the same screen.
- The portrait increases visual warmth and differentiation, but production should optimize the source image and crop for responsive delivery.
- The header is included to show the Hero’s real first-screen context. A future implementation must reconcile its labels and mobile behavior with the global navbar rather than introduce a second navigation component.
- A direct scheduling CTA reduces friction but collects less qualification context than a project brief. Planning should decide what fit guidance appears before booking and confirm the scheduling workflow before implementation.
- The design can map to the existing server-rendered Hero include and global CSS conventions; it does not require a new frontend framework.

## Services section — shared foundation

### Relationship to the preserved Hero

The Services artifact is isolated under [`mockups/services/`](./mockups/services/) and deliberately leaves all files under [`mockups/hero/`](./mockups/hero/) unchanged. Its context bar links back to the preserved Hero rather than reproducing or revising it. In the eventual homepage composition, the Services section would follow the Hero’s Development Process rail and inherit its navy, cream, and peach palette; IBM Plex Mono typography; numbered labels; thin rules; compact interaction motion; and direct Book A Call path.

Direction B consolidates the offer into five user-requested service areas:

1. MVP and Product Development.
2. Custom Web Applications.
3. UX/UI Design and Prototyping.
4. AI and Workflow Automation.
5. Maintenance and Technical Support.

The repository does not confirm these as the final commercial service categories, promises, deliverables, engagement shapes, or qualification rules. The visible content note was removed by user request; this specification remains the source of truth for their provisional status. The mockup avoids price and timeline claims and labels the supporting lists as “Typical deliverables.”

## Services Direction B — editorial service ledger

### Intent and rationale

Direction B is the completed Services mockup direction preserved in the comparison workspace. It uses a linear editorial ledger to guide scanning and establish hierarchy without repeating card chrome. The revised offer consolidates seven overlapping categories into five: MVP and Product Development, Custom Web Applications, UX/UI Design and Prototyping, AI and Workflow Automation, and Maintenance and Technical Support.

### Page structure and visual hierarchy

1. The familiar `01 / Services` label, headline, and animated period preserve continuity with the selected Hero. The introduction now states the audience and full product lifecycle directly: “I help founders and small businesses plan, build, launch, and maintain digital products.”
2. A dark “At a glance” panel gives the right side of the introduction a stronger editorial role. It names the five-service scope, summarizes the accountable-partner promise, and contains the services-deck action.
3. A ruled, full-width service ledger replaces the card grid. Each row aligns its number and icon, service purpose, outcome tags, and fit arrow in a consistent horizontal reading path.
4. MVP and Product Development is the only dark featured row. Its increased height and color reversal establish the lead product-engagement capability without implying that every service has identical weight.
5. A separate deep-navy closing band contains the project-fit prompt and Book A Call action. Its solo-shop voice reads “Together, we’ll shape the next step,” framing “together” as collaboration between Heriberto and the client. The action column intentionally leaves open space above the button instead of repeating the explanatory paragraph as abstract topic tags.

### Existing and proposed components

Existing elements reused: the custom inline SVG language, cream section canvas, navy and peach palette, IBM Plex Mono, numbered section label, animated headline period, services-deck destination, and Calendly path.

Proposed elements: the dark summary panel, bordered service-ledger rows, one featured lead row, compact typical-deliverable tags, circular fit arrows, and a dedicated closing conversion band. These components are isolated to the mockup.

### Tokens and assets

Direction B introduces no new brand tokens or external assets. Cream `#F9E9D5` remains the canvas; navy `#192A51` highlights the lead service; deep navy `#101D3B` carries the closing conversion band; peach `#F29576` marks icons, action, and emphasis; and supporting grey `#AEB7CA` carries secondary copy on dark surfaces. The custom 48-by-48 inline SVG line drawings use `currentColor`, three-pixel strokes, and rounded caps and joins; they were authored for these mockups rather than downloaded from an external icon library. The Maintenance and Technical Support row uses a clean geometric toolbox mark—handle, case, center seam, and latch—to communicate ongoing technical care while matching the structured icon set. It replaces the wrench silhouette, which felt visually awkward beside the other marks. IBM Plex Mono remains the only typeface.

### Responsive behavior

- At desktop widths, each service is a four-part horizontal row: key, purpose, outcome tags, and fit arrow.
- Below 980 px, the introduction and summary stack, while the service rows preserve their horizontal ledger rhythm with narrower columns.
- Below 760 px, each row becomes a two-column composition with the key beside the copy and the outcomes beneath it.
- Below 560 px, every row becomes a single-column block. The number and icon share one compact line, outcome tags wrap naturally, and the fit arrow remains pinned to the upper-right edge.
- The closing conversion band becomes one column below 980 px, keeping the explanatory copy before the Book A Call action.

### Interaction and content states

- Light service rows receive a restrained peach tint and small inset shift on fine-pointer hover; the featured row remains visually stable.
- Fit arrows gain a peach fill and downward nudge on hover, reinforcing their in-page movement toward the conversation band.
- The services-deck link and Book A Call action use directional arrow motion consistent with the Hero.
- The headline period reuses the Hero-derived glow and eight-pixel pointer-hover burst. Reduced-motion preferences leave the period static and suppress row and arrow movement through the shared motion rules.
- All service fit links resolve to the visible project-fit band, while external deck and scheduling links open in a new tab with explicit accessible labels.

### Accessibility considerations

- The isolated mockup has one H1, five service H2s, and one closing-band H2 in logical DOM order.
- Icons are decorative and hidden from assistive technology; service names and descriptions carry the meaning independently.
- The highlighted service uses structure and scale in addition to color, and the outcome tags remain real list items.
- Keyboard focus uses the shared high-visibility outline. Production planning must still run final contrast checks and convert the isolated H1 to the appropriate heading level when composed beneath the homepage Hero.

### Assumptions, tradeoffs, and implementation implications

- Featuring MVP and Product Development assumes it should lead the commercial offer; this priority should be confirmed before implementation.
- The ledger reduces repeated card chrome and makes the offer feel more editorial, but rows carry more information across the horizontal axis and therefore require a larger responsive shift on phones.
- Typical-deliverable tags increase scan speed, but the word “typical” can still imply a standard scope. Each list remains provisional and should be validated against actual engagement practice before implementation.
- Consolidating UX/UI Design with Prototyping and combining AI with Workflow Automation reduces the earlier category overlap. Custom Web Applications remains distinct from MVP and Product Development by focusing on implementation rather than broader product ownership.
- The structure can map to a five-item Django service data set with one featured-item flag plus separate summary and conversation configurations.

## Case Studies section — shared foundation

### Relationship to the completed sections

The Case Studies artifact is isolated under [`mockups/case-studies/`](./mockups/case-studies/) and follows the completed Services section in the proposed buyer journey. It inherits the established navy, deep navy, cream, peach, and supporting-grey palette; IBM Plex Mono; numbered section labels; thin rules; direct external-evidence links; compact motion; visible focus treatment; and the confirmed Calendly scheduling path. Hero Version A and Services Direction B remain unchanged.

The user-supplied services-deck screenshot was treated as visual context, not as an instruction source or verification of the metrics shown inside it. Its editorial “selected work” framing, structured project summaries, dark rounded evidence surfaces, and prominent proof markers informed the hierarchy. Numeric performance claims from the deck remain omitted because the repository does not independently verify them.

Direction B now separates the work by relationship. The default **Client Work** tab presents four projects in the user-selected order:

1. Empowered Path Therapy.
2. Rubix AI.
3. LinkTag.
4. Change Food For Good.

The **Founder Product** tab contains cThink and labels it as a founder product rather than client work.

Repository material supports the project identities, existing roles and dates where noted, public destinations, and available project imagery. The EPT metadata uses the user-supplied `Full-Stack Software Engineer · 2024–2016` wording and keeps the complete role/date string on one line. Change Food For Good is supported by the existing experience entry for Technical Instructor, 2023–2024, and its complete role/date string also remains on one line. The user supplied the public PlantID application and source-repository destinations as additional evidence of the class project. A mockup-only capture of the live PlantID opening view replaces the earlier abstract illustration and shows both the plant photograph and the photo-identification workflow.

Problem statements, scope summaries, ownership language, and outcome framing remain provisional editorial interpretations. Verified client outcomes, client-approved wording, exact responsibilities, constraints, testimonials, and quantitative results must be confirmed before implementation.

## Case Studies Direction B — evidence trail

### Intent and rationale

Direction B is the completed Case Studies mockup structure, pending the separate design checkpoint. It makes the way Heriberto moves from a problem to tangible proof part of the evidence while clearly separating client delivery from founder-led product exploration. A sticky rail contains two tabs and a context-sensitive index. Each visible chapter repeats the same `Understand → Build → Show` structure, preserving a consistent operating-method signal without implying that cThink is client work.

### Page structure and visual hierarchy

1. A dark left rail holds the section label, “Follow the evidence trail.” headline, introduction, and two work-type tabs.
2. **Client Work** is selected by default and exposes an in-page index plus four chapters: Empowered Path Therapy, Rubix AI, LinkTag, and Change Food For Good.
3. **Founder Product** exposes a separate index and cThink chapter labeled `01 / Founder product`.
4. Each chapter begins with project identity and role, followed by a wide project visual.
5. Three bordered steps make the business need, build response, and available proof parallel across cases.
6. Native `<details>` elements expose a structured artifact grid. Each artifact has its own label, short description, and matching destination. The leading item in each view is open by default so collapsed and expanded states remain visible.
7. A bordered closing action asks whether the visitor has a product or workflow challenge, explains what to bring to the conversation, and uses the specific “Discuss Your Project” action.

### Existing and proposed components

Existing elements reused: the production wordmark; cThink, Rubix AI, LinkTag, and Empowered Path Therapy imagery; repository-supported names, roles, dates, destinations, and descriptions; deep-navy surfaces; cream and peach accents; IBM Plex Mono; section numbering; and the direct scheduling path.

Proposed elements: keyboard-accessible work-type tabs, context-sensitive proof indexes, equal case chapters, `Understand / Build / Show` evidence grammar, semantic native disclosures, a linked artifact grid, and the connected trail composition. The method language is a design proposal, not a verified description of a formal commercial process.

The artifact grid uses supported destinations: EPT has separate live-site and user-supplied EPT Figma-design links; Rubix AI has separate LinkedIn company-posts, Figma interface-design, Figma-prototype, and C4-document links; LinkTag has separate live-application and source-repository links; Change Food For Good has separate live-PlantID, PlantID-source, and organization-site links; and cThink has its source repository, whose project content includes the proof-of-concept narrative. Repository-supported role history is not presented as an artifact.

### Tokens and assets

Direction B uses deep navy `#101D3B` as the full section canvas, cream `#F9E9D5` as the case surface, peach `#F29576` as the connecting signal, and supporting grey `#AEB7CA` for secondary copy. It references the production `hr.svg`, `cThink.png`, `rubixAIhomepage.png`, and `EPT_home_page.png` assets without altering them. Change Food For Good uses the mockup-only `plantid-main.png` capture sourced from the user-supplied live PlantID page. LinkTag uses the mockup-only `assets/linktag-home-2026-09-03.jpg` screenshot captured from https://linktag.fly.dev/ on 2026-09-03. Its full 16:9 frame remains visible at every breakpoint, replacing the legacy animated Seeker screenshot without changing the production asset.

### Responsive behavior

- Above 1080 px, the section uses a two-column layout; the case index remains sticky while the evidence chapters scroll.
- At 1080 px and below, the rail becomes static, the selected index forms two columns above the cases, and the tab group retains a bounded width.
- Below 760 px, the two tabs and selected index become one column, project identity stacks while each role/date string remains unbroken on one line, the three evidence steps become vertical, artifact cards become one column, and the Discuss Your Project action becomes full width.
- Below 460 px, case padding and visual height reduce while maintaining readable copy and touch targets.
- Sticky behavior is enhancement only; section order and navigation remain understandable without it.
- Rubix AI’s four artifact cards form a balanced two-by-two grid above 760 px and stack into one column at 760 px and below. The order is LinkedIn updates, Interface design, Interactive prototype, and Software architecture. Other project artifact layouts are unchanged.

### Interaction and content states

- Client Work is the default state. Selecting Founder Product hides the client index and cases and reveals the cThink index and chapter; selecting Client Work reverses that state.
- Tab buttons expose `aria-selected`, `aria-controls`, and roving `tabindex`; Left, Right, Home, and End keys move and activate the selection.
- A direct `#case-cthink` URL opens the Founder Product state automatically. Index links move to their corresponding case using native anchors.
- Case images receive a restrained saturation and scale response on fine-pointer hover. The “evidence trail.” period reuses the Hero’s slow peach-and-cream glow and eight-pixel pointer-hover burst: its glyph disappears while the pixels disperse, then returns on pointer exit; touch devices keep the glow without requiring hover.
- Evidence notes use native `<details>` and `<summary>` so keyboard and no-script behavior remain available. The plus rotates into a close mark while open. Each artifact link opens its specific supporting destination rather than sharing one generic action slot.
- The leading evidence note in each tab is open by default; the remaining client notes are closed to demonstrate both disclosure states.
- Reduced-motion preferences remove index movement, image transforms, smooth scrolling, and the period glow/burst, leaving a restrained static period.

### Accessibility considerations

- The isolated artifact has one H1, one H2 per case, and H3s for the three repeated evidence steps.
- Both context-sensitive case indexes are labeled navigation landmarks; chapter anchors preserve the selected reading order.
- The tab list follows the ARIA tab pattern and provides pointer plus arrow-key operation. Panels and indexes use the native `hidden` state so inactive content leaves the accessibility tree.
- Native disclosures retain keyboard and assistive-technology semantics. Artifact groups use real lists, each artifact name and description precede its link, and all external destinations retain explicit new-tab behavior.
- Image alternatives describe what is visibly shown. The PlantID capture identifies the photograph and upload workflow, and the surrounding copy remains meaningful without it.
- Final production contrast should be formally checked, and the isolated H1 must be reconciled with the homepage heading hierarchy.

### Assumptions, tradeoffs, and implementation implications

- The repeated evidence grammar assumes all five items can support credible problem, response, and proof content. Weak or client-restricted evidence becomes conspicuous in this structure.
- Separating cThink protects the credibility of the client-work narrative and demonstrates founder initiative, but the product becomes less immediately visible than the default client cases.
- Tabs shorten the initial page and clarify classification, but they introduce a small JavaScript interaction that must preserve visible focus, URL behavior, and no-confusion fallback semantics during implementation.
- Native disclosure keeps each evidence note compact, though hiding details behind an action may reduce discovery. Opening the leading item in each view teaches the pattern.
- Change Food For Good now has a three-part evidence set: the live PlantID project, its public repository, and the workforce-program context. Exact instructional responsibilities and production-ready client wording should still be confirmed before implementation.
- Production can use separate bounded client-work and founder-product collections with structured problem, build, proof, evidence-label, evidence-URL, image-or-illustration, and order fields. The tab controller requires a small progressive-enhancement script in addition to semantic HTML and CSS.

## Preview and verification

Version A was revised after browser feedback to replace the improvised header lockup with the exact `hr.svg` production wordmark. Later feedback removed the temporary prototype banner, renamed Selected work to Case Studies, removed the numbered founder-led eyebrow and expectation microcopy, replaced the introduction with user-supplied founder copy, and confirmed the availability label without a marker. The latest revisions remove the visible future-section boundary and Contact navigation item, rename the Process navigation label to “Development Process,” give the Start a project navigation action the same peach-fill and restrained lift behavior as the Hero CTAs, set the headline to “From business problem to working software.” with orange underlined emphasis on “software,” restore a refined 200-millisecond underline-straightening interaction without line movement or resizing, adapt the original luminous orb into a slow peach-and-cream glow pulse on the period, add an eight-pixel hover burst that temporarily disperses the period, replace the project-brief action with “Book A Call,” a calendar icon, and the confirmed Calendly `coffee_chat` destination, increase navigation text, establish Principal Software Engineer as the founder title, change the capability rail to Idea, Prototype, MVP, Product, and Iterate under “Development Process,” use IBM Plex Mono for all mockup text, add 8 pixels between the headline and introduction, pair “One accountable partner” with “Digital products + practical automation” in the founder proof, and increase both proof statements to readable 0.75rem type with 1.45 line height.

- [`Version A desktop preview`](./mockups/hero/previews/hero-a-desktop.jpg) rendered at **1440 × 1168**.
- [`Version A mobile preview`](./mockups/hero/previews/hero-a-mobile.jpg) captured at **390 × 1363**.

The editable HTML remains the source of truth. The saved preview images document the preceding navigation revision and were not refreshed after the latest Case Studies, eyebrow, introduction, title, availability, microcopy, headline, CTA, boundary, typography, capability-stage, rail-label, spacing, navigation, motion, and founder-proof changes because browser automation was blocked from loading the local `file://` mockup. Static verification confirmed that the current HTML contains one H1, uses the user-supplied Principal Software Engineer wording, removes the eyebrow, expectation microcopy, visible future-section boundary, and Contact navigation item, uses Case Studies and Development Process consistently, exposes five matching desktop and mobile destinations, includes the calendar icon and confirmed Calendly URL within the “Book A Call” action, presents the five requested product stages under “Development Process,” loads IBM Plex Mono as its only text typeface, applies the increased headline-to-introduction spacing at desktop and mobile widths, shows “Digital products + practical automation” in the founder proof, includes the 200-millisecond underline interaction, and includes the period glow plus eight-pixel pointer-hover burst with touch and reduced-motion fallbacks. Open the editable mockup to review the current visual.

The selected Services direction was rendered through a temporary local server and visually inspected after revision:

- [`Direction B desktop preview`](./mockups/services/previews/services-b-desktop.jpg) at **1440 × 2100**.
- [`Direction B wide-phone preview`](./mockups/services/previews/services-b-mobile.jpg) at **500 × 3000**.
Visual inspection of Direction B confirmed the cream canvas, dark five-service summary panel, featured MVP and Product Development row, four ruled light ledger rows, compact wrapped Typical deliverables tags, and separate closing conversion band. The Maintenance and Technical Support row now uses a legible geometric toolbox icon at desktop and phone sizes. The closing band uses the collaborative solo-shop wording “Together, we’ll shape the next step,” removes the three redundant topic tags, and preserves intentional open space above the Book A Call action. The desktop layout preserves a clear key-to-description-to-deliverables reading path; the wide-phone layout stacks every row without horizontal overflow and retains the same service order, icons, links, and conversion path. CSS inspection covers the narrower 390 px breakpoint through the same single-column rules; the wide-phone preview is the saved browser artifact because the local headless browser enforces a minimum layout width near 500 px. The comparison workspace preserves this completed Services mockup beside the completed Hero.

The selected Case Studies Direction B was refreshed through the same temporary local server and visually inspected in both work-type states:

- [`Direction B Client Work desktop preview`](./mockups/case-studies/previews/case-studies-b-desktop.jpg) at **1440 × 4900**.
- [`Direction B Client Work wide-phone preview`](./mockups/case-studies/previews/case-studies-b-mobile.jpg) at **500 × 6100**.
- [`Direction B Founder Product desktop preview`](./mockups/case-studies/previews/case-studies-b-products-desktop.jpg) at **1440 × 1750**.

Direction B inspection confirmed the sticky desktop rail, distinct Client Work and Founder Product buttons, context-sensitive indexes, and readable three-column `Understand / Build / Show` steps. Client Work is the default view and presents Empowered Path Therapy, Rubix AI, LinkTag, and Change Food For Good in the requested order. EPT displays the user-supplied `Full-Stack Software Engineer · 2024–2016` metadata on one line, and `Technical Instructor · 2023–2024` also remains on one line for Change Food For Good. EPT’s open disclosure shows separate Live site and Interface design cards with matching destinations; the same grid supports Rubix AI’s four links, LinkTag’s two links, Change Food For Good’s live PlantID, PlantID-source, and organization-site links, and cThink’s source link. Repository-supported role history was removed from the visible artifact copy. The founder-product view presents only cThink with a simple `01 / Founder product` label. The closing band asks “Have a product or workflow challenge?”, explains that the call will clarify fit and a useful next step, and labels the action “Discuss Your Project.” The Change Food For Good chapter now uses a capture of the PlantID opening view and connects the Build and Show copy directly to the working class project. At 500 pixels, the rail becomes a static introduction, tabs and the selected index stack, artifact cards become a single column, client cases remain within the viewport without horizontal overflow, metadata remains unbroken, and the closing action becomes a single-column full-width composition. CSS inspection covers the narrower 460-pixel breakpoint; the saved phone artifact uses 500 pixels because that is the stable minimum width of the local headless renderer.

Static checks also confirmed one H1, four client H2s in the requested order, one founder-product H2, descriptive image alternatives or an accessible illustration label, `rel="noopener noreferrer"` on external new-tab links, visible focus rules, reduced-motion fallbacks, native disclosure behavior, ARIA tab relationships, and keyboard navigation for Left, Right, Home, and End. Direction A and Direction C remain removed. The remaining HTML/CSS files are the editable source of truth.

The latest Rubix AI artifact revision replaces the live-beta destination with the user-supplied LinkedIn company-posts URL and adds the user-supplied Figma interface-design URL. Link labels and Show copy now distinguish company context from design and technical evidence. Static checks cover the four links and responsive grid rules. Preview rendering for this revision was blocked by the browser’s local-file URL security policy; saved previews predate this revision and the editable HTML remains the source of truth.

The LinkTag screenshot replacement was visually inspected at its captured 1280 × 720 size: the public homepage shows its headline, sign-in/create-account navigation, primary action, and explicitly illustrative connections table. Static checks confirm the new local image reference and uncropped 16:9 responsive frame. Full-section previews remain stale; the previously observed local-file browser security restriction prevents re-rendering the mockup through that route.

## Next step

Run `turtle-design-checkpoint` next to review Direction B’s client-versus-product classification, the four-client hierarchy, tab behavior, evidence wording, and disclosure behavior while retaining the completed Hero Version A and Services Direction B. Selection for continued review does not approve implementation.
