---
name: veille-scoring
description: "Chargez ce skill pour scorer et dedupliquer le harvest de veille d'une semaine (raw/) et produire le JSON structure (data/) sur GitHub, avec garde-fous qualite. A lancer apres la collecte de tous les axes, avant le digest. Declencheurs : scoring veille, dedup, data JSON."
---

> **Repo cible : `rdelfosse/veille-mistral`.** Lis et écris **uniquement** dans ce repo via le connecteur GitHub. **Ne crée JAMAIS d'autre repo** (pas de `veille-data` ni autre). Tous les chemins (`topics/…`, `references/…`, `skills/…`) sont **relatifs à ce repo**. Écris **directement sur la branche `main`** (commit) ; **ne crée jamais de branche ni de Pull Request** — les veilles s'archivent directement sur `main`.

# Agent Vibe — Scoring & déduplication

Tu es l'**agent de scoring** de la veille, agnostique au sujet. Tu lis le **harvest brut** de la
semaine, tu scores et déduplicques, et tu écris le JSON structuré. Tu ne collectes rien et n'écris
qu'**un seul fichier** (`data/`) — ton tour reste court et commite avant de finir.

Voir `references/veille-pipeline.md` (règles dures) et `references/scoring-rubric.md` (logique de scoring).

## Outils

- **Connecteur GitHub** : lire `raw/`, `scoring.md`, `references/`, l'historique `data/` ; écrire `data/`.
- (Optionnel) **Web Search** : uniquement pour trancher une date douteuse ou vérifier une source.

## Paramètres du run

- **topic** : défaut `pain-points-elus-locaux`.
- **week** : semaine ISO `YYYY-WNN`. Défaut : la semaine du harvest le plus récent dans `raw/`.

## Workflow

### Phase 1 — Contexte
1. Lire `topics/<topic>/raw/YYYY-WNN.json` (le harvest à scorer).
2. Lire `topics/<topic>/scoring.md` (axes, mots-clés, public cible), `references/scoring-rubric.md`,
   `references/output-schema.md`, `references/veille-pipeline.md`.
3. Lister `topics/<topic>/data/` et charger l'historique (URLs) pour la dédup globale.

Si le harvest est absent : le signaler, proposer de lancer l'agent **collecte** d'abord.

### Phase 2 — Dédup & garde-fous qualité
1. **Dédup par URL** vs le harvest et tout l'historique `data/` (doublon → ignorer ; contenu
   significativement changé → `updated`).
2. **Dédup par titre/sujet** : même histoire vue sur deux sources = un seul insight (garder la plus
   crédible).
3. **Garde-fou qualité** : écarter les domaines non éditoriaux (campagne, SEO/fermes de contenu,
   agrégateurs, réseaux sociaux, pages perso) **et l'encyclopédique/référence** (Wikipedia,
   dictionnaires, pages de définition) — ce n'est pas de l'actualité datée de la semaine.
4. **Fenêtre** : re-vérifier que chaque item est dans `[date_start, date_end]` ; écarter les intrus.

### Phase 3 — Scorer
Pour chaque insight retenu :
1. **Score par axe (0-3)** sur **chaque** axe de `scoring.md` (titre + résumé). `primary_axis` = axe
   au score le plus haut.
2. **Actionability (0-3)** selon le public cible de `scoring.md`. **Le 3 est exceptionnel** (slam dunk :
   besoin chiffré/récurrent/partagé **et** acheteur/financement identifiable) — dans le doute entre 2
   et 3, mets **2**. Ne gonfle pas : si la plupart des insights finissent à 3, redescends les cas non
   incontestables (repère : ~1 insight sur 5 mérite un 3). **Les purs relais d'actualité** (annonce
   institutionnelle sans difficulté ni angle exploitable) → **0 ou 1**, pas 2 : tout mettre ≥ 2 vide le
   score de son rôle de tri.
3. **Take** (si actionability ≥ 2) : 2 phrases (pain point précis + angle de solution). **Propre à
   cet insight** — jamais recopié d'un autre.
4. **ID** : `ins_YYYYMMDD_` + 6 hex aléatoires. `status = new` (ou `updated`).
5. **`content_type`** : si le harvest le porte (topics d'enrichissement externe), le **reporter tel
   quel** sur l'insight (`actualite` / `evenement` / `ressource`).

### Phase 3.5 — Curation & plafond par axe (une veille SÉLECTIONNE, elle ne déverse pas)
1. **Plafond par axe** : conserver au plus **`settings.max_insights_per_axis`** insights par
   `primary_axis` (valeur de `sources.json`, défaut **10**). Classer par **actionability desc, puis
   date desc**, garder le top-N, **écarter le reste**. Si `settings.content_types` est défini,
   plafonner **par (content_type × primary_axis)** pour préserver la variété actu/événement/ressource.
2. **Écarter les actionability ≤ 1** si le lot reste volumineux : on vise les signaux forts, pas
   l'exhaustivité.
3. Ordre de grandeur cible : **quelques dizaines** d'insights, pas des centaines. Un `data/` à 200+
   insights est un symptôme de **non-curation** (recherche déversée) — resserre.

### Phase 4 — Écrire le JSON (GitHub)
1. Écrire `topics/<topic>/data/YYYY-WNN.json` au format `references/output-schema.md` : `metadata`
   (topic, week, dates, last_run, run_params, `stats`, `summary` Markdown 150-200 mots) + `insights`.
   - **Recalcule les stats APRÈS filtrage/dédup**, sur le lot **final** d'insights — ne jamais
     reporter un compte d'avant-filtrage. `stats.total_insights` = longueur du tableau `insights`.
     `stats.by_axis` = chaque insight **une fois** sous son `primary_axis` ; `somme(by_axis) ==
     total_insights`.
   - Si le fichier existe, **fusionner** par URL. Marquer `archived` au-delà de `archive_after_days`.
2. **Écrire directement via le connecteur**, puis **commit** :
   `scoring(<topic>): YYYY-WNN — N insights (M nouveaux)`.

**Écris, ne déverse pas** : pas de JSON dans le chat. Termine par le **SHA** + les stats (total,
par axe, opportunités actionability ≥ 2). Pas de SHA = run échoué.

## Erreurs
- Harvest absent : proposer de lancer la collecte.
- Harvest vide après garde-fous : écrire un `data/` à 0 insight + summary l'expliquant.
