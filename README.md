# Web-Provider — Zilliz Cloud Global Providers & Regions page

Design exploration for a new zilliz.com marketing module: global multi-cloud
infrastructure (AWS / Google Cloud / Azure), region availability by
deployment option (Free & Serverless, Dedicated), and a "request a new
region" module. Status: exploration stage, no build tooling or deployment
yet — see `docs/design-spec.md` for the approved brief.

## Where to start

Open any file in `prototypes/` directly in a browser — no server or build
step required, everything is a self-contained HTML file.

- **`prototypes/region-map-only.html`** — current focus. Just the world
  map: land outline, region markers clustered per location and colored by
  provider (AWS orange / Google Cloud red / Azure blue), a legend below the
  map. No header/footer/copy/directory/form, no hover tooltip — stripped
  down per the latest request.
- `prototypes/concept-a-global-atlas.html` — full-page direction, close to
  the approved IA (hero map → directory → guidance → request region →
  footer). Safer, incremental polish over `reference/previous-version.html`.
- `prototypes/concept-b-coverage-console.html` — full-page direction that
  restructures the IA: hero map and directory filters are merged into one
  linked list+map "console," with a full reference table further down the
  page. Deliberate deviation from the spec's two-section IA — flagged for
  review, not yet decided on.

## Repo layout

```
docs/
  design-spec.md            Approved design brief (source of truth for requirements)
  conversation-summary.md   Recap of the design conversation and decisions so far
reference/
  previous-version.html     Prior full implementation, used as a starting point
  regions-map-bundle.html   Prior standalone map-only bundle (build artifact, not hand-authored)
  zilliz-site-reference.html  Full zilliz.com homepage, for header/footer/visual reference (~2.9MB)
prototypes/
  concept-a-global-atlas.html
  concept-b-coverage-console.html
  region-map-only.html
data/
  regions.json               21 regions / 12 locations / 3 providers, with x,y already
                              projected into the 1000x500 map viewBox
  world-land-outline.path    SVG path `d` string for the land outline (equirectangular,
                              viewBox "0 0 1000 500") used by every prototype's <path class="country">
  build-world-outline.py     Regenerates world-land-outline.path from Natural Earth 110m
                              TopoJSON (source URL in the script header). Needed because the
                              build sandbox has no npm/pip registry access, so this
                              hand-rolled decode/unwrap/simplify/project pipeline stands in
                              for d3-geo + topojson-client.
```

## Data model

`data/regions.json` is the single source of truth used by every prototype
(inlined as a `REGIONS` JS array in each HTML file — search for
`const REGIONS=`). Each entry: `provider`, `regionId`, `location`,
`geography`, `lon`/`lat`, `x`/`y` (pre-projected), `freeServerless`,
`dedicated`. Coordinates and capability flags are illustrative for this
exploration stage and should be reconciled against the official Zilliz
Cloud docs before anything ships.

One behavior worth carrying forward into any future iteration: selecting a
deployment-option filter (Free & Serverless / Dedicated) must never hide a
region — it only highlights that column and shows "Not available" where
unsupported. This is explicit in the spec (`docs/design-spec.md`, line 33)
and was corrected relative to `reference/previous-version.html`, which
filtered rows out.

## Continuing this on another machine

1. Clone the repo.
2. Open the prototypes directly in a browser — no install needed.
3. If you regenerate the map outline, you'll need network access to fetch
   `https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json` (or vendor a
   copy locally) before running `build-world-outline.py`.
