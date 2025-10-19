# 🌊 Workflow de Développement avec WindSurf (Cascade AI)

**Projet** : Analyse des trajectoires ADS-B - Aéroport d'Orly  
**Auteurs** : Nicolas Cusseau et Emile Bleicher  
**Formation** : Mastère Spécialisé ILEMS - ECE 6ILM4  
**Date** : 19 octobre 2025

---

## 📋 Protocole Opérationnel

Ce projet utilise le **ONDOCEAN-MODE-STRICT-OPERATIONAL-WORKFLOW** (protocole RIPER-5) pour garantir un développement rigoureux et sans erreurs avec WindSurf/Cascade AI.

### 🔗 Référence complète

Voir le fichier : [`ONDOCEAN-MODE-STRICT-OPERATIONAL-WORKFLOW.md`](./ONDOCEAN-MODE-STRICT-OPERATIONAL-WORKFLOW.md)

---

## 🎯 Les 5 Modes RIPER

### 1️⃣ MODE: RESEARCH
**Objectif** : Comprendre le code existant

**Quand l'utiliser** :
- Avant toute modification
- Pour explorer une fonctionnalité existante
- Pour comprendre l'architecture

**Commandes** :
```
ENTER RESEARCH MODE
```

**Exemple d'utilisation** :
```
ENTER RESEARCH MODE
Explique-moi comment fonctionne la classe FlightCollection dans ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py
```

---

### 2️⃣ MODE: INNOVATE
**Objectif** : Brainstorming d'idées

**Quand l'utiliser** :
- Pour explorer différentes approches
- Pour comparer des solutions
- Pour discuter d'améliorations

**Commandes** :
```
ENTER INNOVATE MODE
```

**Exemple d'utilisation** :
```
ENTER INNOVATE MODE
Propose différentes approches pour optimiser le filtrage des trajectoires d'atterrissage
```

---

### 3️⃣ MODE: PLAN
**Objectif** : Planifier en détail avant d'implémenter

**Quand l'utiliser** :
- Avant toute implémentation
- Pour créer un plan technique exhaustif
- Pour générer une checklist d'actions

**Commandes** :
```
ENTER PLAN MODE
```

**Exemple d'utilisation** :
```
ENTER PLAN MODE
Planifie l'ajout d'une méthode filter_by_altitude() à la classe FlightCollection
```

**Sortie attendue** :
- Spécification technique complète
- Noms exacts de fichiers, fonctions, variables
- CHECKLIST numérotée d'actions atomiques

---

### 4️⃣ MODE: EXECUTE
**Objectif** : Implémenter EXACTEMENT le plan

**Quand l'utiliser** :
- Uniquement après approbation du plan
- Pour exécuter la checklist point par point

**Commandes** :
```
ENTER EXECUTE MODE
```

⚠️ **ATTENTION** : L'IA ne peut RIEN modifier en dehors du plan approuvé

**Exemple d'utilisation** :
```
ENTER EXECUTE MODE
[L'IA implémente la checklist du plan approuvé]
```

---

### 5️⃣ MODE: REVIEW
**Objectif** : Vérifier que l'implémentation suit le plan

**Quand l'utiliser** :
- Après toute implémentation
- Pour validation avant commit Git

**Commandes** :
```
ENTER REVIEW MODE
```

**Sortie attendue** :
- Comparaison ligne par ligne
- ✅ IMPLEMENTATION MATCHES PLAN EXACTLY
- ou ⚠️ DEVIATION DETECTED

---

## 🔄 Workflow Type pour le Projet

### Scénario 1 : Ajouter une nouvelle fonctionnalité

```bash
# Étape 1 : Comprendre le contexte
ENTER RESEARCH MODE
> "Montre-moi comment sont gérées les trajectoires dans le script OO"

# Étape 2 : Explorer les options
ENTER INNOVATE MODE
> "Propose des approches pour ajouter un export vers format KML"

# Étape 3 : Planifier
ENTER PLAN MODE
> "Planifie l'implémentation de l'export KML avec la meilleure approche discutée"

# Étape 4 : Approuver le plan
> "Le plan est approuvé, ENTER EXECUTE MODE"

# Étape 5 : Vérifier
ENTER REVIEW MODE
> "Vérifie que l'implémentation correspond au plan"
```

