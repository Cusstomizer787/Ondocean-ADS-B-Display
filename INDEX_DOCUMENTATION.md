# 📚 Index de la Documentation - Projet ADS-B Orly

**Mastère Spécialisé ILEMS**  
**Suivi des trajectoires d'atterrissages et de décollages - Aéroport d'Orly**

---

## 🎯 Lecture Rapide

**Nouveau sur le projet ?** Commencez ici :
1. 📖 `PROJET_ADSB_RESUME.md` - **Vue d'ensemble complète**
2. 📐 `architecture_classes.puml` - **Architecture POO**
3. 🗺️ `README_GRAFANA_DASHBOARD.md` - **Dashboard Grafana**

---

## 📁 Documentation Générale

### **PROJET_ADSB_RESUME.md** ⭐
Résumé complet et concis du projet.

**Contenu** :
- Objectif et contexte
- Architecture POO (Flight, FlightCollection)
- Résultats et statistiques
- Technologies utilisées
- Guide d'utilisation

**Pour qui** : Vue d'ensemble pour tous les profils

---

### **INDEX_DOCUMENTATION.md**
Ce fichier - Index de toute la documentation disponible.

---

## 🗺️ Documentation Grafana

### **README_GRAFANA_DASHBOARD.md**
Guide complet du dashboard Grafana.

**Contenu** :
- Description du dashboard
- Instructions d'import
- Configuration des panels et layers
- Personnalisation (couleurs, tooltips)
- Évolutions possibles

**Pour qui** : Utilisateurs Grafana

---

### **GRAFANA_FILES_SUMMARY.md**
Résumé des fichiers générés pour Grafana.

**Contenu** :
- Liste des fichiers (JSON, CSV)
- Statistiques (trajectoires, points)
- Quick start
- Arborescence

**Pour qui** : Quick reference

---

## 📐 Diagrammes PlantUML

### **DIAGRAMMES_PLANTUML.md**
Guide des diagrammes PlantUML disponibles.

**Contenu** :
- Liste des 4 diagrammes
- Description de chacun
- Comment les visualiser
- Génération automatique

**Pour qui** : Tous (documentation visuelle)

---

### Fichiers PlantUML

#### **architecture_classes.puml**
Diagramme UML des classes POO.
- Classes Flight, FlightCollection, FlightCollectionGrafana
- Relations et méthodes
- Notes explicatives

#### **workflow_traitement.puml**
Diagramme d'activité du processus complet.
- De la lecture des données à la visualisation
- Classification atterrissage/décollage
- Export multi-formats

#### **pipeline_data.puml**
Pipeline de transformation des données.
- Ingestion → Transformation → Export → Visualisation
- Formats à chaque étape
- Annotations techniques

#### **structure_projet.puml**
Structure des fichiers du projet.
- Arborescence complète
- Relations entre fichiers
- Légende et fichiers clés

---

## 💻 Documentation Code

### Scripts Python Principaux

#### **ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py** ⭐
Script POO principal avec classes Flight et FlightCollection.

**Classes** :
- `Flight` : Représentation d'un vol
- `FlightCollection` : Collection de vols

**Méthodes clés** :
- `is_landing()`, `is_takeoff()`
- `filter_landings()`, `filter_takeoffs()`
- `get_trajectory()`, `to_geopandas()`

---

#### **ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py**
Extension pour export Grafana.

**Classe** :
- `FlightCollectionGrafana` (hérite de FlightCollection)

**Fonctions** :
- `export_sample_data_csv()` : Export atterrissages
- `export_takeoffs_csv()` : Export décollages

---

#### **export_takeoffs.py**
Script standalone pour exporter les décollages.

**Usage** :
```bash
python export_takeoffs.py
```

---

#### **export_all_trajectories.py**
Script standalone pour exporter les atterrissages.

**Usage** :
```bash
python export_all_trajectories.py
```

---

## 📊 Fichiers de Données

### Données Sources

#### **adsb25/orly.jsonl.gz**
Données ADS-B brutes.
- Format : JSON Lines compressé
- Période : 16/10/2025 15h-16h
- Taille : ~50 MB

---

### Données Exportées

#### **sample_trajectory_for_grafana.csv**
22 trajectoires d'atterrissage (10 302 points).

**Colonnes** : timestamp_dt, latitude, longitude, altitude, vertical_rate, flight_id, icao24, callsign

---

#### **takeoffs_trajectory_for_grafana.csv**
23 trajectoires de décollage (10 067 points).

**Colonnes** : (idem atterrissages)

---

#### **grafana_dashboard_adsb_final.json**
Dashboard Grafana complet (2 MB).
- Données CSV embarquées
- 2 Queries (A: atterrissages, B: décollages)
- 2 Layers (rouge, vert)
- Prêt à l'import

---

## 🔍 Navigation Rapide

### Par Besoin

**Je veux comprendre le projet** :
→ `PROJET_ADSB_RESUME.md`

**Je veux voir l'architecture POO** :
→ `architecture_classes.puml`

**Je veux utiliser Grafana** :
→ `README_GRAFANA_DASHBOARD.md`

**Je veux comprendre le code** :
→ `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py` + `architecture_classes.puml`

**Je veux voir le processus complet** :
→ `workflow_traitement.puml`

**Je veux lister les fichiers** :
→ `GRAFANA_FILES_SUMMARY.md`

**Je veux exporter de nouvelles données** :
→ `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py` ou scripts `export_*.py`

---

### Par Profil

**Étudiant / Apprenant** :
1. `PROJET_ADSB_RESUME.md`
2. `architecture_classes.puml`
3. `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py`

**Développeur** :
1. `architecture_classes.puml`
2. `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py`
3. `pipeline_data.puml`

**Chef de Projet** :
1. `PROJET_ADSB_RESUME.md`
2. `workflow_traitement.puml`
3. `GRAFANA_FILES_SUMMARY.md`

**Analyste Données** :
1. `pipeline_data.puml`
2. `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py`
3. `README_GRAFANA_DASHBOARD.md`

---

## 📈 Statistiques Documentation

| Type | Nombre | Taille totale |
|------|--------|---------------|
| Markdown (.md) | 5 | ~50 KB |
| PlantUML (.puml) | 4 | ~15 KB |
| Scripts Python (.py) | 4 | ~30 KB |
| Dashboard JSON | 1 | 2 MB |
| CSV données | 2 | ~2.3 MB |
| **TOTAL** | **16 fichiers** | **~4.4 MB** |

---

## ✅ Checklist Documentation

- [x] Vue d'ensemble (PROJET_ADSB_RESUME.md)
- [x] Architecture POO (architecture_classes.puml)
- [x] Workflow complet (workflow_traitement.puml)
- [x] Pipeline données (pipeline_data.puml)
- [x] Structure projet (structure_projet.puml)
- [x] Guide Grafana (README_GRAFANA_DASHBOARD.md)
- [x] Résumé fichiers (GRAFANA_FILES_SUMMARY.md)
- [x] Guide diagrammes (DIAGRAMMES_PLANTUML.md)
- [x] Index documentation (INDEX_DOCUMENTATION.md)

---

**Dernière mise à jour** : 19 octobre 2025  
**Projet** : Mastère Spécialisé ILEMS - ADS-B Orly
