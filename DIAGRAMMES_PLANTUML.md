# Diagrammes PlantUML - Projet ADS-B Orly

## 📐 Fichiers Disponibles

### 1. **architecture_classes.puml**
Diagramme de classes UML montrant l'architecture POO du projet.

**Contenu** :
- Classe `Flight` : Représentation d'un vol individuel
- Classe `FlightCollection` : Collection de vols avec méthodes de filtrage
- Classe `FlightCollectionGrafana` : Extension pour export Grafana
- Relations entre classes (composition, héritage)
- Méthodes principales et attributs

**Utilisation** : Comprendre la structure orientée objet et les responsabilités de chaque classe.

---

### 2. **workflow_traitement.puml**
Diagramme d'activité montrant le flux de traitement des données.

**Contenu** :
- Lecture du fichier JSONL.gz
- Filtrage et groupement des vols
- Classification (atterrissage/décollage)
- Export multi-formats
- Visualisation (Matplotlib + Grafana)

**Utilisation** : Suivre le processus complet de bout en bout.

---

### 3. **pipeline_data.puml**
Diagramme de pipeline montrant la transformation des données.

**Contenu** :
- Source : Messages ADS-B bruts
- Ingestion : Parsing et conversion
- Transformation : Groupement, filtrage, enrichissement
- Export : CSV, GeoDataFrame, Dashboard JSON
- Visualisation : Statique et interactive

**Utilisation** : Comprendre les étapes de transformation des données.

---

### 4. **structure_projet.puml**
Diagramme de structure montrant l'organisation des fichiers.

**Contenu** :
- Arborescence complète du projet
- Scripts Python (principaux, Grafana, utilitaires)
- Données sources et exportées
- Documentation
- Relations entre fichiers

**Utilisation** : Naviguer dans le projet et identifier les fichiers clés.

---

## 🔧 Comment Visualiser

### Option 1 : PlantUML Online
1. Aller sur http://www.plantuml.com/plantuml/
2. Copier-coller le contenu d'un fichier .puml
3. Visualiser le diagramme généré

### Option 2 : Extension VSCode
1. Installer l'extension "PlantUML"
2. Ouvrir un fichier .puml
3. `Alt+D` pour prévisualiser

### Option 3 : CLI PlantUML
```bash
java -jar plantuml.jar architecture_classes.puml
```
Génère un fichier PNG.

---

## 📊 Aperçu des Diagrammes

### Architecture Classes
```
┌─────────────────┐
│ FlightCollection│
│  - data         │
│  + filter_*()   │
└────────┬────────┘
         │ contient
         ▼
    ┌─────────┐
    │ Flight  │
    │ - data  │
    │ + is_*()│
    └─────────┘
```

### Workflow
```
[Données ADS-B]
      ↓
[Filtrage & Classification]
      ↓
[Export CSV + Dashboard]
      ↓
[Visualisation]
```

### Pipeline
```
JSONL.gz → DataFrame → Flight Objects → CSV/JSON → Grafana/Matplotlib
```

---

## 🎯 Utilité par Profil

### Développeur
- `architecture_classes.puml` : Comprendre le code POO
- `pipeline_data.puml` : Flux de données

### Chef de Projet
- `workflow_traitement.puml` : Vue d'ensemble du processus
- `structure_projet.puml` : Organisation du projet

### Analyste Données
- `pipeline_data.puml` : Transformation des données
- `workflow_traitement.puml` : Critères de classification

---

## 📝 Génération Automatique

Pour régénérer tous les diagrammes en PNG :

```bash
# Linux/Mac
for f in *.puml; do java -jar plantuml.jar "$f"; done

# Windows PowerShell
Get-ChildItem -Filter *.puml | ForEach-Object { java -jar plantuml.jar $_.FullName }
```

---

## 🔗 Références

- **PlantUML** : https://plantuml.com/
- **Syntaxe** : https://plantuml.com/guide
- **Exemples** : https://real-world-plantuml.com/
