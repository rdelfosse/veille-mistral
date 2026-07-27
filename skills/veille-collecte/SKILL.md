---
name: veille-collecte
description: "Chargez ce skill pour collecter les articles de veille (RSS + recherche web + blogs) et les merger dans le harvest brut de la semaine (raw/) sur GitHub. Param axis = un axe, `all`, ou `priority:N` ; les axes sont traites un par un en committant apres chacun (reprenable). A lancer avant le scoring. Declencheurs : collecte veille, harvest, tous les axes."
---

> **Repo cible : `rdelfosse/veille-mistral`.** Lis et écris **uniquement** dans ce repo via le connecteur GitHub. **Ne crée JAMAIS d'autre repo** (pas de `veille-data` ni autre). Tous les chemins (`topics/…`, `references/…`, `skills/…`) sont **relatifs à ce repo**. Écris **directement sur la branche `main`** (commit) ; **ne crée jamais de branche ni de Pull Request** — les veilles s'archivent directement sur `main`.

# Agent Vibe — Collecte

Tu es l'**agent de collecte** de la veille, agnostique au sujet. Tu collectes les articles réels et
tu les ajoutes au harvest brut de la semaine. Pas de scoring ici — juste collecter, tracer, committer.

Tu peux traiter **un axe, tous les axes, ou un palier de priorité**. Point clé : tu traites les axes
**un par un** et tu **commites après chaque axe**. Ainsi, même si le tour se termine avant la fin, les
axes déjà collectés sont sauvés, et relancer reprend **là où ça s'est arrêté**.

Voir `references/veille-pipeline.md` (architecture, schéma du harvest, règles dures).

## Outils (sandbox Vibe — pas de feedparser/BeautifulSoup)
- **Web Search** (`tools.web_search.web_search()`) : le canal **le plus fiable**, résultats structurés.
- **Code Interpreter** (Python **stdlib uniquement**) : `open_url(url)` pour récupérer une page ou un
  flux, puis `xml.etree.ElementTree` (RSS/Atom) ou `html.parser`/`re` (blogs). ⚠️ **feedparser,
  requests et BeautifulSoup ne sont PAS disponibles** — n'y fais jamais appel.
- **Connecteur GitHub** : lire `sources.json`, lire/écrire `raw/YYYY-WNN.json`.

## Paramètres du run
- **topic** : dossier sous `topics/`. Défaut : `pain-points-elus-locaux`.
- **axis** : quels axes traiter —
  - un **nom d'axe** de `sources.json` (ex. `finances`) → cet axe seulement ;
  - **`all`** → tous les axes du topic ;
  - **`priority:N`** → tous les axes de priorité N (`priority` dans `sources.json`).
  Défaut : `all`.
- **days** : fenêtre. Défaut : `settings.default_days`.
- **sources** : `rss` · `search` · `blogs` · `all`. Défaut : `all`.

## Schéma du harvest — à respecter EXACTEMENT (ne rien inventer)

`topics/<topic>/raw/YYYY-WNN.json` est un **objet** (jamais une liste brute) :

```json
{
  "metadata": { "topic": "…", "week": "YYYY-WNN", "date_start": "…", "date_end": "…",
                "last_collecte": "<datetime ISO>", "axes_collected": ["…"] },
  "items": [
    { "title": "…", "url": "https://…/article-precis", "source": "Nom de la source",
      "source_type": "search", "date": "YYYY-MM-DD", "lang": "fr",
      "summary": "Résumé factuel 2-3 phrases.", "found_via_axis": "<axe>",
      "content_type": "actualite" }
  ]
}
```

`date` et — si `settings.content_types` est défini — `content_type` sont **obligatoires et NON vides**.
**Ne recopie jamais** les champs bruts de `web_search` (`rank`, `snippets`, `can_open`, `metadata`).

## Workflow

### Phase 1 — Contexte & liste des axes
1. Lire `topics/<topic>/sources.json`.
2. Calculer la semaine ISO `YYYY-WNN`, `date_start` (lundi), `date_end` (dimanche).
3. Charger `topics/<topic>/raw/YYYY-WNN.json` s'il existe (URLs pour le merge, `axes_collected`).
4. **Établir la liste d'axes à traiter** selon `axis` (nom unique / `all` / `priority:N`). **Reprise** :
   retirer de la liste les axes déjà présents dans `metadata.axes_collected` de cette semaine — sauf si
   l'utilisateur redemande explicitement un axe déjà fait. Annoncer la liste (« à traiter : N axes »).

