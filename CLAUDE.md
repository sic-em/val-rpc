# CLAUDE.md

Behavioral guidelines to reduce common LLM coding mistakes. Merge with project-specific instructions as needed.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:

- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

## 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

## 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:

- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:

- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

## 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:

- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:

```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## 5. Performance & Snappiness (non-negotiable)

**The UI must feel instant. No sluggish or slow-feeling interactions, ever.**

- Treat 60fps (16.6ms/frame) as the floor. 120fps where the display allows.
- Keystroke → paint: <100ms. Route/view transition: <16ms perceived (no jank, no flash).
- No layout thrash. No synchronous heavy work on the main thread.
- Virtualize any list >100 rows (TanStack Virtual or equivalent).
- Lazy-load images, decode off-main-thread, use blurhash/dominant-color placeholders.
- Memoize expensive renders. Code-split per route. Defer non-critical JS.
- Never ship a loading spinner where a skeleton or optimistic UI would do.
- IPC: batch + debounce. Never block the renderer waiting on main process.
- Measure before guessing. Use the Performance panel + React Profiler.
- If a feature can't hit the perf bar, it doesn't ship until it does.
- **Prefetch all visible third-party metadata in the route loader.** Anything that determines what a card renders (logo, rating, badge) must be resolved before paint, not after. Wrap fan-out in `Promise.race([prefetch, timeout(1500)])` so a slow upstream can't hang the route. See [ADR-0001](./docs/adr/0001-prefetch-third-party-metadata-in-route-loaders.md). The "swap to logo / rating fades in" flicker is the classic violation — don't ship it.

## 6. Animations — ALWAYS invoke `/emil-design-eng` AND `/transitions-dev`

**Every animation must adhere to BOTH skills. Follow them to the letter. No exceptions, no "this case is different."**

- Before adding ANY animation, transition, hover effect, micro-interaction, or motion: invoke BOTH `/emil-design-eng` AND `/transitions-dev` first. Read them. Apply them.
- This includes: page transitions, modal open/close, hover states, tooltips, list reorder, drawer/sheet, loading states, button feedback, scroll-linked motion, popovers, badges, error shakes, success checks, icon swaps, text swaps, number changes, card resizes, panel reveals, side-by-side page slides.
- If `/transitions-dev` has a recipe for the surface you're animating (the table in its index), use that recipe verbatim — don't rewrite selectors, don't collapse to shorthand, don't strip `will-change`. The values are tuned.
- If `/emil-design-eng` says don't do X (e.g. `transition: all`, `scale(0)` entries, `ease-in` on UI, `transform-origin: center` on popovers, animating keyboard-initiated actions), don't do X. Ever.
- Reuse the universal `:root` token block from `/transitions-dev` for `--resize-*`, `--text-swap-*`, `--dropdown-*`, etc. Don't invent parallel duration/easing constants.
- Default easing for stateful UI motion: `cubic-bezier(0.22, 1, 0.36, 1)`. Default UI duration: under 300ms (button press 100–160ms, dropdowns 150–250ms, modals 200–300ms).
- Spring physics for gestures + interruptible motion; CSS transitions for everything else (transitions retarget mid-flight, keyframes don't).
- Respect `prefers-reduced-motion`. Always. Every keyframe ships a guard.
- If unsure whether something counts as an animation: it does. Invoke both skills.

**Checklist before merging any animation:**

- [ ] Did I invoke `/emil-design-eng`? `/transitions-dev`?
- [ ] Exact properties named in `transition:` (no `all`)?
- [ ] Easing is a custom cubic-bezier, not the built-in `ease-in-out`?
- [ ] Duration < 300ms for UI (or justified)?
- [ ] `prefers-reduced-motion` guard present?
- [ ] Origin-aware transform on popovers (not `center`)?
- [ ] No entry from `scale(0)`?

## 7. Native-feel rules (always on)

**Web tells that scream "this is a website." Don't ship them.**

- Buttons, menu items, and links use `cursor: pointer` (a global base rule in `main.css` handles this — don't add `cursor-default` to controls). Draggable controls (sliders) use `cursor: grab` / `grabbing`.
- No hover highlights on most controls (buttons, list items). Hover ≠ desktop affordance.
- Zero flicker on appear/transition. Pre-render before show, never flash white/blank.
- No focus rings. Strip `focus-visible:ring-*`, `ring-*`, and any visible `outline` from all interactive controls. Use `outline-none` and rely on the design's own focused state (e.g. a subtle bg/tone change), never a ring. Rings are a browser/web tell — desktop apps don't draw them.

## 8. Reusable Components — no hardcoded styles

**Every UI primitive lives in a shared component. Variants over duplication.**

- Buttons, badges, labels, inputs, cards, chips, icon buttons, list rows, etc. → reusable component, always.
- Need a new visual style? Add a `variant` prop to the existing component. Don't fork or hardcode.
- Component API pattern: `variant`, `size`, `tone`/`intent`, `loading`, `disabled`. Use `cva` (class-variance-authority) or similar.
- Hardcoding styles is only acceptable for genuinely one-off surfaces (e.g. a single hero CTA, a marketing-only block). Document why inline if so.
- Before building a new component: grep existing primitives. Extend, don't duplicate.
- Tokens (colors, spacing, radii, typography) live in `@theme` / design tokens, not in component files.

## 9. Icons — ALWAYS use the `central-icons` MCP server

**Every icon comes from `central-icons`. No hand-rolled SVGs. No icon libraries (lucide, heroicons, etc.).**

- Before adding ANY icon, call `mcp__central-icons__search_icons` (or `list_icons` if you know the category) with `include_svg: "first"` to fetch the SVG inline in one round-trip.
- If you already know the exact name, use `mcp__central-icons__get_icon` (or `get_icons` for batches).
- Paste the returned SVG directly into a component. Match line weight (1.5px stroke) and corner radius — central-icons handles this consistently.
- If a needed icon doesn't exist in central-icons, stop and ask. Do NOT draft a custom SVG inline. Do NOT pull from a different icon set.
- This applies to context-menu glyphs, button icons, status dots, empty states — every single icon in the app.

**Why:** Visual consistency across the app collapses when icons come from multiple sources (different stroke weights, corner radii, baselines, padding). One source = one visual language.

## 10. Resize transitions — grid-template-rows + transitions-dev curve

**Any container that expands/collapses (popovers, accordions, conditional rows, alerts, tooltips that change size) must animate height with the same curve. No instant snap. No `height: auto` → can't be transitioned directly.**

Pattern (works for `height: auto` content):

```tsx
<div
  className="grid transition-[grid-template-rows] duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]"
  style={{ gridTemplateRows: open ? '1fr' : '0fr' }}
