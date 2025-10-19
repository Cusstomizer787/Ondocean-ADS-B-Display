# %%
# Requirements.txt
import gzip
import json
from datetime import timedelta

import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pyproj
from shapely.geometry import LineString, Point

# Charger les shapefile
base_path = r"C:\Users\ncuss\Documents\GitHub\pyclass\TP_FINAL\ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03\ROUTE500\1_DONNEES_LIVRAISON_2022-01-00175\R500_3-0_SHP_LAMB93_FXX-ED211"
path_to_airport = rf"{base_path}\RESEAU_ROUTIER\AERODROME.shp"
path_to_route = rf"{base_path}\RESEAU_ROUTIER\TRONCON_ROUTE.shp"
path_to_admin = rf"{base_path}\ADMINISTRATIF\LIMITE_ADMINISTRATIVE.shp"
path_to_occupation = rf"{base_path}\HABILLAGE\ZONE_OCCUPATION_SOL.shp"

# Lire shapefiles
gdf_airport = gpd.read_file(path_to_airport)
gdf_route = gpd.read_file(path_to_route, encoding="cp1252")
gdf_limite_admin = gpd.read_file(path_to_admin)
gdf_occupation = gpd.read_file(path_to_occupation)

# Filtrer les données
gdf_route = gdf_route.query('CLASS_ADM == "Autoroute"')
gdf_limite_region_departement = gdf_limite_admin[
    gdf_limite_admin["NATURE"].isin(["Limite de département", "Limite de région"])
]
gdf_airport = gdf_airport[gdf_airport["TOPONYME"].notna()]
gdf_occupation = gdf_occupation.query('NATURE == "Bâti"')

# Calculer les surfaces avant conversion CRS
gdf_route["area"] = gdf_route.area
gdf_airport["area"] = gdf_airport.area
gdf_limite_region_departement["ID_RTE500"] = gdf_limite_region_departement.area

# Centrer sur Paris
center_x, center_y = 652000, 6860000  # en mètres
delta = 25000  # rayon ~50 km

# Créer figure
fig, ax = plt.subplots(figsize=(8, 8))

# Tracer les tronçons et aéroports
gdf_route.plot(column="area", ax=ax, cmap="OrRd", edgecolor="orange", legend=False)
gdf_airport.plot(
    column="area", ax=ax, color="blue", markersize=30, legend=False
)  # points
gdf_limite_region_departement.plot(
    ax=ax, color="black", edgecolor="black", legend=False
)
gdf_occupation.plot(ax=ax, color="lightcoral", edgecolor="none", legend=False)

# Zoom autour de Paris en Lambert-93
ax.set_xlim(center_x - delta, center_x + delta)
ax.set_ylim(center_y - delta, center_y + delta)

# plot map
plt.title("Carte centrée sur Paris (Lambert-93)")
plt.grid()
plt.show()


# Fonctions necessaires pour les classes
def iterate_time(data, threshold):
    idx = np.where(data.timestamp.diff().dt.total_seconds() > threshold)[0]
    start = 0
    for stop in idx:
        yield data.iloc[start:stop]
        start = stop + 1
    yield data.iloc[start:]


def iterate_icao24_callsign(data):
    for _, chunk in data.groupby(["icao24", "callsign"]):
        yield chunk


# class FlightCollection
class FlightCollection:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return f"FlightCollection with {len(self)} flights"

    @classmethod
    def read_json(cls, filename):
        return cls(pd.read_json(filename))

    def __iter__(self):
        for group in iterate_icao24_callsign(self.data):
            for elt in iterate_time(group, 20000):
                yield Flight(elt)

    def __len__(self):
        return sum(1 for _ in self)

    def __getitem__(self, key):
        if isinstance(key, str):
            result = FlightCollection(
                self.data.query("callsign == @key or icao24 == @key")
            )
        if isinstance(key, pd.Timestamp):
            before = key
            after = key + timedelta(days=1)
            result = FlightCollection(self.data.query("@before < timestamp < @after"))

        if len(result) == 1:
            return Flight(result.data)
        else:
            return result

    def filter_by_icao24_only(self):
        """Itère sur les vols groupés par icao24 seulement (plus efficace)"""
        for icao24, group in self.data.groupby("icao24"):
            if len(group) > 1:  # Au moins 2 points pour une trajectoire
                yield Flight(group)

    def filter_landings(self):
        """Retourne les vols d'atterrissage"""
        landings = []
        for flight in self.filter_by_icao24_only():
            if flight.is_landing() and flight.has_valid_trajectory():
                landings.append(flight)
        return landings

    def filter_takeoffs(self):
        """Retourne les vols de décollage"""
        takeoffs = []
        for flight in self.filter_by_icao24_only():
            if flight.is_takeoff() and flight.has_valid_trajectory():
                takeoffs.append(flight)
        return takeoffs

    def get_statistics(self):
        """Retourne les statistiques de la collection"""
        total_flights = 0
        landings = 0
        takeoffs = 0

        for flight in self.filter_by_icao24_only():
            total_flights += 1
            if flight.is_landing():
                landings += 1
            if flight.is_takeoff():
                takeoffs += 1

        return {
            "total_flights": total_flights,
            "landings": landings,
            "takeoffs": takeoffs,
        }