---

### Scénario 2 : Corriger un bug

```bash
# Étape 1 : Comprendre le bug
ENTER RESEARCH MODE
> "Analyse le code qui filtre les atterrissages et identifie pourquoi certains vols sont manqués"

# Étape 2 : Planifier la correction
ENTER PLAN MODE
> "Planifie la correction du bug identifié en RESEARCH"

# Étape 3 : Implémenter
> "Plan approuvé, ENTER EXECUTE MODE"

# Étape 4 : Vérifier
ENTER REVIEW MODE
```

---

### Scénario 3 : Refactoring

```bash
# Étape 1 : Analyser le code actuel
ENTER RESEARCH MODE
> "Analyse la structure du script GRAFANA et identifie les opportunités de refactoring"

# Étape 2 : Discuter des options
ENTER INNOVATE MODE
> "Propose différentes architectures pour améliorer la maintenabilité"

# Étape 3 : Planifier le refactoring
ENTER PLAN MODE
> "Planifie le refactoring selon l'approche X discutée"

# Étape 4 : Exécuter par phases
> "Plan approuvé pour la Phase 1, ENTER EXECUTE MODE"
[Une fois Phase 1 terminée]
> "ENTER PLAN MODE pour la Phase 2"
```

---

## 🛡️ Règles de Sécurité Critiques

### ❌ INTERDICTIONS ABSOLUES

1. **Jamais d'implémentation sans plan approuvé**
2. **Jamais de modifications "sur le tas"**
3. **Jamais d'améliorations non demandées**
4. **Jamais de changements de mode sans signal explicite**

### ✅ BONNES PRATIQUES

1. **Toujours déclarer le mode** : `[MODE: RESEARCH]`
2. **Toujours demander confirmation** avant EXECUTE
3. **Toujours vérifier** avec REVIEW après EXECUTE
4. **Toujours commencer par RESEARCH** si on ne connaît pas le code

---

## 📁 Fichiers du Projet à Protéger

### ⭐ Fichiers critiques (JAMAIS modifier sans plan)

```
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py          # Architecture POO principale
ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_GRAFANA.py     # Export Grafana
adsb25/orly.jsonl.gz                                    # Données sources
grafana_dashboard_adsb_final.json                       # Dashboard final
```

### 📝 Fichiers de documentation (Modification autorisée)

```
README.md
PROJET_ADSB_RESUME.md
*.puml (diagrammes)
```

---

## 🎓 Exemples Concrets d'Utilisation

### Exemple 1 : Ajouter un filtre par vitesse

```plaintext
Vous: ENTER RESEARCH MODE
     Montre-moi comment sont filtrées les trajectoires actuellement

AI: [MODE: RESEARCH]
    [Analyse du code...]

Vous: ENTER INNOVATE MODE
     Propose des approches pour ajouter un filtre par ground_speed

AI: [MODE: INNOVATE]
    [Proposition de 3 approches...]

Vous: L'approche 2 semble la meilleure. ENTER PLAN MODE
     Planifie l'implémentation de l'approche 2

AI: [MODE: PLAN]
    [Plan détaillé avec checklist...]
    IMPLEMENTATION CHECKLIST:
    1. Ajouter méthode filter_by_speed() à FlightCollection
    2. ...

Vous: Plan approuvé. ENTER EXECUTE MODE

AI: [MODE: EXECUTE]
    [Implémentation stricte du plan...]

Vous: ENTER REVIEW MODE

AI: [MODE: REVIEW]
    [Vérification...]
    ✅ IMPLEMENTATION MATCHES PLAN EXACTLY
```

---

### Exemple 2 : Debugger un problème

