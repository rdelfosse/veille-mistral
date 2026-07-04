# Veille — pipeline en étapes (pour Vibe)

La veille est **découpée en petits agents** qui se passent le relais via des fichiers committés sur
GitHub. Raison : un agent monolithique (collecter 12 axes × 3 canaux, scorer, écrire 2 fichiers)
dépasse le budget d'un tour Vibe et **meurt avant de committer**. Découpé, chaque étape est courte
et **commite son seul fichier** avant de finir.

```
collecte[× axe]  →  scoring  →  digest   →   angles-morts  →  idées  →  critique
raw/YYYY-WNN.json    data/…json   digest/…md      analysis/…md
```

| Étape | Agent | Lit | Écrit (1 fichier) |
|---|---|---|---|
| Collecte | `skills/veille-collecte/SKILL.md` | `sources.json` (un axe) | `raw/YYYY-WNN.json` (append) |
| Scoring | `skills/veille-scoring/SKILL.md` | `raw/`, `scoring.md`, `references/` | `data/YYYY-WNN.json` |
| Digest | `skills/veille-digest/SKILL.md` | `data/YYYY-WNN.json` | `digest/YYYY-WNN.md` |
| + aval | `angles-morts` / `idees-microservices` / `critique-idees` | voir `analysis-method.md` | `analysis/…` |

La **collecte est shardée par axe** : on lance l'agent collecte une fois par axe (chaque run append
au même `raw/YYYY-WNN.json`). Une fois tous les axes voulus collectés, on lance scoring puis digest.

## Schéma du harvest brut (`topics/<topic>/raw/YYYY-WNN.json`)

Données **non scorées** : juste ce qui a été collecté, tracé par source.

```json
{
  "metadata": {
    "topic": "mon-sujet",
    "week": "2026-W27",
    "date_start": "2026-06-29",
    "date_end": "2026-07-05",
    "last_collecte": "2026-07-04T08:00:00Z",
    "axes_collected": ["finances", "climat-transition"]
  },
  "items": [
    {
      "title": "Titre exact de l'article",
      "url": "https://source.fr/rubrique/article-precis",
      "source": "Nom de la source",
      "source_type": "rss",
      "date": "2026-06-30",
      "lang": "fr",
      "summary": "Résumé factuel 2-3 phrases.",
      "found_via_axis": "finances"
    }
  ]
}
```

- **Merge par URL** à chaque run de collecte : ne jamais dupliquer un item déjà présent ; ajouter
  l'axe courant à `axes_collected`. `found_via_axis` note l'axe dont les sources ont fait remonter
  l'item (informatif — le scoring re-score sur **tous** les axes).

## Règles dures — communes à toutes les étapes

### Repo cible & environnement (sandbox Vibe)
- **Repo cible unique : `rdelfosse/veille-mistral`.** Toute lecture/écriture passe par le connecteur
  GitHub sur **ce** repo. **Ne crée jamais d'autre repo** (pas de `veille-data`). Les chemins
  `topics/…`, `references/…`, `skills/…` sont relatifs à ce repo.
- **Écriture directe sur `main`.** Commit directement sur la branche par défaut ; **jamais de branche
  ni de Pull Request**. Les veilles s'archivent en continu sur `main` (l'historique git EST l'archive
  qui sert à repérer les signaux dans le temps) — une PR non mergée = une veille perdue.
- **Outils réellement disponibles** : `tools.web_search.web_search()` (fiable), `open_url(url)` (fetch),
  et la **stdlib Python** (`xml.etree.ElementTree`, `html.parser`, `re`, `json`, `datetime`…).
  ⚠️ **feedparser, requests et BeautifulSoup ne sont PAS disponibles.** RSS = XML → `ElementTree` ;
  blogs → Web Search `site:` de préférence, sinon `html.parser`/`re`.

### Zéro fabrication (surtout collecte)
1. Chaque item = **un article réel effectivement collecté**. `url` = **page d'article précise**,
   jamais un flux/rubrique/racine (`…/flux/…`, `…/localtis.xml`, `…/feed/`, accueil, catégorie).
2. **Pas de remplissage** : jamais d'item générique pour « couvrir » un axe. Un axe sans article réel
   n'apparaît pas dans le harvest — c'est un résultat valide.
3. **URL verbatim** : l'URL exacte de la source ; jamais reconstruite depuis le titre ni ré-encodée
   (aucun mojibake `%C3%A3%C2%A9`). URL douteuse → écarter l'item.

### Fenêtre temporelle dure
Ne garder que les items dont la **vraie date** de publication tombe dans `[date_start, date_end]`
(ou < `days` jours). Vérifier la date réelle de l'article ; rejeter tout item hors semaine et tout
contenu *evergreen* sans date (fiche pratique, page « formation »).

### Qualité & dédup (surtout scoring)
- Écarter les domaines **non éditoriaux** : sites de campagne, fermes de contenu/SEO, agrégateurs,
  réseaux sociaux, pages perso.
- Dédup **par URL et par titre/sujet** : même histoire vue sur deux sites = un seul insight.

### Écris, ne déverse pas (dompter Le Chat) — TOUTES les étapes
- **N'affiche jamais le fichier complet dans le chat.** Écris-le **directement** via le connecteur
  GitHub (create/update file), puis commit.
- **Termine par le SHA du commit** + un résumé court. Pas de SHA = run **échoué** : le dire, ne pas
  faire semblant ni inviter à copier-coller à la main. Jamais de commandes `git`.
- Un agent = **un fichier** à écrire : la charge tient dans un tour, commite avant de conclure.
