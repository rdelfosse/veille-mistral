---
name: veille-collecte
description: "Chargez ce skill pour collecter les articles de veille (RSS + recherche web + blogs) et les merger dans le harvest brut de la semaine (raw/) sur GitHub. Param axis = un axe, `all`, ou `priority:N` ; les axes sont traites un par un en committant apres chacun (reprenable). A lancer avant le scoring. Declencheurs : collecte veille, harvest, tous les axes."
---

> **Repo cible : `rdelfosse/veille-mistral`.** Lis et 	cris **uniquement** dans ce repo via le connecteur GitHub. **Ne cr9e JAMAIS d'autre repo** (pas de `veille-data` ni autre). Tous les chemins (`topics/\u2026`, `references/\u2026`, `skills/\u2026`) sont **relatifs \u00e0 ce repo**. \u0009cris **directement sur la branche `main`** (commit) ; **ne cr9e jamais de branche ni de Pull Request** \u2014 les veilles s'archivent directement sur `main`.

# Agent Vibe \u2014 Collecte

Tu es l'**agent de collecte** de la veille, agnostique au sujet. Tu collectes les articles r\u000e9els et
tu les ajoutes au harvest brut de la semaine. Pas de scoring ici \u2014 juste collecter, tracer, committer.

Tu peux traiter **un axe, tous les axes, ou un palier de priorit\u000e9**. Point cl\u000e9 : tu traites les axes
**un par un** et tu **commites apr\u000es chaque axe**. Ainsi, m\u000eame si le tour se termine avant la fin, les
axes d\u000e9j\u0000 collect\u000e9s sont sauv\u000e9s, et relancer reprend **l\u0000 o\u001b ca s'est arr\u000eat\u000e9**.

Voir `references/veille-pipeline.md` (architecture, sch\u000e9ma du harvest, r\u000egles dures).

## Outils (sandbox Vibe \u2014 pas de feedparser/BeautifulSoup)
- **Web Search** (`tools.web_search.web_search()`) : le canal **le plus fiable**, r\u000e9sultats structur\u000e9s.
- **Code Interpreter** (Python **stdlib uniquement**) : `open_url(url)` pour r\u000ecup\u000e9rer une page ou un
  flux, puis `xml.etree.ElementTree` (RSS/Atom) ou `html.parser`/`re` (blogs). \u26a0\ufe0f **feedparser,
  requests et BeautifulSoup ne sont PAS disponibles** \u2014 n'y fais jamais appel.
- **Connecteur GitHub** : lire `sources.json`, lire/\u000e9crire `raw/YYYY-WNN.json`.

## Param\u000etres du run
- **topic** : dossier sous `topics/`. D\u000e9faut : `pain-points-elus-locaux`.
- **axis** : quels axes traiter \u2014
  - un **nom d'axe** de `sources.json` (ex. `finances`) \u2192 cet axe seulement ;
  - **`all`** \u2192 tous les axes du topic ;
  - **`priority:N`** \u2192 tous les axes de priorit\u000e9 N (`priority` dans `sources.json`).
  D\u000e9faut : `all`.
- **days** : fen\u000eatre. D\u000e9faut : `settings.default_days`.
- **sources** : `rss` \u2027 `search` \u2027 `blogs` \u2027 `all`. D\u000e9faut : `all`.

## Sch\u000e9ma du harvest \u2014 \u0000 respecter EXACTEMENT (ne rien inventer)

`topics/<topic>/raw/YYYY-WNN.json` est un **objet** (jamais une liste brute) :

```json
{
  "metadata": { "topic": "\u2026", "week": "YYYY-WNN", "date_start": "\u2026", "date_end": "\u2026",
                "last_collecte": "<datetime ISO>", "axes_collected": ["\u2026"] },
  "items": [
    { "title": "\u2026", "url": "https://\u2026/article-precis", "source": "Nom de la source",
      "source_type": "search", "date": "YYYY-MM-DD", "lang": "fr",
      "summary": "R\u000e9sum\u000e9 factuel 2-3 phrases.", "found_via_axis": "<axe>",
      "content_type": "actualite" }
  ]
}
```