```plaintext
Vous: ENTER RESEARCH MODE
     Le script plante lors du chargement de orly.jsonl.gz
     Analyse le code de lecture du fichier

AI: [MODE: RESEARCH]
    [Analyse et identifie le problème...]

Vous: ENTER PLAN MODE
     Planifie la correction du bug identifié

AI: [MODE: PLAN]
    [Plan de correction...]

Vous: ENTER EXECUTE MODE

AI: [MODE: EXECUTE]
    [Correction...]

Vous: ENTER REVIEW MODE

AI: [MODE: REVIEW]
    ✅ IMPLEMENTATION MATCHES PLAN EXACTLY
```

---

## 📊 Checklist Avant Commit Git

Avant tout commit, suivre cette procédure :

```bash
# 1. Vérifier l'implémentation
ENTER REVIEW MODE
> "Vérifie que tous les changements correspondent au plan approuvé"

# 2. Tester le code
python verify_data.py
python ILEMS2025_ECE_6ILM4_TA_Bleicher_Cusseau_OO.py

# 3. Vérifier la documentation
> "ENTER RESEARCH MODE - Vérifie que la documentation est à jour"

# 4. Commit
git add .
git commit -m "feat: [description du changement]"
```

---

## 🚨 Gestion des Urgences

### Si l'IA ne suit pas le protocole

```plaintext
Vous: STOP. Tu as violé le protocole RIPER-5.
     Retourne en MODE: RESEARCH et reprends.
```

### Si une déviation est détectée en REVIEW

```plaintext
AI: [MODE: REVIEW]
    ⚠️ DEVIATION DETECTED: Ajout d'une optimisation non prévue

Vous: ENTER PLAN MODE
     Planifie la correction pour revenir au plan initial
```

---

## 🔗 Intégration avec Git

### Convention de commits (respecter le protocole)

```bash
# Après REVIEW réussie
git commit -m "feat(flight): add filter_by_speed method [RIPER-5 EXECUTE+REVIEW ✅]"

# Si modifications mineures
git commit -m "docs: update README with new filter [RIPER-5 PLAN ✅]"
```

---

## 📚 Ressources

### Documents du projet

- [`ONDOCEAN-MODE-STRICT-OPERATIONAL-WORKFLOW.md`](./ONDOCEAN-MODE-STRICT-OPERATIONAL-WORKFLOW.md) - Protocole complet RIPER-5
- [`README.md`](./README.md) - Vue d'ensemble du projet
- [`PROJET_ADSB_RESUME.md`](./PROJET_ADSB_RESUME.md) - Architecture technique

### Commandes rapides

```bash
# Activer un mode
ENTER RESEARCH MODE
ENTER INNOVATE MODE
ENTER PLAN MODE
ENTER EXECUTE MODE
ENTER REVIEW MODE

# Vérifier la conformité
git diff  # Avant commit
python verify_data.py  # Test d'intégrité
```

---

## ✅ Avantages du Workflow RIPER-5

### Pour le projet ADS-B

1. **Zéro modification involontaire** du code POO stable
2. **Traçabilité complète** des changements
3. **Documentation automatique** via les plans
4. **Réduction des bugs** grâce à REVIEW systématique
5. **Collaboration efficace** avec l'IA

### Pour l'équipe

- **Nicolas et Emile** : Contrôle total sur les modifications
- **Cascade AI** : Instructions claires et non ambiguës
- **Projet** : Code stable et maintenable

---

## 🎯 Résumé en 5 Points

1. **Toujours commencer par RESEARCH** pour comprendre
2. **Planifier avant d'agir** (MODE: PLAN obligatoire)
3. **Exécuter uniquement le plan approuvé** (MODE: EXECUTE)
4. **Vérifier systématiquement** (MODE: REVIEW)
5. **Déclarer le mode à chaque réponse** `[MODE: XXX]`

---

**Workflow créé le** : 19 octobre 2025  
**Auteurs** : Nicolas Cusseau et Emile Bleicher  
**IA Assistant** : Cascade AI (WindSurf)  
**Protocole** : RIPER-5 / ONDOCEAN MODE STRICT OPERATIONAL
