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

## 1. Veille (agent `Veille élus locaux`)

```
Lance la veille pour le topic pain-points-elus-locaux sur les 7 derniers jours, toutes sources
(rss + search + blogs), tous axes. Lis d'abord la config et l'historique dans le repo GitHub
rdelfosse/veille-mistral (sources.json, scoring.md, references/, data/), puis écris le JSON ET le
digest de la semaine et commit-les.

Exécute réellement chaque étape en appelant les outils : lance effectivement les search_queries
(Web Search) et les blogs de chaque axe, pas seulement le premier flux RSS. Respecte le contrôle
qualité avant de conclure (les DEUX fichiers committés, URLs verbatim sans mojibake, aucun take
dupliqué, somme(by_axis) == total_insights). N'affiche pas de plan, ne simule rien, ne me demande
rien à faire manuellement ; toute écriture passe par le connecteur GitHub, jamais par git. Termine
seulement après avoir committé data/ et digest/.
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
