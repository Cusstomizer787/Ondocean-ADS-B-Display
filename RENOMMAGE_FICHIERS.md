# 🔄 Renommage des Fichiers - Nomenclature Académique

**Date** : 19 octobre 2025  
**Auteurs** : Nicolas Cusseau et Emile Bleicher  
**Formation** : Mastère Spécialisé ILEMS - ECE 6ILM4

---

## ✅ Fichiers Renommés

### Scripts Principaux

| Ancien Nom | Nouveau Nom | Description |
|------------|-------------|-------------|
| `tests5.py` | `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau.py` | Version initiale fonctionnelle |
| `tests5_clean.py` | `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py` | Architecture POO (Flight & FlightCollection) |
| `tests_Grafana.py` | `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py` | Export Grafana |

---

## 📝 Nomenclature Adoptée

**Format** : `ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_[SUFFIXE].py`

### Éléments du nom
- **ILEMS2025** : Formation et année
- **ECE** : École (École Centrale-Supélec Executive Education)
- **6ILM4** : Code du cours
- **TA** : Type d'activité (Travail Autonome)
- **Bleicher_Cusseau** : Noms des auteurs (ordre alphabétique)
- **[SUFFIXE]** : Identification du contenu
  - *(vide)* : Version initiale
  - **OO** : Orienté Objet (POO)
  - **GRAFANA** : Export Grafana

---

## 🔄 Mises à Jour Effectuées

### 1. Documentation Markdown

#### **README.md**
- ✅ Quick start : `python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py`
- ✅ Export Grafana : `python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py`
- ✅ Fichiers clés : Références mises à jour

#### **PROJET_ADSB_RESUME.md**
- ✅ Section Scripts Principaux : 3 fichiers renommés
- ✅ Section Utilisation : Commandes mises à jour

#### **INDEX_DOCUMENTATION.md**
- ✅ Documentation Code : Références aux nouveaux noms
- ✅ Navigation par besoin : Liens mis à jour
- ✅ Navigation par profil : Chemins mis à jour

---

### 2. Diagrammes PlantUML

#### **structure_projet.puml**
- ✅ Scripts Principaux : 3 fichiers renommés
- ✅ Relations entre fichiers : Références mises à jour
- ✅ Légende : Fichiers clés mis à jour
- ✅ Suppression émojis pour compatibilité PlantUML

#### **pipeline_data.puml**
- ✅ Suppression émojis et accents (compatibilité PlantUML)

---

### 3. Scripts Python

#### **export_takeoffs.py**
```python
# Avant
from tests_Grafana import export_takeoffs_csv

# Après
from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import export_takeoffs_csv
```

#### **export_all_trajectories.py**
```python
# Avant
from tests_Grafana import export_sample_data_csv

# Après
from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import export_sample_data_csv
```

---

## 📊 Statistiques

### Fichiers Renommés
- **3 fichiers Python** principaux

### Fichiers Modifiés
- **3 fichiers Markdown** (.md)
- **2 fichiers PlantUML** (.puml)
- **2 scripts utilitaires** (.py)
- **Total** : 7 fichiers mis à jour

### Références Changées
- **~25 occurrences** de `tests5.py` / `tests5_clean.py`
- **~30 occurrences** de `tests_Grafana.py`

---

## 🎯 Cohérence du Projet

### Fichiers avec Nouvelle Nomenclature ✅
```
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau.py
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py
```

### Scripts Utilitaires (Inchangés)
```
export_takeoffs.py
export_all_trajectories.py
```

### Données (Inchangées)
```
sample_trajectory_for_grafana.csv
takeoffs_trajectory_for_grafana.csv
grafana_dashboard_adsb_final.json
```

---

## ✅ Vérifications Post-Renommage

### Imports Python
- [x] `export_takeoffs.py` : Import mis à jour
- [x] `export_all_trajectories.py` : Import mis à jour
- [x] Aucune erreur d'import

### Documentation
- [x] README.md : Toutes les références mises à jour
- [x] PROJET_ADSB_RESUME.md : Toutes les références mises à jour
- [x] INDEX_DOCUMENTATION.md : Toutes les références mises à jour

### Diagrammes
- [x] structure_projet.puml : Références et émojis corrigés
- [x] pipeline_data.puml : Émojis et accents supprimés
- [x] Compatibilité PlantUML : OK

---

## 🚀 Utilisation Post-Renommage

### Exécuter le script POO
```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
```

### Exporter pour Grafana
```bash
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py
```

### Ou utiliser les scripts utilitaires
```bash
python export_takeoffs.py           # Décollages
python export_all_trajectories.py   # Atterrissages
```

---

## 📌 Points d'Attention

### ⚠️ Si vous clonez le projet
Les anciens noms (`tests5.py`, `tests5_clean.py`, `tests_Grafana.py`) n'existent plus. Utilisez les nouveaux noms.

### ⚠️ Si vous avez des imports
Mettez à jour vos imports :
```python
# Ancien
from tests_Grafana import FlightCollectionGrafana

# Nouveau
from ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA import FlightCollectionGrafana
```

---

## 🎓 Contexte Académique

Ce renommage s'inscrit dans le cadre du **Travail Autonome** du cours **6ILM4** au sein du **Mastère Spécialisé ILEMS** de l'**ECE Paris**, promotion 2025.

**Objectif** : Analyse et visualisation des trajectoires ADS-B à l'aéroport d'Orly.

**Encadrants** : [À compléter]  
**Date de remise** : [À compléter]

---

**Document créé le** : 19 octobre 2025  
**Auteurs** : Nicolas Cusseau et Emile Bleicher
