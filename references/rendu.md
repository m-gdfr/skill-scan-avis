# Rendu des livrables

Remplace `references/livrable-md.md` et `references/livrable-html.md` : la structure exacte des
deux livrables ne vit plus dans un document à lire, elle est encodée une fois dans `build.py` (le
Markdown) et dans `assets/gabarit.html` (le HTML). Ce fichier documente uniquement ce qu'il reste à
savoir pour produire `donnees.json` — le seul artefact que tu écris à la main.

## Procédure

1. Termine le cadrage, la collecte et la qualification (`SKILL.md`, phases 1 à 4).
2. Remplis `donnees.json` selon le schéma ci-dessous.
3. Exécute `python3 build.py donnees.json` depuis la racine du skill.
4. Le script écrit `scan-avis-[marque-slug].html` et `scan-avis-[marque-slug].md` (option `--out-dir`
   pour changer le dossier de sortie).
5. N'ouvre ni ne réécris jamais `assets/gabarit.html` : le script s'en charge, et lui seul.

Les deux livrables viennent de la même donnée : ils portent donc par construction les mêmes chiffres.
Il reste à ta charge que le contenu texte (constat, méthode, verbatims) dise la même chose des deux
côtés — le script ne peut pas le vérifier pour toi.

## Schéma de `donnees.json`

Voir `assets/donnees.exemple.json` pour un exemple complet et réaliste.

| Champ | Type | Contenu |
|---|---|---|
| `marque` | string | Nom de la marque. Sert au titre, au nom de fichier (slug) et au h1. |
| `date_scan` | string | Date du scan, format `JJ/MM/AAAA`. |
| `perimetre` | string | Périmètre linguistique et géographique retenu (ex. `"France, avis francophones"`). N'apparaît que dans le Markdown : la page HTML ne montre que la date et la fenêtre fixe de 12 mois. |
| `avis_exploitables` | int | Volume d'avis retenus. |
| `sources` | string[] | Plateformes activées, dans l'ordre d'affichage. Noms reconnus pour l'icône : `Trustpilot`, `Reddit`, `App Store`, `Google Play`, `Google Reviews`, `LinkedIn`, `X`, `G2`, `Avis vérifiés` — toute autre valeur retombe sur une icône générique. |
| `mode_allege` | bool | `true` si aucun irritant n'atteint Probable (voir plus bas). |
| `constat` | string[2] | Exactement deux paragraphes : les irritants qui pèsent et pourquoi ils diffèrent, puis où ils se concentrent dans le parcours. |
| `irritants` | objet[] | Un objet par irritant priorisé (voir ci-dessous). Ignoré si `mode_allege`. |
| `besoins` | string[] | Demandes explicites d'évolution. Ignoré si `mode_allege`. |
| `points_forts.items` | string[] | Ce que les utilisateurs défendent. Ignoré si `mode_allege`. |
| `points_forts.note` | string | Ce qu'une correction ne doit pas casser. Ignoré si `mode_allege`. |
| `signaux_faibles` | string[] | Irritants sous le seuil de fiabilité, avec leur volume. Toujours présent, y compris en mode allégé. |
| `methode.intro` | string | Périmètre, sources activées/écartées et pourquoi, passes, requêtes menées. |
| `methode.limites` | string | Ce que le scan ne dit pas. |

### Un objet de `irritants`

```json
{
  "nom": "Libellé complet, celui du tableau et des cartes",
  "freq": 7,
  "grav": 3,
  "fiab": "Confirmé",
  "verbatims": [
    {"fragment": "quelques mots, pas l'avis entier", "source": "Trustpilot, 14/03, @pseudo", "url": "https://..."}
  ]
}
```

- `grav` : entier de 1 (mineur) à 4 (churn explicite).
- `fiab` : `"Confirmé"` ou `"Probable"` uniquement — un irritant sous ce seuil part dans
  `signaux_faibles`, pas dans `irritants`.
- `score` ne se saisit pas : `build.py` le calcule (`freq × grav`), et trie le tableau et le top 3
  par score décroissant. Les deux livrables l'affichent donc toujours identique.
- `url` : permalien, ou page source à défaut. `build.py` ne le valide pas dans le Markdown (lien
  brut) ; côté HTML, le gabarit ignore silencieusement une URL mal formée ou non http(s).

### Échappement

Écris le texte normalement, avec ses accents et ses apostrophes françaises — aucun champ n'attend de
HTML ni de Markdown. `build.py` échappe `&`, `<`, `>` pour le HTML et sérialise `irritants`/`sources`
en JSON (donc en JS valide) pour le script du gabarit. N'écris jamais toi-même une apostrophe ou un
guillemet échappé (`&apos;`, `\'`...) : ce serait échappé une seconde fois.

## Mode allégé

Aucun irritant n'atteint Probable : passe `mode_allege` à `true`. `irritants`, `besoins` et
`points_forts` peuvent alors être omis ou vides, `build.py` les ignore. Les deux livrables se
réduisent à : l'en-tête de périmètre, « Ce qui ressort », « Signaux faibles » et « Méthode et
limites ». Le script retire lui-même les blocs cartes / tableau / légende / besoins / points forts
plutôt que de les laisser vides.

## Légende du tableau

Une seule source de vérité : le texte vit dans `assets/gabarit.html` (bloc HTML, affiché en
accordéon replié sous le tableau) et dans `build.py` (constante `MD_LEGENDE`, ajoutée en fin de
Markdown). Ne le décris plus dans `SKILL.md` — voir le rapport de chantier pour la modification
précise à y apporter.