# Class Flight
class Flight:
    def __init__(self, data):
        self.data = data

    def __repr__(self):
        return (
            f"Flight {self.callsign} with aircraft {self.icao24} "
            f"on {self.min('timestamp'):%Y-%m-%d}"
        )

    def __lt__(self, other):
        return self.min("timestamp") <= other.min("timestamp")

    def max(self, feature):
        return self.data[feature].max()

    def min(self, feature):
        return self.data[feature].min()

    @property
    def callsign(self):
        return self.min("callsign")

    @property
    def icao24(self):
        return self.min("icao24")

    def altitude_range(self):
        """Retourne (alt_min, alt_max) pour ce vol"""
        alt_data = self.data["altitude"].dropna()
        if len(alt_data) == 0:
            return None, None
        return alt_data.min(), alt_data.max()

    def vertical_rate_range(self):
        """Retourne (vr_min, vr_max) pour ce vol"""
        vr_data = self.data["vertical_rate"].dropna()
        if len(vr_data) == 0:
            return None, None
        return vr_data.min(), vr_data.max()

    def is_landing(self, ground_altitude_threshold=100, descent_rate_threshold=-1500):
        """Détermine si le vol est un atterrissage"""
        alt_min, alt_max = self.altitude_range()
        vr_min, vr_max = self.vertical_rate_range()

        if alt_min is None or vr_min is None:
            return False

        # Critères: altitude minimale proche du sol ET forte descente
        return alt_min <= ground_altitude_threshold and vr_min <= descent_rate_threshold

    def is_takeoff(self, ground_altitude_threshold=100, climb_rate_threshold=3000):
        """Détermine si le vol est un décollage"""
        alt_min, alt_max = self.altitude_range()
        vr_min, vr_max = self.vertical_rate_range()

        if alt_min is None or vr_max is None:
            return False

        # Critères: altitude minimale proche du sol ET forte montée
        return alt_min <= ground_altitude_threshold and vr_max >= climb_rate_threshold

    def get_trajectory(self):
        """Retourne les coordonnées de la trajectoire avec timestamp"""
        trajectory = (
            self.data[
                ["latitude", "longitude", "altitude", "timestamp", "vertical_rate"]
            ]
            .dropna(subset=["latitude", "longitude", "altitude"])
            .copy()
        )

        if len(trajectory) > 0:
            trajectory["timestamp_dt"] = pd.to_datetime(
                trajectory["timestamp"], unit="s"
            )
            trajectory = trajectory.sort_values("timestamp_dt")

        return trajectory

    def has_valid_trajectory(self):
        """Vérifie si le vol a une trajectoire valide"""
        return len(self.get_trajectory()) > 1

    def to_geopandas(self, transformer=None):
        """Convertit la trajectoire en GeoDataFrame"""
        import pyproj
        from shapely.geometry import LineString, Point

        trajectory = self.get_trajectory()
        if len(trajectory) == 0:
            return None

        if transformer is None:
            transformer = pyproj.Transformer.from_crs(
                "EPSG:4326", "EPSG:2154", always_xy=True
            )

        # Conversion des coordonnées
        x_coords, y_coords = transformer.transform(
            trajectory["longitude"].values, trajectory["latitude"].values
        )

        # Filtrage des valeurs aberrantes (région parisienne)
        center_x, center_y = 650000, 6860000
        max_distance = 100000

        valid_mask = (abs(x_coords - center_x) <= max_distance) & (
            abs(y_coords - center_y) <= max_distance
        )

        if not valid_mask.any():
            return None

        # Créer GeoDataFrame avec points et ligne
        trajectory_filtered = trajectory[valid_mask].copy()
        x_filtered = x_coords[valid_mask]
        y_filtered = y_coords[valid_mask]

        trajectory_filtered["x_lambert"] = x_filtered
        trajectory_filtered["y_lambert"] = y_filtered
        trajectory_filtered["geometry"] = [
            Point(x, y) for x, y in zip(x_filtered, y_filtered)
        ]

        gdf = gpd.GeoDataFrame(trajectory_filtered, crs="EPSG:2154")

        # Ajouter la ligne de trajectoire
        if len(gdf) > 1:
            coords = [(row.x_lambert, row.y_lambert) for _, row in gdf.iterrows()]
            line_gdf = gpd.GeoDataFrame(
                [{"icao24": self.icao24, "geometry": LineString(coords)}],
                crs="EPSG:2154",
            )
            return gdf, line_gdf

        return gdf, None


