# Business-Focused Homepage Design Audit

- Feature slug: `business_focused_homepage`
- Audit date: 2026-08-27
- Live URL: `https://heriberto.codes/`
- Status: ready for `turtle-mockup` once the ideal-client and offer assumptions are confirmed or clearly marked as provisional

## Objective and audience

Evolve the homepage from a personal software-engineering portfolio into a business-focused site that helps suitable prospects recognize their problem, understand how Hroman Codes can help, trust the business, and submit a qualified client inquiry.

The inferred primary audience is decision-makers at small businesses, startups, and growing organizations with an inefficient workflow, product idea, integration need, or software system that requires design and engineering support. The desired primary action is a qualified project inquiry or appropriately prepared discovery call. Secondary actions should help a prospect evaluate service fit and review relevant evidence before contacting the business.

The current hero supports this audience inference. The exact ideal-client profile, engagement size, vertical focus, geographic scope, budget floor, and preferred inquiry path have not yet been confirmed.

## Evidence inspected

- Live homepage on 2026-08-27 in the Codex in-app browser.
- Live desktop rendering at 1440 × 900, including full-page structure and section dimensions.
- Live mobile rendering at 390 × 844, including the hero, experience, contact, and navigation interaction.
- Live DOM and accessibility-oriented snapshots covering navigation, headings, links, project content, blog content, and contact actions.
- Live interaction test of the mobile navigation toggle.
- Live document inventory: page title, meta description, forms, inputs, buttons, heading count, section order, mail and Calendly links.
- `templates/home.html` and `templates/base.html`: composition, metadata, dependencies, and document structure.
- `templates/includes/navbar.html`, `hero.html`, `about.html`, `experience.html`, `tools.html`, `work.html`, `blog_home_page.html`, `contact.html`, and `footer.html`.
- `static/style.css`: brand tokens, responsive rules, motion, navigation, card, CTA, and contact styling.
- `apps/pages/views.py` and existing page tests: homepage data boundary and blog-post context.
- Authored assets under `static/pages/images/` and `static/images/`.
- `agents.md`, `architecture.md`, `repo_map.md`, and `docs/system/design-workflow.md`.

The live page was visually inspected at desktop and phone sizes. The linked services PDF, Calendly flow, mail-client flow, project destinations, analytics outside the repository, and user behavior data were not inspected.

## Current design inventory

- Section order: Hero → About → Experience → Tools → Work → Blog → Contact → Footer.
- Desktop page height observed at approximately 11,453 pixels. The Work section accounts for approximately 5,750 pixels, more than half of the desktop journey.
- Mobile page height observed at approximately 12,959 pixels. The contact section appears near the end of this journey.
- A sticky, auto-hiding navigation with About, Experience, Tools, Work, Blog, Contact, and a visually emphasized Resume action. There is no Services or Process destination.
- A founder-led hero with Heriberto's name, a broad software-and-automation value proposition, and two actions: `Let's Talk` and `Explore Services`.
- A long personal About narrative, portrait, animated availability statement, and skillset model.
- A chronological experience list focused on company, role, and date.
- A large animated tool inventory containing eighteen technologies and tools.
- Six featured projects in separate desktop and mobile template structures, emphasizing screenshots, technology badges, GitHub, Figma, architecture, product links, and Trello artifacts.
- A YouTube build-content block, two recent blog posts, project/blog archive links, and developer-oriented social channels.
- A contact section offering mail and Calendly. The copy states availability for both full-time positions and contract work.
- No homepage inquiry form, input field, testimonial, client quote, service description section, process section, pricing or engagement guidance, explicit qualification criteria, or on-page case study was found.
- Live document metadata uses the generic title `Hroman.codes` and no meta description was present.
- The live DOM contained eighteen `h1` elements, partly because desktop and mobile project variants coexist in the source.

## Strengths to preserve

- **The hero has begun the business transition.** It names a real audience and connects inefficient workflows and ideas to digital products, automation, and scalable software.
- **The founder is credible and human.** The portrait, first-person voice, teaching background, product breadth, and visible engineering work establish authenticity that a generic agency site would lack.
- **The brand is distinctive.** Navy, beige, orange, IBM Plex Mono, numbered sections, line details, and the Hroman Codes mark form a recognizable visual system.
- **Primary actions are visually clear above the fold.** Desktop and mobile both present two large, high-contrast actions, and mobile correctly makes them full width.
- **There is substantial proof material to curate.** Empowered Path Therapy, Rubix AI, Linktag, Turtle AI, cThink, architecture artifacts, design artifacts, and technical writing provide raw material for business-relevant case studies.
- **The site demonstrates breadth and active thinking.** Experience across HealthTech, EdTech, SaaS, e-commerce, AI workflows, teaching, design, architecture, and implementation can support a strong end-to-end positioning.
- **The site is maintained and current in visible areas.** The footer, resume link, and blog entries show 2026 content.
- **The server-rendered template architecture supports incremental redesign.** Existing includes, tokens, Bootstrap structure, and local assets allow the homepage to evolve without a framework change.

## Findings, ordered by impact

### 1. The homepage communicates two competing businesses

**Observed evidence:** The hero positions Hroman Codes as helping organizations build products and automation. The navigation prioritizes a Resume. The About section says `I am for hire`, and the final contact copy actively seeks both full-time positions and contract work. Most section labels are personal: `About Me`, `My Tools`, `Experience`, and `Some Things I've Built`.

