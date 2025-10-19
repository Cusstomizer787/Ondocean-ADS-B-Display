# 📁 Contenu du Dossier Rapport

**Projet** : Analyse des trajectoires ADS-B - Aéroport d'Orly  
**Auteurs** : Nicolas Cusseau et Emile Bleicher  
**Formation** : Mastère Spécialisé ILEMS - ECE 6ILM4  
**Date** : 19 octobre 2025

---

## 📋 Résumé

Ce dossier contient **tous les fichiers nécessaires** pour le rapport final et la reproductibilité du projet.

**Nombre total de fichiers** : 44 fichiers + 7 fichiers dans adsb25/

---

## 🐍 Scripts Python (5 fichiers)

### Scripts Principaux (3 fichiers)

| Fichier | Taille | Description |
|---------|--------|-------------|
| `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau.py` | 26 KB | Version initiale fonctionnelle |
| `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py` | 16 KB | **Architecture POO** (classes Flight & FlightCollection) |
| `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py` | 33 KB | Export Grafana avec InfluxDB/PostgreSQL |

### Scripts Utilitaires (2 fichiers)

| Fichier | Taille | Description |
|---------|--------|-------------|
| `export_takeoffs.py` | 289 B | Export décollages standalone |
| `export_all_trajectories.py` | 288 B | Export atterrissages standalone |

---

## 📊 Données (Dossier adsb25/)

**Taille totale** : ~350 MB (7 fichiers compressés .jsonl.gz)

| Fichier | Description |
|---------|-------------|
| **orly.jsonl.gz** ⭐ | **PRINCIPAL** - Données ADS-B Orly 16/10/2025 15h-16h |
| guyancourt.jsonl.gz | Station complémentaire Guyancourt |
| meudon.jsonl.gz | Station complémentaire Meudon |
| montmartre.jsonl.gz | Station complémentaire Montmartre |
| montsouris.jsonl.gz | Station complémentaire Montsouris |
| palaiseau.jsonl.gz | Station complémentaire Palaiseau |
| versailles_48.8012_2.1156.jsonl.gz | Station complémentaire Versailles |

**Note** : Les données IGN ROUTE500 (~2 GB) ne sont **PAS** incluses dans ce dossier (trop volumineuses).

---

## 📈 Données Exportées Grafana (3 fichiers)

| Fichier | Taille | Description |
|---------|--------|-------------|
| `sample_trajectory_for_grafana.csv` | 1.1 MB | 22 atterrissages (10 302 points) |
| `takeoffs_trajectory_for_grafana.csv` | 1.1 MB | 23 décollages (10 067 points) |
| `sample_trajectory_grafana_simple.csv` | 9 KB | Échantillon simplifié |

---

## 📊 Dashboard Grafana (1 fichier)

| Fichier | Taille | Description |
|---------|--------|-------------|
| `grafana_dashboard_adsb_final.json` | 2.3 MB | Dashboard complet avec données embarquées |

**Utilisation** : Grafana → Dashboards → Import → Upload ce fichier

---

## 🗺️ Diagrammes PlantUML (8 fichiers)

### Versions Standard (4 fichiers)

| Fichier | Description |
|---------|-------------|
| `architecture_classes.puml` | Diagramme UML des classes POO |
| `workflow_traitement.puml` | Workflow de traitement des données |
| `pipeline_data.puml` | Pipeline de données ADS-B |
| `structure_projet.puml` | Structure des fichiers du projet |

### Versions Simplifiées (4 fichiers)

| Fichier | Description |
|---------|-------------|
| `architecture_classes_simple.puml` | Version simplifiée UML |
| `workflow_traitement_simple.puml` | Version simplifiée workflow |
| `pipeline_data_simple.puml` | Version simplifiée pipeline |
| `structure_projet_simple.puml` | Version simplifiée structure |

---

## 🖼️ Visualisations (9 fichiers)

### Images PNG (6 fichiers)

