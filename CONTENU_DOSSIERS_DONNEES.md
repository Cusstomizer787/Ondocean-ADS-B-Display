# 📂 Contenu des Dossiers de Données

**Projet** : Analyse des trajectoires ADS-B - Aéroport d'Orly  
**Date** : 19 octobre 2025

---

## 📁 Dossier adsb25/

**Chemin** : `c:\Users\ncuss\Documents\GitHub\pyclass\TP_FINAL\adsb25\`

### Liste des fichiers

| Fichier | Description | Utilisation |
|---------|-------------|-------------|
| **orly.jsonl.gz** ⭐ | Données ADS-B Orly | **PRINCIPAL** - 16/10/2025 15h-16h |
| guyancourt.jsonl.gz | Données ADS-B Guyancourt | Station complémentaire |
| meudon.jsonl.gz | Données ADS-B Meudon | Station complémentaire |
| montmartre.jsonl.gz | Données ADS-B Montmartre | Station complémentaire |
| montsouris.jsonl.gz | Données ADS-B Montsouris | Station complémentaire |
| palaiseau.jsonl.gz | Données ADS-B Palaiseau | Station complémentaire |
| versailles_48.8012_2.1156.jsonl.gz | Données ADS-B Versailles | Station complémentaire |

### Fichier principal : orly.jsonl.gz

**Caractéristiques** :
- **Format** : JSON Lines (JSONL) compressé avec gzip
- **Période** : 16 octobre 2025, 15h00 - 16h00
- **Taille** : ~50 MB (compressé)
- **Contenu** : Messages ADS-B bruts

**Structure des données** :
```json
{
  "timestamp": 1729092000.123,
  "icao24": "3c6654",
  "callsign": "AFR1234",
  "latitude": 48.7262,
  "longitude": 2.3650,
  "altitude": 1500.0,
  "vertical_rate": -500.0,
  "ground_speed": 250.0,
  "track": 180.0
}
```

**Champs disponibles** :
- `timestamp` : Unix timestamp (secondes depuis epoch)
- `icao24` : Code ICAO24 unique de l'aéronef
- `callsign` : Indicatif du vol (ex: AFR1234)
- `latitude` : Latitude WGS84 (degrés décimaux)
- `longitude` : Longitude WGS84 (degrés décimaux)
- `altitude` : Altitude barométrique (pieds)
- `vertical_rate` : Taux de montée/descente (pieds/minute)
- `ground_speed` : Vitesse sol (nœuds)
- `track` : Cap magnétique (degrés)

### Stations complémentaires

Les autres fichiers contiennent des données des stations ADS-B environnantes :

**Coverage géographique** :
- **Orly** : Aéroport principal (48.7262°N, 2.3650°E)
- **Guyancourt** : Ouest de Paris (48.7714°N, 2.0742°E)
- **Meudon** : Sud-ouest de Paris (48.8094°N, 2.2356°E)
- **Montmartre** : Nord de Paris (48.8867°N, 2.3431°E)
- **Montsouris** : Sud de Paris (48.8219°N, 2.3361°E)
- **Palaiseau** : Sud (48.7144°N, 2.2464°E)
- **Versailles** : Ouest (48.8012°N, 2.1156°E)

**Utilisation** :
Ces stations permettent une couverture redondante et étendue de la région parisienne. Elles peuvent être utilisées pour :
- Validation croisée des données
- Extension de la couverture géographique
- Analyse multi-stations

---

## 📁 Dossier jet1090/

**Chemin** : `c:\Users\ncuss\Documents\GitHub\pyclass\TP_FINAL\jet1090\`

**Statut** : ❌ Dossier non trouvé dans le projet actuel

### Si le dossier existe, il pourrait contenir :

**Fichiers attendus** :
```
jet1090/
├── config.json              # Configuration du récepteur jet1090
├── logs/                    # Logs de réception
│   ├── 2025-10-16.log
│   └── ...
├── data/                    # Données brutes reçues
│   ├── raw_messages.jsonl
│   └── ...
└── scripts/                 # Scripts de traitement
    ├── decode_messages.py
    └── ...
```

**jet1090** est typiquement :
- Un logiciel de réception/décodage ADS-B
- Utilisé pour capturer les messages en temps réel
- Peut générer des fichiers JSONL similaires à ceux du dossier adsb25/

### Si vous avez des données jet1090 :

**Intégration possible** :
1. Placer les fichiers JSONL dans `jet1090/`
2. Modifier les scripts pour lire depuis `jet1090/` au lieu de `adsb25/`
3. Documenter les différences de format (si existantes)

**Exemple d'utilisation dans le code** :
```python
# Option 1: Lire depuis adsb25
data_path = "adsb25/orly.jsonl.gz"

# Option 2: Lire depuis jet1090
data_path = "jet1090/orly_realtime.jsonl"

