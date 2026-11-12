"""Map of Peru's departments with the CRONICAS sites.

Writes peru-map.jpg to slides/assets/
Run: ~/.venvs/npgh/bin/python slides/assets/map/peru-map.py
"""
import json
from pathlib import Path
from urllib.request import urlopen

import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

# INEI department limits, WGS84 lon/lat
URL = "https://raw.githubusercontent.com/juaneladio/peru-geojson/master/peru_departamental_simple.geojson"
SITES = {"TUMBES", "LIMA", "PUNO"}
SPIRIT_PURPLE = "#4B2E83"  # SpiritPurple in preamble/preamble.tex
OUT = Path(__file__).resolve().parent.parent / "peru-map.jpg"

features = json.load(urlopen(URL, timeout=30))["features"]
missing = SITES - {f["properties"]["NOMBDEP"] for f in features}
assert not missing, f"departments not found in GeoJSON: {missing}"

# Figure sized to the slide (about 5.5 cm tall) so line widths print true
fig = plt.figure(figsize=(1.5, 2.2))
ax = fig.add_axes((0, 0, 1, 1))
for f in features:
    geom = f["geometry"]
    polygons = geom["coordinates"] if geom["type"] == "MultiPolygon" else [geom["coordinates"]]
    fill = SPIRIT_PURPLE if f["properties"]["NOMBDEP"] in SITES else "none"
    for rings in polygons:
        # Outer ring only: the inner rings are lakes, not department limits
        ax.add_patch(Polygon(rings[0], facecolor=fill, edgecolor="black", linewidth=0.4))
ax.margins(0.01)
ax.autoscale_view()
ax.set_aspect("equal")
ax.set_axis_off()
fig.savefig(OUT, dpi=600, bbox_inches="tight", pad_inches=0.02, pil_kwargs={"quality": 95})
print("wrote", OUT)