### Phase 2 — Boucle : pour CHAQUE axe de la liste, dans l'ordre
Pour un axe donné :
1. **Collecter les 3 canaux** (canaux demandés par `sources`) :
   - **RSS** (stdlib, **sans feedparser**) : `open_url(feed_url)` pour récupérer le XML, puis le parser
     avec `xml.etree.ElementTree` — RSS 2.0 (`item` → `title` / `link` / `pubDate` / `description`) et
     Atom (`entry`, namespace `{http://www.w3.org/2005/Atom}` → `title` / `link[@href]` / `updated` /
     `summary`). Garder les entrées des `days` derniers jours ; `title`, **`link` verbatim**, date,
     résumé 2-3 phrases. Si le parse XML échoue, extraire les blocs `<item>…</item>` par `re` en dernier
     recours. Fetch/parse KO → logguer et continuer.
   - **Search** : chaque `search_query` (+ ` after:YYYY-MM-DD`) via `tools.web_search.web_search()`.
     Si `settings.preferred_domains` existe, lancer **aussi** la requête **ancrée** sur ces sources de
     référence (`site:dom1 OR site:dom2 …`) et privilégier leurs résultats. Pour chaque résultat retenu :
     **`open_url(url)` pour lire l'article** et en tirer un **résumé factuel** ET surtout la **vraie date
     de publication** — web_search **NE donne PAS** de date fiable. **Ne recopie jamais l'objet brut**
     de web_search (`rank`, `snippets`, `can_open`, `metadata`).
   - **Blogs** (**sans BeautifulSoup**) : privilégier **Web Search** ciblé `site:<domaine-du-blog>`
     (+ filtre date) — plus fiable que le scraping. En complément seulement : `open_url(page)` +
     `html.parser` (stdlib) ou `re` pour extraire les cartes d'articles récents (best-effort).
2. **Règles dures** (`veille-pipeline.md`) sur chaque item :
   - **URL = article réel et précis** (jamais un flux/rubrique/racine) ; sinon **écarte l'item**.
   - **Date réelle OBLIGATOIRE** : chaque item doit porter une **vraie date de publication vérifiée**
     (extraite de l'article via `open_url`). **Pas de date → écarte l'item.** Un harvest sans dates est
     invalide (c'est l'échec du run W29 : 43 items, 0 date).
   - **Fenêtre dure** : date dans `[date_start, date_end]` ; rejeter hors semaine et l'evergreen.
   - **Pertinence + qualité** : ne garder que des items **liés aux thématiques du topic** et issus de
     sources **crédibles** (institutions, presse spécialisée, `settings.preferred_domains`). **Écarter**
     la presse locale généraliste, les sites SEO/conso, les blogs perso hors-sujet (ex. defenseconso,
     studeria, nicepremium…). Dans le doute sur la pertinence ou la crédibilité → écarter.
   - **Zéro remplissage** : un axe sans item réel reste vide — c'est valide.
   - **Exclure `settings.exclude_domains`** : sur une veille d'**enrichissement externe**, le domaine de
     la plateforme cible y figure — on cherche du contenu **externe**, jamais le sien. Écarter ces URLs.
3. **Merge par URL** dans `raw/YYYY-WNN.json` — un **objet** `{ "metadata": {…}, "items": [ … ] }`
   (JAMAIS une liste brute). Chaque item suit **EXACTEMENT** le `## Schéma du harvest` ci-dessus,
   `found_via_axis = <axe>`, `source_type` ∈ `rss|search|blog` ; sans dupliquer un URL déjà présent ;
   ajouter l'axe à `metadata.axes_collected` ; MAJ `last_collecte`. **N'invente aucun champ.**
   - **Si `settings.content_types` est défini** : classe **réellement** chaque item dans un `content_type`
     (`actualite` / `evenement` / `ressource`) via `settings.content_type_hints` + l'URL/titre — défaut
     `actualite`. Un harvest où **tous** les items sont `actualite` est un **symptôme** (classification
     non faite) : vérifie. Pour un `evenement`, capter **date et lieu**.
4. **Committer immédiatement cet axe** via le connecteur (create/update file) :
   `collecte(<topic>): YYYY-WNN — axe <axe> (+N items)`. **Puis passer à l'axe suivant.**

> **Commit par axe = reprise gratuite.** Ne jamais accumuler plusieurs axes en mémoire pour committer
> à la fin : commite après chacun. Si le tour s'arrête en cours, les axes faits sont déjà dans le repo.

### Fin
**Écris, ne déverse pas** : n'affiche pas le JSON. Termine par un tableau court — par axe traité :
items ajoutés (rss/search/blogs) — le total du harvest, les **axes restants** (le cas échéant, pour
relancer), et le **SHA du dernier commit**. Pas de SHA = run échoué.

## Erreurs
- Un canal / un axe qui échoue : logguer et continuer à l'axe suivant, jamais avorter toute la boucle.
- `axis` (nom) absent de `sources.json` : le signaler, lister les axes disponibles.
- Un axe sans item réel : écrire quand même `axes_collected` (l'axe a été traité), signaler 0.
