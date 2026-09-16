---
name: scan-avis
description: >
  Scanne les avis publiés en ligne sur une entreprise ou une marque pour en extraire les irritants
  utilisateurs, les besoins exprimés et les points forts à préserver, puis produit deux livrables :
  un fichier Markdown pour la lecture machine et une page HTML autonome pour la lecture humaine.
  Déclencher sur la commande "/scan-avis", et aussi systématiquement dès que l'utilisateur formule
  une intention d'analyse produit à partir d'avis : "que disent les utilisateurs de X", "les irritants
  de X", "scanne les avis de X", "qu'est-ce qui coince chez X", "analyse les retours utilisateurs sur
  X", "pourquoi les gens se plaignent de X". À déclencher même sur des formulations très courtes comme
  "avis sur X" dès qu'un objectif produit est perceptible. Ne pas déclencher pour une simple recherche
  de note ou de réputation de marque.
---

# Scan avis

Tu analyses ce que les utilisateurs disent publiquement d'une marque pour en tirer de la matière
produit : ce qui les bloque, ce qu'ils réclament, ce qu'ils défendent. L'objectif n'est pas de mesurer
une réputation mais d'identifier des irritants exploitables, hiérarchisés et traçables.

## Fichiers du skill

| Fichier | Quand le lire |
|---|---|
| `SKILL.md` | La méthode : cadrage, collecte, qualification, scoring. À lire en entier avant de commencer. |
| `references/rendu.md` | Au moment de produire les livrables. Schéma de `donnees.json`, mode allégé. |
| `build.py` | Génère `.html` et `.md` à partir de `donnees.json`. Ne jamais ouvrir `assets/gabarit.html` : le script s'en charge seul. |

## Entrée

Le minimum requis est le **nom de la marque**. Si l'utilisateur fournit des précisions (produit
spécifique, question produit, marché visé), exploite-les pour resserrer le cadrage. Ne réclame jamais
d'informations complémentaires : le skill s'exécute d'un bout à l'autre sans pause de validation.

## Phase 1 — Cadrage

Avant toute requête d'avis, établis trois choses dans cet ordre. Cette phase conditionne la qualité
de tout le reste : chercher à l'aveugle produit des résultats génériques.

1. **Nature du produit et parcours utilisateur type.** Que vend la marque, comment on l'utilise,
   quelles sont les étapes du parcours. Ça te dit quels irritants sont plausibles et où les chercher.
2. **Où vivent réellement les utilisateurs.** Quelles plateformes hébergent effectivement des avis
   sur cette marque. Une app grand public vit sur les stores, un SaaS B2B sur G2 et LinkedIn, un
   service local sur Google Reviews. N'active que les sources qui contiennent de la matière.
3. **Le vocabulaire des utilisateurs.** Comment ils nomment le produit, ses fonctions et ses
   problèmes. C'est ce vocabulaire qui alimente les requêtes, pas le vocabulaire marketing de la marque.

Déduis de ce cadrage le **périmètre linguistique et géographique** : marque locale → avis
francophones, marque globale → français et anglais. Annonce ce périmètre en tête des deux livrables
pour qu'il soit corrigeable après coup.

**Fenêtre temporelle : les 12 derniers mois.** Au-delà, les avis décrivent un produit qui n'existe
plus. Un avis plus ancien n'est retenu que s'il éclaire une régression toujours mentionnée aujourd'hui.

## Phase 2 — Collecte

Familles de sources à considérer : stores d'applications, sites d'avis généralistes (Trustpilot,
Google Reviews, Avis Vérifiés, G2), réseaux sociaux et forums (Reddit, X, LinkedIn).

Privilégie la **recherche sémantique Exa** plutôt que des requêtes par mots-clés rigides : les
formulations d'irritants sont infiniment variables, la recherche sémantique les capte mieux. Construis
les requêtes à partir du vocabulaire relevé en phase 1.

Appelle toujours `web_search_exa` avec **`numResults: 5`**. Chaque résultat ramène le texte complet
de la page ; au-delà du cinquième, la pertinence sémantique décroche et tu paies du bruit au prix
fort.

### Budget de collecte

La saturation thématique absolue est inatteignable sur une marque grand public — il y aura toujours un
avis isolé mentionnant un irritant inédit. La collecte est donc bornée par un budget, pas par
l'épuisement.

**10 recherches maximum pour l'ensemble du scan**, réparties ainsi :

1. **Tour de chauffe.** Une passe large garantie sur chacune des sources activées en phase 1. C'est
   le plancher : il protège l'exigence de recoupement sur au moins deux sources, qui est l'invariant
   central de la qualification. Ne sacrifie jamais une source entière pour approfondir une autre.
2. **Relances.** Le reliquat va aux sources qui ont produit des thèmes qualifiés au tour de chauffe,
   par ordre de rendement décroissant : la source la plus riche reçoit la relance suivante. Une
   relance est une requête ciblée sur un thème précis issu de ce que tu as déjà lu, jamais une
   reformulation de la passe large.

Deux règles d'arrêt encadrent la réallocation :

- **Saturation qualifiée.** Un nouveau thème ne compte comme tel que s'il est mentionné par au moins
  deux avis. Une mention isolée est enregistrée en signal faible et n'ouvre pas de nouvelle piste
  de recherche.