# %%
# Chargement optimisé des données ADS-B
print("\nChargement en cours...")
data = []
with gzip.open(
    "adsb25/orly.jsonl.gz", "rt", encoding="utf-8", errors="ignore"
) as f:
    for line in f:
        if line.strip():
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue
# Pensez au cp1252 si pb sur un pc
df = pd.DataFrame(data)
print(f"Loaded: {df.shape}")

# %%
# Recherche des colonnes d'altitude
print("\nColonnes contenant 'alt':")
alt_cols = [col for col in df.columns if "alt" in col.lower()]
for col in alt_cols:
    print(f"  {col}: {df[col].notna().sum()} valeurs non-null")

# Histogrammes avec règle de Sturges (nombre optimal de bins)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Règle de Sturges: k = 1 + log2(n)
alt_data = df["altitude"].dropna()
vr_data = df["vertical_rate"].dropna()
bins_alt = int(1 + np.log2(len(alt_data)))
bins_vr = int(1 + np.log2(len(vr_data)))

# Histogramme altitude
alt_data.hist(bins=bins_alt, ax=ax1)
ax1.set_title(f"Distribution Altitude (bins={bins_alt})")
ax1.set_xlabel("Altitude (ft)")

# Histogramme vertical_rate
vr_data.hist(bins=bins_vr, ax=ax2)
ax2.set_title(f"Distribution Vitesse Verticale (bins={bins_vr})")
ax2.set_xlabel("Vertical Rate (ft/min)")

plt.tight_layout()
plt.savefig("histogrammes_adsb.png", dpi=300)
plt.show()

# %%
# Analyse orientée objet avec FlightCollection
print("\nAnalyse orientée objet avec FlightCollection")

# Créer FlightCollection
flight_collection = FlightCollection(df)

# Obtenir les statistiques
stats = flight_collection.get_statistics()
print(f"Total des vols: {stats['total_flights']}")
print(f"Atterrissages: {stats['landings']}")
print(f"Décollages: {stats['takeoffs']}")

# Extraire les vols d'atterrissage et de décollage
print("\nExtraction des trajectoires...")
landing_flights = flight_collection.filter_landings()
takeoff_flights = flight_collection.filter_takeoffs()

print(f"Vols d'atterrissage avec trajectoires: {len(landing_flights)}")
print(f"Vols de décollage avec trajectoires: {len(takeoff_flights)}")

# Exemples de trajectoires
if landing_flights:
    example_landing = landing_flights[0]
    traj = example_landing.get_trajectory()
    print(f"\nExemple atterrissage {example_landing.icao24}:")
    print(f"  Points de trajectoire: {len(traj)}")
    alt_min, alt_max = example_landing.altitude_range()
    print(f"  Altitude: {alt_min:.0f}-{alt_max:.0f} ft")

if takeoff_flights:
    example_takeoff = takeoff_flights[0]
    traj = example_takeoff.get_trajectory()
    print(f"\nExemple décollage {example_takeoff.icao24}:")
    print(f"  Points de trajectoire: {len(traj)}")
    alt_min, alt_max = example_takeoff.altitude_range()
    print(f"  Altitude: {alt_min:.0f}-{alt_max:.0f} ft")

# %%
# Visualisation orientée objet avec FlightCollection
print("\nVisualisation orientée objet avec FlightCollection")

# Transformer pour les coordonnées
transformer = pyproj.Transformer.from_crs("EPSG:4326", "EPSG:2154", always_xy=True)

# Convertir les trajectoires d'atterrissage en GeoDataFrames
landing_points_list = []
landing_lines_list = []

