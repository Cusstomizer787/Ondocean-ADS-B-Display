# Dashboard Grafana ADS-B - Trajectoires d'Orly

## 📊 Description

Dashboard Grafana visualisant les trajectoires d'atterrissage et de décollage à l'aéroport d'Orly à partir de données ADS-B.

## 📁 Fichiers

### Dashboard Grafana
- **`grafana_dashboard_adsb_final.json`** : Dashboard Grafana complet (2MB)
  - Contient les données CSV embarquées des 45 trajectoires (22 atterrissages + 23 décollages)
  - Prêt à l'import dans Grafana
  - Version Grafana : 12.2.0

### Données CSV
- **`sample_trajectory_for_grafana.csv`** : 22 trajectoires d'atterrissage (10 302 points)
- **`takeoffs_trajectory_for_grafana.csv`** : 23 trajectoires de décollage (10 067 points)

### Scripts d'export
- **`ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py`** : Script principal avec les fonctions d'export
- **`export_takeoffs.py`** : Script pour exporter uniquement les décollages

## 🚀 Utilisation

### Import du Dashboard

1. Ouvrez Grafana
2. Menu **Dashboards** → **Import**
3. Cliquez sur **Upload JSON file**
4. Sélectionnez `grafana_dashboard_adsb_final.json`
5. Configurez la data source si demandé : **TestData DB**
6. Cliquez sur **Import**

### Visualisation

Le dashboard affiche :
- **🔴 Trajectoires d'atterrissage (rouge)** : 22 vols
- **🟢 Trajectoires de décollage (vert)** : 23 vols
- **📍 Carte centrée sur Orly** (48.7262°N, 2.3650°E)

### Régénérer les données CSV

Pour mettre à jour les données avec de nouvelles trajectoires :

```bash
# Export des atterrissages
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py

# Export des décollages
python export_takeoffs.py
```

## 📋 Structure du Dashboard

### Panel : Geomap
- **Type** : Geomap
- **Data Source** : TestData DB
- **Queries** :
  - Query A : Atterrissages (CSV Content)
  - Query B : Décollages (CSV Content)

### Layers
1. **Layer 1 - Atterrissages**
   - Type : Markers
   - Couleur : Rouge (#FF0000)
   - Location Mode : Coords (latitude, longitude)

2. **Layer 2 - Décollages**
   - Type : Markers
   - Couleur : Vert (#00FF00)
   - Location Mode : Coords (latitude, longitude)

## 🔧 Configuration

### Données Sources
- **Fichier source** : `adsb25/orly.jsonl.gz`
- **Format** : ADS-B messages (JSON Lines compressé)
- **Période** : 16 octobre 2025

### Filtres appliqués
- Atterrissages : Altitude finale < 500 ft + Vertical Rate < -200 ft/min
- Décollages : Altitude finale > 20000 ft + Vertical Rate > 200 ft/min

### Champs exportés
- `timestamp_dt` : Horodatage (format ISO, arrondi à la seconde)
- `latitude` : Latitude (degrés décimaux)
- `longitude` : Longitude (degrés décimaux)
- `altitude` : Altitude (pieds)
- `vertical_rate` : Taux de montée/descente (ft/min)
- `flight_id` : Identifiant unique du vol
- `icao24` : Code ICAO24 de l'aéronef
- `callsign` : Indicatif du vol

## 🎨 Personnalisation

### Changer les couleurs
1. Éditez le panel
2. Map Layers → Cliquez sur le layer
3. Styles → Color → Sélectionnez une nouvelle couleur

### Modifier la vue
1. Map view → Ajustez Latitude, Longitude, Zoom
2. Basemap → Choisissez un fond de carte (OpenStreetMap, etc.)

### Ajouter des tooltips
1. Layer options → Tooltip → Activez
2. Les informations (altitude, callsign) s'afficheront au survol

## 📊 Statistiques

- **Total trajectoires** : 45 (22 atterrissages + 23 décollages)
- **Total points de données** : 20 369
- **Aéroport** : Paris-Orly (LFPO)
- **Zone géographique** : Région parisienne

## 🛠️ Dépendances

### Python
```
pandas>=1.3.0
numpy>=1.21.0
geopandas>=0.10.0
```

### Grafana
- Version : 12.2.0 ou supérieure
- Plugin requis : TestData (inclus par défaut)

## 📝 Notes

- Le fichier JSON contient les données CSV embarquées pour faciliter l'import
- La taille du fichier (2MB) est normale car il inclut ~20 000 points de données
- Pour des performances optimales, utilisez des layers **Route** au lieu de **Markers** si vous avez beaucoup de points
- Le timestamp est arrondi à la seconde pour compatibilité Grafana

## 🔗 Évolutions possibles

1. **Connexion base de données** : Remplacer CSV par InfluxDB ou PostgreSQL
2. **Temps réel** : Intégrer un flux ADS-B en direct
3. **Panels additionnels** :
   - Altitude Profile (time series)
   - Flight Data Table
   - Statistiques (nombre de vols, altitude moyenne, etc.)
4. **Filtres dynamiques** : Ajouter des variables Grafana (période, airline, etc.)

## 📄 Licence

Projet académique - TP Final Python