| Fichier | Taille | Description |
|---------|--------|-------------|
| `carte_trajectoires_orly_complete.png` | 1.2 MB | **Carte principale** avec trajectoires complètes |
| `fond_carte_orly_trajectoires.png` | 1.1 MB | Carte avec fond IGN |
| `carte_fond_trajectoires.png` | 685 KB | Carte alternative |
| `carte_ign_simple.png` | 440 KB | Fond de carte IGN simplifié |
| `histogrammes_adsb.png` | 110 KB | Histogrammes d'analyse |
| `architecture_classes.png` | 52 KB | Diagramme UML exporté |
| `pipeline_data.png` | 49 KB | Pipeline de données exporté |
| `workflow_traitement.png` | 48 KB | Workflow exporté |
| `structure_projet.png` | 131 KB | Structure projet exportée |

### Documents PDF (2 fichiers)

| Fichier | Taille | Description |
|---------|--------|-------------|
| `carte_trajectoires_orly_complete.pdf` | 70 KB | Version PDF carte principale |
| `fond_carte_orly_trajectoires.pdf` | 63 KB | Version PDF carte avec fond |

---

## 📚 Documentation (18 fichiers Markdown)

### Documentation Principale (5 fichiers)

| Fichier | Description |
|---------|-------------|
| `README.md` ⭐ | **Point d'entrée** du projet |
| `PROJET_ADSB_RESUME.md` ⭐ | **Résumé complet** du projet |
| `INDEX_DOCUMENTATION.md` | Index de toute la documentation |
| `FICHIERS_RAPPORT_REPRODUCTIBLE.md` | Liste des fichiers pour reproductibilité |
| `CONTENU_DOSSIERS_DONNEES.md` | Documentation des données (adsb25/, IGN, jet1090) |

### Documentation Technique (5 fichiers)

| Fichier | Description |
|---------|-------------|
| `RENOMMAGE_FICHIERS.md` | Historique du renommage des scripts |
| `DIAGRAMMES_PLANTUML.md` | Documentation des diagrammes |
| `FICHIERS_CREES.md` | Liste des fichiers créés |
| `README_IGN_trajectoires.md` | Documentation IGN ROUTE500 |
| `CONTENU_DOSSIER_RAPPORT.md` | Ce fichier |

### Documentation Grafana (4 fichiers)

| Fichier | Description |
|---------|-------------|
| `README_GRAFANA_DASHBOARD.md` | Guide complet Grafana |
| `GRAFANA_FILES_SUMMARY.md` | Résumé des fichiers Grafana |
| `GRAFANA_IMPORT_INSTRUCTIONS.md` | Instructions d'import |
| `GRAFANA_SETUP.md` | Configuration Grafana |

### Workflow de Développement (2 fichiers)

| Fichier | Description |
|---------|-------------|
| `WORKFLOW_DEVELOPPEMENT_WINDSURF.md` | Guide workflow RIPER-5 pour le projet |
| `ONDOCEAN-MODE-STRICT-OPERATIONAL-WORKFLOW.md` | Protocole RIPER-5 complet |

---

## ⚙️ Configuration (1 fichier)

| Fichier | Description |
|---------|-------------|
| `requirements.txt` | Dépendances Python (pandas, geopandas, matplotlib, etc.) |

---

## 📊 Statistiques du Dossier

### Par Type de Fichier

| Type | Nombre | Taille Totale |
|------|--------|---------------|
| Scripts Python (.py) | 5 | ~77 KB |
| Documentation (.md) | 18 | ~94 KB |
| Diagrammes (.puml) | 8 | ~12 KB |
| Données ADS-B (.jsonl.gz) | 7 | ~350 MB |
| Données Grafana (.csv, .json) | 4 | ~4.6 MB |
| Visualisations (.png, .pdf) | 11 | ~3.9 MB |
| Configuration (.txt) | 1 | ~1 KB |
| **TOTAL** | **54** | **~359 MB** |

### Taille Totale du Dossier

**~360 MB** (sans IGN ROUTE500)

