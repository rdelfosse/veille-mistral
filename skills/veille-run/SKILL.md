---
name: veille-run
description: "Chargez ce skill pour lancer TOUT le pipeline de veille d'un topic en une invocation : collecte de tous les axes, puis scoring, puis digest (et en option l'analyse aval). Orchestre les autres skills veille-* dans l'ordre, en committant a chaque etape (reprenable). Declencheurs : lance toute la veille, pipeline complet, tous les axes puis scoring et digest."
---

> **Repo cible : `rdelfosse/veille-mistral`.** Lis et écris **uniquement** dans ce repo via le connecteur GitHub. **Ne crée JAMAIS d'autre repo** (pas de `veille-data` ni autre). Tous les chemins (`topics/…`, `references/…`, `skills/…`) sont **relatifs à ce repo**.

# Agent Vibe — Orchestrateur du pipeline de veille

Tu orchestres le pipeline complet d'un topic **dans l'ordre**, en **committant à chaque étape** pour
que tout soit reprenable. Séquence :

```
veille-collecte (tous les axes)  →  veille-scoring  →  veille-digest
        └─ (option) →  veille-angles-morts  →  veille-idees-microservices  →  veille-critique-idees
```

## Comment tu enchaînes (lis d'abord)

Deux cas, selon ce que ton environnement permet :

1. **Si tu peux invoquer d'autres skills** : appelle-les dans l'ordre ci-dessous, une par une, en
   attendant que chacune ait **committé** (elle te rend un SHA) avant de lancer la suivante.
2. **Sinon** : exécute toi-même la logique de chaque étape en suivant son fichier de skill
   (`skills/veille-<étape>/SKILL.md`, lisible sur GitHub), **en committant à chaque frontière**
   (après chaque axe de collecte, puis après le scoring, puis après le digest).

> ⚠️ **Reprise > exhaustivité en un tour.** Ne cherche pas à tout finir en mémoire avant d'écrire. Un
> tour trop long peut s'arrêter : ce n'est grave que si rien n'a été committé. Commite tôt et souvent
> (chaque axe, chaque étape). Relancer ce skill **reprend là où ça s'est arrêté** (les axes déjà
> collectés sont dans `raw/`, le JSON déjà écrit dans `data/`, etc.).

## Paramètres
- **topic** : défaut `pain-points-elus-locaux`.
- **week** : semaine ISO `YYYY-WNN`. Défaut : semaine courante.
- **include_analysis** : `true` pour enchaîner aussi angles-morts → idées → critique. Défaut : `false`
  (veille seule ; l'analyse aval tourne moins souvent).

## Séquence

### 1. Collecte — tous les axes
Lancer **veille-collecte** avec `axis = all` (il traite chaque axe et **commite après chacun**). À la
fin, vérifier que `metadata.axes_collected` du harvest couvre bien les axes voulus ; sinon relancer la
collecte sur les axes restants. Ne pas passer au scoring tant que la collecte n'est pas complète.

### 2. Scoring
Lancer **veille-scoring** pour la semaine → écrit et commite `data/YYYY-WNN.json`. Attendre son SHA.

### 3. Digest
Lancer **veille-digest** pour la semaine → écrit et commite `digest/YYYY-WNN.md`. Attendre son SHA.

### 4. Analyse aval (seulement si `include_analysis = true`)
Enchaîner, chacun attendant le SHA du précédent :
**veille-angles-morts** → **veille-idees-microservices** → **veille-critique-idees**.

## Fin
**Écris, ne déverse pas.** Termine par un récap : pour chaque étape, son **SHA de commit** (ou la
liste des SHA d'axes pour la collecte), et l'état final (nombre d'insights, opportunités). Signale
toute étape non terminée + comment la reprendre. Pas de SHA à une étape = cette étape a **échoué**.

## Erreurs
- Une étape échoue : committer ce qui a réussi, **s'arrêter proprement**, et dire par où reprendre.
- Ne jamais sauter le scoring/digest en prétendant les avoir faits sans commit correspondant.
