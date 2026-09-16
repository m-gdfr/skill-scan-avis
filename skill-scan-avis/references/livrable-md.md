# Livrable 1 — le fichier Markdown

Destiné à la lecture machine et à la reprise par un autre agent. C'est la source de vérité du
contenu : rédige-le avant la page HTML, puis alimente la page depuis lui.

Il n'est pas fait pour être lu confortablement par un humain — c'est le rôle de la page HTML. Ne
cherche donc pas à l'alléger : densité et exhaustivité sont ici des qualités.

## Structure exacte

```
# Scan avis — [Marque]

Périmètre retenu : [langue/géo] · 12 derniers mois · scan du [date]
Sources activées : [liste]
Matière collectée : [n] avis exploitables

## Ce qui ressort
[3 à 5 lignes. Les irritants qui pèsent, et le constat d'ensemble.]

## Irritants priorisés *

| Irritant | Fréq. | Gravité | Score | Fiabilité | Verbatims et sources |
|---|---|---|---|---|---|
| [Nom court] | 7 | 3 | 21 | Confirmé | « fragment » — Trustpilot, 12/03, @pseudo · [lien]<br>« fragment » — Reddit, 04/05, @pseudo · [lien] |

\* Voir la légende en fin de document.

## Besoins exprimés
[Demandes explicites de fonctionnalités ou d'évolutions, distinctes des irritants.]

## Points forts à préserver
[Ce que les utilisateurs défendent — utile pour ne pas casser en corrigeant.]

## Signaux faibles
[Sous le seuil de fiabilité. Irritants potentiellement émergents.]

## Méthode et limites
[Requêtes menées, sources fermées et pourquoi, biais des plateformes,
ce que le scan ne dit pas.]

## Légende

**Fréquence** — nombre d'avis distincts où l'irritant apparaît. Les avis publiés
dans une même fenêtre courte avec des formulations proches comptent pour un seul.

**Gravité** — 1 cosmétique · 2 friction · 3 perte de confiance · 4 churn explicite.
La note s'appuie sur les signaux présents dans les verbatims : mention de
résiliation, de passage à la concurrence, intensité du reproche.

**Score** — Fréquence × Gravité. Sert à comparer les irritants entre eux au sein
de ce scan uniquement : le score dépend du volume collecté et n'est pas comparable
d'un scan à l'autre.

**Fiabilité** — Confirmé : corroboré par une source primaire (changelog, page
produit, communiqué) ou par ≥5 avis sur ≥2 sources. Probable : ≥3 avis sur
≥2 sources. En dessous, l'irritant part en Signaux faibles et n'est pas priorisé.
```

Le tableau est trié par score décroissant.

## Nom de fichier

`scan-avis-[marque-slug].md`

## Cas de matière insuffisante

Aucun irritant n'atteint le niveau Probable : livre un document allégé — en-tête de périmètre,
section « Ce qui ressort », section Signaux faibles, section Méthode et limites. Pas de tableau de
score, pas de légende.
