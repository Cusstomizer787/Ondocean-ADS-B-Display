# Guide IGN Route 500 pour Trajectoires d'Avion

Ce guide explique comment charger et simplifier les données IGN Route 500 pour créer des fonds de carte optimisés pour superposer des trajectoires d'avion.

## 📁 Scripts disponibles

### 1. **`exemple_simple_ign.py`** - Script de base
- Charge toutes les données IGN Route 500
- Filtre autour d'Orly (25km)
- Simplifie les données pour réduire la complexité
- Génère 2 cartes : complète et simplifiée

### 2. **`carte_fond_trajectoires.py`** - Fond de carte optimisé
- **Données minimales** : seulement les routes principales et communes simplifiées
- **Style discret** : couleurs très claires pour faire ressortir les trajectoires
- **Cercles de référence** : 5, 10, 15, 20 km autour d'Orly
- **Formats multiples** : PNG haute résolution + PDF vectoriel

### 3. **`exemple_trajectoires_orly.py`** - Exemple complet
- Montre comment superposer des trajectoires sur le fond IGN
- Trajectoires d'exemple avec différents types (atterrissage, décollage, transit)
- Code couleur : 🔵 bleu=atterrissage, 🔴 rouge=décollage, 🟢 vert=transit

## 🎯 Stratégies de simplification

### Réduction des données routes
```python
# Garder seulement les routes principales
routes_principales = routes[
    routes['VOCATION'].isin([
        'Autoroute', 'Quasi-autoroute', 
        'Liaison principale', 'Liaison régionale'
    ])
]
```

### Simplification géométrique
```python
# Simplifier les géométries (tolérance en mètres)
communes_simples['geometry'] = communes['geometry'].simplify(tolerance=200)
routes_simples['geometry'] = routes['geometry'].simplify(tolerance=100)
```

### Filtrage spatial
```python
# Zone d'étude autour d'Orly
orly_x, orly_y = 652000, 6860000  # Lambert93
rayon_km = 20
bbox = (orly_x - rayon_km*1000, orly_y - rayon_km*1000, 
        orly_x + rayon_km*1000, orly_y + rayon_km*1000)
donnees_filtrees = gdf.cx[bbox[0]:bbox[2], bbox[1]:bbox[3]]
```

## 📊 Résultats de simplification

| Données | Original | Filtré (25km) | Simplifié |
|---------|----------|---------------|-----------|
| **Routes** | 1,302,758 | 30,228 | 11,021 |
| **Communes** | 34,836 | 403 | 403 |
| **Aérodromes** | 163 | 34 | 34 |

## 🎨 Style de carte pour trajectoires

### Couleurs discrètes
- **Communes** : `#f8f8f8` (gris très clair)
- **Routes** : `#d0d0d0` (gris clair, alpha=0.3)
- **Aérodromes** : `red` (bien visibles)

### Éléments de référence
- **Orly** : étoile rouge au centre
- **Cercles** : rayons de 5, 10, 15, 20 km
- **Grille** : coordonnées Lambert93 discrètes

## 🛫 Intégration avec données ADS-B

### Code couleur recommandé
```python
couleurs_trajectoires = {
    'atterrissage': 'blue',      # Approches
    'decollage': 'red',          # Décollages  
    'transit': 'green',          # Survols
    'attente': 'orange'          # Circuits d'attente
}
```

### Filtrage par altitude
```python
# Séparer les phases de vol
approches = df[df['altitude'] < 3000]      # < 3000 ft
decollages = df[df['altitude'] < 5000]     # < 5000 ft  
transits = df[df['altitude'] > 10000]      # > 10000 ft
```

## 📁 Fichiers générés

### Shapefiles simplifiés
- `donnees_ign_extraites/routes.shp` - Routes principales
- `donnees_ign_extraites/communes.shp` - Communes simplifiées
- `donnees_ign_extraites/aerodromes.shp` - Aérodromes

### Cartes de fond
- `fond_carte_orly_trajectoires.png` - Fond optimisé (PNG)
- `fond_carte_orly_trajectoires.pdf` - Fond optimisé (PDF)
- `carte_trajectoires_orly_complete.png` - Exemple avec trajectoires

## 💡 Conseils d'utilisation

### Pour de nombreuses trajectoires
- Utilisez `alpha=0.6` pour la transparence
- Groupez par heure/jour pour éviter la surcharge
- Utilisez des couleurs dégradées par altitude

### Performance
- Chargez une seule fois le fond de carte
- Réutilisez la figure matplotlib pour ajouter des trajectoires
- Sauvegardez en PDF pour la qualité vectorielle

### Projection Lambert93
- Toutes les coordonnées sont en mètres
- Orly : X=652000, Y=6860000
- Distances directement calculables en mètres

## 🚀 Utilisation rapide

```bash
# Créer le fond de carte optimisé
python carte_fond_trajectoires.py

# Voir l'exemple avec trajectoires
python exemple_trajectoires_orly.py

# Script complet avec simplification
python exemple_simple_ign.py
```

Le fond de carte est maintenant prêt pour superposer vos trajectoires ADS-B d'Orly ! 🛫
