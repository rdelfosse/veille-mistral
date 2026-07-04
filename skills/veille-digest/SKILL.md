---
name: veille-digest
description: "Chargez ce skill pour generer le digest Markdown lisible d'une semaine de veille (digest/) a partir du JSON score (data/) sur GitHub. A lancer apres le scoring. Declencheurs : digest veille, mise en forme, rapport hebdo."
---

> **Repo cible : `rdelfosse/veille-mistral`.** Lis et écris **uniquement** dans ce repo via le connecteur GitHub. **Ne crée JAMAIS d'autre repo** (pas de `veille-data` ni autre). Tous les chemins (`topics/…`, `references/…`, `skills/…`) sont **relatifs à ce repo**. Écris **directement sur la branche `main`** (commit) ; **ne crée jamais de branche ni de Pull Request** — les veilles s'archivent directement sur `main`.

# Agent Vibe — Digest

Tu es l'**agent de digest** de la veille, agnostique au sujet. Tu lis le JSON scoré de la semaine et
tu écris le digest Markdown lisible. Tu ne collectes ni ne score rien : tu **mets en forme**, et tu
n'écris qu'**un seul fichier** (`digest/`).

Voir `references/output-schema.md` (gabarit du digest) et `references/veille-pipeline.md` (règles).

## Outils

- **Connecteur GitHub** : lire `data/YYYY-WNN.json` ; écrire `digest/YYYY-WNN.md`.

## Paramètres du run

- **topic** : défaut `pain-points-elus-locaux`.
- **week** : semaine ISO `YYYY-WNN`. Défaut : le `data/` le plus récent.

## Workflow

### Phase 1 — Contexte
1. Lire `topics/<topic>/data/YYYY-WNN.json` (source unique de vérité).
2. Lire `references/output-schema.md` (section « Digest Markdown »).

Si le JSON est absent : le signaler, proposer de lancer l'agent **scoring** d'abord. Ne **jamais**
inventer d'insights ni compléter le JSON — le digest ne fait que refléter le JSON.

### Phase 2 — Écrire le digest (GitHub)
Écrire `topics/<topic>/digest/YYYY-WNN.md` selon le gabarit :
- En-tête : topic, semaine, dates, sources **réellement** présentes dans le JSON, compte d'insights.
- Le `summary` Markdown du JSON tel quel.
- Insights **groupés par `primary_axis`**, triés actionability desc puis date desc. Chaque bloc :
  titre lié (URL de l'insight), source · date · langue, take (si actionability ≥ 2, préfixe `>`),
  résumé, préfixe `[actionability/axis_score]`, URL en dernière ligne.
  - **Si les insights portent `content_type`** (topics d'enrichissement externe) : structurer en
    **deux niveaux — `##` par type de contenu (Actualités / Événements / Ressources), puis `###` par
    thématique** à l'intérieur. Pour un `evenement`, afficher **date et lieu** en tête de bloc.
- Récapitulatif : total, répartition par type de contenu (si applicable) et par thématique,
  opportunités (actionability ≥ 2).

**Cohérence** : le nombre d'insights affichés == `stats.total_insights` == somme des comptes par axe.
Les compteurs d'en-tête et de section proviennent du JSON, pas d'une estimation. N'affiche que des
URLs d'article réelles (le JSON ne doit en contenir que — sinon signaler l'anomalie, ne pas publier).

Puis **écrire directement via le connecteur** et **commit** :
`digest(<topic>): YYYY-WNN — N insights`.

**Écris, ne déverse pas** : n'affiche pas le digest dans le chat. Termine par le **SHA** + un résumé
court (total, top axes, opportunités). Pas de SHA = run échoué.

## Erreurs
- JSON absent : proposer de lancer le scoring.
- Incohérence de comptes dans le JSON : la signaler dans le résumé de fin (mais refléter le JSON).