# Chargement identique
flight_collection = FlightCollectionGrafana.read_jsonl_gz(data_path)
```

---

## 📊 Comparaison des Sources

| Aspect | adsb25/ | jet1090/ |
|--------|---------|----------|
| **Format** | JSONL gzip | JSONL (non compressé) |
| **Source** | Archive/Dataset | Temps réel |
| **Période** | Fixe (16/10/2025) | Variable |
| **Taille** | ~50 MB/fichier | Dépend de la durée |
| **Utilisation** | Analyse historique | Capture temps réel |

---

## 🔄 Lecture des Données dans le Code

### Méthode 1 : Lecture depuis adsb25/ (Actuelle)

```python
from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import FlightCollectionGrafana

# Lecture du fichier principal
fc = FlightCollectionGrafana.read_jsonl_gz("adsb25/orly.jsonl.gz")

print(f"Nombre de vols détectés : {len(fc)}")
```

### Méthode 2 : Lecture depuis jet1090/ (Si disponible)

```python
# Si jet1090 utilise le même format
fc = FlightCollectionGrafana.read_jsonl_gz("jet1090/orly_capture.jsonl.gz")

# Ou si format non compressé
import pandas as pd
data = pd.read_json("jet1090/orly_capture.jsonl", lines=True)
fc = FlightCollectionGrafana(data)
```

### Méthode 3 : Lecture multi-sources

```python
# Combiner plusieurs sources
sources = [
    "adsb25/orly.jsonl.gz",
    "adsb25/montmartre.jsonl.gz",
    "adsb25/meudon.jsonl.gz"
]

all_data = []
for source in sources:
    fc = FlightCollectionGrafana.read_jsonl_gz(source)
    all_data.append(fc.data)

# Fusionner toutes les données
combined_data = pd.concat(all_data, ignore_index=True)
fc_combined = FlightCollectionGrafana(combined_data)
```

---

## 📋 Vérification des Données

### Script de vérification

Créer un fichier `verify_data.py` :

```python
import os
import gzip
import json

def verify_adsb25():
    """Vérifie l'intégrité des fichiers adsb25"""
    folder = "adsb25"
    
    if not os.path.exists(folder):
        print(f"❌ Dossier {folder}/ introuvable")
        return False
    
    files = os.listdir(folder)
    print(f"✅ Dossier {folder}/ trouvé")
    print(f"   Fichiers : {len(files)}")
    
    for file in files:
        if file.endswith('.jsonl.gz'):
            filepath = os.path.join(folder, file)
            try:
                with gzip.open(filepath, 'rt') as f:
                    first_line = f.readline()
                    data = json.loads(first_line)
                    print(f"   ✅ {file} - OK (champs: {list(data.keys())})")
            except Exception as e:
                print(f"   ❌ {file} - Erreur: {e}")
    
    return True

def verify_jet1090():
    """Vérifie l'existence du dossier jet1090"""
    folder = "jet1090"
    
    if not os.path.exists(folder):
        print(f"❌ Dossier {folder}/ introuvable")
        return False
    
    files = os.listdir(folder)
    print(f"✅ Dossier {folder}/ trouvé")
    print(f"   Fichiers : {len(files)}")
    
    return True

if __name__ == "__main__":
    print("=== Vérification des données ===\n")
    verify_adsb25()
    print()
    verify_jet1090()
```

Exécution :
```bash
python verify_data.py
```

---

## 📦 Archive des Données

### Sauvegarder adsb25/

```bash
# Windows
Compress-Archive -Path adsb25 -DestinationPath adsb25_backup.zip

# Linux/Mac
tar -czf adsb25_backup.tar.gz adsb25/
```

### Restaurer adsb25/

```bash
# Windows
Expand-Archive -Path adsb25_backup.zip -DestinationPath .

# Linux/Mac
tar -xzf adsb25_backup.tar.gz
```

---

## 🔍 Exploration des Données

### Commandes utiles

```bash
# Compter les lignes (messages ADS-B) dans orly.jsonl.gz
zcat adsb25/orly.jsonl.gz | wc -l          # Linux/Mac
# Windows: utiliser 7-Zip ou Python

# Voir les premiers messages
zcat adsb25/orly.jsonl.gz | head -n 5

# Extraire un échantillon
zcat adsb25/orly.jsonl.gz | head -n 1000 > sample.jsonl
```

### Script Python d'exploration

```python
import gzip
import json
import pandas as pd

# Charger un échantillon
with gzip.open('adsb25/orly.jsonl.gz', 'rt') as f:
    sample = [json.loads(line) for line in f.readlines()[:1000]]

df = pd.DataFrame(sample)