print("Conversion des atterrissages")
for i, flight in enumerate(landing_flights):  # Tous les vols d'atterrissage
    result = flight.to_geopandas(transformer)
    if result and result[0] is not None:
        points_gdf, line_gdf = result
        landing_points_list.append(points_gdf)
        if line_gdf is not None:
            landing_lines_list.append(line_gdf)

# Convertir les trajectoires de décollage en GeoDataFrames
takeoff_points_list = []
takeoff_lines_list = []

print("Conversion des décollages")
for i, flight in enumerate(takeoff_flights):  # Tous les vols de décollage
    result = flight.to_geopandas(transformer)
    if result and result[0] is not None:
        points_gdf, line_gdf = result
        takeoff_points_list.append(points_gdf)
        if line_gdf is not None:
            takeoff_lines_list.append(line_gdf)

# Combiner les GeoDataFrames
if landing_points_list:
    gdf_landing_points = pd.concat(landing_points_list, ignore_index=True)
    print(f"Points d'atterrissage: {len(gdf_landing_points)}")
else:
    gdf_landing_points = None

if landing_lines_list:
    gdf_landing_lines = pd.concat(landing_lines_list, ignore_index=True)
    print(f"Lignes d'atterrissage: {len(gdf_landing_lines)}")
else:
    gdf_landing_lines = None

if takeoff_points_list:
    gdf_takeoff_points = pd.concat(takeoff_points_list, ignore_index=True)
    print(f"Points de décollage: {len(gdf_takeoff_points)}")
else:
    gdf_takeoff_points = None

if takeoff_lines_list:
    gdf_takeoff_lines = pd.concat(takeoff_lines_list, ignore_index=True)
    print(f"Lignes de décollage: {len(gdf_takeoff_lines)}")
else:
    gdf_takeoff_lines = None

# %%
# Carte finale combinée avec approche orientée objet
print("\nCarte finale combinée")

fig, ax = plt.subplots(figsize=(15, 12))

# Fond de carte IGN
gdf_route.plot(
    column="area", ax=ax, cmap="OrRd", edgecolor="orange", legend=False, alpha=0.3
)
gdf_airport.plot(ax=ax, color="blue", markersize=50, legend=False, alpha=0.7)
gdf_limite_region_departement.plot(
    ax=ax, color="black", edgecolor="black", legend=False, alpha=0.5
)

# Trajectoires d'atterrissage en rouge
if gdf_landing_points is not None:
    gdf_landing_points.plot(
        ax=ax, color="red", markersize=1, alpha=0.4, label="Points atterrissage"
    )
if gdf_landing_lines is not None:
    gdf_landing_lines.plot(
        ax=ax, color="red", linewidth=1.5, alpha=0.6, label="Trajectoires atterrissage"
    )

# Trajectoires de décollage en vert
if gdf_takeoff_points is not None:
    gdf_takeoff_points.plot(
        ax=ax, color="green", markersize=1, alpha=0.4, label="Points décollage"
    )
if gdf_takeoff_lines is not None:
    gdf_takeoff_lines.plot(
        ax=ax, color="green", linewidth=1.5, alpha=0.6, label="Trajectoires décollage"
    )

# Calculer les limites pour le zoom
all_x = []
all_y = []

if gdf_landing_points is not None:
    all_x.extend(
        [gdf_landing_points["x_lambert"].min(), gdf_landing_points["x_lambert"].max()]
    )
    all_y.extend(
        [gdf_landing_points["y_lambert"].min(), gdf_landing_points["y_lambert"].max()]
    )

if gdf_takeoff_points is not None:
    all_x.extend(
        [gdf_takeoff_points["x_lambert"].min(), gdf_takeoff_points["x_lambert"].max()]
    )
    all_y.extend(
        [gdf_takeoff_points["y_lambert"].min(), gdf_takeoff_points["y_lambert"].max()]
    )

# Ajuster le zoom
if all_x and all_y:
    margin = 5000  # 5km de marge
    ax.set_xlim(min(all_x) - margin, max(all_x) + margin)
    ax.set_ylim(min(all_y) - margin, max(all_y) + margin)

plt.title(
    "Trajectoires ADS-B - Approche Orientée Objet\nAtterrissages (rouge) et Décollages (vert) - Orly",
    fontsize=14,
)
plt.legend(loc="upper right")
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(
    f"Visualisation terminée - {len(landing_flights)} atterrissages, {len(takeoff_flights)} décollages"
)