>
  <div className="overflow-hidden">{/* content — stays mounted so exit anim renders */}</div>
</div>
```

For fixed-dimension boxes (cards/sheets with known sizes), animate `width`/`height` directly:

```tsx
<div
  className="transition-[width,height] duration-300 ease-[cubic-bezier(0.22,1,0.36,1)]"
  style={{ width, height }}
/>
```

Rules:

- **Duration:** 300ms. Faster = snap, slower = sluggish. Same value everywhere keeps the app cohesive.
- **Easing:** `cubic-bezier(0.22, 1, 0.36, 1)` (strong ease-out from transitions-dev). Never `ease`, `ease-in`, `linear`.
- **Keep content mounted** while collapsed (snapshot last value if data changes) — unmounting drops the exit anim.
- **`overflow-hidden`** on the inner wrapper of the grid pattern, otherwise the collapsing content spills.
- **`will-change: width, height`** is fine for grid-row collapses; don't add for one-off rare transitions.
- **Respect `prefers-reduced-motion`** — wrap the className with reduce check or rely on the global rule in main.css.

Common violations:

- `transition-all` — never. Specify exact properties.
- `transition-[height]` with `height: auto` — won't transition. Use the grid trick.
- Conditional render (`{open ? <X /> : null}`) when you want an exit animation — content unmounts instantly, no fade-out.

## 11. No useless comments

**Default to zero comments. Code says what; comments must earn their place.**

- Do NOT explain WHAT the code does — well-named identifiers do that. `// fetch user` above `fetchUser()` is noise.
- Do NOT annotate arithmetic with its breakdown. `// gutter 78 + ml-6 24 + buttons 32×4 + gaps 8×3 + pad 16` above the same expression is restating the code. If the constants need labels, give them labels in code (`const TRAFFIC_LIGHT_GUTTER = 78`).
- Do NOT label sections (`// state`, `// handlers`, `// render`) — structure is visible.
- Do NOT reference the task, PR, or caller (`// added for X`, `// used by Y`) — that rots and lives in commit messages.
- DO write a comment only when the WHY is non-obvious: a hidden constraint, a workaround for a specific upstream bug (link the issue), a subtle invariant, behavior that would surprise the next reader. One short line.
- If removing a comment wouldn't confuse anyone reading the diff, delete it.