**Likely impact:** A prospective client cannot tell whether Hroman Codes is a focused consulting business, a freelancer seeking any opportunity, or a portfolio supporting a full-time job search. This ambiguity weakens confidence and makes qualification difficult in both directions.

**Recommended design response:** Establish one primary commercial identity and make other availability secondary and non-competing. The homepage hierarchy, navigation, proof, and final CTA should consistently address the intended buyer and engagement model.

### 2. Prospects cannot evaluate the actual service offer on the homepage

**Observed evidence:** `Explore Services` opens an external PDF. There is no Services navigation item or on-page explanation of service categories, business problems addressed, likely deliverables, engagement shape, or who is and is not a fit.

**Likely impact:** Visitors must leave the site before they can understand the offer. Prospects with a vague problem cannot map their need to a service, while poor-fit prospects receive no self-selection guidance.

**Recommended design response:** Give the homepage enough service and fit information for a buyer to answer: `Is this for an organization like mine?`, `Can Hroman Codes address my type of problem?`, and `What kind of engagement would we discuss?` The PDF can remain supporting material rather than carrying the entire offer.

### 3. Proof emphasizes developer activity rather than client outcomes

**Observed evidence:** Experience entries show only company, role, and dates. Project cards devote substantial space to technology badges and developer artifacts such as GitHub, Figma, Trello, and architecture diagrams. Project descriptions explain what products do but rarely state the client problem, Heriberto's ownership, delivery constraints, result, or business value. No testimonial, client quote, outcome metric, or case-study structure was found.

**Likely impact:** Technical peers can assess tool familiarity, but business buyers cannot easily judge whether Heriberto understands business constraints, manages delivery risk, communicates well, or produces valuable outcomes.

**Recommended design response:** Reframe selected proof around problem, role, approach, delivered result, and verified outcome. Technical depth should remain available as supporting evidence, not the primary story. Do not invent metrics, testimonials, or responsibilities.

### 4. The conversion path does not qualify inquiries

**Observed evidence:** The homepage has zero forms and zero form inputs. Its conversion destinations are a generic `Let's Talk` Calendly link, `coffee_chat`, a mailto link, and the services PDF. The final CTA says `Get in touch` and appears after roughly 12,959 mobile pixels. There is no visible explanation of what happens next, response expectations, project-fit criteria, or information a prospect should prepare.

**Likely impact:** High-intent buyers receive little guidance, hesitant buyers may not be ready to book immediately, and low-fit visitors can schedule without self-qualification. Mailto also depends on a configured email client and provides no consistent intake structure or success state.

**Recommended design response:** Create a guided, confidence-building inquiry path that communicates next steps and captures enough project context to distinguish fit before or alongside scheduling. Repeat a context-appropriate client CTA before the end of the page rather than relying on one long-scroll destination.

### 5. Information architecture is portfolio-first and delays buyer questions

**Observed evidence:** The first business-specific offer detail is outside the site in a PDF. The on-page journey moves through a long biography, employment history, eighteen tools, and a 5,750-pixel project section before reaching contact. Navigation mirrors this portfolio taxonomy and does not expose services, client fit, process, results, or an inquiry action.

**Likely impact:** A buyer must translate personal credentials into business relevance without assistance. Important questions about fit, trust, working process, and next steps are deferred while lower-priority technical inventory dominates the journey.

**Recommended design response:** Reorder and rename the homepage around the prospect's decision sequence: relevance, offer, evidence, working relationship, founder credibility, and inquiry. Personal history, tools, education, archives, and long-form content should support that sequence rather than define it.

### 6. Calls to action are visually strong but semantically generic

**Observed evidence:** `Let's Talk`, `Explore Services`, `Message Me`, and `Book Time With Me` describe actions but not the value, qualification level, or expected next step. The hero actions point directly to third-party destinations, and the page does not explain what a conversation covers.