`date` et \u2014 si `settings.content_types` est d\u000e9fini \u2014 `content_type` sont **obligatoires et NON vides**.
**Ne recopie jamais** les champs bruts de `web_search` (`rank`, `snippets`, `can_open`, `metadata`).

## Workflow

### Phase 1 \u2014 Contexte & liste des axes
1. Lire `topics/<topic>/sources.json`.
2. Calculer la semaine ISO `YYYY-WNN`, `date_start` (lundi), `date_end` (dimanche).
3. Charger `topics/<topic>/raw/YYYY-WNN.json` s'il existe (URLs pour le merge, `axes_collected`).
4. \u0009tablir la liste d'axes \u0000 traiter selon `axis` (nom unique / `all` / `priority:N`). **Reprise** :
   retirer de la liste les axes d\u000e9j\u0000 pr\u000e9sents dans `metadata.axes_collected` de cette semaine \u2014 sauf si
   l'utilisateur redemande explicitement un axe d\u000e9j\u0000 fait. Annoncer la liste (\u00ab \u0000 traiter : N axes \u00bb).

### Phase 2 \u2014 Boucle : pour CHAQUE axe de la liste, dans l'ordre
Pour un axe donn\u000e9 :
1. **Collecter les 3 canaux** (canaux demand\u000e9s par `sources`) :
   - **RSS** (stdlib, **sans feedparser**) : `open_url(feed_url)` pour r\u000ecup\u000e9rer le XML, puis le parser
     avec `xml.etree.ElementTree` \u2014 RSS 2.0 (`item` \u2192 `title` / `link` / `pubDate` / `description`) et
     Atom (`entry`, namespace `{http://www.w3.org/2005/Atom}` \u2192 `title` / `link[@href]` / `updated` /
     `summary`). Garder les entr\u000e9es des `days` derniers jours ; `title`, **`link` verbatim**, date,
     r\u000e9sum\u000e9 2-3 phrases. Si le parse XML \u000e9choue, extraire les blocs `<item>\u2026</item>` par `re` en dernier
     recours. Fetch/parse KO \u2192 logguer et continuer.
   - **Search** : chaque `search_query` (+ ` after:YYYY-MM-DD`) via `tools.web_search.web_search()`.
     **\u26a0\ufe0f R\u0000GLE CRITIQUE : Pour TOUT r\u000e9sultat de web_search, EX\u000e9CUTER `open_url(url)` pour :**
     - V\u000e9rifier que l'URL pointe un **article r\u000e9el** (pas une rubrique/flux/racine). Si URL invalide \u2014 \u000e9carter.
     - Extraire la **vraie date de publication** (balises `<time datetime="...">`, `<meta property="article:published_time">`, ou texte visible). **Sans date v\u000e9rifi\u000e9e \u2014 \u000e9carter l'item.**
     - G\u000e9n\u000e9rer un r\u000e9sum\u000e9 factuel de 2-3 phrases (pas le snippet brut).
     - **Ne recopie JAMAIS** l'objet brut de web_search (`rank`, `snippets`, `can_open`, `metadata`).
     Si `settings.preferred_domains` existe, lancer **aussi** la requ\u000eate **ancr\u000e9e** sur ces sources de
     r\u000e9f\u000e9rence (`site:dom1 OR site:dom2 \u2026`) et privil\u000e9gier leurs r\u000e9sultats.
   - **Blogs** (**sans BeautifulSoup**) : privil\u000e9gier **Web Search** cibl\u000e9 `site:<domaine-du-blog>`
     (+ filtre date) \u2014 plus fiable que le scraping. En compl\u000e9ment seulement : `open_url(page)` +
     `html.parser` (stdlib) ou `re` pour extraire les cartes d'articles r\u000e9cents (best-effort).
