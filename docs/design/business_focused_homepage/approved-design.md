# Business-Focused Homepage — Approved Design

- Feature slug: `business_focused_homepage`
- Status: `approved`
- Approval date: 2026-09-08
- Authorization: This approval authorizes `turtle-plan` only. It does not authorize implementation, production changes, or plan-state changes.

## Selected direction

The approved homepage is the assembled direction set:

1. Hero Direction C — Kinetic mosaic.
2. Services Direction B — Editorial service ledger.
3. Case Studies Direction B — Evidence trail.
4. Development Process Direction D — The working canvas.
5. Insights Direction C — Signal tuner.
6. About Direction A — Founder profile.
7. Start a Project Direction B — Three-step brief builder.
8. Footer Direction B — Closing signal.

Insights Article Direction B — Signal transcript is approved as a separate detail experience reached only from the featured Guardrails article in Insights C. It does not appear inline in the homepage sequence. Other Insights choices continue to their respective article pages.

## Approved goals and hierarchy

The homepage must present Hroman Codes as a founder-led software business and guide prospective clients through a coherent buyer journey:

1. Recognize the business problem and delivery promise.
2. Understand the service offer and likely fit.
3. Evaluate client evidence separately from founder-product evidence.
4. Understand the working process.
5. Review current thinking through a compact Insights layer.
6. Build trust in Heriberto as the accountable founder and engineer.
7. Submit a qualified project brief or choose the direct scheduling path.
8. End with a memorable brand close and clear recovery routes.

The founder identity remains prominent as a trust signal, but the commercial offer and buyer needs lead the page. Portfolio-oriented material must support this journey rather than dominate it.

## Required structure and components

- Buyer-oriented desktop and mobile navigation: Services, Case Studies, Development Process, Insights, About, and Start a Project.
- One logical homepage H1 and a non-duplicated heading hierarchy across responsive layouts.
- Hero problem-to-software statement, working-photo mosaic, founder proof card, Book A Call action, and Review Services action.
- Five-service editorial ledger with MVP and Product Development as the visually featured lead service and a closing Start a Project path.
- Case Studies split into default Client Work and separate Founder Product views, using the `Understand → Build → Show` evidence structure and project-specific artifact links.
- Five-stage Development Process canvas: Idea, Prototype, MVP, Product, and Iterate.
- Three-channel Insights tuner using current published posts, with the entire active story stage linking to its matching article and one archive route.
- Guardrails article detail using Insights Article B when that featured article is opened from Insights C.
- Founder profile with portrait, supplied biography, five-part skillset visualization, Watch Me Build embed, résumé route, and conversation route.
- Three-step Start a Project brief builder: Challenge, Context, and Connection, with a live project-signal summary, validation, confirmation, and direct scheduling alternative.
- Closing footer signal with Start a Project, Book A Call, homepage route board, verified social routes, copyright, founder credit, and return-to-top action.

## Approved visual system, tokens, and assets

- IBM Plex Mono remains the sole typeface.
- Primary palette: deep navy `#101D3B`, navy `#192A51`, cream `#F9E9D5`, peach `#F29576`, supporting grey `#AEB7CA`, and focus yellow `#FFD26A`.
- Related surfaces and functional colors documented in the specification may be retained where required, including soft navy, paper, error red, and success green.
- Preserve numbered section labels, thin rules, subtle grids, rounded borders, restrained shadows, peach accents, and expressive period motion.
- Reuse the official Hroman Codes wordmark, approved founder photographs, verified project imagery, `turtleAI.png`, the existing résumé destination, services deck, Calendly destination, project evidence destinations, blog routes, YouTube embed, and verified social destinations.
- Do not invent client metrics, testimonials, outcomes, responsibilities, commercial promises, or qualification rules.

## Responsive and interaction behavior

- Preserve the documented desktop compositions and stack them into one semantic content sequence at the specified tablet and phone breakpoints.
- Keep primary mobile actions full width with comfortable touch targets and no horizontal overflow.
- Use the native mobile-menu foundation with Escape, outside-pointer, focus-return, and reduced-motion behavior.
- Preserve keyboard-operable tabs, native disclosures, native form controls, visible focus states, meaningful alternatives, and written state labels.
- Keep essential content understandable without imagery, hover, JavaScript, animation, or color.
- Honor reduced-motion preferences across mosaic movement, headline particles, period bursts, card motion, signal waves, chart movement, status pulses, and directional transitions.
- Provide progressive fallbacks for the Case Studies tabs, Insights `:has()` selection, the interactive skillset, and the three-step brief builder.
- Final implementation must verify contrast, keyboard behavior, screen-reader behavior, mobile navigation, and motion/performance on representative devices.

## Accepted tradeoffs

- The expressive motion and layered imagery strengthen the brand but add rendering and testing cost.
- The full buyer journey is intentionally long; repeated, context-specific actions provide shorter paths to service evaluation and inquiry.
- The Case Studies tabs and Insights tuner improve focus but hide some content until visitors interact.
- Insights Direction C requires three eligible posts rather than the homepage's current two-post query.
- The skillset model is self-described and illustrative, not a measurement of proficiency or contractual effort.
- The YouTube embed provides direct proof but adds third-party page weight, privacy, network, and availability considerations.
- The staged inquiry reduces visible cognitive load but adds validation, focus-management, fallback, and server-error complexity.
- Insights Article B is a curated treatment for the featured Guardrails article. Extending it to arbitrary CMS content is not implied by this approval.

## Unresolved implementation questions for planning

- Validate the final service taxonomy, lead-service priority, typical deliverables, and all provisional commercial copy against actual engagement practice.
- Confirm client-approved case-study wording, responsibilities, evidence permissions, and any outcomes that may be published.
- Decide whether the three-post Insights contract uses the newest posts or an explicit featured-post selection, including its empty-state behavior.
- Decide whether Signal Transcript remains a Guardrails-only featured template or becomes a reusable article treatment with an explicit content model.
- Reconcile final homepage numbering, navigation anchors, Footer route-board entries, and isolated mockup H1 elements when sections are composed.
- Define the Start a Project server workflow: endpoint, CSRF, validation, spam controls, notification owner, failure and retry behavior, privacy language, retention, analytics, and confirmation contract.
- Confirm Calendly meeting length, availability, timezone behavior, intake expectations, and the balance between direct scheduling and qualification.
- Decide the production approach for third-party video privacy, loading, and failure behavior.
- Define conversion measurement for service evaluation, inquiry start, qualified submission, and scheduled calls.
- Profile the mosaic, particle effects, article signal visuals, and other motion on representative mobile hardware; reduce work where necessary without changing the approved static composition.
- Complete formal color-contrast, assistive-technology, keyboard, no-script, browser-compatibility, and real-device checks during implementation planning and verification.

## Source artifacts

- [Design audit](./audit.md)
- [Design specification](./design-spec.md)
- [Visual review workspace](./mockups/index.html)
- [Checkpoint record](./checkpoint.md)
- [Hero Direction C](./mockups/hero/direction-c.html)
- [Services Direction B](./mockups/services/direction-b.html)
- [Case Studies Direction B](./mockups/case-studies/direction-b.html)
- [Development Process Direction D](./mockups/development_process/direction-d.html)
- [Insights Direction C](./mockups/insights/direction-c.html)
- [Insights Article Direction B](./mockups/insights-subpage/direction-b.html)
- [About Direction A](./mockups/about/direction-a.html)
- [Start a Project Direction B](./mockups/start-a-project/direction-b.html)
- [Footer Direction B](./mockups/footer/direction-b.html)
