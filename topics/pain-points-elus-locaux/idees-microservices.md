# Micro-services pour collectivités — idées à fort signal « on vous aide »

> 2026-06-28. Suite de `analyse-angles-morts-bdt.md`. Objectif : des **micro-services** (physiques
> ou digitaux), **non-financiers**, plus **impactants et démonstratifs** que des plateformes
> génériques. Critères : déployable vite, **visible / photographiable**, résout une douleur
> ressentie, idéalement bâti sur des briques **souveraines** (Mistral, données publiques ouvertes).
> Filtre : un bon micro-service tient en une phrase et produit une **preuve** (une photo, une carte,
> un chiffre économisé) en quelques jours.

## A. Déployables « cette semaine » — la preuve visible

| Nom | Pain (chiffre veille) | Le micro-service en 1 phrase | Preuve produite | Type |
|---|---|---|---|---|
| **Kit Fraîcheur École** | 80 % des écoles inadaptées à la chaleur | Une équipe itinérante pose en 48 h : voiles d'ombrage + brasseurs + film solaire + 1 **capteur de température connecté par classe** | La photo de la cour ombragée + la courbe « -6 °C » le jour même | [P]+[D] |
| **La Carte de la Chaleur des Écoles** | dilemme fermer/maintenir | Capteurs → carte publique live « quelles classes dépassent 30 °C » à l'échelle de l'EPCI | Une carte que le maire montre en conseil pour justifier l'action | [D][O] |
| **Voirie-Scan** | « dette grise » des routes, aide PNP épuisée | Un smartphone clipsé au pare-brise ; on roule une fois, l'IA rend une **carte priorisée des nids-de-poule/fissures** | « On a cartographié toute la voirie du village en un après-midi » | [D] |
| **Ma Vitrine** | vacance commerciale des centres-bourgs | Habillage des cellules vides (trompe-l'œil, artistes locaux, calendrier de boutiques éphémères, QR « louez-moi ») | Le bourg ne « fait plus mort » — avant/après photographiable | [P] |
| **Chasse aux Fuites express** | Saint-Savin : 5 fuites/sem., 150 m³/j sauvés | Capteurs acoustiques posés 2-3 semaines sur le réseau → liste géolocalisée des fuites | Des m³ et des € économisés, chiffrés | [P]+[D] |

## B. Micro-SaaS souverains — l'usage quotidien qui change la vie

> Tous bâtis sur une IA **souveraine (Mistral)** → cohérent avec l'écosystème que la BdT a déjà
> retenu (Territoires d'IA × Mistral). Petits, mono-tâche, adoptés en minutes.

| Nom | Pain | Ce que ça fait | Pourquoi ça marque |
|---|---|---|---|
| **Délib' Express** | ~1 200 secrétaires de mairie manquants | De 2 lignes d'intention → une **délibération / arrêté / compte-rendu** mis en forme et juridiquement sourcé | Utilisé *à chaque conseil municipal* : gain d'heures, visible immédiatement |
| **Allô Commune** | mairie injoignable, secrétaire à temps partiel | Standard **WhatsApp/SMS + IA** : répond aux administrés 24/7, prend les rendez-vous, enregistre les signalements, escalade au secrétaire | « La mairie ne rate plus jamais un appel » — sans appli, rural-friendly |
| **Conseil Municipal en Clair** | défiance, incivilités, 2 501 atteintes aux élus | Enregistre la séance → **résumé citoyen neutre** + un bot Q&R public | Transparence radicale, low-cost, désamorce les conflits |
| **Cantine Zéro-Gaspi** | coûts cantine, gaspillage (cas Nantes) | Micro-IA qui prédit le nombre de repas (croisé aux absences) | Des repas et des € économisés, mesurés chaque semaine |

## C. Paris plus ambitieux — fort impact, vrai changement d'échelle

1. **~~« Le Airbnb des agents territoriaux »~~ → écarté (2026-06-28)** `[D]+[P]` — l'idée d'une place
   de marché de partage/remplacement d'agents est **déjà préemptée par les Centres de Gestion (CDG)**
   (service de missions temporaires/remplacement, bourse de l'emploi, plateformes de mutualisation
   type CDG35+AMF35). Inutile d'en faire un concurrent. **Repositionnement** : le goulot est l'**offre**
   (pas assez d'agents) et l'**outillage**. Deux pistes complémentaires des CDG :
   - **« Prépa-secrétaire de mairie » express** `[P]` — reconversion accélérée (quelques semaines +
     alternance) pour **alimenter le vivier** que les CDG n'arrivent pas à remplir.
   - **« Secrétaire augmenté »** (= **Délib' Express**, section B) `[D]` — multiplier chaque agent rare
     plutôt que d'en chercher un de plus ; vendable **avec** les CDG. *C'est désormais le vrai pari RH.*

2. **« Capteurs en partage »** `[P]+[D][O]` — une **flotte mutualisée de capteurs frugaux** (chaleur,
   eau/fuites, fissures RGA du bâti, qualité de l'air, énergie) qui **tourne** d'une commune à l'autre.
   Une petite commune ne peut pas s'équiper seule ; en partage, elle « loue » 3 semaines de données
   qui débloquent une décision. Backbone physique+data reliant canicule / eau / RGA / énergie — une
   donnée que **la BdT ne collecte jamais**. *Preuve : des cartes et des chiffres là où il n'y avait rien.*

3. **« Le Camion des Communes »** `[P]` — un **véhicule-tournée** qui apporte au village ce qu'il n'a
   plus : créneau de **téléconsultation assistée** (avec un médiateur humain, le vrai chaînon manquant
   des cabines), démarches administratives, **check cyber** de la mairie, point info. Un objet visible,
   attendu, qui matérialise « on vient à vous ». *Preuve : une file devant le camion, des photos.*

4. **« Médiateur de téléconsultation itinérant »** `[P]` — non pas la borne (déjà financée par la BdT
   en pilote), mais **la personne** qui aide les personnes âgées à téléconsulter, en rotation entre
   mairies/France services. Le service, c'est le chaînon humain — exactement la couche « exploitation »
   que la BdT laisse vide. Cible désert médical **et** isolement du grand âge.

5. **« Bouclier Élu »** `[P]+[D]` — pour les violences contre les élus (angle mort total : ni BdT, ni
   opérateur privé) : **bouton d'alerte discret** + **hotline juridique/psy** immédiate + **constitution
   automatique du dossier de plainte** par IA. Un dispositif tangible de soutien, pas un produit financier.

## Principe directeur

Les meilleurs candidats partagent 4 traits : **(1) une preuve en < 3 semaines** (photo, carte,
chiffre), **(2) mono-tâche** (un seul problème, bien résolu), **(3) la couche que la BdT ne fait pas**
(exploitation, RH, dernier kilomètre), **(4) souverain par construction** (Mistral / données ouvertes).

Wedge recommandé pour démarrer : **un objet qui produit une image forte** (Kit Fraîcheur École,
Voirie-Scan, Ma Vitrine) pour la notoriété + **un micro-SaaS quotidien** (Délib' Express ou Allô
Commune) pour la rétention. Le « Airbnb des agents » et les « Capteurs en partage » sont les paris
de changement d'échelle, à viser ensuite.
