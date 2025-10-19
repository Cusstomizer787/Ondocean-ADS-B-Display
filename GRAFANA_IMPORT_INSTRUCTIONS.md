# Instructions d'Import et Configuration Grafana Dashboard

## 1. Import du Dashboard

### Fichier à utiliser :
`grafana_dashboard_importable.json`

### Procédure d'import :
1. Ouvrez Grafana : `http://localhost:3000`
2. Menu **"+"** → **"Import"**
3. **"Upload JSON file"** → Sélectionnez `grafana_dashboard_importable.json`
4. **Name** : `ADS-B Flight Trajectories Dashboard` (pré-rempli)
5. **Folder** : Laissez "General" ou choisissez un dossier
6. Cliquez **"Import"**

## 2. Configuration Post-Import

Après l'import, vous verrez 3 panels vides :
- **Flight Trajectories Map** (carte géographique)
- **Altitude Profile** (graphique temporel)
- **Flight Data Table** (tableau de données)

### Étape 1: Ajouter les données CSV

Pour chaque panel :

1. **Cliquez sur le titre du panel** → **"Edit"** (icône crayon)
2. Dans l'onglet **"Query"** :
   - **Data source** : `TestData DB` (déjà configuré)
   - **Scenario** : `CSV Content` (déjà configuré)
3. Dans le champ **"CSV Content"** :
   - Effacez le contenu actuel (header seulement)
   - Copiez-collez **tout le contenu** de `sample_trajectory_for_grafana.csv`
4. Cliquez **"Apply"**

### Étape 2: Vérification des Configurations

#### Panel "Flight Trajectories Map" :
- **Type** : Geomap ✅
- **View** : Paris (48.8566, 2.3522, zoom 10) ✅
- **Layers** : Markers avec couleur/taille basée sur altitude ✅
- **Fields** : latitude/longitude automatiquement détectés ✅

#### Panel "Altitude Profile" :
- **Type** : Time series ✅
- **X-axis** : timestamp_dt (automatique) ✅
- **Y-axis** : altitude ✅
- **Unit** : feet (lengthft) ✅

#### Panel "Flight Data Table" :
- **Type** : Table ✅
- **Affichage** : Toutes les colonnes CSV ✅

## 3. Personnalisation Optionnelle

### Ajuster la vue de la carte :
1. Éditez le panel "Flight Trajectories Map"
2. **Options** → **View** → Ajustez lat/lon/zoom si nécessaire

### Modifier les couleurs/styles :
1. **Field options** → **Overrides**
2. Configurez les couleurs, tailles, etc.

### Ajouter des filtres :
1. **Dashboard settings** → **Variables**
2. Créez des variables pour filtrer par callsign, icao24, etc.

## 4. Sauvegarde

1. Cliquez sur l'icône **"Save dashboard"** (💾)
2. Ajoutez un commentaire si nécessaire
3. Cliquez **"Save"**

## 5. Dépannage

### Problème : Panels vides après ajout CSV
- Vérifiez que le CSV est complet (header + données)
- Vérifiez le format des timestamps
- Rafraîchissez le dashboard (Ctrl+R)

### Problème : Carte ne s'affiche pas
- Vérifiez que latitude/longitude sont des nombres
- Ajustez la vue géographique dans les options

### Problème : Graphique d'altitude vide
- Vérifiez le format timestamp_dt
- Assurez-vous que la colonne altitude contient des nombres

## 6. Données d'Exemple

Votre fichier `sample_trajectory_for_grafana.csv` contient :
- **82 points** de trajectoire
- **Vol DAH1000** (icao24: 0a0075)
- **Région parisienne** (coordonnées 48.x, 1.x-2.x)
- **Altitude** : 19225 → 14475 ft (descente)
- **Durée** : ~3 minutes (13:20 → 13:23)

## 7. Extensions Possibles

- Ajouter d'autres vols en combinant plusieurs CSV
- Créer des alertes sur altitude critique
- Ajouter des annotations pour événements spéciaux
- Intégrer avec InfluxDB pour données temps réel
