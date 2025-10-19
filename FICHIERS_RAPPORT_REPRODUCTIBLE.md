# 📋 Fichiers Nécessaires pour un Rapport Reproductible

**Projet** : Analyse des trajectoires ADS-B - Aéroport d'Orly  
**Auteurs** : Nicolas Cusseau et Emile Bleicher  
**Formation** : Mastère Spécialisé ILEMS - ECE 6ILM4  
**Date** : 19 octobre 2025

---

## 📁 Structure des Fichiers Essentiels

### 1. **Scripts Python Principaux** ⭐

```
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau.py         # Version initiale
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py      # Architecture POO (PRINCIPAL)
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py # Export Grafana
```

**Description** :
- **_OO.py** : Classes `Flight` et `FlightCollection` (POO)
- **_GRAFANA.py** : Export CSV pour visualisation Grafana
- Ancien nom : `tests5_clean.py` → maintenant `_OO.py`

---

### 2. **Scripts Utilitaires**

```
export_takeoffs.py              # Export décollages standalone
export_all_trajectories.py      # Export atterrissages standalone
```

---

### 3. **Données Sources** (Sous-dossier adsb25/)

```
adsb25/
├── orly.jsonl.gz                               # ⭐ PRINCIPAL - Données Orly
├── guyancourt.jsonl.gz
├── meudon.jsonl.gz
├── montmartre.jsonl.gz
├── montsouris.jsonl.gz
├── palaiseau.jsonl.gz
└── versailles_48.8012_2.1156.jsonl.gz
```

**Fichier principal** : `adsb25/orly.jsonl.gz`
- Format : JSON Lines compressé (gzip)
- Contenu : Messages ADS-B bruts du 16/10/2025 15h-16h
- Taille : ~50 MB

---

### 4. **Données Exportées** (Générées par les scripts)

```
sample_trajectory_for_grafana.csv       # 22 atterrissages (10 302 points)
takeoffs_trajectory_for_grafana.csv     # 23 décollages (10 067 points)
```

**Format CSV** :
```
timestamp_dt,latitude,longitude,altitude,vertical_rate,flight_id,icao24,callsign
```

---

### 5. **Dashboard Grafana**

```
grafana_dashboard_adsb_final.json       # Dashboard complet (2 MB, données embarquées)
```

**Contenu** :
- 2 Queries (A: atterrissages, B: décollages)
- 2 Layers Geomap (rouge/vert)
- Données CSV embarquées

---

### 6. **Documentation Markdown**

```
README.md                               # ⭐ Point d'entrée principal
PROJET_ADSB_RESUME.md                   # ⭐ Résumé complet du projet
INDEX_DOCUMENTATION.md                  # Index de toute la documentation
README_GRAFANA_DASHBOARD.md             # Guide Grafana
GRAFANA_FILES_SUMMARY.md                # Résumé fichiers Grafana
RENOMMAGE_FICHIERS.md                   # Documentation du renommage
FICHIERS_RAPPORT_REPRODUCTIBLE.md       # Ce fichier
```

---

### 7. **Diagrammes PlantUML**

```
architecture_classes.puml               # Architecture POO (UML)
workflow_traitement.puml                # Workflow de traitement
pipeline_data.puml                      # Pipeline de données
structure_projet.puml                   # Structure des fichiers
```

**Versions simplifiées** (backup) :
```
architecture_classes_simple.puml
workflow_traitement_simple.puml
pipeline_data_simple.puml
structure_projet_simple.puml
```

---

### 8. **Visualisations générées**

```
carte_trajectoires_orly_complete.png    # Carte Matplotlib avec trajectoires
carte_trajectoires_orly_complete.pdf    # Version PDF
architecture_classes.png                # Diagramme UML exporté
```

---

### 9. **Données Géographiques IGN ROUTE500** ⭐ (Essentiel pour visualisation)

#### Archive originale
```
ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03.7z         # Archive compressée (~500 MB)
```