- **Fermeture par source.** Une passe sans nouveau thème qualifié ferme la source : elle ne reçoit
  plus de relance. Une source fermée ne se rouvre que si une piste précise émerge ailleurs et la
  concerne directement.

Le scan se clôt quand le budget est consommé ou quand toutes les sources activées sont fermées — le
premier des deux. Un budget non consommé n'est pas un défaut : sur une marque peu exposée, cinq
recherches suffisent souvent.

## Phase 3 — Qualification

Regroupe les avis par thème, puis attribue à chaque irritant un niveau de fiabilité :

- **Confirmé** — corroboré par une source primaire (changelog, page produit, communiqué, page
  tarifs), ou par au moins 5 avis répartis sur au moins 2 sources.
- **Probable** — au moins 3 avis répartis sur au moins 2 sources, sans confirmation primaire.
- **Signal faible** — tout le reste : 1 ou 2 avis, ou plusieurs avis d'une seule source.

Deux règles empruntées au recoupement journalistique :

- Des avis publiés dans une fenêtre courte avec des formulations proches comptent **pour un seul**
  (campagne coordonnée probable).
- Un avis détaillé et reproductible pèse plus qu'un reproche vague répété dix fois. Quand un irritant
  est factuel et vérifiable, va chercher la source primaire plutôt que d'accumuler des témoignages.

**Vérification par source primaire.** C'est le seul moment où tu ouvres une page directement, avec
`web_fetch_exa` et `maxCharacters: 1500`. Réserve-le aux irritants factuels qu'une page publique
peut trancher — une hausse de tarif sur la page prix, une fonction retirée dans le changelog — et
seulement quand la confirmation ferait basculer l'irritant de Probable à Confirmé. **Trois appels
maximum par scan.** Vérifier un irritant déjà Confirmé par le volume, ou un ressenti qu'aucune page
ne peut confirmer, ne sert à rien.

Seuls les irritants **Confirmé** et **Probable** entrent dans le tableau priorisé. Les signaux faibles
partent dans leur propre section — c'est souvent là que se trouvent les irritants émergents, ils ne
doivent pas être jetés.

## Phase 4 — Scoring

**Fréquence** : nombre d'avis distincts où l'irritant apparaît, en comptage brut.

**Gravité**, sur 4 niveaux, en s'appuyant sur les signaux présents dans les verbatims :

| Note | Niveau | Signaux typiques |
|---|---|---|
| 1 | Cosmétique | remarque esthétique, préférence, détail sans conséquence d'usage |
| 2 | Friction | l'utilisateur y arrive mais au prix d'un effort, d'un détour, d'une attente |
| 3 | Perte de confiance | doute sur la fiabilité, le sérieux, la sécurité, l'honnêteté commerciale |
| 4 | Churn explicite | mention de résiliation, de désinstallation, de passage à la concurrence |

**Score = Fréquence × Gravité.** La fiabilité reste une colonne informative et n'entre pas dans le
calcul. Le score dépend du volume collecté : il sert à comparer les irritants **entre eux au sein d'un
même scan**, jamais d'un scan à l'autre. Les deux livrables doivent le dire.

## Verbatims et traçabilité

Cite des **fragments courts** entre guillemets — quelques mots, ceux qui portent le sens. L'analyse
est portée par ta reformulation, pas par l'accumulation de citations. Ne reproduis jamais un avis
intégralement.

Chaque verbatim porte un lien cliquable vers l'avis ou le fil cité. Quand aucun permalien n'existe
— c'est le cas de la plupart des avis de stores — pointe vers la page source et ajoute la date et le
pseudo pour permettre de retrouver l'avis.

## Livrables

Deux fichiers, produits systématiquement, jamais l'un sans l'autre, à partir d'une seule source :

1. Remplis `donnees.json` selon le schéma de `references/rendu.md` — c'est le seul artefact que tu
   écris à la main.
2. Exécute `python3 build.py donnees.json`. Il génère `scan-avis-[marque-slug].html` (lecture
   humaine) et `scan-avis-[marque-slug].md` (lecture machine) dans le même passage.

Comme les deux viennent de la même donnée, ils portent par construction les mêmes chiffres. N'ouvre
et ne réécris jamais `assets/gabarit.html` toi-même.

### Cas de matière insuffisante

Si aucun irritant n'atteint le niveau Probable — cas fréquent pour une PME ou une marque B2B peu
exposée — passe `mode_allege` à `true` dans `donnees.json` (voir `references/rendu.md`) : `build.py`
retire lui-même les blocs cartes/tableau/légende/besoins/points forts des deux livrables. Dis
explicitement que le volume d'avis disponibles ne permet pas de hiérarchiser.

## Ce qu'on évite

- Produire un score de réputation, une note moyenne ou un NPS estimé : ce n'est pas l'objet.
- Présenter les chiffres comme des statistiques représentatives. Les avis en ligne surreprésentent
  les extrêmes ; la section Méthode et limites doit le rappeler à chaque fois.
- Inventer un verbatim ou un lien. Un irritant sans source vérifiable ne figure dans aucun des deux
  livrables.
- Traduire un verbatim sans le signaler quand il est cité depuis une autre langue.
- Mélanger irritant et besoin : « le filtre ne marche pas » est un irritant, « il faudrait un filtre
  par date » est un besoin. Les deux sections restent distinctes.
- Noyer le tableau : au-delà d'une dizaine d'irritants priorisés, regroupe les thèmes proches plutôt
  que d'allonger la liste.
