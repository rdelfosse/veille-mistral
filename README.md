# Veille-Mistral

Agent de veille hebdomadaire **réutilisable sur n'importe quel sujet**, conçu pour tourner
dans **Mistral Le Chat / Vibe** (app grand public `chat.mistral.ai`) par l'équipe Lab des Territoires.

La logique est : collecte → scoring multi-axes → dédup → digest hebdo. L'exécution repose sur
les briques natives de Vibe :

| Outil et description |
|---|
| **Agent custom** dont les instructions = `agent/instructions.md` |
| Un agent qui boucle : **Web Search** (requêtes) + **Code Interpreter** (RSS/blogs en Python) |
| **Tâche planifiée** Work Mode (ex. tous les lundis 8h) |
| **Connecteur GitHub (MCP)** → l'agent lit/écrit ce repo |
| Lecture des JSON existants depuis GitHub |

> **Le Chat est devenu « Vibe »** (rebrand mi-2026, même compte). Les tâches planifiées
> récurrentes et les agents custom sont natifs. C'est cette version qui est ciblée ici.

## Structure du repo

```
veille-mistral/
├─ agent/
│  ├─ instructions.md           ← prompt de l'agent de veille (le cœur)
│  ├─ angles-morts.md           ← agent d'analyse : cartographie les angles morts
│  ├─ idees-microservices.md    ← agent d'idéation : idées de micro-services
│  └─ critique-idees.md         ← agent de critique : destruction Garry Tan → reframe CEO
├─ references/
│  ├─ scoring-rubric.md         ← logique de scoring (générique)
│  ├─ output-schema.md          ← format JSON + digest
│  └─ analysis-method.md        ← méthode des agents aval (angles morts → idées → critique)
└─ topics/
   ├─ _template/                ← gabarit à cloner (jamais exécuté)
   │  ├─ sources.json
   │  ├─ scoring.md
   │  └─ analysis.md            ← brief des agents aval (acteurs, contraintes, critères)
   └─ pain-points-elus-locaux/  ← 1er sujet
      ├─ sources.json           ← settings + axes + sources
      ├─ scoring.md             ← barème de scoring du sujet
      ├─ analysis.md            ← brief d'analyse du sujet
      ├─ data/                  ← un JSON par semaine (YYYY-WNN.json) — écrit par la veille
      ├─ digest/                ← un Markdown par semaine (YYYY-WNN.md) — écrit par la veille
      └─ analysis/              ← livrables des agents aval (angles-morts / idees / critique)
```

Un **topic** = une thématique (un dossier). À l'intérieur, plusieurs **axes** (sous-angles)
permettent un scoring multi-dimensionnel.

## Le pipeline en 4 agents

Quatre agents Vibe distincts, chaînés — chacun lit la sortie GitHub du précédent :

```
veille  →  angles-morts  →  idées-microservices  →  critique
```

1. **veille** (`agent/instructions.md`) — collecte hebdo, scoring multi-axes, digest.
2. **angles-morts** (`agent/angles-morts.md`) — cartographie ce que les acteurs en place (BdT, État…)
   font DÉJÀ pour isoler les trous exploitables.
3. **idées-microservices** (`agent/idees-microservices.md`) — transforme les angles morts en idées de
   micro-services concrets, filtrés par les critères du topic.
4. **critique** (`agent/critique-idees.md`) — critique adversariale : les *six forcing questions* de
   Garry Tan (office hours) tuent les idées non soutenues par la donnée, puis reframe stratégique CEO
   des survivantes.

Les agents 2-4 sont **agnostiques au sujet** : toute la spécificité vit dans `topics/<topic>/analysis.md`
+ `scoring.md`. Voir `references/analysis-method.md` pour la méthode. Ils tournent **moins souvent que
la veille** (mensuel ou à la demande).

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

### 3. Créer l'agent

Le Chat → **Agents** → *Nouvel agent* :
- **Nom** : `Veille élus locaux`
- **Instructions** : coller l'intégralité de [`agent/instructions.md`](agent/instructions.md).
- **Outils à activer** : `Web Search`, `Code Interpreter`, **connecteur GitHub**.
- (Optionnel) **Memories** : activé, pour le contexte de dédup léger entre runs.

Créer de la même façon **trois agents d'analyse** (mêmes outils ; le Code Interpreter est facultatif) :
- `Angles morts` → instructions = [`agent/angles-morts.md`](agent/angles-morts.md)
- `Idées micro-services` → instructions = [`agent/idees-microservices.md`](agent/idees-microservices.md)
- `Critique idées` → instructions = [`agent/critique-idees.md`](agent/critique-idees.md)

> **Anti-simulation** : dans le prompt de déclenchement de chaque agent, exiger l'exécution réelle —
> *« Exécute réellement chaque étape en appelant les outils. N'affiche pas de plan, ne me demande rien
> à faire manuellement, ne simule aucun résultat. Toute écriture passe par le connecteur GitHub, jamais
> par des commandes git. Termine seulement après avoir committé les fichiers. »*

### 4. Planifier la veille (Work Mode)

Le Chat → **Tâches / Work Mode** → nouvelle tâche récurrente :
- **Agent** : `Veille élus locaux`
- **Cadence** : hebdomadaire, **lundi 08:00**
- **Prompt de déclenchement** : voir [`agent/prompts-declenchement.md`](agent/prompts-declenchement.md)
  (prompts prêts à coller pour les 4 agents, avec la clause anti-simulation).

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
