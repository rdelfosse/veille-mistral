# Scoring Rubric — Guide générique

Ce document explique **comment fonctionne le scoring**. Le barème concret (les mots-clés)
vit dans `topics/<topic>/scoring.md`, propre à chaque sujet. Voir `topics/_template/scoring.md`
pour le gabarit à remplir.

## Scoring par axe (0–3 par axe)

Chaque insight est scoré sur **chaque** axe défini dans le `sources.json` du topic. Un insight
peut scorer sur plusieurs axes (ex. un article qui touche deux sous-angles du sujet).

| Score | Critère générique |
|-------|-------------------|
| **3** | Mots-clés « cœur » de l'axe présents dans titre + résumé — match direct et fort |
| **2** | Mots-clés « proches »/connexes — pertinence claire mais secondaire |
| **1** | Pertinence indirecte / contextuelle seulement |
| **0** | Aucune pertinence |

`primary_axis` = l'axe au score le plus élevé pour cet insight.

## Scoring d'actionability (0–3)

L'actionability mesure le **potentiel d'exploitation pour le public cible** défini en tête du
`scoring.md` du topic. Selon le sujet, « exploiter » peut vouloir dire : écrire un contenu,
**lancer un produit/service**, prioriser une décision, ou contacter un acteur. Le `scoring.md`
du topic précise quelle lecture s'applique.

| Score | Critère |
|-------|---------|
| **3** | Signal fort directement exploitable par le public cible : pain point précis et récurrent, opportunité émergente, étude de cas, ou prise à contre-courant |
| **2** | Pourrait nourrir une piste : complète un besoin connu avec données/exemples frais |
| **1** | Utile en référence / contexte, pas assez pour agir seul |
| **0** | Pur relais d'actualité, aucun angle exploitable |

### Cross-références (optionnel)

Uniquement si `settings.cross_reference` est configuré dans le `sources.json` du topic
(ex. un chemin vers des contenus à rapprocher). Sinon, laisser `cross_links: []`.

### « Take » éditorial / opportunité

Pour chaque insight avec actionability ≥ 2, écrire un take de 2 phrases :
1. POURQUOI ça compte pour le **public cible du sujet** (le besoin / pain point précis).
2. ANGLE concret : contenu à produire, **offre/produit à imaginer**, ou décision à prendre.

## Comment remplir le `scoring.md` d'un topic

1. Définir le **public cible** (1-2 phrases) — il oriente l'actionability et le take.
2. Lister les **mots-clés** du sujet (réutilisés dans le `summary` Markdown).
3. Pour chaque axe : un tableau Score 3/2/1/0 avec les listes de mots-clés correspondantes,
   sur le modèle ci-dessus.