**Likely impact:** Visitors with different intent levels cannot confidently choose the right path. A generic meeting request can feel premature, while `Explore Services` unexpectedly leaves the site for a PDF.

**Recommended design response:** Give each CTA a specific role in the decision journey and set expectations in adjacent copy. Distinguish evaluation from inquiry and scheduling, and make destination behavior predictable.

### 7. The founder brand overwhelms the business identity

**Observed evidence:** Heriberto's name is the largest hero element; the hero claim is `I build for the web`; the About section occupies approximately 1,499 desktop pixels; section language repeatedly uses `my` and `I`; and the footer emphasizes that Heriberto built the site. Hroman Codes appears in the logo and copy but has no clear on-page operating promise beyond the founder.

**Likely impact:** The founder's personality builds trust, but the business can feel like an individual résumé rather than a dependable client service with a repeatable way of working.

**Recommended design response:** Preserve the founder-led advantage while giving Hroman Codes a clearer business promise, service vocabulary, and working model. This is a balance problem, not a recommendation to hide Heriberto.

### 8. Mobile navigation failed in the tested live environment

**Observed evidence:** At 390 × 844, the hamburger was visible and labeled `Toggle navigation`. Activating it left `aria-expanded="false"`, and the collapsed navigation remained `display: none`. Runtime inspection found `window.jQuery`, the Bootstrap collapse plugin, and Popper unavailable even though their external script tags were present.

**Likely impact:** In the observed environment, mobile visitors cannot use the menu to reach any section, service information, or contact destination. This is especially damaging on a 12,959-pixel page.

**Recommended design response:** Treat reliable mobile navigation as a prerequisite for any conversion redesign. Validate the eventual mockup's information architecture independently of third-party JavaScript and verify the production behavior across real mobile browsers. Because this failure may involve the test environment or external CDN delivery, broader device verification is still required before assigning a universal root cause.

### 9. Mobile readability and journey length increase conversion friction

**Observed evidence:** The mobile hero uses 0.8rem body copy, muted grey text, and a large gap between navigation and the message. Experience titles wrap across several lines while fixed date columns compete for width. The contact section remains at the bottom of a nearly 13,000-pixel page. The strongest positive mobile behavior is the full-width hero CTAs.

**Likely impact:** Visitors must work harder to read and scan, particularly when comparing experience or reaching a later CTA. Long-form content provides depth but does not offer a shorter buyer path.

**Recommended design response:** Preserve full-width mobile actions, increase scannability and text comfort, and provide shorter routes to service fit, proof, and inquiry. Mobile hierarchy should be designed from content priorities rather than compressed desktop structures.

### 10. Search, semantic, and accessibility signals do not describe the business clearly

**Observed evidence:** The live title is `Hroman.codes`; no meta description was present; the hero name is an `h2` rather than the primary page heading; and the live DOM contains eighteen `h1` elements, including duplicated desktop/mobile project headings. Several project image alternatives are generic, such as `EPT gif` and `Card image cap`. No section-specific reduced-motion treatment was found for multiple animation systems.

**Likely impact:** Search previews do not communicate the offer, assistive-technology heading navigation is noisy, and some visual evidence lacks meaningful alternatives. Motion and low-contrast secondary copy may further reduce usability for some visitors.

**Recommended design response:** Make the business purpose explicit in document metadata and heading structure, expose one logical content hierarchy regardless of responsive variant, improve meaningful image descriptions, preserve visible focus, and ensure content remains understandable without animation.

### 11. Several attention-heavy elements do not clearly support conversion

**Observed evidence:** The page contains animated tool icons, card tilt, logo-scaling effects, an animated availability statement, a large skillset chart, a YouTube embed, project archives, blog categories, likes, and extensive technology badges.

**Likely impact:** These elements demonstrate personality and activity, but together they compete with the service offer and create many exit paths before inquiry. The effect is cumulative rather than a defect in any single element.

**Recommended design response:** For each element, identify the buyer question it answers and the next action it supports. Preserve the strongest credibility signals and de-emphasize or relocate material that primarily serves technical peers. The degree of visual restraint is a recommendation to explore, not an objective requirement.

### 12. The current experience provides no visible conversion measurement contract

**Observed evidence:** No analytics or conversion instrumentation was found in the inspected templates or authored application code. There is no on-site inquiry submission or success state to define a completed conversion.

**Likely impact:** It is difficult to determine whether visitors understand the offer, where qualified prospects abandon the journey, or whether the redesign improves inquiry quality.

