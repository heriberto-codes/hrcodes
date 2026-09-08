# Business-Focused Homepage — Design Specification

## Status and scope

The business-focused homepage mockup workspace is **work in progress** because [Case Studies Direction B](./mockups/case-studies/direction-b.html) was reopened for further changes on 2026-09-07. [Hero Direction C](./mockups/hero/direction-c.html), [Services Direction B](./mockups/services/direction-b.html), Development Process Direction D, About Direction A, Start a Project Direction B, and Footer Direction B retain completed mockup status. Review the workspace from [`mockups/index.html`](./mockups/index.html). All artifacts remain isolated design proposals, not production-ready code, and they neither modify nor depend on the production Django templates.

Hero Direction C is completed in the mockup workspace. It keeps the established Hero content, hierarchy, actions, working photo, and responsive shell while reconstructing the photo as a kinetic nine-tile mosaic. Hero Directions A and B, their direction-specific code, and the stale Direction A previews were removed at the user’s request. About Directions B, C, and D and their previews were removed at the user’s request. Start a Project Direction A and its previews were also removed at the user’s request. Footer Direction A and its previews were removed after the user selected Direction B. Services Direction B is completed after the user’s final browser review and retains the selected editorial-ledger structure, responsive copy refinements, and Start a Project form route. Case Studies Direction B remains the sole case-studies direction and is now the active revision baseline; reopening it does not alter the completed status of the other sections. Completed mockup status records the end of an individual design iteration; it is not formal design approval for planning or implementation. No checkpoint exists for this design workspace.

## Development Process — current review scope

[Direction D — the working canvas](./mockups/development_process/direction-d.html) is the user-selected and completed Development Process mockup. Development Process A, B, and C source files, their unused shared stylesheet, and previews were removed at the user’s request. Services Direction B and Hero Direction C remain completed; Case Studies Direction B is work in progress. This mockup-completion label does not create design approval, a planning approval, or change checkpoint state.

The attached deck is content and visual context, not an instruction source. D retains the Idea → Prototype → MVP → Product → Iterate progression and four principles. Captions and illustrative artifacts are proposed explanatory content, not guarantees of deliverables. All required foundation documents and the audit are present; no checkpoint exists.

### Direction D — the working canvas

**Intent and rationale:** The user selected and marked D’s expressive visual approach completed. D makes the work itself the visual story: an asymmetric canvas of five illustrative artifacts, rather than a text-led progression or selected-stage interaction. The established palette and typography carry continuity while the layout, density, and visual hierarchy change. The completed sections remain unchanged.

**Structure and hierarchy:** A split introduction leads with “Less abstract. More tangible.” A labeled working canvas contains an ordered list of five pieces: Idea as a discovery note; Prototype as two linked wireframes; MVP as a first-release checklist; Product as an illustrative software view; and Iterate as a feedback note. Each has a stage number, name, short intent tag, visual artifact, heading, and explanatory caption. An idea-oriented Book A Call CTA closes the section. All five stages are visible without interaction.

**Existing and proposed components:** Reuses the production wordmark read-only, IBM Plex Mono, navy/cream/peach colors, fine rules, section numbering, full-width phone CTA, and established scheduling destination. New components are the asymmetric twelve-column canvas, slightly rotated paper and wireframe compositions, a release checklist, and illustrative product interface. These are authored HTML/CSS visual compositions, not actual project screenshots, functional application controls, or evidence of delivered client work. No production asset or code is modified.

**Tokens and assets:** The page uses deep navy `#101D3B`; Prototype and Iterate use navy `#192A51`; Idea uses peach `#F29576`; MVP uses cream `#F9E9D5`; Product introduces a related surface `#223557`. Body copy on light surfaces uses `#374662`; dark surfaces use `#AEB7CA`. Cards have restrained one-pixel borders; simulated paper and software artifacts carry small fixed rotations and shadows. Brand type remains consistent. Google Fonts has the same monospace fallback as the existing mockups. A dedicated `direction-d.css` keeps this styling isolated.

**Responsive behavior:** Above 1150px, the first row allocates four, five, and three columns to Idea, Prototype, and MVP; the second allocates seven and five to Product and Iterate. At 1150px and below, Idea/Prototype share a row, MVP/Product share the next, and Iterate spans the canvas. At 760px and below, all pieces form one column in semantic stage order; inner Product and Iterate layouts stack. Essential captions remain upright and readable while illustration widths adapt. Below 380px, padding and decorative type reduce. The CTA becomes full width and principles become a two-column list.

**Interactions and states:** The only actions are the skip link, comparison navigation, and scheduling link. The decorative artifacts contain no inputs or interactive buttons and are not hover-dependent. No JavaScript, tabs, carousel, loading, error, or empty state is required. Hover changes link/CTA color, while keyboard focus uses a visible outline. Both headline periods reuse the established Case Studies 2.4-second peach-and-cream glow. On hover-capable devices, each period independently disperses into eight pixels over 560ms and returns when the pointer leaves. The original cream and peach glyph colors are retained. Touch devices keep the glow; reduced-motion preferences disable the pulse, keep each glyph visible, and hide the particle layer. Decorative particles are excluded from the accessibility tree. Each of the five entire process cards now performs a single 320ms shake on hover entry: at most 3px horizontal movement, 2px upward movement, and 0.35 degrees of rotation, then returns to rest. Leaving and re-entering retriggers the effect; it does not loop while hovered. The transform leaves grid layout unchanged. This decorative motion runs only for hover-capable fine pointers with no reduced-motion preference; touch and reduced-motion users receive static cards. The illustrations retain their fixed rotations within each moving card. External scheduling announces its new-tab behavior.

**Accessibility:** One H1, an ordered list of five stage H2s, and H3 captions preserve the reading sequence. Illustrative compositions are hidden from assistive technology with `aria-hidden`; the adjacent headings and captions communicate the process without them. The genuine CTA has a comfortable touch target and visible focus. Homepage implementation must shift section headings beneath the page H1.

**Assumptions, tradeoffs, and implementation:** All artifacts and captions are proposed explanatory content, not guaranteed deliverables, validated outcomes, or a prescribed project scope. D is more expressive and visually concrete, but the artwork adds height on phones and favors short captions over detailed decision/outcome language. The canvas should be assessed beside existing sections for overall page density. The clarification line that described the visuals as “illustrative process artifacts” was mockup disclosure copy, not language from the Agile Manifesto; it was removed after it created ambiguity. A future Django include can render the five captions with local presentational markup; no framework or backend feature is needed. Selection still requires the design checkpoint.

**Revision after browser feedback:** Removed the decorative down-left arrow, moved the supporting heading and body higher beside the headline, removed the ambiguous illustrative-artifacts note, and removed the entire “The way we work” principles strip. The process now moves directly from the five-stage canvas to the closing CTA. A later refinement increases “Every step makes the next one clearer.” from 1.15rem to 1.35rem and its supporting paragraph from 0.85rem to 1rem on desktop, with proportional phone increases. The recurring stage-number badges and each card’s primary visual artifact or symbol are enlarged slightly: discovery paper, prototype wireframes and flow arrow, MVP release heading and checklist marks, Product window, and Iterate loop. Following review, the two MVP checkmarks and its third return-arrow symbol are increased again to 1.15rem with a consistent 25px symbol column so all three read clearly without shifting their labels.

