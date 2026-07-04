# Veille-Mistral

Agent de veille hebdomadaire **réutilisable sur n'importe quel sujet**, conçu pour tourner
dans **Mistral Le Chat / Vibe** (app grand public `chat.mistral.ai`) par l'équipe Lab des Territoires.

La logique est : collecte → scoring multi-axes → dédup → digest hebdo. L'exécution repose sur
les briques natives de Vibe :

| Outil et description |
|---|
| **Skills Vibe** (`skills/`) chargées dans Work — ou un agent custom collant un `SKILL.md` |
| Un agent qui boucle : **Web Search** (requêtes) + **Code Interpreter** (RSS/blogs en Python) |
| **Tâche planifiée** Work Mode (ex. tous les lundis 8h) |
| **Connecteur GitHub (MCP)** → l'agent lit/écrit ce repo |
| Lecture des JSON existants depuis GitHub |

> **Le Chat est devenu « Vibe »** (rebrand mi-2026, même compte). Les tâches planifiées
> récurrentes et les agents custom sont natifs. C'est cette version qui est ciblée ici.

## Structure du repo

```
veille-mistral/
├─ skills/                        ← Skills Vibe (1 dossier = 1 SKILL.md auto-porteur)
│  ├─ veille-collecte/            ← étape 1 : collecte par axe → raw/
│  ├─ veille-scoring/             ← étape 2 : scoring & dédup → data/
│  ├─ veille-digest/              ← étape 3 : mise en forme → digest/
│  ├─ veille-tout-en-un/          ← veille monolithe (run unique / petit topic)
│  ├─ veille-angles-morts/        ← analyse : cartographie les angles morts
│  ├─ veille-idees-microservices/ ← idéation : idées de micro-services
│  └─ veille-critique-idees/      ← critique : destruction Garry Tan → reframe CEO
├─ references/
│  ├─ scoring-rubric.md         ← logique de scoring (générique)
│  ├─ output-schema.md          ← format JSON + digest
│  ├─ veille-pipeline.md        ← architecture du pipeline veille + schéma harvest + règles dures
│  ├─ analysis-method.md        ← méthode des agents aval (angles morts → idées → critique)
│  └─ prompts-declenchement.md  ← messages d'invocation prêts à coller (anti-simulation)
└─ topics/
   ├─ _template/                ← gabarit à cloner (jamais exécuté)
   │  ├─ sources.json
   │  ├─ scoring.md
   │  └─ analysis.md            ← brief des agents aval (acteurs, contraintes, critères)
   └─ pain-points-elus-locaux/  ← 1er sujet
      ├─ sources.json           ← settings + axes + sources
      ├─ scoring.md             ← barème de scoring du sujet
      ├─ analysis.md            ← brief d'analyse du sujet
      ├─ raw/                   ← harvest brut par semaine — écrit par l'agent collecte
      ├─ data/                  ← un JSON par semaine (YYYY-WNN.json) — écrit par le scoring
      ├─ digest/                ← un Markdown par semaine (YYYY-WNN.md) — écrit par le digest
      └─ analysis/              ← livrables des agents aval (angles-morts / idees / critique)
```

Un **topic** = une thématique (un dossier). À l'intérieur, plusieurs **axes** (sous-angles)
permettent un scoring multi-dimensionnel.

## Le pipeline

