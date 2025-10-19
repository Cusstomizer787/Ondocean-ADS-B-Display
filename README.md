# Projet ADS-B Orly - Suivi des Trajectoires

**Mastère Spécialisé ILEMS**  
Analyse des trajectoires d'atterrissage et de décollage à l'aéroport Paris-Orly

---

## 🚀 Quick Start

### Visualiser les trajectoires
```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
```

### Exporter pour Grafana
```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py      # Atterrissages + décollages
python export_takeoffs.py                                       # Décollages uniquement
```

### Importer dans Grafana
1. Grafana → Dashboards → Import
2. Upload `grafana_dashboard_adsb_final.json`

---

## 📊 Résultats

| Type | Trajectoires | Points |
|------|--------------|--------|
| 🔴 Atterrissages | 22 | 10 302 |
| 🟢 Décollages | 23 | 10 067 |
| **Total** | **45** | **20 369** |

**Données** : 16 octobre 2025, 15h-16h  
**Aéroport** : Paris-Orly (LFPO)

---

## 🏗️ Architecture

### Classes POO

```python
class Flight:
    """Un vol individuel avec ses points ADS-B"""
    - is_landing()      # Détecte atterrissage
    - is_takeoff()      # Détecte décollage
    - get_trajectory()  # Retourne trajectoire

class FlightCollection:
    """Collection de vols avec filtrage"""
    - filter_landings()   # Filtre atterrissages
    - filter_takeoffs()   # Filtre décollages
    - get_statistics()    # Statistiques
```

**Critères de détection** :
- **Atterrissage** : altitude ≤ 100 ft ET vertical_rate ≤ -1500 ft/min
- **Décollage** : altitude ≤ 100 ft ET vertical_rate ≥ 3000 ft/min

---

## 📁 Fichiers Clés

### Scripts
- `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py` ⭐ - Architecture POO principale
- `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py` - Export Grafana
- `export_takeoffs.py` - Export décollages

### Données
- `adsb25/orly.jsonl.gz` - Données ADS-B sources
- `sample_trajectory_for_grafana.csv` - Atterrissages
- `takeoffs_trajectory_for_grafana.csv` - Décollages

### Dashboard
- `grafana_dashboard_adsb_final.json` - Dashboard complet (2 MB)

### Documentation
- `PROJET_ADSB_RESUME.md` ⭐ - Résumé complet du projet
- `INDEX_DOCUMENTATION.md` - Index de toute la doc
- `README_GRAFANA_DASHBOARD.md` - Guide Grafana
- `DIAGRAMMES_PLANTUML.md` - Guide des diagrammes

### Diagrammes PlantUML
- `architecture_classes.puml` - Classes UML
- `workflow_traitement.puml` - Workflow complet
- `pipeline_data.puml` - Pipeline de données
- `structure_projet.puml` - Structure fichiers

---

## 🔧 Technologies

**Python** : pandas, geopandas, matplotlib, shapely, pyproj  
**Grafana** : TestData DB, Geomap panel (v12.2.0)  
**Géomatique** : IGN Route500, Lambert-93, WGS84

---

## 📖 Documentation Complète

Pour plus de détails, consultez :
- **Vue d'ensemble** → `PROJET_ADSB_RESUME.md`
- **Index documentation** → `INDEX_DOCUMENTATION.md`
- **Guide Grafana** → `README_GRAFANA_DASHBOARD.md`

---

## 📐 Visualiser les Diagrammes

```bash
# PlantUML Online
http://www.plantuml.com/plantuml/

# Ou avec VSCode + Extension PlantUML
Alt+D sur un fichier .puml
```

---

## 🎯 Parcours Recommandés

### Comprendre le Projet
1. `README.md` (ce fichier)
2. `PROJET_ADSB_RESUME.md`
3. `architecture_classes.puml`

### Utiliser le Code
1. `tests5_clean.py` (code source)
2. `architecture_classes.puml` (architecture)
3. `tests_Grafana.py` (export)

### Visualiser dans Grafana
1. `README_GRAFANA_DASHBOARD.md` (guide)
2. Import `grafana_dashboard_adsb_final.json`
3. Personnalisation

---

**Projet académique** - Mastère Spécialisé ILEMS  
**Auteur** : Nicolas Cusseau et Emile Bleicher 
**Date** : Octobre 2025