**Preview and verification:** [D desktop](./mockups/previews/process-d-desktop.png) at 1440 × 1750 and [D wide phone](./mockups/previews/process-d-mobile.png) at 500 × 3200 were rendered through the local server and visually inspected. The desktop shows the intended asymmetric two-row canvas; phone presents all five stages in order, upright captions, and the full-width CTA without visible clipping. The refreshed previews also confirm the direct transition from the canvas to the CTA after removing the disclosure and principles content. A joined Product heading on phone was corrected by preserving whitespace around its desktop line break. Preview refreshed after the correction. Static checks cover semantic stage count and local references; narrower phone rendering and assistive-technology testing remain unverified. No Django tests apply to these isolated static artifacts.

## Hero — shared foundation

### Intent and rationale

The Hero should make Hroman Codes read as a software business within the first screen while preserving Heriberto Roman as the source of trust. The hierarchy therefore begins with the client constraint, names Hroman Codes as the partner, shows the founder alongside the promise, and offers one high-intent action plus one evaluation action.

This responds directly to the audit’s primary tension: the current Hero has useful business language, but the surrounding résumé cues and founder-first headline leave the commercial identity ambiguous. The proposed direction keeps the personality and existing visual system without leading with a name, job title, or “I build for the web.”

### Structure and visual hierarchy

1. A compact header uses the official Hroman Codes wordmark and buyer-oriented navigation: Services, Case Studies, Development Process, About, and Start a project. The scheduling action remains the primary contact path.
2. One semantic H1 connects the client’s business constraint to a concrete delivery outcome: “From business problem to working software.” The word “software” carries the peach emphasis and hand-drawn underline.
3. User-supplied supporting copy introduces Heriberto as Principal Software Engineer and founder of HROMAN CODES, LLC, then connects ideas and inefficient workflows to digital products, practical automation, and scalable software for small businesses, startups, and growing organizations.
4. “Book A Call,” paired with a calendar icon, is the primary action; “Review Services” supports prospects who want to understand the offer before scheduling.
5. A founder portrait and proof card establish direct collaboration and end-to-end ownership, use “Founder + Principal Software Engineer,” and provide the Hero-level About destination.

### Existing elements preserved

- Colors derived from production tokens: navy `#192A51`, cream `#F9E9D5`, peach `#F29576`, white, and a lightened supporting grey.
- IBM Plex Mono across headlines, navigation, body copy, controls, labels, and proof content to create one consistent brand voice. Hierarchy comes from weight, scale, spacing, and color rather than a second typeface.
- The exact production `hr.svg` wordmark used by the current desktop navbar. The founder image is now a mockup-local copy of the user-supplied `IMG_0943.JPG`, showing Heriberto working at a laptop and external monitor; the earlier `aboutMeImage.png` reference has been removed from this Hero.
- Rounded CTA borders, subtle rules, numbered labels, dark surfaces, orange accents, full-width mobile actions, the original Hero underline’s playful straightening behavior, and its luminous endpoint detail adapted to the headline period.
- Founder-led credibility within the first screen.

### Proposed components

- Business-oriented brand lockup and navigation labels.
- Client-problem H1 with a restrained hand-drawn underline accent.
- Scheduling CTA with an inline calendar icon as the primary conversion action.
- Founder proof composition combining portrait, role, availability state, the accountable-partner promise, and the focus on digital products and practical automation. The two proof statements use 0.75rem type with 1.45 line height so the credibility details remain readable rather than behaving like decorative microcopy.
- Native `<details>` mobile navigation that does not depend on third-party JavaScript.

### Tokens and assets

- `--navy` and `--navy-deep` provide the primary and layered dark surfaces.
- `--cream` is the main text color; `--peach` is reserved for emphasis and action.
- The production grey is lightened in the mockup to protect readability for normal-size copy. Production implementation should confirm exact contrast values before selecting a final token.
- IBM Plex Mono uses its available 700 weight, slightly relaxed display tracking, and fluid `clamp()` sizing for headlines; supporting copy retains a lighter monospaced cadence. An additional 8 pixels separates the headline and introduction at desktop and mobile sizes.
- The portrait area uses the local working photo, CSS-rendered mosaic tiles, grid lines, blend colors, and gradients rather than additional decorative image assets.

### Responsive behavior

- Desktop uses a two-column Hero: message first, founder proof second.
- Below 860 px, the Hero becomes a single-column sequence with message and CTAs before the portrait.
- Desktop navigation changes to a native mobile menu at the same breakpoint.
- Below 480 px, actions become full width, the headline scales fluidly, and proof facts stack.
- Essential content is not duplicated between breakpoints, preserving one logical heading hierarchy.

### Interaction and content states