## 12. User-facing copy — no dev jargon

**Changelogs, empty states, toasts, error messages — written for end users, not for me.**

- NEVER mention dev/build-pipeline jargon: "installed app", "packaged build", "dev mode", "production build", "the built version", "in dev", "the binary".
- Talk about what the user sees and does. Say "the app", "Vesper", "your library" — not "the renderer", "the main process", "the bundle".
- Describe outcomes, not internals. "Avatar uploads work again." not "R2 CORS allows the renderer origin."
- If a fix only manifests in one environment, say it neutrally ("fixed an upload failure") — don't expose where it lived.
- This applies everywhere copy reaches a non-developer: changelog mdx, sidebar update card, settings descriptions, error banners, notifications.

## 13. Be consistent with neighboring code

**When adding a new component, row, badge, label, separator, or any UI that mirrors an existing one, copy the existing convention exactly. Don't invent a parallel style.**

- Separators in meta lines: use the same character (`,` vs `·` vs `•`) as the closest sibling. If `ItemRow` uses `Show, 2019`, then `RecRow` MUST use `Show, 2019` — not `Show · 2019`.
- Number formatting (`2h 13m` vs `2:13` vs `133 min`), date formatting, casing (`Movie` vs `movie`), pluralization rules, truncation thresholds: pick the existing one.
- Before writing a meta line, list row, badge, or any small UI molecule, grep the codebase for the closest existing version and copy its format string verbatim. Same applies to spacing classes, gap sizes, icon sizes — match the neighbor.
- If the existing convention is wrong, fix BOTH (the existing one and your new one) in the same PR. Never ship two styles side-by-side.

**Why:** users perceive consistency as polish even when they can't articulate it. Two near-identical rows with one using `,` and one using `·` feels broken in a way that's hard to name but easy to notice.

## 14. Changelog — only one entry at a time

**`packages/changelog/src/entries/` holds exactly one `.mdx` file: the current release. Old entries are deleted, not archived.**

- When you ship a new version, write the new `0.X.Y.mdx`, then DELETE the previous `.mdx` and remove its import from `entries/index.ts`. There is no version history surface — the changelog page and sidebar update card only ever show the latest.
- This applies to user-facing changelog copy only; commit history + git tags are the real release log.
- Delete unused MDX components in `packages/changelog/src/components/` when they stop being referenced by the current entry. Keep components that might recur in future entries (e.g. `LinkBadge`) even if the current entry doesn't use them — but anything that was specific to a prior entry (one-off island, badge, illustration) goes.
- Update `components/index.ts` + the root `index.ts` to drop the removed exports in the same change.

**Why:** old entries clutter the page, MDX bundles them all into the renderer, and users only care about what just shipped. The changelog is a "what's new" surface, not a release archive.

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, clarifying questions come before implementation rather than after mistakes, the UI feels native and instant, and the component library grows by variants instead of one-offs.

<!-- convex-ai-start -->

This project uses [Convex](https://convex.dev) as its backend.

When working on Convex code, **always read
`convex/_generated/ai/guidelines.md` first** for important guidelines on
how to correctly use Convex APIs and patterns. The file contains rules that
override what you may have learned about Convex from training data.

Convex agent skills for common tasks can be installed by running
`npx convex ai-files install`.

<!-- convex-ai-end -->