#### Dossier décompressé
```
ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03/
├── ROUTE500/
│   ├── 1_DONNEES_LIVRAISON_2022-01-00175/
│   │   └── R500_3-0_SHP_LAMB93_FXX-ED211/
│   │       ├── RESEAU_ROUTIER/
│   │       │   ├── AERODROME.shp               # ⭐ Aéroports
│   │       │   ├── TRONCON_ROUTE.shp           # ⭐ Autoroutes
│   │       │   └── ... (+ fichiers .dbf, .shx, .prj)
│   │       ├── ADMINISTRATIF/
│   │       │   ├── LIMITE_ADMINISTRATIVE.shp   # ⭐ Départements/régions
│   │       │   └── ...
│   │       └── HABILLAGE/
│   │           ├── ZONE_OCCUPATION_SOL.shp     # ⭐ Bâti
│   │           └── ...
│   ├── 2_METADONNEES_LIVRAISON_2022-01-00175/
│   ├── 3_SUPPLEMENTS_LIVRAISON_2022-01-00175/
│   └── LISEZ-MOI.pdf                        # Documentation IGN
└── ROUTE500.md5                                 # Vérification intégrité
```

**Utilisation** : 
- Fond de carte IGN pour visualisation Matplotlib
- Projection : Lambert-93 (EPSG:2154)
- Shapefiles utilisés dans `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py`

**Fichiers essentiels pour le projet** :
1. `AERODROME.shp` - Localisation des aéroports (dont Orly)
2. `TRONCON_ROUTE.shp` - Réseau routier (autoroutes)
3. `LIMITE_ADMINISTRATIVE.shp` - Limites départements/régions
4. `ZONE_OCCUPATION_SOL.shp` - Zones bâties

**Taille** : ~2 GB (décompressé), ~500 MB (compressé)

---

### 10. **Sous-dossier jet1090** (À ajouter si disponible)

```
jet1090/
└── [Fichiers jet1090 à documenter]
```

**Note** : Ce dossier n'existe pas actuellement dans le projet.

---

## 📦 Fichiers de Configuration

### Requirements Python ⭐

**Fichier** : `requirements.txt` (CRÉÉ)

Liste complète de toutes les dépendances du projet.

**Dépendances essentielles** :
- pandas>=2.0.0
- numpy>=1.24.0
- geopandas>=0.13.0
- shapely>=2.0.0
- pyproj>=3.5.0
- fiona>=1.9.0
- matplotlib>=3.7.0
- seaborn>=0.12.0

**Dépendances optionnelles** (commentées dans le fichier) :
- influxdb-client (pour Grafana avec InfluxDB)
- psycopg2-binary (pour Grafana avec PostgreSQL)
- sqlalchemy (pour bases de données)
- contextily (pour cartes web)
- jupyter (pour notebooks)

**Installation** :
```bash
pip install -r requirements.txt
```

---

### Workflow de Développement 🌊

**Fichiers** :
- `ONDOCEAN-MODE-STRICT-OPERATIONAL-WORKFLOW.md` - Protocole RIPER-5 complet
- `WORKFLOW_DEVELOPPEMENT_WINDSURF.md` - Guide d'utilisation pour le projet (CRÉÉ)

**Protocole RIPER-5** - 5 modes pour développer avec WindSurf/Cascade AI :
1. **RESEARCH** - Comprendre le code existant
2. **INNOVATE** - Brainstorming d'idées
3. **PLAN** - Planification détaillée avec checklist
4. **EXECUTE** - Implémentation stricte du plan
5. **REVIEW** - Vérification de conformité

**Commandes** :
```bash
ENTER RESEARCH MODE  # Pour comprendre
ENTER PLAN MODE      # Pour planifier
ENTER EXECUTE MODE   # Pour implémenter
ENTER REVIEW MODE    # Pour vérifier
```

---

## 🚀 Reproduction du Projet

### Étape 1 : Cloner/Télécharger les fichiers

**Fichiers minimaux requis** :
```
TP_FINAL/
├── ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py       ⭐
├── ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py
├── adsb25/
│   └── orly.jsonl.gz                                    ⭐
├── README.md                                            ⭐
├── PROJET_ADSB_RESUME.md                               ⭐
└── requirements.txt
```

### Étape 2 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 3 : Exécuter le script principal

```bash
cd TP_FINAL
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
```

### Étape 4 : Générer les exports Grafana

```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py
```

### Étape 5 : Visualiser dans Grafana

1. Ouvrir Grafana
2. Dashboards → Import
3. Upload `grafana_dashboard_adsb_final.json`
4. Import

---

## 📊 Résultats Attendus

### Statistiques
- **Total vols détectés** : ~460
- **Atterrissages classifiés** : 22 trajectoires (10 302 points)
- **Décollages classifiés** : 23 trajectoires (10 067 points)
- **Période analysée** : 16/10/2025 15h00-16h00