print("Aperçu des données:")
print(df.head())
print("\nStatistiques:")
print(df.describe())
print("\nICAO24 uniques:", df['icao24'].nunique())
print("Callsigns uniques:", df['callsign'].nunique())
```

---

## ✅ Checklist Données

### Vérifications à effectuer

- [ ] Dossier `adsb25/` présent
- [ ] Fichier `adsb25/orly.jsonl.gz` présent et lisible
- [ ] Format JSON valide dans orly.jsonl.gz
- [ ] Dossier `jet1090/` (si applicable)
- [ ] Données couvrent la période 16/10/2025 15h-16h
- [ ] Champs essentiels présents (latitude, longitude, altitude)
- [ ] Pas de corruption des fichiers gzip

---

---

## 🗺️ Dossier ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03/

**Chemin** : `c:\Users\ncuss\Documents\GitHub\pyclass\TP_FINAL\ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03\`

### Description

**Données géographiques IGN ROUTE500** - Base de données cartographique pour fond de carte France.

**Version** : ROUTE500 v3.0  
**Projection** : Lambert-93 (EPSG:2154)  
**Format** : Shapefiles (.shp + .dbf + .shx + .prj)  
**Source** : Institut Géographique National (IGN)  
**Date livraison** : Novembre 2021

### Structure du dossier

```
ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03/
├── ROUTE500.md5                              # Vérification intégrité
└── ROUTE500/
    ├── LISEZ-MOI.pdf                         # ⭐ Documentation officielle IGN
    ├── 1_DONNEES_LIVRAISON_2022-01-00175/   # 📂 Données principales
    │   ├── 1_DONNEES_LIVRAISON_2022-01-00175.md5
    │   └── R500_3-0_SHP_LAMB93_FXX-ED211/
    │       ├── RESEAU_ROUTIER/
    │       │   ├── AERODROME.shp                 # ⭐ Aéroports (Orly inclus)
    │       │   ├── AERODROME.dbf
    │       │   ├── AERODROME.shx
    │       │   ├── AERODROME.prj
    │       │   ├── TRONCON_ROUTE.shp             # ⭐ Réseau routier (autoroutes)
    │       │   ├── TRONCON_ROUTE.dbf
    │       │   ├── TRONCON_ROUTE.shx
    │       │   ├── TRONCON_ROUTE.prj
    │       │   └── ... (autres couches routieres)
    │       ├── ADMINISTRATIF/
    │       │   ├── LIMITE_ADMINISTRATIVE.shp     # ⭐ Départements/Régions
    │       │   ├── LIMITE_ADMINISTRATIVE.dbf
    │       │   ├── LIMITE_ADMINISTRATIVE.shx
    │       │   ├── LIMITE_ADMINISTRATIVE.prj
    │       │   └── ... (autres couches admin)
    │       └── HABILLAGE/
    │           ├── ZONE_OCCUPATION_SOL.shp       # ⭐ Zones bâties
    │           ├── ZONE_OCCUPATION_SOL.dbf
    │           ├── ZONE_OCCUPATION_SOL.shx
    │           ├── ZONE_OCCUPATION_SOL.prj
    │           └── ... (autres couches habillage)
    ├── 2_METADONNEES_LIVRAISON_2022-01-00175/
    │   └── Métadonnées XML
    └── 3_SUPPLEMENTS_LIVRAISON_2022-01-00175/
        └── Documents supplémentaires
```

### Shapefiles utilisés dans le projet

#### 1. AERODROME.shp ⭐

**Utilisation** : Localiser l'aéroport d'Orly et les autres aéroports de la région

**Attributs principaux** :
- `TOPONYME` : Nom de l'aérodrome (ex: "Orly")
- `NATURE` : Type (aérodrome, héliport, etc.)
- `geometry` : Géométrie (Point ou Polygon)

**Filtrage dans le code** :
```python
gdf_airport = gpd.read_file(path_to_airport)
gdf_airport = gdf_airport[gdf_airport["TOPONYME"].notna()]
```

#### 2. TRONCON_ROUTE.shp ⭐

**Utilisation** : Afficher le réseau autoroutier comme contexte

**Attributs principaux** :
- `CLASS_ADM` : Classification administrative ("Autoroute", "Route nationale", etc.)
- `geometry` : LineString

**Filtrage dans le code** :
```python
gdf_route = gpd.read_file(path_to_route, encoding="cp1252")
gdf_route = gdf_route.query('CLASS_ADM == "Autoroute"')
```

#### 3. LIMITE_ADMINISTRATIVE.shp ⭐

**Utilisation** : Afficher les limites de départements et régions

**Attributs principaux** :
- `NATURE` : Type de limite ("Limite de département", "Limite de région")
- `geometry` : LineString

**Filtrage dans le code** :
```python
gdf_limite_admin = gpd.read_file(path_to_admin)
gdf_limite_region_departement = gdf_limite_admin[
    gdf_limite_admin["NATURE"].isin(["Limite de département", "Limite de région"])
]
```

#### 4. ZONE_OCCUPATION_SOL.shp ⭐

**Utilisation** : Afficher les zones urbaines bâties

**Attributs principaux** :
- `NATURE` : Type d'occupation ("Bâti", "Forêt", "Eau", etc.)
- `geometry` : Polygon

**Filtrage dans le code** :
```python
gdf_occupation = gpd.read_file(path_to_occupation)
gdf_occupation = gdf_occupation.query('NATURE == "Bâti"')
```

### Configuration dans le code

**Chemin dans le script** (`ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py`) :

```python
base_path = r"C:\Users\ncuss\Documents\GitHub\pyclass\TP_FINAL\ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03\ROUTE500\1_DONNEES_LIVRAISON_2022-01-00175\R500_3-0_SHP_LAMB93_FXX-ED211"

