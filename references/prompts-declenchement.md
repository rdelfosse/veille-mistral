# Prompts de déclenchement — prêts à coller (Vibe)

Un prompt par agent. Coller tel quel dans la conversation avec l'agent Vibe correspondant (ou comme
prompt de la tâche planifiée). Adapter `topic` / `week` si besoin. Le repo est `rdelfosse/veille-mistral`.

Chaque prompt embarque la **clause anti-simulation** — c'est elle qui a manqué aux premiers runs.

---

## Clause anti-simulation (rappel)

> Exécute réellement chaque étape en appelant les outils. N'affiche pas de plan, ne me demande rien à
> faire manuellement, ne simule aucun résultat, ne laisse aucun placeholder. Toute lecture/écriture
> passe par le connecteur GitHub (create/update file), jamais par des commandes git. Ne conclus
> qu'après avoir committé les fichiers dans le repo `rdelfosse/veille-mistral`.

---

## 1. Veille — pipeline shardé (recommandé)

Trois agents courts qui committent chacun un fichier. **Collecte** se lance une fois **par axe**.

### 1a. Collecte (agent `Collecte`) — un run par axe

```
Collecte les articles de l'axe finances pour le topic pain-points-elus-locaux, semaine courante,
toutes sources (rss + search + blogs). Lis topics/pain-points-elus-locaux/sources.json et
references/veille-pipeline.md dans rdelfosse/veille-mistral, puis merge les items réels dans
topics/pain-points-elus-locaux/raw/<YYYY-WNN>.json et commit.

Chaque url doit ouvrir un article précis (jamais un lien …/flux/…, …/feed, .xml, ni une page
d'accueil/rubrique). Rejette tout article hors de la semaine et tout contenu evergreen sans date.
N'invente aucun item pour remplir l'axe. N'affiche pas le JSON : écris via le connecteur GitHub et
réponds-moi uniquement le SHA du commit + le nombre d'items ajoutés (rss/search/blogs).
```
> Relancer en remplaçant `finances` par chaque axe voulu : `rh-ingenierie`, `climat-transition`, etc.
> (liste dans `sources.json`). Chaque run append au même `raw/<semaine>.json`.

### 1b. Scoring (agent `Scoring`) — une fois, après la collecte

```
Score le harvest de la semaine courante pour le topic pain-points-elus-locaux. Lis
topics/pain-points-elus-locaux/raw/<YYYY-WNN>.json, scoring.md, references/scoring-rubric.md,
output-schema.md et veille-pipeline.md, ainsi que l'historique data/ pour la dédup. Déduplique
(URL + titre/sujet), applique les garde-fous qualité, score chaque insight sur tous les axes +
actionability + take, puis écris topics/pain-points-elus-locaux/data/<YYYY-WNN>.json et commit.

Recalcule les stats APRÈS filtrage : total_insights == nombre réel d'insights, somme(by_axis) ==
total. N'affiche pas le JSON : écris via le connecteur et réponds-moi uniquement le SHA + les stats.
```

### 1c. Digest (agent `Digest`) — une fois, après le scoring

```
Génère le digest de la semaine courante pour le topic pain-points-elus-locaux à partir de
topics/pain-points-elus-locaux/data/<YYYY-WNN>.json (et output-schema.md pour le gabarit). Groupe
par primary_axis, trie par actionability puis date, et vérifie que les comptes collent au JSON.
Écris topics/pain-points-elus-locaux/digest/<YYYY-WNN>.md et commit.

Ne complète ni n'invente rien : le digest ne fait que refléter le JSON. N'affiche pas le digest :
écris via le connecteur et réponds-moi uniquement le SHA du commit + total/top axes.
```

## 1-bis. Veille tout-en-un (monolithe, petit topic / run unique)

```
Lance la veille pour le topic pain-points-elus-locaux sur les 7 derniers jours, toutes sources
(rss + search + blogs), tous axes. Lis d'abord la config et l'historique dans le repo GitHub
rdelfosse/veille-mistral (sources.json, scoring.md, references/, data/), puis écris le JSON ET le
digest de la semaine et commit-les.

Exécute réellement chaque étape en appelant les outils : lance effectivement les search_queries
(Web Search) et les blogs de chaque axe, pas seulement le premier flux RSS. Respecte le contrôle
qualité avant de conclure (les DEUX fichiers committés, URLs d'article réelles sans mojibake, aucun
item hors semaine, aucun take dupliqué, stats recalculées après filtrage : somme(by_axis) ==
total_insights). N'affiche pas le contenu, ne simule rien, ne me demande rien à faire manuellement ;
écriture via le connecteur GitHub, jamais par git. Termine par les SHA des commits data/ et digest/.
```

## 2. Angles morts (agent `Angles morts`)

```
Analyse les angles morts pour le topic pain-points-elus-locaux, semaine la plus récente présente
dans data/. Lis dans le repo GitHub rdelfosse/veille-mistral : topics/<topic>/analysis.md,
scoring.md, references/analysis-method.md, et le data/ + digest/ de la semaine. Cartographie par
Web Search ce que chaque acteur en place (listé dans analysis.md) propose DÉJÀ, isole les angles
morts sous la contrainte du topic, puis écris topics/<topic>/analysis/angles-morts-YYYY-WNN.md et
commit-le.

Exécute réellement chaque recherche et l'écriture via le connecteur GitHub. N'affiche pas de plan,
ne simule aucun résultat, ne me demande rien à faire manuellement, jamais de commandes git. Termine
seulement après avoir committé le fichier.
```

## 3. Idées micro-services (agent `Idées micro-services`)

```
Génère les idées de micro-services pour le topic pain-points-elus-locaux à partir de la dernière
analyse d'angles morts. Lis dans le repo GitHub rdelfosse/veille-mistral : le dernier
topics/<topic>/analysis/angles-morts-*.md, le digest/ correspondant, analysis.md et scoring.md.
Produis des idées mono-tâche filtrées par les critères du topic, groupées par catégorie, puis écris
topics/<topic>/analysis/idees-YYYY-WNN.md et commit-le.

Si aucune analyse d'angles morts n'existe, dis-le et arrête-toi (ne l'invente pas). Exécute
réellement l'écriture via le connecteur GitHub. N'affiche pas de plan, ne simule rien, ne me demande
rien à faire manuellement, jamais de commandes git. Termine seulement après avoir committé le fichier.
```

## 4. Critique (agent `Critique idées`)

```
Critique les idées du topic pain-points-elus-locaux à partir du dernier fichier
topics/<topic>/analysis/idees-*.md. Lis dans le repo GitHub rdelfosse/veille-mistral : ce fichier
d'idées, le data/ + digest/ de la même semaine (la base de preuves), analysis.md et scoring.md.
Applique d'abord les six forcing questions (Garry Tan) en grille de notation sur la donnée réelle de
veille — verdict KILL / REWORK / SURVIVE par idée — puis le reframe CEO des survivants. Écris
topics/<topic>/analysis/critique-YYYY-WNN.md et commit-le.

N'invente aucune preuve : si la donnée de veille ne soutient pas une réponse, c'est un signal ❌
(c'est le but). Exécute réellement l'écriture via le connecteur GitHub. N'affiche pas de plan, ne
simule rien, ne me demande rien à faire manuellement, jamais de commandes git. Termine seulement
après avoir committé le fichier.
```

---

## Variantes utiles

- **Fenêtre / axe ciblés (veille)** : « … sur les 14 derniers jours, axe finances seulement … ».
- **Semaine précise (agents aval)** : « … pour la semaine 2026-W27 … ».
- **Tous les topics (veille)** : remplacer le topic par « tous les topics (hors _template) ».
