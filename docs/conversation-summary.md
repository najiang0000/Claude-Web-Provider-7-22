# Conversation summary — Global Providers & Regions page

For full detail, see `design-spec.md` (the approved brief) and the
prototype files themselves; this is a recap of how we got from brief to
current state, kept so work can resume on another machine without
re-deriving context.

## Brief

Jenna owns content, structure, copy, visuals, motion, interaction, front-end
code, and launch for a new zilliz.com marketing module covering global
multi-cloud infrastructure. Provided context: the approved design spec
(`design-spec.md`), a prior full implementation
(`reference/previous-version.html`), and the general zilliz.com site as a
visual/brand reference (`reference/zilliz-site-reference.html`). Explicit
instruction: explore and confirm direction before worrying about real
front-end/deployment concerns; the page will eventually be embedded into
zilliz.com as a standalone module, so wording/visuals/interaction need to
stay consistent with the site.

## Step 1 — reviewed the previous version

`reference/previous-version.html` turned out to already implement nearly
everything in the spec closely: hero world map with provider-colored
markers, legend below the map, filterable region directory (table on
desktop, cards on mobile), deployment guidance cards, a "request a region"
form, and a fully static header/footer copied from zilliz.com.

Asked Jenna what she wanted to do next given that; she chose to explore new
directions rather than audit/polish the existing one.

## Step 2 — built two full-page concepts

Both reuse the real zilliz.com header/footer markup (static, per spec) and
the same 21-region / 12-location / 3-provider dataset. The world map itself
is a from-scratch build: the previous version's map used a large minified
JS bundle (d3-geo + topojson-client + a bundled world atlas) that wasn't
practical to reverse-engineer, so this project instead fetches Natural
Earth 110m land TopoJSON directly and decodes/projects it with a small
hand-rolled Python pipeline (`data/build-world-outline.py`) — no d3
dependency, single static SVG `path`.

- **Concept A — Global Atlas**: incremental, low-risk polish of the
  existing IA (hero map → directory → guidance → request region → footer).
  Larger edge-to-edge map, ambient glow, pulsing provider-colored markers,
  refined directory table/cards.
- **Concept B — Coverage Console**: structural experiment. Merges the hero
  map and the directory's filters into one linked panel — a scrollable
  location list on the left, the map on the right, hover/click syncs both
  — with one shared filter state driving the console, a full reference
  table further down the page, and the map-below legend/counts. This
  deviates from the spec's two-section IA (hero vs. directory as separate
  sections) and was explicitly flagged to Jenna as an open question, not a
  decision.

**Spec correction applied to both concepts:** selecting a deployment option
(Free & Serverless / Dedicated) must never remove a region from view — it
only highlights that column and marks unsupported regions "Not available."
The previous version's filter logic hid non-matching rows, which conflicts
with `design-spec.md` line 33. Both new concepts filter only on
provider/geography and treat deployment selection as emphasis-only.

Both files were validated with `node --check` on every inline `<script>`
block and an HTML tag-balance pass (no headless browser was available in
the build sandbox to take real screenshots — the world map's correctness
was instead verified by rendering the decoded land polygons with
matplotlib before wiring them into the page).

## Step 3 — simplified to map-only

Jenna's next request: drop everything except the map itself, and remove
the hover tooltip entirely. Produced `prototypes/region-map-only.html`: no
header, footer, hero copy, directory, filters, guidance, or request form —
just the land outline, provider-colored/clustered markers (with a count
badge for locations with multiple regions), and the legend below the map
(kept because the spec requires it and colors alone aren't legible without
it). Hover/focus now only adds a subtle highlight ring on the marker, no
info panel. Also dropped the ambient pulse animation from Concept A's
markers here, since the spec explicitly cautions against decorative motion
and there's no longer any filter state for a marker "pulse" to meaningfully
represent.

## Open questions for next session

- Which full-page direction (A, B, a hybrid, or something new) to develop
  further once the map itself is settled.
- Whether `reference/zilliz-site-reference.html` (2.9MB, the full zilliz.com
  homepage) is still needed in the repo, or was only useful during this
  session for visual/brand reference.
- Real region data (coordinates, capability flags, documentation links)
  still needs to be reconciled against the official Zilliz Cloud docs —
  current dataset is illustrative, carried over from the previous version.