- Hover states distinguish both Hero CTA priorities, while the header’s Start a project action uses the same peach fill and restrained two-pixel lift for consistent conversion affordance.
- Hovering the emphasized word “software” eases its underline from a two-degree tilt to straight over 200 milliseconds. The original 900-millisecond invitation delay is retained; after that pause, the visible letters now resolve more deliberately over 2.4 seconds into an original canvas-rendered field of peach and cream circular pixels and remain in that inviting state. On hover-capable fine pointers, particles within the pointer’s radius are displaced and spring back to their sampled letter positions as the pointer moves away. The user-supplied [Maria João Abrantes reference](https://www.mariajoaoabrantes.work) informs the interaction behavior, not its code or visual styling.
- The period after “software” carries a slow 2.4-second peach-and-cream glow pulse adapted from the current portfolio’s luminous orb. On pointer-hover devices, hovering the period makes the glyph disappear into an eight-pixel radial burst; it returns when the pointer leaves. Touch-only devices retain the glow without a hover-dependent effect, while reduced-motion preferences replace both animations with a static, restrained glow.
- The selected Direction C portrait behavior is documented below. The shared availability dot carries a restrained 2.8-second pulse, and none of the Hero motion communicates essential information.
- All links and the mobile-menu summary have a high-visibility keyboard focus state.
- The mobile menu preserves native `<details>` as its fallback and exposes the same navigation choices as desktop. A small progressive-enhancement controller keeps the panel mounted during a 260-millisecond close, combines clip, fade, and vertical motion on the panel, staggers the links on entry, morphs the hamburger into a close icon, updates the accessible open/close label, closes on outside pointer input or Escape, and returns keyboard focus after Escape.
- Anchor destinations are illustrative because this mockup covers only the Hero. About points to visible Hero content; Services, Case Studies, Development Process, and Contact retain nonvisual targets for the corresponding section mockups without displaying prototype boundary labels.
- “Book A Call” opens the confirmed `https://calendly.com/heriberto_codes/coffee_chat` scheduling destination in a new tab. Production implementation still needs confirmation of the meeting length, availability, timezone handling, and concise expectations for what the call covers.
- The mockup demonstrates the pre-scheduling state only. External scheduling, loading, error, confirmation, privacy, and follow-up states remain outside this Hero artifact.
- Reduced-motion preferences disable smooth scrolling, transitions, CTA lift transforms, the period pulse and pixel burst, automatic software-particle substitution, menu transitions, mosaic tile movement and hover expansion, and the availability pulse. The original “software” text remains visible in that mode.

### Accessibility considerations

- The Hero uses one H1 and a logical H2 for founder identity.
- The official wordmark has a concise accessible name inside the home link; the founder portrait has meaningful alternative text. “Software” remains real text in the heading while its canvas particle layer is decorative and hidden from assistive technology.
- Navigation landmarks are separately labeled for desktop and mobile.
- Focus treatment does not rely on color alone, actions meet comfortable touch-target sizing, and copy remains understandable without imagery or motion.
- The final palette requires a formal contrast check before production implementation.

### Assumptions and items requiring confirmation

- The primary conversion begins with a scheduled call through the user-confirmed Calendly `coffee_chat` destination rather than a project brief or email.
- Heriberto can promise one accountable partner.

The user-supplied audience statement, Principal Software Engineer title, all-IBM-Plex-Mono typography, “Accepting select projects” label, and working photo are treated as confirmed for this mockup. The remaining assumptions must be settled before implementation.

### Tradeoffs and implementation implications

- Leading with the business problem improves commercial clarity but reduces the immediate prominence of Heriberto’s name. The portrait and founder card intentionally restore that trust signal within the same screen.
- The portrait increases visual warmth and differentiation, but the mosaic treatment adds multiple composited layers and continuous transform animation. Production should optimize the source image and crop for responsive delivery, keep the motion restrained, and verify its cost on lower-powered mobile devices.
- The header is included to show the Hero’s real first-screen context. A future implementation must reconcile its labels and mobile behavior with the global navbar rather than introduce a second navigation component. The canvas interaction uses `requestAnimationFrame` only while hovered or settling and rebuilds when the word resizes; production should profile particle count and canvas work on representative devices.
- A direct scheduling CTA reduces friction but collects less qualification context than a project brief. Planning should decide what fit guidance appears before booking and confirm the scheduling workflow before implementation.
- The design can map to the existing server-rendered Hero include and global CSS conventions; it does not require a new frontend framework.

## Completed Hero Direction C — Kinetic mosaic

### Intent and rationale

Direction C treats the photograph as a system assembled from parts. Nine independently moving tiles reconstruct the complete workstation scene with alternating natural, navy, monochrome, and peach treatments. It is the most radical direction and uses composition—not glitch—to connect modular product development with the founder image.

### Structure and visual hierarchy

The surrounding Hero uses the shared foundation above. Inside the portrait, a muted complete image provides continuity behind a three-by-three grid. Each tile displays its corresponding region of the source photo, allowing the nine pieces to reconstruct the scene rather than repeat it. A `WORKING_VIEW / 09 TILES` readout labels the visual concept, while the founder card and availability message retain their established positions.

### Existing and proposed components

Existing elements include the shared content, navigation, working-photo asset, brand palette, founder proof card, actions, period motion, and responsive behavior. Proposed elements are the nine-piece reconstruction, alternating per-tile color treatments, small depth shadows, independent float vectors, responsive grid gap, and decorative mosaic readout. The semantic image remains present beneath the decorative tiles.

### Tokens and assets

Direction C uses the same local working photo and established tokens. Each tile uses a 300% background size with a unique background position to reconstruct one ninth of the photograph. Selected tiles use peach or navy blend colors; the central tile receives a stronger peach outline and depth shadow. No second photo file or external visual dependency is required.

### Responsive behavior

The mosaic is percentage-based and remains a three-by-three composition inside the portrait frame on desktop, tablet, and phone. The shared Hero still stacks below 860 pixels. Tile gaps reduce from seven to five pixels below 480 pixels so the image remains legible within the narrower frame, while the readout moves slightly inward.

### Interaction and content states

Each tile floats on a 7.2-second loop using its own direction and negative delay, keeping the image recognizable while preventing mechanical synchronization. Hovering the frame increases the tile spacing and halves the loop duration, creating a more dramatic “parts separating” response. The complete muted image beneath the tiles prevents open gaps from becoming empty holes. Direction C also carries the shared graceful mobile-menu transition and pointer-responsive “software” particle reconstruction.

### Accessibility considerations

The underlying semantic photo retains the descriptive alternative text. The nine reconstructive tiles and readout are `aria-hidden`, and no meaning depends on their color, movement, or separation. The headline particle canvas is also `aria-hidden` while the semantic word remains in the H1 even after its visual opacity transition. Reduced-motion preferences stop all tile movement, hover expansion, and headline particle substitution while preserving a coherent static mosaic and the original visible word. Direction C keeps the shared focus, heading, navigation, contrast, touch-target, Escape-key, and native-menu fallback behavior.

### Assumptions, tradeoffs, and implementation implications

The mosaic strongly communicates systems thinking and modular construction, but it intentionally fragments the human image and is less immediately personal than an untreated photograph. Nine background layers increase paint work and need real-device performance testing. A production version should consider reducing movement or tile count on low-power devices while preserving the static composition. Implementation remains local HTML/CSS with no framework or backend change. Direction C is completed as a mockup, not formally approved for planning or implementation.

## Services section — shared foundation

### Relationship to the preserved Hero

The Services artifact is isolated under [`mockups/services/`](./mockups/services/). Its context bar links back to the Hero workspace rather than reproducing it. In the eventual homepage composition, the Services section would follow the selected Hero direction directly and inherit its navy, cream, and peach palette; IBM Plex Mono typography; numbered labels; thin rules; compact interaction motion; and direct Book A Call path.

Direction B consolidates the offer into five user-requested service areas:

1. MVP and Product Development.
2. Custom Web Applications.
3. UX/UI Design and Prototyping.
4. AI and Workflow Automation.
5. Maintenance and Technical Support.

The repository does not confirm these as the final commercial service categories, promises, deliverables, engagement shapes, or qualification rules. The visible content note was removed by user request; this specification remains the source of truth for their provisional status. The mockup avoids price and timeline claims and labels the supporting lists as “Typical deliverables.”

## Services Direction B — completed editorial service ledger

### Intent and rationale

Direction B is the selected and completed Services mockup direction. Its editorial service ledger guides scanning and establishes hierarchy without repeating card chrome. The completed offer presentation consolidates seven overlapping categories into five: MVP and Product Development, Custom Web Applications, UX/UI Design and Prototyping, AI and Workflow Automation, and Maintenance and Technical Support.

### Page structure and visual hierarchy

1. The familiar `01 / Services` label, headline, and animated period preserve continuity with the selected Hero. The introduction now states the audience and full product lifecycle directly: “I help founders and small businesses plan, build, launch, and maintain digital products.”
2. A dark “At a glance” panel gives the right side of the introduction a stronger editorial role. It names the five-service scope, summarizes the accountable-partner promise, and contains the services-deck action.
3. A ruled, full-width service ledger replaces the card grid. Each row aligns its number and icon, service purpose, outcome tags, and fit arrow in a consistent horizontal reading path.
4. MVP and Product Development is the only dark featured row. Its increased height and color reversal establish the lead product-engagement capability without implying that every service has identical weight.
5. A separate deep-navy closing band contains the project-fit prompt and a Start a Project action leading to the homepage contact form. Its solo-shop voice reads “Together, we’ll shape the next step,” framing “together” as collaboration between Heriberto and the client. The action column intentionally leaves open space above the button instead of repeating the explanatory paragraph as abstract topic tags.

### Existing and proposed components

Existing elements reused: the custom inline SVG language, cream section canvas, navy and peach palette, IBM Plex Mono, numbered section label, animated headline period, services-deck destination, and selected Start a Project contact-form artifact.

Proposed elements: the dark summary panel, bordered service-ledger rows, one featured lead row, compact typical-deliverable tags, circular fit arrows, and a dedicated closing conversion band. These components are isolated to the mockup.

### Tokens and assets

Direction B introduces no new brand tokens or external assets. Cream `#F9E9D5` remains the canvas; navy `#192A51` highlights the lead service; deep navy `#101D3B` carries the closing conversion band; peach `#F29576` marks icons, action, and emphasis; and supporting grey `#AEB7CA` carries secondary copy on dark surfaces. The introductory sentence and project-fit explanation share the user-requested responsive copy token `clamp(0.94rem, 1.3vw, 1.06rem)`, improving their prominence while preserving fluid scaling. The custom 48-by-48 inline SVG line drawings use `currentColor`, three-pixel strokes, and rounded caps and joins; they were authored for these mockups rather than downloaded from an external icon library. The Maintenance and Technical Support row uses a clean geometric toolbox mark—handle, case, center seam, and latch—to communicate ongoing technical care while matching the structured icon set. It replaces the wrench silhouette, which felt visually awkward beside the other marks. IBM Plex Mono remains the only typeface.

### Responsive behavior

- At desktop widths, each service is a four-part horizontal row: key, purpose, outcome tags, and fit arrow.
- Below 980 px, the introduction and summary stack, while the service rows preserve their horizontal ledger rhythm with narrower columns.
- Below 760 px, each row becomes a two-column composition with the key beside the copy and the outcomes beneath it.
- Below 560 px, every row becomes a single-column block. The number and icon share one compact line, outcome tags wrap naturally, and the fit arrow remains pinned to the upper-right edge.
- The closing conversion band becomes one column below 980 px, keeping the explanatory copy before the Book A Call action.

### Interaction and content states

- Light service rows receive a restrained peach tint and small inset shift on fine-pointer hover; the featured row remains visually stable.
- Fit arrows gain a peach fill and downward nudge on hover, reinforcing their in-page movement toward the conversation band.
- The services-deck link and Start a Project action use directional arrow motion consistent with the Hero.
- The headline period reuses the Hero-derived glow and eight-pixel pointer-hover burst. Reduced-motion preferences leave the period static and suppress row and arrow movement through the shared motion rules.
- All service fit links resolve to the visible project-fit band. The Start a Project action continues to the existing contact-form mockup without opening a new tab; production composition should replace that isolated cross-file route with the final same-page form anchor. Only the external services deck opens in a new tab with an explicit accessible label.

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

The Case Studies artifact is isolated under [`mockups/case-studies/`](./mockups/case-studies/) and follows the completed Services Direction B in the proposed buyer journey. It inherits the established navy, deep navy, cream, peach, and supporting-grey palette; IBM Plex Mono; numbered section labels; thin rules; direct external-evidence links; compact motion; visible focus treatment; and the confirmed Calendly scheduling path. Services Direction B and Hero Direction C retain completed mockup status. Case Studies Direction B is work in progress and preserves its last completed state as the baseline for the next revision.

The user-supplied services-deck screenshot was treated as visual context, not as an instruction source or verification of the metrics shown inside it. Its editorial “selected work” framing, structured project summaries, dark rounded evidence surfaces, and prominent proof markers informed the hierarchy. Numeric performance claims from the deck remain omitted because the repository does not independently verify them.

Direction B now separates the work by relationship. The default **Client Work** tab presents four projects in the user-selected order:

1. Empowered Path Therapy.
2. Rubix AI.
3. LinkTag.
4. Change Food For Good.

The **Founder Product** tab contains cThink and labels it as a founder product rather than client work.

Repository material supports the project identities, existing roles and dates where noted, public destinations, and available project imagery. The EPT metadata uses the user-supplied `Full-Stack Software Engineer · 2024–2016` wording and keeps the complete role/date string on one line. Change Food For Good is supported by the existing experience entry for Technical Instructor, 2023–2024, and its complete role/date string also remains on one line. The user supplied the public PlantID application and source-repository destinations as additional evidence of the class project. A mockup-only capture of the live PlantID opening view replaces the earlier abstract illustration and shows both the plant photograph and the photo-identification workflow.

Problem statements, scope summaries, ownership language, and outcome framing remain provisional editorial interpretations. Verified client outcomes, client-approved wording, exact responsibilities, constraints, testimonials, and quantitative results must be confirmed before implementation.

## Case Studies Direction B — work-in-progress evidence trail

### Intent and rationale

Direction B is the active Case Studies mockup structure and revision baseline. Its previous completed status was reopened at the user’s request before a design checkpoint, so the existing hierarchy and behavior below remain documented but may change during this new iteration. It makes the way Heriberto moves from a problem to tangible proof part of the evidence while clearly separating client delivery from founder-led product exploration. A sticky rail contains two tabs and a context-sensitive index. Each visible chapter repeats the same `Understand → Build → Show` structure, preserving a consistent operating-method signal without implying that cThink is client work.

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

## Development Process preview and verification

The selected D retains its [desktop preview](./mockups/previews/process-d-desktop.png) and [wide-phone preview](./mockups/previews/process-d-mobile.png). These previews are refreshed for the headline-period revision. Static checks confirm two independent period wrappers with eight decorative pixels each, hover-capable pointer treatment, and reduced-motion fallbacks. Animation behavior is reused from the established Case Studies CSS; still previews do not demonstrate the full animation cycle. Removed Development Process directions have no remaining workspace navigation or asset dependencies. The later card-shake revision was statically checked for its five-card selector, single-run duration, transform-only keyframes, and pointer/reduced-motion guard. Existing still previews remain representative of the resting layout; the new hover cycle has not been captured or browser-verified.

## Preview and verification — section workspace

The [Business-Focused Homepage Workspace](./mockups/index.html) remains a historical snapshot of the prior completed iteration. This specification is the current source of truth for workflow state: Case Studies Direction B and the overall workspace are work in progress, while the other preserved sections retain completed mockup status. This status-only revision does not alter any layout or saved preview.

The Hero foundation was revised after browser feedback to use the exact `hr.svg` production wordmark; rename Selected work to Case Studies and Process to Development Process; remove the temporary banner, founder eyebrow, expectation microcopy, visible future-section boundary, Contact navigation item, and Development Process rail; replace the introduction with user-supplied founder copy; rename the secondary action to “Review Services”; and replace the prior portrait with the user-supplied working photo. The shared Hero also preserves the user-confirmed availability label, Principal Software Engineer title, all-IBM-Plex-Mono typography, “Book A Call” action, confirmed Calendly `coffee_chat` destination, founder proof, 200-millisecond underline interaction, and reduced-motion-safe period glow and pixel burst.

[Direction C](./mockups/hero/direction-c.html) is the editable visual source of truth. It does not have a rendered preview because the in-app browser security policy blocks loading the local `file://` mockup for automated capture. The supplied 1080 × 1080 JPEG was inspected directly and copied into the isolated Hero assets. Static verification covers one H1; the expected Hero copy and destinations; the descriptive semantic image; nine uniquely positioned, decorative `aria-hidden` mosaic tiles; the `WORKING_VIEW / 09 TILES` readout; responsive gaps; independent animation delays; local-only asset references; and static reduced-motion reconstruction. The final interaction revision adds valid isolated JavaScript for the native-details menu transition and semantic-text-preserving headline particle field, including its restored 900-millisecond invitation delay, slower 2.4-second automatic reveal, persistent particle state, spring return, Escape, outside-pointer, resize, fine-pointer, touch, and reduced-motion guards. Directions A and B, their direction-specific code, and the stale Direction A previews were removed at the user’s request. The user completed this Hero mockup after reviewing it in the local browser; formal checkpoint review remains separate.

The selected Services direction was rendered through a temporary local server and visually inspected after revision:

- [`Direction B desktop preview`](./mockups/services/previews/services-b-desktop.jpg) at **1440 × 2100**.
- [`Direction B wide-phone preview`](./mockups/services/previews/services-b-mobile.jpg) at **500 × 3000**.
Visual inspection of Direction B confirmed the cream canvas, dark five-service summary panel, featured MVP and Product Development row, four ruled light ledger rows, compact wrapped Typical deliverables tags, and separate closing conversion band. The Maintenance and Technical Support row now uses a legible geometric toolbox icon at desktop and phone sizes. The closing band uses the collaborative solo-shop wording “Together, we’ll shape the next step,” removes the three redundant topic tags, and preserves intentional open space above the Start a Project action. The desktop layout preserves a clear key-to-description-to-deliverables reading path; the wide-phone layout stacks every row without horizontal overflow and retains the same service order, icons, links, and conversion path. The final revisions apply `clamp(0.94rem, 1.3vw, 1.06rem)` to the introductory sentence and project-fit explanation and route the closing action to the existing Start a Project contact-form artifact in response to browser comments. The revised project-fit copy was visually checked in Safari at the current desktop viewport and remained readable without clipping; the final top-of-page capture was interrupted when browser focus changed. Static inspection confirms both copy selectors use the same clamp, the CTA has no external-tab attributes, its accessible label identifies the contact form, and its destination resolves to the existing `#project-b` form page. CSS inspection covers the narrower 390 px breakpoint through the existing single-column rules. The saved desktop and wide-phone previews predate these final refinements; the completed editable HTML and CSS are the current source of truth. The user marked Services Direction B completed after browser review. The comparison workspace preserves this completed Services direction beside the completed Hero.

The selected Case Studies Direction B was refreshed through the same temporary local server and visually inspected in both work-type states:

- [`Direction B Client Work desktop preview`](./mockups/case-studies/previews/case-studies-b-desktop.jpg) at **1440 × 4900**.
- [`Direction B Client Work wide-phone preview`](./mockups/case-studies/previews/case-studies-b-mobile.jpg) at **500 × 6100**.
- [`Direction B Founder Product desktop preview`](./mockups/case-studies/previews/case-studies-b-products-desktop.jpg) at **1440 × 1750**.

Direction B inspection confirmed the sticky desktop rail, distinct Client Work and Founder Product buttons, context-sensitive indexes, and readable three-column `Understand / Build / Show` steps. Client Work is the default view and presents Empowered Path Therapy, Rubix AI, LinkTag, and Change Food For Good in the requested order. EPT displays the user-supplied `Full-Stack Software Engineer · 2024–2016` metadata on one line, and `Technical Instructor · 2023–2024` also remains on one line for Change Food For Good. EPT’s open disclosure shows separate Live site and Interface design cards with matching destinations; the same grid supports Rubix AI’s four links, LinkTag’s two links, Change Food For Good’s live PlantID, PlantID-source, and organization-site links, and cThink’s source link. Repository-supported role history was removed from the visible artifact copy. The founder-product view presents only cThink with a simple `01 / Founder product` label. The closing band asks “Have a product or workflow challenge?”, explains that the call will clarify fit and a useful next step, and labels the action “Discuss Your Project.” The Change Food For Good chapter now uses a capture of the PlantID opening view and connects the Build and Show copy directly to the working class project. At 500 pixels, the rail becomes a static introduction, tabs and the selected index stack, artifact cards become a single column, client cases remain within the viewport without horizontal overflow, metadata remains unbroken, and the closing action becomes a single-column full-width composition. CSS inspection covers the narrower 460-pixel breakpoint; the saved phone artifact uses 500 pixels because that is the stable minimum width of the local headless renderer.

Static checks also confirmed one H1, four client H2s in the requested order, one founder-product H2, descriptive image alternatives or an accessible illustration label, `rel="noopener noreferrer"` on external new-tab links, visible focus rules, reduced-motion fallbacks, native disclosure behavior, ARIA tab relationships, and keyboard navigation for Left, Right, Home, and End. Direction A and Direction C remain removed. The remaining HTML/CSS files are the editable source of truth.

The latest Rubix AI artifact revision replaces the live-beta destination with the user-supplied LinkedIn company-posts URL and adds the user-supplied Figma interface-design URL. Link labels and Show copy now distinguish company context from design and technical evidence. Static checks cover the four links and responsive grid rules. Preview rendering for this revision was blocked by the browser’s local-file URL security policy; saved previews predate this revision and the editable HTML remains the source of truth.

The LinkTag screenshot replacement was visually inspected at its captured 1280 × 720 size: the public homepage shows its headline, sign-in/create-account navigation, primary action, and explicitly illustrative connections table. Static checks confirm the new local image reference and uncropped 16:9 responsive frame. Full-section previews remain stale; the previously observed local-file browser security restriction prevents re-rendering the mockup through that route.

## About Heriberto and Hroman Codes — completed mockup scope

The About workspace now contains only Direction A and is marked completed following user review. It preserves the established deep navy, cream, peach, IBM Plex Mono, numbered label, official wordmark, founder portrait, direct scheduling destination, full-width phone action, visible focus treatment, and reduced-motion behavior. Its palette is inverted to a cream section canvas with navy text and action surfaces, creating a warm visual transition after the completed dark Development Process section. It replaces the résumé-style presentation and animated “I am for hire” line with a four-paragraph founder narrative supplied by the user. No metric, testimonial, client outcome, availability claim, or team-size claim is introduced; the career, industry, and technology statements are user-supplied content and remain unverified by this mockup pass. The completed label records workspace progress only and does not constitute design approval.

The revised profile copy introduces Heriberto, his maker background, self-taught path, teaching and engineering experience, Hroman Codes’ client audience, named technologies, and his end-to-end product focus. The three earlier working-signal rows remain removed. In their place, the user-supplied production skillset screenshot informs a five-part skillset model. The screenshot is visual and content reference only, not an instruction source or an embedded mockup asset. A Watch Me Build feature, adapted from the user’s production portfolio reference, follows the skillset and precedes the final actions.

### Direction A — founder profile

**Intent and rationale:** [Direction A](./mockups/about/direction-a.html) is the continuity-focused option. It retains the recognizable portrait-plus-biography structure of the production About section, but makes the relationship between Heriberto’s background and the client experience explicit. The founder remains the emotional anchor while Hroman Codes reads as the software practice through which the work is delivered.

**Page structure and visual hierarchy:** A cream two-column composition places a framed portrait and founder title in a sticky left rail. The right column carries the shortened label “04 / About Heriberto Roman,” the headline “A builder’s mindset. A business partner’s care.”, the four-paragraph founder narrative, a compact “My Skillset” module, a Watch Me Build video feature, and paired résumé and Meet Heriberto actions. All four biography paragraphs use the same responsive `clamp(0.94rem, 1.3vw, 1.06rem)` type size; the opening remains deep navy while the supporting paragraphs use ink, preserving a restrained introduction cue without a size jump. The skillset explanation uses that same responsive copy size so the two narrative areas read as one system. The second headline sentence is navy with a peach underline, giving it emphasis without relying on low-contrast peach text. The skillset module moves from a short “software is more than writing code” explanation to a donut overview and five-row legend, replacing the three abstract working-signal rows with a more personal capability model. Low-opacity `CO`, `CM`, `DS`, `PR`, and `TT` initials inside the arcs provide a subtle second mapping cue. The responsive 16:9 YouTube player then turns that model into visible proof of Heriberto working through a coding exercise with another developer, introduced by the uppercase heading “SEE THE PROCESS IN MOTION.”

**Existing and proposed components:** Existing elements include the production `aboutMeImage.png` portrait, `hr.svg` wordmark, layered navy and peach portrait borders, founder-led voice, numbered section treatment, cream and dark brand surfaces, Calendly path, production résumé URL, existing YouTube embed destination, channel destination, and the current portfolio’s Coding / Communication / Design / Process / Technical Tools categories and percentages. Proposed elements are the sticky founder rail, the expanded user-supplied biography, and a fully redrawn semantic skillset figure with five independently interactive SVG arcs and a text legend. The Watch Me Build area now uses the existing video as an inline iframe rather than a poster link, allowing playback without leaving the homepage when served normally. The skillset screenshot itself is not copied into the artifact. The review header remains deep navy so the official cream wordmark stays legible; the About canvas below it is cream. The redundant business-identity footer text remains removed, leaving two direct actions after the video feature.

**Tokens and assets:** The canvas uses cream `#F9E9D5`, with deep navy `#101D3B` primary text and CTA, navy `#192A51` headline emphasis, ink `#293754` supporting copy, peach `#F29576` for the portrait field and decorative emphasis, and translucent navy rules. The donut stays within this system and introduces only two related data-visualization shades: muted blue `#6378A5` and deep peach `#C65F45`. The arc initials use the established light/dark pair at 48% resting opacity, rising to 85% only with the matching segment interaction. Biography copy and the skillset explanation share the responsive `clamp(0.94rem, 1.3vw, 1.06rem)` token. Both orange section kickers use 0.82rem type so “How I Build” and “Watch Me Build” remain legible without competing with their headings. Small copy does not use peach on cream because that pairing does not provide sufficient text contrast. IBM Plex Mono supplies all type. The existing portrait is shown with a reversible grayscale treatment and the production-style offset border construction. The iframe reuses the current production portfolio’s standard YouTube embed URL and video ID; no new runtime library is introduced.

**Responsive behavior:** At desktop widths, the portrait remains sticky while the longer story column scrolls; the skillset donut and legend share a row. At 1000 pixels and below, the skillset header, donut, legend, Watch Me Build header, and action buttons stack, and both actions fill the available story-column width for tablet and phone layouts. At 760 pixels and below, semantic visual order becomes label, headline, portrait, business introduction, skillset, video feature, and actions; sticky behavior is removed and the portrait height is fluidly bounded. The donut reduces again below 430 pixels, while the video remains 16:9. No duplicate desktop/mobile content is used.

**Interaction and content states:** The portrait shifts four pixels and returns to color on fine-pointer hover. Hovering or keyboard-focusing any donut segment moves that segment 5–6 pixels outward, adds a restrained drop shadow, increases its subtle initial from 48% to 85% opacity, and fills the corresponding label/percentage row with the same category color. Hovering a legend row triggers the matching segment lift, making the relationship work in both directions. Focus increases the active arc’s stroke width, so the state is not color-only; reduced-motion removes segment movement and transitions while retaining the row color connection. The iframe exposes the native YouTube play, pause, seek, captions, volume, fullscreen, and playback states without a custom controller. The primary CTA changes from deep navy to peach, while the outlined résumé action reverses to deep navy. Both headline periods reuse the completed sections’ 2.4-second glow and eight-pixel radial burst on fine-pointer hover. Because this About canvas is cream, alternating burst pixels use peach and deep navy instead of peach and cream so every particle remains visible. Touch devices retain the ambient glow without requiring hover; reduced-motion preferences remove the pulse and particles while leaving each period visible. Channel and Meet Heriberto links open their existing external destinations in new tabs and announce that behavior to assistive technology. The résumé action references the existing production PDF and visually represents a download; final implementation must verify the remote host’s download response. The section has no form, empty, success, tab, or disclosure state; YouTube owns the player’s loading and error states.

**Accessibility considerations:** The artifact contains one H1, separate H2s for skillset and video, a meaningful portrait alternative, visible focus, a skip link, comfortable action sizing, and a reading order that matches the mobile visual order. Each SVG segment is a focusable link with a category-and-percentage accessible name; the visible semantic list and hidden figcaption repeat the complete data without relying on color, initials, or pointer interaction. The arc initials are marked `aria-hidden` because they duplicate the accessible names. The iframe has a descriptive title, supports fullscreen, and retains native YouTube keyboard and caption controls. Decorative headline particles are excluded from the accessibility tree, and the visible period glyphs remain real text. Deep navy and ink provide strong text contrast on cream. Peach is limited to nonessential accent roles. A formal contrast audit and reconciliation with the homepage’s single H1 remain implementation requirements.

**Assumptions, tradeoffs, and implementation implications:** Direction A assumes the founder profile, broad skillset, and real build footage are useful trust devices. The percentages are reused from the user-supplied production portfolio and treated as a self-described balance of attention, not measured proficiency, client outcomes, or a contractual allocation of project time. The model adds personality but requires that visitors interpret an abstract percentage framework; the connected legend interaction makes that mapping explicit. Sticky positioning is enhancement-only. The inline iframe keeps playback on the homepage as requested, but adds third-party page weight, privacy, network, and availability considerations; lazy loading limits initial network work but does not eliminate those costs. A future Django include needs semantic template markup and CSS, with no backend, custom player JavaScript, chart library, or new framework required.

**Preview and verification:** [Desktop preview](./mockups/about/previews/about-a-desktop.png) was refreshed at 1440 × 2700, [tablet preview](./mockups/about/previews/about-a-tablet.png) at 900 × 3200, and [wide-phone preview](./mockups/about/previews/about-a-mobile.png) at 500 × 4200 after applying the shared responsive copy token to the biography and skillset explanation. All three were visually inspected for the cream-to-navy header transition, portrait crop, headline underline wrapping, consistent four-paragraph biography typography, skillset hierarchy, unique subtle initial placement, donut/legend correspondence, 16:9 player sizing, paired-action hierarchy, text contrast, content order, and horizontal overflow. Tablet and phone show full-width stacked actions and a stacked video header; desktop retains the compact side-by-side action pair. The rendered section remains readable and unclipped at all three sizes. The saved previews show YouTube Error 153 because the mockup is rendered directly from `file://`, which cannot send the HTTP referrer YouTube now requires; this is a local artifact limitation rather than the proposed homepage state, and the user-supplied production screenshot already demonstrates this video playing from the served site. Static inspection confirmed the iframe source/title/permissions, five focusable SVG segments, five `aria-hidden` initial labels, matching category IDs, bidirectional `:has()` hover/focus selectors, and reduced-motion overrides. Still previews do not demonstrate the interaction cycles. The in-app browser’s local-file security policy prevented a second automated live hover capture, so chart motion was verified from the editable CSS source rather than by bypassing that restriction.

## Start a Project form section — completed mockup scope

The Start a Project workspace now contains only the user-selected and completed [Direction B](./mockups/start-a-project/direction-b.html). It continues the buyer journey after About and uses `05 / Start a Project`, reflecting the preserved Services, Case Studies, Development Process, and About sequence. It responds to the audit’s conversion finding by capturing enough business context to evaluate fit while preserving a direct Calendly path for visitors ready to talk. Direction A and its two previews were removed at the user’s request; mockup completion remains pending formal design checkpoint approval.

The service names come from the completed Services Direction B. Timing choices, project-stage language, review sequence, field requirements, success messages, and qualification structure remain design proposals because the repository does not define an intake workflow, capacity, response time, budget floor, CRM, email destination, privacy policy, or follow-up contract. The selected direction does not ask for a budget: the audit identifies pricing and project-size thresholds as unknown, so introducing a financial qualifier would imply a business rule that has not been supplied. The form cautions against sending passwords or sensitive customer data.

The prototype demonstrates client-side validation and confirmation states without transmitting or persisting any data. Production implementation must define a secure server-side submission path, CSRF handling, validation, spam controls, privacy copy, notification ownership, failure handling, data retention, and analytics before the form can be considered functional.

### Direction B — three-step brief builder

**Intent and rationale:** [Direction B](./mockups/start-a-project/direction-b.html) is the user-selected and completed mockup option, pending formal checkpoint approval. It reduces the number of decisions shown at once by splitting the intake into Challenge, Context, and Connection. A live “project signal” summary turns the visitor’s answers into an emerging brief and reinforces that business context—not a prewritten technical specification—is the useful starting point.

**Page structure and visual hierarchy:** A cream grid canvas begins with the numbered label, “Build the brief. One decision at a time.” headline, and a compact framing statement. The main builder pairs a deep-navy summary rail with a paper-colored form panel. The summary begins with only the “Your project signal” label; the redundant `01—03` corner marker has been removed. Step 1 presents six work-area cards, including “Not sure yet.” Step 2 captures current stage and the desired business outcome. Step 3 gathers identity, optional company and timing, optional supporting context, and data-use confirmation. A three-part progress control exposes the current position and enables completed steps for review. The final success state replaces the form and progress control but keeps the surrounding summary visible.

**Existing and proposed components:** Direction B reuses the established wordmark, palette, IBM Plex Mono, section numbering, five service names, direct scheduling destination, and action language from the completed homepage mockups. Proposed components are the progressive three-step form, selectable service cards, project-signal definition list, enabled-step navigation, text summary truncation, back/continue controls, and resettable confirmation state. The faint 32-pixel grid extends the completed Development Process canvas language without reusing its illustrative cards.

**Tokens and assets:** Cream `#F9E9D5` becomes the primary canvas, deep navy `#101D3B` the summary rail, paper `#FFF9F0` the active form surface, navy `#192A51` selected cards, and peach `#F29576` the progress and action signal. Deep peach is reserved for small text on light backgrounds. The heading’s two periods now reuse the completed sections’ 2.4-second navy-and-peach glow plus eight-pixel hover burst. The user-selected framing paragraph and summary-principle copy both use `clamp(0.94rem, 1.3vw, 1.06rem)`. Error red `#A83B36` and success green `#2E6C59` remain proposed functional colors, while yellow `#FFD26A` carries keyboard focus. Direction B introduces no new image or external runtime dependency beyond the existing wordmark and optional web-font request.

**Responsive behavior:** Above 1020 pixels, the summary and builder form a side-by-side workspace. Below 1020 pixels, the summary moves above the form; its three live values form a horizontal row while the framing note and call path remain readable. At 700 pixels and below, the summary values, service cards, stage choices, connection fields, and actions become one column. Step labels stay visible in a compact three-column progress row, and actions become full width. Content remains in one DOM sequence, with inactive steps hidden rather than duplicated.

**Interaction and content states:** The first step is the default state. Visitors cannot jump ahead until preceding required fields are valid, but can revisit unlocked steps. Selecting a service or stage updates the `aria-live` summary; typing the project goal adds a shortened summary without replacing the full input. Continue validates only the current step and moves focus context to the next panel. Back preserves answers. Final submit validates the complete form, then exposes the confirmation and reset control. Radio cards use structure, inset rules, and written values in addition to color. Each headline period carries a slow ambient glow; on hover-capable fine pointers, the glyph disperses into eight peach-and-navy pixels and returns on pointer exit. Touch users retain the glow without a hover dependency, and reduced-motion preferences replace the animation with a static glow. Disabled, active, hover, focus, invalid, success, and reduced-motion states are present. JavaScript is progressive prototype behavior only; no submission leaves the page.

**Accessibility considerations:** Each step is a labeled section inside one form, choice groups use native radios and fieldsets, progress is a labeled navigation region, disabled future steps cannot receive focus, and the current progress button exposes `aria-current="step"`. Live summary values use a polite announcement region. All errors are written, required controls remain native, and external scheduling announces its new-tab behavior. Production should add a robust step-status announcement, connect each error to its control, decide whether a stepper or grouped fieldsets best serves no-JavaScript users, preserve entered data after server errors, and test the complete flow with screen readers and keyboard-only navigation.

**Assumptions, tradeoffs, and implementation implications:** The staged approach lowers visible cognitive load but hides the total form length and introduces JavaScript state, validation sequencing, focus management, browser-history considerations, and more test cases. The live summary may help a visitor feel progress, but it duplicates answer content and must remain concise. “Not sure yet” prevents the service taxonomy from becoming a qualification barrier. An implementation could remain server-rendered with a small progressive-enhancement controller, but the no-script fallback should expose all fieldsets rather than leave later steps inaccessible. Backend, privacy, spam-control, notification, error, and retention decisions remain implementation prerequisites.

**Preview and verification:** [Desktop preview](./mockups/start-a-project/previews/start-project-b-desktop.png) at **1440 × 1700** and [wide-phone preview](./mockups/start-a-project/previews/start-project-b-mobile.png) at **500 × 2400** document the completed direction. They were refreshed and visually inspected after increasing the two requested copy sizes, adding the paired headline-period motion, and removing the `01—03` summary-corner marker. The desktop framing copy remains readable beside the headline, and the larger summary-principle copy stays within the dark rail. The phone view stacks cleanly without horizontal overflow; a minimal phone-only headline adjustment keeps the first period attached to “brief.” Saved previews show the resting first-step state; the glow and burst cycles are not fully represented in still images. Live browser testing selected a work area, advanced to Context, updated the project-signal summary, entered a project goal, advanced to Connection, exposed all three written required-field errors, moved focus to the first invalid field, reached the confirmation state with fictional test values, and reset the flow successfully. Static checks confirmed valid JavaScript syntax, one H1, native form controls and fieldsets, two period wrappers with eight decorative pixels each, hover and reduced-motion rules, local preview references, removal of the alternate direction’s files and links, absence of the removed corner marker and its styling, and no production-code changes. The completed label records mockup-workspace progress only and does not constitute formal design approval.

## Footer section — completed mockup scope

The Footer workspace is complete and contains only the user-selected [Direction B](./mockups/footer/direction-b.html). Direction A source and preview files were removed at the user’s request. Direction B follows the completed `05 / Start a Project` section and shows a short mockup-only transition edge so its relationship to that section’s cream grid canvas can be judged. The transition edge is context, not an additional homepage section. The direction preserves the production footer’s verified copyright, founder credit, email, GitHub, LinkedIn, and YouTube destinations while replacing the current centered sentence-and-icon treatment with a business-oriented close.

The footer does not introduce a newsletter, testimonial, client logo, response-time promise, office location, privacy route, or other unsupported destination. The prototype’s internal journey links open the corresponding preserved mockup sections; implementation must resolve them to the final homepage IDs. `Accepting select projects` is reused by the completed Hero Direction C. The isolated artifact uses one H1 so it has a navigable outline; production composition must demote that heading beneath the homepage H1. Completed mockup status records workspace progress only and does not constitute formal design approval.

### Direction B — closing signal

**Intent and rationale:** [Direction B](./mockups/footer/direction-b.html) is the user-selected and completed Footer mockup, pending formal checkpoint approval. It treats the footer as the last memorable brand moment: the oversized “Make the next version useful.” line closes the product-development story, while a peach project card and structured route board preserve practical next steps. The composition draws from the Development Process working canvas and Start a Project grid without repeating either section literally.

**Page structure and visual hierarchy:** A cream handoff strip condenses the completed brief-builder sequence as `Challenge → Context → Connection`. The first dark footer band pairs the oversized closing statement with a slightly rotated peach signal card containing a fit-oriented sentence, availability status, Start a Project action, and Book A Call action. The second band becomes a cream route board: an inset navy brand panel, a numbered five-row homepage index, and written social links. A compact dark baseline carries copyright, founder credit, and a return-to-beginning action.

**Existing and proposed components:** Existing elements include the wordmark, palette, IBM Plex Mono, numbered buyer journey, 32-pixel grid, underlined display phrase, glowing period motif, availability copy, verified internal and external destinations, copyright, and founder credit. Proposed elements are the handoff strip, oversized closing line, angled signal card, numbered route board, and wide brand panel. The signal card is editorial navigation, not a form submission state or guarantee that an inquiry has been received.

**Tokens and assets:** Direction B uses deep navy `#101D3B` for the closing canvas, navy `#192A51` for the brand panel, cream `#F9E9D5` for text and the route board, peach `#F29576` for the project card and display emphasis, supporting grey `#AEB7CA`, and focus yellow `#FFD26A`. A related navy `#223557` forms the signal-card offset shadow. The official wordmark remains the only image. The grid, one-pixel rules, uppercase micro-labels, underline, and expressive period reuse established mockup details.

**Responsive behavior:** Above 1060 pixels, the closing message and project card share one row, and the route board uses three columns. Below 1060 pixels, the signal card drops below the message; the route board becomes two columns with social links spanning the width. At 700 pixels and below, the handoff strip, closing composition, route board, social group, and legal baseline all become one column. The card loses its rotation on phones, actions remain at least 52 pixels tall, the oversized line scales fluidly, and no essential content is removed.

**Interaction and content states:** The period carries the established 2.4-second ambient glow. On hover-capable fine pointers, hovering the period pauses the glow, hides the glyph, and disperses eight alternating cream-and-peach pixels over 560 milliseconds before the glyph returns on pointer exit, matching the established Hero, Case Studies, Development Process, About, and Start a Project motion language. Touch devices retain the glow without requiring hover. The availability marker uses a restrained pulse. Links use fill or text-color changes plus directional-arrow movement. External destinations announce new-tab behavior. No JavaScript, hidden route, loading, error, or empty state is required. Reduced-motion preferences remove the period burst, glow, status animation, and directional transitions while retaining the visible period and status label.

**Accessibility considerations:** The visual grid does not alter source order: closing message, project routes, business identity, homepage navigation, social navigation, then legal details. The availability state is written, not conveyed by pulse alone. Navigation landmarks are labeled, social names remain explicit, and all actions have visible focus. The cream/navy combinations provide strong contrast; peach carries large text or dark text and is not the only signal for state. Formal production contrast testing remains required.

**Assumptions, tradeoffs, and implementation implications:** Direction B assumes a distinctive final brand moment is worth more vertical space after an already substantial homepage. Its repeated Start a Project and Book A Call routes give visitors an immediate recovery path after reaching the end, but may feel conversion-heavy beside the preceding form. The handoff language is an explanatory bridge, not evidence of a submitted brief. The angled card and background grid are presentation-only and require no runtime library. A future Django include can implement the layout with semantic HTML/CSS; the ambient motion should remain decorative and reduced-motion safe.

**Preview and verification:** [`Desktop preview`](./mockups/footer/previews/footer-b-desktop.png) at **1440 × 1700** and [`wide-phone preview`](./mockups/footer/previews/footer-b-mobile.png) at **500 × 2600** document the resting layouts. They were refreshed after adding the requested period burst. Visual inspection confirmed the oversized-line wrap, unchanged period alignment, signal-card offset, cream route-board hierarchy, three-column-to-one-column reflow, complete route/social/legal sequence, minimum action heights, strong text contrast, and absence of visible horizontal overflow. Static checks confirm one period glyph, eight decorative pixels, alternating cream/peach colors, the 560-millisecond fine-pointer burst, touch-safe resting glow, and reduced-motion fallback. Still previews do not demonstrate focus or the full period, status, and arrow motion cycles.

## Next step

Continue revising [Case Studies Direction B](./mockups/case-studies/direction-b.html) from the documented baseline. After the Case Studies changes and responsive visual verification are complete, run `turtle-design-checkpoint` to review the updated business-focused homepage mockup workspace and decide whether its directions may move into planning. Mockup completion does not approve planning or production implementation.