**Recommended design response:** Define the meaningful conversion states during design—such as service evaluation, inquiry start, qualified submission, and scheduled call—so the future experience can be evaluated. This audit does not assume that repository absence proves no external measurement exists.

## Existing components, tokens, and assets to reuse

- Global brand tokens: `--hrbgColor`, `--hrColorWhite`, `--hrColorOrange`, `--hrColorBeige`, `--hrTextColorGrey`, `--hrSectionMaxWidth`, and existing section-spacing variables.
- IBM Plex Mono as the primary brand typeface; Inter is already loaded for stronger hierarchy where appropriate.
- Hroman Codes logo assets: `H.svg`, `hr.svg`, and `hLogoBlueOutline.svg`.
- The numbered-section convention, orange line accents, rounded borders, subtle shadows, and dark surfaces.
- Hero primary and secondary CTA styling, especially the successful full-width mobile treatment.
- Heriberto's portrait and founder story as trust-building business assets.
- The skillset model's `understand → design → engineer → ship → communicate` narrative, which can support a client-facing working-process story more directly than a generic tool list.
- Existing project imagery for Empowered Path Therapy, Rubix AI, Linktag, cThink, and Turtle AI.
- Existing work descriptions, technology badges, design artifacts, architecture documents, and links as source material for curated case studies.
- Current blog and YouTube material as optional authority evidence after the core buyer journey is established.
- Server-rendered Django includes and Bootstrap conventions; the audit finds no need for a new frontend framework or public API.

## Responsive and accessibility considerations

- Resolve and verify mobile menu behavior before relying on navigation for conversion.
- Validate the buyer journey at narrow phone, wide phone, tablet, laptop, and large desktop widths with real service and case-study copy.
- Preserve full-width mobile CTAs and comfortable touch targets.
- Avoid fixed text/date splits that force long names or offer descriptions into narrow columns.
- Keep primary and secondary text at readable sizes and contrast. The existing grey token is approximately 4.59:1 against navy and is close to the WCAG AA threshold for normal text.
- Provide a visible keyboard focus state equivalent to hover and make external/new-window destinations predictable.
- Use one logical heading hierarchy; responsive variants should not duplicate the page outline.
- Respect reduced-motion preferences across Animate.css, Font Awesome animation, tilt, logo scaling, and other decorative movement.
- Ensure service fit, proof, process, and inquiry remain understandable without imagery, motion, hover, or color.
- Use meaningful alternative text for client/project imagery and treat decorative marks as decorative.
- Do not place essential offer information only inside a PDF, video, chart, icon, or third-party embed.

## Constraints, assumptions, and missing evidence

- The audit assumes the business should prioritize client services over full-time employment. If both must remain equally prominent, the homepage will require explicit audience routing rather than a single linear conversion journey.
- The ideal client, buyer role, core verticals, service packages, preferred project size, budget floor, timeline constraints, geographic availability, and capacity are unknown.
- It is unknown which services are currently offered, which are most profitable, and which should drive inquiries.
- Verified client outcomes, metrics, testimonials, logos, responsibilities, and permission to publish them were not supplied.
- The services PDF was not inspected, so existing offer language may already be available for reuse.
- The Calendly intake questions, availability, and follow-up process were not inspected.
- Existing analytics, CRM, email automation, or externally configured tracking may exist outside the repository.
- The mobile menu failure was reproduced in one controlled browser environment; additional real-device verification is required.
- No traffic sources, search queries, funnel analytics, inquiry volume, lead quality, sales objections, or user interviews were available.
- The audit does not determine pricing strategy, service packaging, or sales operations; those business decisions constrain the design.

## Prioritized opportunities for `turtle-mockup`

1. Demonstrate one coherent business identity and buyer journey from problem recognition to qualified inquiry.
2. Make the offer and ideal-client fit understandable on the homepage without requiring the services PDF.
3. Reframe selected work as business evidence using verified problem, ownership, process, result, and outcome content.
4. Compare a continuity-focused direction that preserves the current founder portfolio structure with a stronger business-first direction that substantially reprioritizes sections.
5. Demonstrate an inquiry path with clear expectations, qualification, and next steps at more than one decision point.
6. Redesign navigation labels and hierarchy around services, proof, working process, and contact while preserving access to appropriate founder content.
7. Preserve the Hroman Codes palette, typography, personality, founder portrait, and strongest project assets without allowing tools, archives, or motion to dominate.
8. Demonstrate the complete mobile journey, including a reliable menu, readable service copy, concise proof, and accessible CTAs.
9. Identify all provisional service, outcome, testimonial, and qualification copy in the mockup so it cannot be mistaken for verified business information.