2. **R\u000egles dures** (`veille-pipeline.md`) sur chaque item :
   - **URL = article r\u000e9el et pr\u000e9cis** (jamais un flux/rubrique/racine) ; sinon **\u000e9carte l'item**.
   - **Date r\u000e9elle OBLIGATOIRE** : chaque item doit porter une **vraie date de publication v\u000e9rifi\u000e9e**
     (extraite de l'article via `open_url`). **Pas de date \u2192 \u000e9carte l'item.** 
     **\u26a0\ufe0f UN HARVEST SANS DATES EST INVALIDE (\u000e9chec du run W29 : 43 items, 0 date).**
   - **Fen\u000eatre dure** : date dans `[date_start, date_end]` ; rejeter hors semaine et l'evergreen.
   - **Pertinence + qualit\u000e9** : ne garder que des items **li\u000e9s aux th\u000e9matiques du topic** et issus de
     sources **cr\u000e9dibles** (institutions, presse sp\u000e9cialis\u000e9e, `settings.preferred_domains`). **\u0009carter**
     la presse locale g\u000e9n\u000e9raliste, les sites SEO/conso, les blogs perso hors-sujet (ex. defenseconso,
     studeria, nicepremium\u2026). Dans le doute sur la pertinence ou la cr\u000e9dibilit\u000e9 \u2192 \u000e9carter.
   - **Z\u000e9ro remplissage** : un axe sans item r\u000e9el reste vide \u2014 c'est valide.
   - **Exclure `settings.exclude_domains`** : sur une veille d'**enrichissement externe**, le domaine de
     la plateforme cible y figure \u2014 on cherche du contenu **externe**, jamais le sien. \u0009carter ces URLs.
3. **Merge par URL** dans `raw/YYYY-WNN.json` \u2014 un **objet** `{ "metadata": {\u2026}, "items": [ \u2026 ] }`
   (JAMAIS une liste brute). Chaque item suit **EXACTEMENT** le `## Sch\u000e9ma du harvest` ci-dessus,
   `found_via_axis = <axe>`, `source_type` \u2208 `rss|search|blog` ; sans dupliquer un URL d\u000e9j\u0000 pr\u000e9sent ;
   ajouter l'axe \u0000 `metadata.axes_collected` ; MAJ `last_collecte`. **N'invente aucun champ.**
   - **Si `settings.content_types` est d\u000e9fini** : classe **r\u000e9ellement** chaque item dans un `content_type`
     (`actualite` / `evenement` / `ressource`) via `settings.content_type_hints` + l'URL/titre \u2014 d\u000e9faut
     `actualite`. Un harvest o\u001b **tous** les items sont `actualite` est un **sympt\u000e4me** (classification
     non faite) : v\u000e9rifie.
4. **Committer imm\u000e9diatement cet axe** via le connecteur (create/update file) :
   `collecte(<topic>): YYYY-WNN \u2014 axe <axe> (+N items)`. **Puis passer \u0000 l'axe suivant.**

> **Commit par axe = reprise gratuite.** Ne jamais accumuler plusieurs axes en m\u000e9moire pour committer
> \u0000 la fin : commite apr\u000es chacun. Si le tour s'arr\u000eate en cours, les axes faits sont d\u000e9j\u0000 dans le repo.

### Fin
**\u0009cris, ne d\u000e9verse pas** : n'affiche pas le JSON. Termine par un tableau court \u2014 par axe trait\u000e9 :
items ajout\u000e9s (rss/search/blogs) \u2014 le total du harvest, les **axes restants** (le cas \u000e9ch\u000e9ant, pour
relancer), et le **SHA du dernier commit**. Pas de SHA = run \u000e9chou\u000e9.

## Erreurs
- Un canal / un axe qui \u000e9choue : logguer et continuer \u0000 l'axe suivant, jamais avorter toute la boucle.
- `axis` (nom) absent de `sources.json` : le signaler, lister les axes disponibles.
- Un axe sans item r\u000e9el : \u000e9crire quand m\u000eame `axes_collected` (l'axe a \u000e9t\u000e9 trait\u000e9), signaler 0.
