---
name: veille-publish-notion
description: "Chargez ce skill pour publier un digest de veille dans Notion : lit le digest Markdown d'une semaine sur GitHub (rdelfosse/veille-mistral) et cree (ou met a jour) une page Notion avec son contenu. Necessite un connecteur Notion. Declencheurs : publier digest sur Notion, page Notion veille."
---

> **Sources & cibles.** Lis le digest depuis le repo GitHub **`rdelfosse/veille-mistral`** (connecteur
> GitHub) et écris dans **Notion** (connecteur Notion). Ne crée aucun repo GitHub, aucune branche/PR.
> Requiert qu'un **connecteur Notion en écriture** soit activé dans la session Vibe.

# Agent Vibe — Publier un digest dans Notion

Tu publies un digest hebdomadaire de veille sous forme de **page Notion** lisible. Un digest = une page.

## Outils
- **Connecteur GitHub** : lire `topics/<topic>/digest/YYYY-WNN.md`.
- **Connecteur Notion** : créer / mettre à jour une page.

## Paramètres du run
- **topic** : défaut `pain-points-elus-locaux`.
- **week** : semaine ISO `YYYY-WNN`. Défaut : le digest le plus récent du topic.
- **notion_parent** : ID de la page ou base Notion parente où créer la page. Si absent, demander une
  seule fois à l'utilisateur l'emplacement, puis continuer.

## Workflow
### Phase 1 — Lire le digest (GitHub)
1. Lire `topics/<topic>/digest/YYYY-WNN.md`. S'il est absent : le signaler, proposer de lancer le
   pipeline de veille (`veille-digest`) d'abord. Ne rien inventer.

### Phase 2 — Créer / mettre à jour la page (Notion)
1. **Titre** : `Veille — <label du topic> — <YYYY-WNN>` (label depuis `sources.json`).
2. **Idempotence** : si une page du même titre existe déjà sous `notion_parent`, la **mettre à jour**
   (remplacer le corps) plutôt que d'en créer une seconde.
3. **Corps** : convertir le Markdown du digest en blocs Notion — titres `#`/`##`/`###` → headings,
   listes → bullets, liens conservés, citations `>` (les *takes*) → callouts/quotes. Conserver l'ordre.
4. (Optionnel) Renseigner des **propriétés** si la cible est une base : `Semaine`, `Topic`, `Date de
   publication`, `Nb insights` (lus dans le digest / le JSON).

### Fin
**Écris, ne déverse pas** : n'affiche pas le contenu recopié. Termine par l'**URL (ou l'ID) de la page
Notion** créée/mise à jour + un résumé d'une ligne. Pas d'URL/ID = échec (le dire, ne pas simuler).

## Erreurs
- Connecteur Notion absent/en lecture seule : le signaler clairement (l'utilisateur doit l'activer),
  ne pas contourner en collant le contenu dans le chat.
- Digest absent : proposer de lancer `veille-digest`.

## Note
Cette skill publie **une page par digest** (résumé hebdo lisible). Pour un usage « base de signaux
filtrable » (une ligne par insight), une variante future pourrait pousser le `data/*.json` vers une
base Notion — non couvert ici.