### Fichiers générés
1. `sample_trajectory_for_grafana.csv` (1.2 MB)
2. `takeoffs_trajectory_for_grafana.csv` (1.1 MB)
3. Visualisation Matplotlib (si IGN disponible)
4. Dashboard Grafana fonctionnel

---

## 📋 Checklist Complétude

### Fichiers Essentiels
- [ ] Scripts Python (3 fichiers `ILEMS2025_*.py`)
- [ ] Données ADS-B (`adsb25/orly.jsonl.gz`)
- [ ] Documentation principale (`README.md`, `PROJET_ADSB_RESUME.md`)
- [ ] Dashboard Grafana (`grafana_dashboard_adsb_final.json`)

### Fichiers Optionnels mais Recommandés
- [ ] Diagrammes PlantUML (4 fichiers `.puml`)
- [ ] Données IGN (shapefiles)
- [ ] Visualisations PNG/PDF
- [ ] Documentation complète (7 fichiers `.md`)

### Fichiers Générés (À recréer)
- [ ] `sample_trajectory_for_grafana.csv`
- [ ] `takeoffs_trajectory_for_grafana.csv`
- [ ] Visualisations Matplotlib

---

## 🔗 Archive Complète

### Pour un rapport reproductible complet

**Fichiers à inclure** (par ordre de priorité) :

#### **Priorité 1 - Essentiels** (≈ 55 MB)
```
1. ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
2. ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py
3. adsb25/orly.jsonl.gz
4. README.md
5. PROJET_ADSB_RESUME.md
6. requirements.txt
```

#### **Priorité 2 - Documentation** (≈ 500 KB)
```
7. INDEX_DOCUMENTATION.md
8. README_GRAFANA_DASHBOARD.md
9. GRAFANA_FILES_SUMMARY.md
10. RENOMMAGE_FICHIERS.md
11. architecture_classes.puml
12. workflow_traitement.puml
13. pipeline_data.puml
14. structure_projet.puml
```

#### **Priorité 3 - Visualisations** (≈ 4 MB)
```
15. grafana_dashboard_adsb_final.json
16. carte_trajectoires_orly_complete.png
17. architecture_classes.png
```

#### **Priorité 4 - Optionnel** (≈ 2 GB)
```
18. ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03/ (Données IGN)
19. Autres fichiers adsb25/*.jsonl.gz
```

---

## 💾 Commandes d'archivage

### Créer une archive minimale (Priorité 1+2)

```bash
# Windows (PowerShell)
Compress-Archive -Path `
  ILEMS2025_*.py, `
  adsb25/, `
  *.md, `
  *.puml, `
  requirements.txt `
  -DestinationPath Projet_ADS-B_Orly_Minimal.zip

# Linux/Mac
tar -czf Projet_ADS-B_Orly_Minimal.tar.gz \
  ILEMS2025_*.py \
  adsb25/ \
  *.md \
  *.puml \
  requirements.txt
```

### Créer une archive complète (avec Grafana)

```bash
# Windows (PowerShell)
Compress-Archive -Path `
  ILEMS2025_*.py, `
  adsb25/, `
  *.md, `
  *.puml, `
  grafana_dashboard_adsb_final.json, `
  *.png, `
  requirements.txt `
  -DestinationPath Projet_ADS-B_Orly_Complet.zip
```

---

## 📝 Notes Importantes

### Fichiers à NE PAS inclure dans le rapport
```
__pycache__/                    # Cache Python
*.pyc                           # Bytecode compilé
Tests2.py, Tests3.py            # Scripts de test
Consignes.txt                   # Fichiers temporaires
*.7z, *.zip                     # Archives intermédiaires
grafana_dashboard_*.json        # Versions anciennes (sauf _final)
```

### Fichiers générés automatiquement
Les fichiers CSV peuvent être régénérés avec :
```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py
```

Donc pas strictement nécessaires dans l'archive source.

---

## ✅ Validation de Complétude

Pour vérifier que vous avez tous les fichiers nécessaires :

```bash
# Vérifier présence des fichiers essentiels
ls ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
ls adsb25/orly.jsonl.gz
ls README.md
ls PROJET_ADSB_RESUME.md

# Tester l'exécution
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
```

Si tout fonctionne, le projet est reproductible ! ✅

---

**Document créé le** : 19 octobre 2025  
**Version** : 1.0  
**Auteurs** : Nicolas Cusseau et Emile Bleicher
