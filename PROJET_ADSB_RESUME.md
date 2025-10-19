# Projet ADS-B Orly - Suivi des Trajectoires

**Mastère Spécialisé ILEMS**  
**Date** : 16 octobre 2025, 15h-16h  
**Aéroport** : Paris-Orly (LFPO)

---

## 🎯 Objectif

Analyse et visualisation des trajectoires d'atterrissage et de décollage à l'aéroport d'Orly à partir de données ADS-B.

---

## 📂 Structure du Projet

### Données Sources
```
adsb25/orly.jsonl.gz
```
- **Format** : JSON Lines compressé (gzip)
- **Contenu** : Messages ADS-B bruts (position, altitude, vitesse)
- **Période** : 16/10/2025 15h-16h

### Scripts Principaux

#### 1. **ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau.py** - Script Initial
- Première implémentation fonctionnelle
- Analyse et filtrage des trajectoires
- Visualisation matplotlib

#### 2. **ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py** - Version POO ⭐
- Architecture Orientée Objet propre
- Classes `Flight` et `FlightCollection`
- Code réutilisable et maintenable

#### 3. **ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py** - Export Grafana
- Classe `FlightCollectionGrafana` (hérite de `FlightCollection`)
- Export CSV pour visualisation Grafana
- Fonctions : `export_sample_data_csv()`, `export_takeoffs_csv()`

#### 4. **Scripts Utilitaires**
- `export_takeoffs.py` : Export décollages standalone
- `export_all_trajectories.py` : Export atterrissages standalone

---

## 🏗️ Architecture POO

### Classe `Flight`
Représente un vol individuel.

**Attributs** :
- `data` : DataFrame pandas avec les points ADS-B
- `icao24` : Code ICAO de l'aéronef
- `callsign` : Indicatif du vol

**Méthodes principales** :
- `is_landing()` : Détecte si c'est un atterrissage
- `is_takeoff()` : Détecte si c'est un décollage  
- `get_trajectory()` : Retourne la trajectoire (lat, lon, alt, timestamp)
- `to_geopandas()` : Convertit en GeoDataFrame pour visualisation

**Critères de détection** :
- **Atterrissage** : `altitude_min ≤ 100 ft` ET `vertical_rate_min ≤ -1500 ft/min`
- **Décollage** : `altitude_min ≤ 100 ft` ET `vertical_rate_max ≥ 3000 ft/min`

### Classe `FlightCollection`
Collection de vols avec méthodes de filtrage.

**Méthodes principales** :
- `filter_landings()` : Retourne les atterrissages
- `filter_takeoffs()` : Retourne les décollages
- `get_statistics()` : Statistiques (total, atterrissages, décollages)
- `__iter__()` : Itération sur les vols
- `__getitem__()` : Accès par callsign ou icao24

---

## 📊 Résultats

### Statistiques
- **Total vols détectés** : ~460
- **Atterrissages** : 22 trajectoires (10 302 points)
- **Décollages** : 23 trajectoires (10 067 points)

### Visualisations

#### 1. **Matplotlib** (tests5_clean.py)
- Fond de carte IGN Route500 (Lambert-93)
- Trajectoires atterrissage : 🔴 Rouge
- Trajectoires décollage : 🟢 Vert
- Points au sol : 🔵 Bleu

#### 2. **Grafana** (Dashboard interactif)
- Panel Geomap avec 2 layers
- Données CSV embarquées
- Fichier : `grafana_dashboard_adsb_final.json`

---

## 📁 Fichiers Générés

### CSV Grafana
```
sample_trajectory_for_grafana.csv     (22 atterrissages)
takeoffs_trajectory_for_grafana.csv   (23 décollages)
```

### Dashboard Grafana
```
grafana_dashboard_adsb_final.json     (2 MB, prêt à l'import)
```

### Documentation
```
README_GRAFANA_DASHBOARD.md           (Guide complet)
GRAFANA_FILES_SUMMARY.md              (Résumé fichiers)
PROJET_ADSB_RESUME.md                 (Ce fichier)
```

---

## 🔧 Technologies Utilisées

### Python
- **pandas** : Manipulation de données
- **geopandas** : Données géospatiales
- **matplotlib** : Visualisation
- **shapely** : Géométries (Point, LineString)
- **pyproj** : Projections cartographiques

### Grafana
- **TestData DB** : Source de données CSV
- **Geomap Panel** : Visualisation cartographique
- **Version** : 12.2.0

### Données Géographiques
- **IGN Route500** : Fond de carte France
- **Lambert-93** (EPSG:2154) : Projection cartographique
- **WGS84** (EPSG:4326) : Coordonnées GPS

---

## 🚀 Utilisation

### Régénérer les CSV
```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py    # Atterrissages + décollages
python export_takeoffs.py                                     # Décollages uniquement
```

### Visualiser avec Matplotlib
```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
```

### Importer dans Grafana
1. Grafana → Dashboards → Import
2. Upload `grafana_dashboard_adsb_final.json`
3. Import

---

## 📐 Diagrammes

Voir les fichiers PlantUML :
- `architecture_classes.puml` : Architecture POO
- `workflow_traitement.puml` : Workflow de traitement
- `pipeline_data.puml` : Pipeline de données

---

## 🎓 Concepts Appliqués

### Programmation Orientée Objet
- Encapsulation (Flight, FlightCollection)
- Héritage (FlightCollectionGrafana)
- Itérateurs (`__iter__`, `__getitem__`)
- Propriétés (`@property`)

### Traitement de Données
- Lecture JSONL compressé
- Filtrage et agrégation
- Détection de patterns (atterrissage/décollage)
- Export multi-formats (CSV, GeoJSON)

### Géomatique
- Projections cartographiques (WGS84 ↔ Lambert-93)
- Shapefiles IGN
- Visualisation géospatiale

---

## 📌 Points Clés

✅ **Architecture modulaire** : Code réutilisable et maintenable  
✅ **POO propre** : Classes avec responsabilités claires  
✅ **Multi-visualisation** : Matplotlib + Grafana  
✅ **Performance** : Gestion efficace de ~20k points  
✅ **Documentation** : Code commenté + README complets