Des agents Vibe distincts, chaînés — chacun lit la sortie GitHub du précédent et **commite son seul
fichier** (un agent = un tour court = un commit, pour ne jamais « tomber en rade » avant d'écrire) :

```
collecte[× axe] → scoring → digest   →   angles-morts → idées → critique
     raw/          data/     digest/          analysis/
```

**Veille** (voir `references/veille-pipeline.md`) :
1. **collecte** (`skills/veille-collecte/SKILL.md`) — un run **par axe** ; collecte les articles réels → `raw/`.
2. **scoring** (`skills/veille-scoring/SKILL.md`) — score multi-axes, déduplique, garde-fous qualité → `data/`.
3. **digest** (`skills/veille-digest/SKILL.md`) — mise en forme lisible → `digest/`.
   *(Alternative : `skills/veille-tout-en-un/SKILL.md`, le monolithe tout-en-un, pour un petit topic / run unique.)*

**Analyse aval** (voir `references/analysis-method.md`) :
4. **angles-morts** (`skills/veille-angles-morts/SKILL.md`) — ce que les acteurs en place (BdT, État…) font DÉJÀ,
   pour isoler les trous.
5. **idées-microservices** (`skills/veille-idees-microservices/SKILL.md`) — les angles morts → idées concrètes.
6. **critique** (`skills/veille-critique-idees/SKILL.md`) — les *six forcing questions* de Garry Tan tuent les idées
   non soutenues par la donnée, puis reframe stratégique CEO des survivantes.

Tous les agents sont **agnostiques au sujet** : la spécificité vit dans `topics/<topic>/` (`sources.json`,
`scoring.md`, `analysis.md`). Prompts prêts à coller : `references/prompts-declenchement.md`.

## Installation côté Mistral Le Chat / Vibe

### 1. Mettre ce repo sur GitHub

L'agent persiste ses résultats via le connecteur GitHub. Il faut donc que ce dossier soit
un repo GitHub (privé recommandé) :

```bash
git init
git add .
git commit -m "Scaffold veille-mistral"
gh repo create veille-mistral --private --source=. --push   # ou via l'UI GitHub
```

### 2. Connecter GitHub dans Le Chat

Le Chat → **Connectors** → ajouter le connecteur **GitHub** → autoriser l'accès au repo
`veille-mistral`. (Réf. : directory de connecteurs MCP de Le Chat.)

### 3. Installer les Skills (Vibe Work)

Vibe Work charge des **Skills** depuis `/home/user/skills/<nom>/SKILL.md`. Copie chaque dossier de
[`skills/`](skills/) du repo vers `/home/user/skills/` (ou fais-les générer par le skill natif
`skill-creator`). Une fois installés, ils se déclenchent par mot-clé (leur `description`) ou à la
demande :

- **Veille** : `veille-collecte` · `veille-scoring` · `veille-digest` (pipeline, voir §4), ou
  `veille-tout-en-un` pour un run unique / petit topic.
- **Analyse aval** : `veille-angles-morts` · `veille-idees-microservices` · `veille-critique-idees`.

Outils à activer pour la session : `Web Search`, `Code Interpreter`, **connecteur GitHub**.
(Optionnel) **Memories** pour un contexte de dédup léger entre runs.

> **Alternative sans Skills** : coller le corps d'un `SKILL.md` comme instructions d'un **agent custom**
> (Le Chat → Agents → Nouvel agent). Même contenu, invocation par agent au lieu de mot-clé.

> **Anti-simulation** : à l'invocation, exiger l'exécution réelle —
> *« Exécute réellement chaque étape en appelant les outils. N'affiche pas de plan, ne me demande rien
> à faire manuellement, ne simule aucun résultat. Toute écriture passe par le connecteur GitHub, jamais
> par des commandes git. Termine seulement après avoir committé les fichiers (réponds le SHA). »*

### 4. Planifier la veille (Work Mode)

Le Chat → **Tâches / Work Mode** → nouvelle tâche récurrente :
- **Agent** : `Veille élus locaux`
- **Cadence** : hebdomadaire, **lundi 08:00**
- **Prompt de déclenchement** : voir [`references/prompts-declenchement.md`](references/prompts-declenchement.md)
  (messages d'invocation prêts à coller pour chaque skill, avec la clause anti-simulation).

### 5. Lire les résultats dans Obsidian (optionnel) ou un lecteur MD

Le connecteur GitHub écrit `digest/YYYY-WNN.md` dans le repo. Pour les lire dans Obsidian :
faire de ce repo (ou du dossier `topics/*/digest/`) un dossier du vault et installer le plugin
**Obsidian Git** (pull auto). L'automatisation reste 100 % cloud Mistral, pas de tunnel ni de
machine allumée nécessaires.

## Lancement manuel

Dans une conversation avec l'agent :

```
Lance la veille pour le topic pain-points-elus-locaux, 14 derniers jours, axe finances seulement.
```

| Paramètre | Valeurs | Défaut |
|-----------|---------|--------|
| topic | nom d'un dossier sous `topics/` | `pain-points-elus-locaux` |
| axis | un axe du `sources.json`, ou `all` | `all` |
| days | nombre de jours en arrière | `settings.default_days` (7) |
| sources | `rss` · `search` · `blogs` · `all` | `all` |

## Ajouter un nouveau sujet

1. Copier `topics/_template/` vers `topics/<mon-sujet>/`.
2. Remplir `sources.json` (label, axes, flux RSS, requêtes, blogs).
3. Remplir `scoring.md` (public cible, mots-clés, barème par axe).
4. Commit + push sur GitHub.
5. Demander à l'agent : `Lance la veille pour le topic <mon-sujet>`.

## Sortie

Pour chaque run et chaque topic :
- `topics/<topic>/data/YYYY-WNN.json` — données structurées (dédupliquées, scorées).
- `topics/<topic>/digest/YYYY-WNN.md` — digest lisible.

Relancer dans la même semaine **fusionne** les nouveaux insights dans le fichier existant
(dédup par URL).

## Licence & crédits

Ce projet est sous licence **MIT** (voir [`LICENSE`](LICENSE)).

L'agent de critique (`skills/veille-critique-idees/SKILL.md`) **adapte** des idées de
[gstack](https://github.com/garrytan/gstack) de **Garry Tan** (skills `office-hours` et
`plan-ceo-review`), sous licence MIT. Détails et notice d'origine dans
[`THIRD-PARTY-NOTICES.md`](THIRD-PARTY-NOTICES.md).