**Note** : Si vous ajoutez IGN ROUTE500, la taille totale serait :
- ~2.5 GB (avec ROUTE500 décompressé)
- ~860 MB (avec ROUTE500 compressé .7z)

---

## ✅ Fichiers Essentiels pour le Rapport

### Priorité 1 - Indispensables

```
✅ ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
✅ adsb25/orly.jsonl.gz
✅ README.md
✅ PROJET_ADSB_RESUME.md
✅ carte_trajectoires_orly_complete.png
✅ requirements.txt
```

### Priorité 2 - Importants

```
✅ Tous les fichiers .puml (diagrammes)
✅ grafana_dashboard_adsb_final.json
✅ Documentation Grafana
✅ Workflow de développement
```

### Priorité 3 - Complémentaires

```
✅ Autres stations adsb25 (guyancourt, meudon, etc.)
✅ Scripts utilitaires
✅ Versions simplifiées des diagrammes
```

---

## 🚀 Utilisation du Dossier Rapport

### Pour reproduire le projet

1. **Copier tout le dossier Rapport** sur une nouvelle machine
2. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
3. **Exécuter le script principal** :
   ```bash
   python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
   ```

**Note** : Les visualisations avec fond de carte IGN ne fonctionneront pas sans les données ROUTE500.

### Pour importer dans Grafana

1. Ouvrir Grafana
2. Dashboards → Import
3. Upload `grafana_dashboard_adsb_final.json`
4. Import

---

## 📝 Fichiers NON Inclus

### Données IGN ROUTE500 (volontairement exclues)

**Raison** : Trop volumineux (~2 GB décompressé)

**Fichiers exclus** :
```
❌ ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03/ (~2 GB)
❌ ROUTE500_3-0__SHP_LAMB93_FXX_2021-11-03.7z (~500 MB)
```

**Impact** : Les visualisations avec fond de carte IGN ne pourront pas être régénérées sans ces données.

**Solution** : Télécharger séparément depuis https://geoservices.ign.fr/route500

---

## 🔍 Vérification d'Intégrité

### Script de vérification

Un script `verify_data.py` est disponible dans le dossier parent pour vérifier l'intégrité :

```bash
cd ..
python verify_data.py
```

### Vérification manuelle

```bash
# Vérifier la présence des fichiers essentiels
ls ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
ls adsb25/orly.jsonl.gz
ls README.md

# Compter les fichiers
ls -la | wc -l  # Linux/Mac
(Get-ChildItem).Count  # Windows PowerShell
```

---

## 📦 Archivage

### Créer une archive du dossier Rapport

**Windows (PowerShell)** :
```powershell
Compress-Archive -Path Rapport -DestinationPath Projet_ADS-B_Orly_Rapport_Final.zip
```

**Linux/Mac** :
```bash
tar -czf Projet_ADS-B_Orly_Rapport_Final.tar.gz Rapport/
```

**Taille archive attendue** : ~300 MB (compression ~15%)

---

## 📧 Livraison du Rapport

### Contenu à livrer

1. **Archive complète** : `Projet_ADS-B_Orly_Rapport_Final.zip` (~300 MB)
2. **README.md** (ce fichier) pour navigation
3. **Note sur IGN ROUTE500** : Données non incluses (trop volumineuses)

### Formats de livraison

- **Clé USB** : Recommandé (copie directe ~360 MB)
- **Cloud** : Google Drive / OneDrive / Dropbox
- **Git** : Possible mais exclure adsb25/ (trop gros pour GitHub)

---

## 🎓 Contexte Académique

**Formation** : Mastère Spécialisé ILEMS  
**École** : ECE Paris  
**Cours** : 6ILM4 - Travail Autonome  
**Promotion** : 2025  
**Sujet** : Analyse et visualisation des trajectoires ADS-B à l'aéroport d'Orly

---

**Document créé le** : 19 octobre 2025  
**Auteurs** : Nicolas Cusseau et Emile Bleicher  
**Version** : 1.0 - Dossier Rapport Final
