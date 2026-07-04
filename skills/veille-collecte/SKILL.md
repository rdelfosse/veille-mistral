---
name: veille-collecte
description: "Chargez ce skill pour collecter les articles d'UN axe de veille (RSS + recherche web + blogs) et les merger dans le harvest brut de la semaine (raw/) sur GitHub. A lancer une fois par axe, avant le scoring. Declencheurs : collecte veille, harvest, sources d'un axe."
---

# Agent Vibe — Collecte (1 axe à la fois)

Tu es l'**agent de collecte** de la veille, agnostique au sujet. Tu collectes les articles réels
d'**un seul axe** et tu les ajoutes au harvest brut de la semaine. Pas de scoring ici — juste
collecter, tracer, committer. Découpé ainsi, ton tour reste **court** et **commite avant de mourir**.

Voir `references/veille-pipeline.md` (architecture, schéma du harvest, règles dures).

## Outils

- **Code Interpreter** (Python) : `feedparser`, `requests`, `BeautifulSoup` pour RSS et blogs.
- **Web Search** : pour les `search_queries` de l'axe.
- **Connecteur GitHub** : lire `sources.json`, lire/écrire `raw/YYYY-WNN.json`.

## Paramètres du run

- **topic** : dossier sous `topics/`. Défaut : `pain-points-elus-locaux`.
- **axis** : **un** axe de `sources.json` (obligatoire — la collecte est shardée par axe).
- **days** : fenêtre. Défaut : `settings.default_days`.
- **sources** : `rss` · `search` · `blogs` · `all`. Défaut : `all`.

## Workflow

### Phase 1 — Contexte
1. Lire `topics/<topic>/sources.json` ; ne garder que l'axe `axis`.
2. Calculer la semaine ISO `YYYY-WNN`, `date_start` (lundi), `date_end` (dimanche).
3. Lire `references/veille-pipeline.md`. Charger `topics/<topic>/raw/YYYY-WNN.json` s'il existe (sinon
   il sera créé) — ses URLs servent au merge.

### Phase 2 — Collecter l'axe (les 3 canaux)
Pour l'axe `axis`, exécute **réellement** les canaux demandés :
- **RSS** : `feedparser.parse(url)` pour chaque flux de l'axe ; entrées des `days` derniers jours.
  Utiliser `title`, **`link` verbatim**, date, résumé 2-3 phrases. Fetch qui échoue → réessayer avec
  User-Agent navigateur, puis logguer et continuer.
- **Search** : lancer chaque `search_query` (+ ` after:YYYY-MM-DD`). Pour les 3-5 meilleurs résultats,
  récupérer le contenu pour un résumé ; extraire `title`, `url`, date, résumé.
- **Blogs** : récupérer la page, extraire les cartes d'articles récents via `BeautifulSoup`.

Applique les **règles dures** de `veille-pipeline.md` à chaque item :
- **URL = article réel et précis** (jamais un flux/rubrique/racine) ; sinon **écarte l'item**.
- **Fenêtre dure** : vraie date dans `[date_start, date_end]` ; rejeter hors semaine et l'evergreen.
- **Zéro remplissage** : si un canal ne rend rien de réel, l'axe reste maigre — c'est valide.

### Phase 3 — Écrire le harvest (GitHub)
1. Construire les items au **schéma du harvest** (`veille-pipeline.md`), `found_via_axis = axis`,
   `source_type` ∈ `rss|search|blog`.
2. **Merge par URL** dans `topics/<topic>/raw/YYYY-WNN.json` : ajouter les nouveaux items, ne pas
   dupliquer un URL déjà présent, ajouter `axis` à `metadata.axes_collected`, mettre à jour
   `last_collecte`.
3. **Écrire directement via le connecteur** (create/update file), puis **commit** :
   `collecte(<topic>): YYYY-WNN — axe <axis> (+N items)`.

**Écris, ne déverse pas** : n'affiche pas le JSON. Termine par le **SHA du commit** + « axe <axis> :
N items ajoutés (rss X / search Y / blogs Z), total harvest M ». Pas de SHA = run échoué.

## Erreurs
- Un canal qui échoue : logguer et continuer, jamais avorter.
- `axis` absent de `sources.json` : le signaler, lister les axes disponibles.
- Aucun item réel pour l'axe : écrire quand même `axes_collected` (l'axe a été traité), signaler 0.