path_to_airport = rf"{base_path}\RESEAU_ROUTIER\AERODROME.shp"
path_to_route = rf"{base_path}\RESEAU_ROUTIER\TRONCON_ROUTE.shp"
path_to_admin = rf"{base_path}\ADMINISTRATIF\LIMITE_ADMINISTRATIVE.shp"
path_to_occupation = rf"{base_path}\HABILLAGE\ZONE_OCCUPATION_SOL.shp"
```

### Projection Lambert-93

**Code EPSG** : 2154  
**Projection** : Lambert Conformal Conic  
**Datum** : RGF93 (Réseau Géodésique Français 1993)  
**Unités** : Mètres

**Conversion depuis WGS84** (utilisée pour les données ADS-B) :
```python
import pyproj

# Définir les projections
wgs84 = pyproj.CRS("EPSG:4326")    # Latitude/Longitude
lambert93 = pyproj.CRS("EPSG:2154") # Lambert-93

# Créer le transformateur
transformer = pyproj.Transformer.from_crs(wgs84, lambert93, always_xy=True)

# Convertir des coordonnées
lon, lat = 2.3650, 48.7262  # Orly en WGS84
x, y = transformer.transform(lon, lat)
print(f"Orly en Lambert-93: x={x:.2f}m, y={y:.2f}m")
```

### Zone géographique couverte

**Centrage sur Paris** :
```python
center_x, center_y = 652000, 6860000  # Coordonnées Lambert-93 (en mètres)
delta = 25000  # Rayon ~50 km

# Définir les limites de visualisation
ax.set_xlim(center_x - delta, center_x + delta)
ax.set_ylim(center_y - delta, center_y + delta)
```

Cette configuration centre la carte sur Paris avec un rayon de 50 km, couvrant :
- Paris intra-muros
- Petite couronne (92, 93, 94)
- Aéroports : Orly, Le Bourget, Villacoublay

### Taille des données

| Élément | Taille |
|---------|--------|
| Archive compressée (.7z) | ~500 MB |
| Dossier décompressé | ~2 GB |
| AERODROME.shp | ~200 KB |
| TRONCON_ROUTE.shp | ~150 MB |
| LIMITE_ADMINISTRATIVE.shp | ~50 MB |
| ZONE_OCCUPATION_SOL.shp | ~800 MB |

### Licence et source

**Source** : Institut Géographique National (IGN)  
**Produit** : ROUTE500®  
**Licence** : Licence Ouverte / Open Licence  
**URL** : https://geoservices.ign.fr/route500

**Licence Ouverte** permet :
- ✅ Reproduction, redistribution
- ✅ Adaptation, modification
- ✅ Exploitation commerciale
- ❗ Mention obligatoire : "Source: IGN - ROUTE500®"

### Vérification de l'intégrité

**Fichier MD5** : `ROUTE500.md5`

```bash
# Windows (PowerShell)
Get-FileHash -Algorithm MD5 "ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03.7z"

# Linux/Mac
md5sum ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03.7z

# Comparer avec ROUTE500.md5
```

### Extraction de l'archive

**Windows** :
```powershell
# Avec 7-Zip installé
7z x ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03.7z
```

**Linux/Mac** :
```bash
7z x ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03.7z
```

### Alternatives sans IGN

Si les données IGN ne sont pas disponibles, le script peut fonctionner sans fond de carte :

```python
# Option 1: Utiliser un fond de carte en ligne (Contextily)
import contextily as ctx

ax = gdf.plot(figsize=(10, 10))
ctx.add_basemap(ax, crs=gdf.crs, source=ctx.providers.OpenStreetMap.Mapnik)

# Option 2: Afficher uniquement les trajectoires
fig, ax = plt.subplots(figsize=(10, 10))
for flight in flights:
    traj = flight.get_trajectory()
    ax.plot(traj['longitude'], traj['latitude'])
```

---

**Document créé le** : 19 octobre 2025  
**Auteurs** : Nicolas Cusseau et Emile Bleicher
