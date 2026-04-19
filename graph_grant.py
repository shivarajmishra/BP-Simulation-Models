import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

# Load ABS shapefile
gdf = gpd.read_file("STE_2021_AUST_GDA2020.shp")

# Hypertension data by state (ABS NHS 2022 / SBS-AAP)
data = {
    "New South Wales":      {"prev": 33.0, "pop": 2000000},
    "Victoria":             {"prev": 34.3, "pop": 1500000},
    "Queensland":           {"prev": 33.4, "pop": 1170000},
    "South Australia":      {"prev": 36.0, "pop": 460000},
    "Western Australia":    {"prev": 32.0, "pop": 597000},
    "Tasmania":             {"prev": 43.0, "pop": 170000},
    "Northern Territory":   {"prev": 26.0, "pop": 35000},
    "Australian Capital Territory": {"prev": 34.0, "pop": 98000},
}

gdf["prevalence"] = gdf["STE_NAME21"].map(
    lambda x: data.get(x, {}).get("prev", None)
)
gdf["population"] = gdf["STE_NAME21"].map(
    lambda x: data.get(x, {}).get("pop", None)
)
import pandas as pd

# Plot
fig, ax = plt.subplots(1, 1, figsize=(9, 9))
cmap = LinearSegmentedColormap.from_list("htn", ["#FFCC88", "#FF6600", "#CC0000", "#800000"])

gdf.plot(
    column="prevalence",
    ax=ax,
    cmap=cmap,
    legend=True,
    legend_kwds={
        "label": "Hypertension prevalence (% adults)",
        "orientation": "horizontal",
        "shrink": 0.5,
        "pad": 0.02
    },
    missing_kwds={"color": "lightgrey"},
    edgecolor="white",
    linewidth=1.5
)

# States too small to label in-place — text offset + arrow
arrow_offsets = {
    "Victoria":                       (133.0, -40.0),   # west, clear of Tasmania
    "Australian Capital Territory":   (154.0, -34.0),   # northeast corner
    "Tasmania":                       (154.0, -43.0),   # southeast corner
}

# Add state labels
for _, row in gdf.iterrows():
    if pd.notna(row["prevalence"]) and row.geometry is not None:
        centroid = row.geometry.centroid
        x, y = centroid.x, centroid.y
        col = "white" if row["prevalence"] > 35 else "#800000"
        name = row["STE_NAME21"]
        label = f"{name}\n({row['prevalence']}%)\n{row['population']:,.0f} adults"

        if name in arrow_offsets:
            tx, ty = arrow_offsets[name]
            ax.annotate(
                label,
                xy=(x, y), xytext=(tx, ty),
                ha="center", va="center",
                fontsize=8, fontweight="bold", color="#333333",
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#800000", alpha=0.85),
                arrowprops=dict(arrowstyle="->", color="#800000", lw=1.5),
            )
        else:
            ax.annotate(name, xy=(x, y + 1.2), ha="center", va="center",
                        fontsize=14, fontweight="bold", color=col)
            ax.annotate(f"({row['prevalence']}%)", xy=(x, y + 0.0), ha="center", va="center",
                        fontsize=8, fontweight="bold", color=col)
            ax.annotate(f"{row['population']:,.0f} adults", xy=(x, y - 0.9), ha="center", va="center",
                        fontsize=7, fontweight="bold", color=col)

ax.set_title(
    "",
    fontsize=10, fontweight="bold", pad=15
)
ax.axis("off")
ax.set_xlim([112, 155])
ax.set_ylim([-44, -10])

plt.figtext(
    0.1, 0.02,
    "",
    fontsize=11, color="grey"
)

plt.tight_layout()
plt.savefig("hypertension_australia_map.png", dpi=300, bbox_inches="tight")
plt.show()