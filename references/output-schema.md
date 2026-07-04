# Output Schema — Veille (multi-topics)

Format de sortie : un JSON structuré + un digest Markdown par semaine ISO, dans le dossier
du topic (écrits dans le repo GitHub via le connecteur).

```
topics/<topic>/data/YYYY-WNN.json     ← données structurées (machine)
topics/<topic>/digest/YYYY-WNN.md     ← version lisible (humain)
```

## 1. JSON Schema (`topics/<topic>/data/YYYY-WNN.json`)

Un fichier par semaine ISO (ex. `2026-W26.json`).

```json
{
  "metadata": {
    "topic": "mon-sujet",
    "week": "2026-W26",
    "date_start": "2026-06-22",
    "date_end": "2026-06-28",
    "last_run": "2026-06-28T10:30:00Z",
    "summary": "### Premier angle\n\nParagraphe en **Markdown** avec *nuance éditoriale* et chiffres clés...\n\n### Second angle\n\nDeuxième paragraphe...",
    "run_params": {
      "axes": ["all"],
      "days": 7,
      "sources": ["rss", "search", "blogs"]
    },
    "stats": {
      "total_insights": 18,
      "by_axis": {
        "axe_a": 7,
        "axe_b": 11
      }
    }
  },
  "insights": [
    {
      "id": "ins_20260628_a1b2c3",
      "title": "Titre de l'article ou du post",
      "url": "https://example.com/article",
      "source": "Nom de la source",
      "source_type": "rss",
      "date": "2026-06-27",
      "collected_at": "2026-06-28T10:30:00Z",
      "lang": "fr",
      "summary": "Résumé factuel en 2-3 phrases.",
      "editorial_take": "Le pain point précis exprimé. L'angle de solution / d'offre suggéré.",
      "axes": {
        "axe_a": 1,
        "axe_b": 3
      },
      "primary_axis": "axe_b",
      "actionability": {
        "score": 2,
        "article_potential": 2,
        "cross_links": []
      },
      "status": "new"
    }
  ]
}
```

### Champs metadata

| Champ | Type | Description |
|-------|------|-------------|
| `topic` | string | Nom du dossier de topic |
| `week` | string | Identifiant semaine ISO : `YYYY-WNN` |
| `date_start` | string | Lundi de la semaine (date ISO) |
| `date_end` | string | Dimanche de la semaine (date ISO) |
| `last_run` | string | Horodatage du dernier run (datetime ISO) |
| `summary` | string | Résumé 150-200 mots en **Markdown** (`###` + paragraphes, `**gras**`, `*italique*`). 2-3 blocs. Mots-clés du `scoring.md` tissés naturellement. |
| `run_params` | object | Paramètres du run |
| `stats` | object | `total_insights` + `by_axis`. `by_axis` compte chaque insight **une seule fois sous son `primary_axis`** ; `somme(by_axis) == total_insights`. |

### Champs insight

| Champ | Type | Description |
|-------|------|-------------|
| `id` | string | ID unique : `ins_YYYYMMDD_` + 6 hex aléatoires |
| `title` | string | Titre original |
| `url` | string | URL source (clé de déduplication) |
| `source` | string | Nom de la source depuis `sources.json` |
| `source_type` | string | `"rss"`, `"search"` ou `"blog"` |
| `date` | string | Date de publication (date ISO 8601) |
| `collected_at` | string | Horodatage de collecte (datetime ISO 8601) |
| `lang` | string | `"fr"`, `"en"`, ... |
| `summary` | string | Résumé factuel 2-3 phrases |
| `editorial_take` | string | Take 2 phrases (pain point + angle de solution), seulement si actionability ≥ 2 |
| `axes` | object | Score 0-3 pour chaque axe défini dans `sources.json` |
| `primary_axis` | string | Axe au score le plus haut |
| `actionability` | object | `score` (0-3), `article_potential` (0-3), `cross_links` (array, vide si pas de cross-référence configurée) |
| `status` | string | `"new"`, `"updated"` ou `"archived"` |

### Cycle de vie du statut

1. `"new"` — collecté pour la première fois
2. `"updated"` — recollecté avec nouvelles infos (même URL, contenu différent)
3. `"archived"` — plus vieux que `archive_after_days`

## 2. Digest Markdown (`topics/<topic>/digest/YYYY-WNN.md`)

```markdown
# Veille — <Label du topic> — Semaine 2026-W26

> 2026-06-22 → 2026-06-28 · sources : rss + search + blogs · axes : all
> 18 insights (12 nouveaux, 1 mis à jour)

<!-- summary Markdown généré -->
### Premier angle
Paragraphe...

### Second angle
Paragraphe...

---

## Axe A (7 insights, 5 nouveaux)

### [3/3] Titre de l'insight
**Source** : Nom · 2026-06-27 · FR
> Take : le pain point précis exprimé. L'angle de solution / d'offre suggéré.

Résumé factuel en 2-3 phrases.

🔗 https://example.com/article

### [2/3] Autre titre
...

---

## Axe B (11 insights, 7 nouveaux)
...

---

## Récapitulatif
- **Total** : 18 insights (12 nouveaux, 1 mis à jour)
- **Top axes** : Axe B (11) · Axe A (7)
- **Opportunités (actionability ≥ 2)** : 6
- **Sources auto-ajoutées** : 1
```

## 3. Résumé de fin de conversation

```
VEILLE — mon-sujet — 2026-06-28 — 7 derniers jours
Sources: rss + search + blogs | Axes: all
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

AXE: Axe B (11 insights, 7 nouveaux)
─────────────────────────────────────────────────────
[3/3] Titre de l'insight
      Source: Nom | 2026-06-27 | FR
      > Take : le pain point + l'angle de solution.
      https://example.com/article

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RÉSUMÉ
  Total insights: 18 (12 nouveaux, 1 mis à jour)
  Top axes:  Axe B (11) | Axe A (7)
  Opportunités (actionability ≥ 2): 6
```

## Règles d'affichage

1. **Trier par axe**, puis actionability (desc), puis date (desc).
2. **Format** : préfixe `[actionability/axis_score]` pour le scan rapide.
3. **Take** : seulement pour actionability ≥ 2, indenté avec `>`.
4. **URL** : toujours en dernière ligne du bloc insight.
5. **Récapitulatif** : stats agrégées en bas.
