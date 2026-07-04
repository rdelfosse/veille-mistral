# Analysis Method — Guide générique (angles morts → idées)

Ce document explique **comment fonctionnent les deux agents d'analyse aval** qui prolongent la
veille. Le brief concret (acteurs, contraintes, critères) vit dans `topics/<topic>/analysis.md`,
propre à chaque sujet. Voir `topics/_template/analysis.md` pour le gabarit.

Le pipeline complet est :

```
veille  →  angles-morts  →  idées-microservices  →  critique
(data/)     (angles-morts-*.md)   (idees-*.md)       (critique-*.md)
```

Chaque agent lit la sortie GitHub du précédent. Tous sont **agnostiques au sujet** : toute la
spécificité vit dans `topics/<topic>/analysis.md` + `scoring.md`. Les livrables d'analyse sont
écrits sous `topics/<topic>/analysis/`.

## 1. Angles morts

**But** : partant des insights/opportunités de la veille, cartographier ce que les **acteurs en
place** (section « Acteurs en place » de `analysis.md`) proposent DÉJÀ, pour isoler ce qu'ils
**ne font pas** — les angles morts exploitables, sous la contrainte du topic.

Logique :
1. Lire le `data/YYYY-WNN.json` (ou plusieurs semaines) → la liste des pain points / opportunités.
2. Pour chaque acteur du brief : recherche web sur son offre réelle (dispositifs récents).
3. Croiser : pour chaque pain point, **couverture** de chaque acteur (forte 🟢 / moyenne 🟡 /
   faible-nulle 🔴, « $ » si couvert seulement par du financement).
4. Isoler les **angles morts** = pain point réel × couverture faible × contrainte respectée.
5. Classer un **top** par « blancheur » de l'angle × taille du besoin.

## 2. Idées micro-services

**But** : transformer les angles morts en **idées concrètes et actionnables**, filtrées par les
**critères** du brief (`analysis.md`).

Logique :
1. Lire le dernier `analysis/angles-morts-*.md` du topic (+ le digest pour le chiffrage).
2. Pour chaque angle mort porteur, proposer une ou plusieurs idées **mono-tâche**.
3. Filtrer/scorer par les critères du brief (preuve rapide, mono-tâche, couche laissée vide,
   contrainte respectée).
4. Regrouper selon les **catégories de sortie** du brief (ou une simple liste triée par impact).
5. Terminer par un **wedge recommandé** : par quoi démarrer et pourquoi.

## 3. Critique (destruction Garry Tan → reframe CEO)

**But** : critique **adversariale** des idées, pas de l'encouragement. Deux lentilles, dans l'ordre :

1. **Office Hours (Garry Tan)** — les *six forcing questions* (Demand Reality, Status Quo, Desperate
   Specificity, Narrowest Wedge, Observation & Surprise, Future-Fit) appliquées en **grille de
   notation** : chaque idée est notée sur la **donnée réelle de la veille**. L'absence de preuve = le
   signal de mort. Verdict par idée : **KILL** (Q1/Q2/Q3 ❌), **REWORK** (pivot à nommer), **SURVIVE**.
2. **Revue CEO** — sur les survivants seulement : choisir un **mode** (REDUCTION par défaut / EXPANSION
   *10x check* / HOLD), affûter le wedge, appliquer les instincts CEO (*inversion*, *focus as
   subtraction*, *leverage*). Finir par **une action concrète** à faire cette semaine.

Écrit `analysis/critique-YYYY-WNN.md`. Ne réécrit pas les idées : produit un **verdict séparé**.
Rejouer l'agent **idées** avec ces verdicts en tête pour une v2.

## Cadence

Ces analyses tournent **moins souvent que la veille** (ex. mensuel, ou à la demande) : l'offre des
acteurs en place bouge lentement. Rejouer sur un digest à jour pour rafraîchir la cartographie.
La **critique** se rejoue après chaque run de l'agent idées.
