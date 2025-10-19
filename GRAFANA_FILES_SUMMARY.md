# 📁 Fichiers Grafana - Résumé

## ✅ Fichiers générés avec succès

### 🗺️ Dashboard Grafana (Prêt à l'import)
```
grafana_dashboard_adsb_final.json          (2.0 MB)
```
**Contenu** : Dashboard complet avec 45 trajectoires embarquées  
**Import** : Dashboards → Import → Upload JSON file  

---

### 📊 Données CSV (Sources)

#### Atterrissages
```
sample_trajectory_for_grafana.csv          (1.2 MB)
```
- **22 trajectoires** d'atterrissage
- **10 302 points** de données
- Couleur recommandée : 🔴 Rouge

#### Décollages
```
takeoffs_trajectory_for_grafana.csv        (1.1 MB)
```
- **23 trajectoires** de décollage  
- **10 067 points** de données
- Couleur recommandée : 🟢 Vert

---

### 🔧 Scripts Python

#### Script principal
```
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py
```
Fonctions disponibles :
- `export_sample_data_csv()` - Export atterrissages
- `export_takeoffs_csv()` - Export décollages
- `generate_requirements_txt()` - Génère requirements.txt

#### Script export décollages
```
export_takeoffs.py
```
Utilisation : `python export_takeoffs.py`

---

### 📖 Documentation

```
README_GRAFANA_DASHBOARD.md
```
Guide complet d'utilisation du dashboard

```
GRAFANA_FILES_SUMMARY.md
```
Ce fichier - Liste des fichiers générés

---

## 🎯 Fichier original exporté

```
ADS-B Flight Trajectories Dashboard-1760902951681.json
```
*(Renommé en grafana_dashboard_adsb_final.json)*

---

## 🚀 Quick Start

### 1. Import rapide dans Grafana
```bash
# Fichier à importer :
grafana_dashboard_adsb_final.json
```

### 2. Régénérer les données
```bash
# Atterrissages + décollages
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py

# Ou uniquement décollages
python export_takeoffs.py
```

### 3. Lire la documentation
```bash
README_GRAFANA_DASHBOARD.md
```

---

## 📊 Statistiques totales

| Type | Trajectoires | Points | Fichier |
|------|--------------|--------|---------|
| 🔴 Atterrissages | 22 | 10 302 | sample_trajectory_for_grafana.csv |
| 🟢 Décollages | 23 | 10 067 | takeoffs_trajectory_for_grafana.csv |
| **TOTAL** | **45** | **20 369** | - |

---

## 🗂️ Arborescence

```
TP_FINAL/
├── grafana_dashboard_adsb_final.json          # ← À IMPORTER
├── sample_trajectory_for_grafana.csv          # Données atterrissages
├── takeoffs_trajectory_for_grafana.csv        # Données décollages
├── ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py  # Script export
├── export_takeoffs.py                         # Script décollages
├── README_GRAFANA_DASHBOARD.md                # Documentation
└── GRAFANA_FILES_SUMMARY.md                   # Ce fichier
```

---

## ✨ Prochaines étapes

1. ✅ **Import du dashboard** dans Grafana
2. ✅ **Visualisation** des 45 trajectoires
3. 🎨 **Personnalisation** (couleurs, layers, tooltips)
4. 📊 **Ajout de panels** (altitude profile, table)
5. 🔗 **Connexion DB** (InfluxDB/PostgreSQL pour temps réel)

---

**Dashboard créé le** : 19 octobre 2025  
**Version Grafana** : 12.2.0  
**Aéroport** : Paris-Orly (LFPO)
