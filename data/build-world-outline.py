"""
Regenerates data/world-land-outline.path from Natural Earth 110m land data.

Source: https://cdn.jsdelivr.net/npm/world-atlas@2/land-110m.json (TopoJSON)
Output: a single SVG path `d` string (equirectangular projection,
        viewBox "0 0 1000 500"), used by all map prototypes in
        prototypes/*.html and matching the marker coordinates in
        data/regions.json (same projection formula).

Why this exists: the sandbox used to build this project has no network
access to npm/pip registries, so d3-geo/topojson-client weren't available.
This script re-implements the small slice of both needed: TopoJSON arc
decoding, antimeridian unwrapping (Chukotka/Fiji cross the 180 degree
seam and need special handling or the fill "wraps" across the whole map),
Douglas-Peucker simplification, and equirectangular projection.

Usage:
  python3 build-world-outline.py land-110m.json > world-land-outline.path
"""
import json, math, statistics, sys

W, H = 1000, 500  # must match the viewBox used in the HTML prototypes

def load_polygons(topojson_path):
    d = json.load(open(topojson_path))
    scale, translate = d['transform']['scale'], d['transform']['translate']

    def decode_arc(arc):
        x = y = 0
        pts = []
        for dx, dy in arc:
            x += dx; y += dy
            pts.append((x * scale[0] + translate[0], y * scale[1] + translate[1]))
        return pts

    arcs = [decode_arc(a) for a in d['arcs']]
    def get_arc(i):
        return arcs[i][:] if i >= 0 else list(reversed(arcs[~i]))

    polygons = []
    for geom in d['objects']['land']['geometries']:
        rings_idx = [geom['arcs']] if geom['type'] == 'Polygon' else geom['arcs']
        for poly in rings_idx:
            rings = []
            for ring_arc_indices in poly:
                ring_pts = []
                for ai in ring_arc_indices:
                    pts = get_arc(ai)
                    if ring_pts and pts and ring_pts[-1] == pts[0]:
                        ring_pts.extend(pts[1:])
                    else:
                        ring_pts.extend(pts)
                rings.append(ring_pts)
            polygons.append(rings)
    return polygons

def unwrap_ring(ring):
    """Keeps a ring spatially continuous across the +/-180 seam, then
    renormalizes so the bulk of the ring lands back in [-180, 180]."""
    out = [ring[0]]
    offset = 0.0
    for i in range(1, len(ring)):
        lon, lat = ring[i]
        plon, _ = ring[i - 1]
        d = lon - plon
        if d > 180: offset -= 360
        elif d < -180: offset += 360
        out.append((lon + offset, lat))
    med = statistics.median(p[0] for p in out)
    shift = round(med / 360) * 360
    return [(lon - shift, lat) for lon, lat in out] if shift else out

def project(lon, lat):
    return (lon + 180) / 360 * W, (90 - lat) / 180 * H

def rdp(points, epsilon):
    if len(points) < 3 or epsilon <= 0:
        return points
    def perp_dist(pt, a, b):
        (x, y), (x1, y1), (x2, y2) = pt, a, b
        if (x1, y1) == (x2, y2):
            return math.hypot(x - x1, y - y1)
        num = abs((y2 - y1) * x - (x2 - x1) * y + x2 * y1 - y2 * x1)
        return num / math.hypot(y2 - y1, x2 - x1)
    dmax, idx = 0, 0
    for i in range(1, len(points) - 1):
        dd = perp_dist(points[i], points[0], points[-1])
        if dd > dmax: idx, dmax = i, dd
    if dmax > epsilon:
        left, right = rdp(points[:idx + 1], epsilon), rdp(points[idx:], epsilon)
        return left[:-1] + right
    return [points[0], points[-1]]

def build_path(polygons, epsilon=0.6):
    parts = []
    for poly in polygons:
        for ring in poly:
            lons = [p[0] for p in ring]
            if max(lons) - min(lons) > 300 and len(ring) < 20:
                continue  # antimeridian-crossing sliver islands; imperceptible to drop
            pts = [project(lon, lat) for lon, lat in unwrap_ring(ring)]
            pts = rdp(pts, epsilon)
            if len(pts) < 3:
                continue
            parts.append("M" + " L".join(f"{x:.2f},{y:.2f}" for x, y in pts) + " Z")
    return " ".join(parts)

if __name__ == "__main__":
    path_json = sys.argv[1] if len(sys.argv) > 1 else "land-110m.json"
    print(build_path(load_polygons(path_json)))
