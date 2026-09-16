# Livrable 2 — la page HTML

Destinée à la lecture humaine. Deux profils de lecteur, tous deux en lecture individuelle sur écran :
l'utilisateur lui-même, comme outil de travail pour digérer le scan, et un client ou un supérieur, en
lecture autonome. Aucun des deux n'a quelqu'un à côté pour commenter la page : elle doit tenir debout
seule.

Elle n'est pas un atelier projeté, ni un support de présentation à commenter.

## Contraintes techniques

- **Un seul fichier `.html`**, CSS et JavaScript inline. Zéro dépendance externe : pas de CDN, pas de
  police distante, pas de bibliothèque. La page doit s'afficher dans la fenêtre de rendu de Claude,
  qui n'ira chercher aucune ressource.
- Pas de `localStorage` ni de `sessionStorage`.
- Nom de fichier : `scan-avis-[marque-slug].html`.
- Ne recode pas la page : copie `assets/gabarit.html` et remplis les données. Le gabarit contient déjà
  la structure, le tri, les filtres et les déplis.

## Ordre des blocs

Cet ordre a été arbitré. Ne le réorganise pas.

1. **Titre et bandeau de cadrage.** Périmètre, fenêtre, date du scan, volume d'avis exploitables,
   sources activées. Présent mais discret : le cadrage est nécessaire, il n'est pas ce qui doit
   frapper en premier.
2. **Les trois irritants au score le plus élevé, en cartes détaillées.** Chaque carte est
   autoportante : nom, fréquence, gravité, score, fiabilité. Les verbatims sont repliés et se
   déplient au clic.
3. **Le constat d'ensemble rédigé.** Deux paragraphes courts. C'est le seul endroit où tu prends la
   parole en analyse : ce qui pèse, et pourquoi ces irritants ne sont pas de même nature.
4. **Le tableau complet.** Tous les irritants priorisés, top 3 inclus : c'est la référence complète,
   pas un complément. Tri sur toutes les colonnes, filtre par gravité, filtre par fiabilité,
   recherche texte libre portant sur les noms d'irritants et les verbatims. **Pas de filtre par
   source.** Clic sur une ligne : les verbatims et leurs liens apparaissent sous la ligne.
5. **La légende**, en accordéon replié, juste sous le tableau. Style visuel distinct des autres
   sections repliées : elle se lit comme une annexe du tableau, pas comme une section du document.
6. **Le reste du scan**, en accordéons repliés par défaut, dans cet ordre : besoins exprimés, points
   forts à préserver, signaux faibles, méthode et limites.

## Identité visuelle

Fixée : sans-serif, fond Linen Canvas, cartes Paper White, radius unique de 16px, aucune ombre. La
gravité se lit uniquement par une pastille colorée (dégradé rouge sombre → rose sourd, du niveau 4 au
niveau 1) suivie du nom du niveau — jamais par un chiffre nu (« 3 confiance » ne doit plus apparaître
nulle part). Le rang du top 3 n'a plus de représentation séparée depuis la suppression du nuage ; les
trois cartes du haut suffisent à le signaler. Garde ce système sur chaque scan plutôt que d'improviser
une nouvelle direction graphique par génération — les couleurs et polices vivent dans les tokens en
tête du gabarit, ne les redéfinis pas au cas par cas.

## Responsive

Sous 700px : le tableau passe en fiches empilées (une par irritant, champs étiquetés) plutôt qu'en
défilement horizontal ; les filtres et la recherche passent en pleine largeur. Ce comportement est déjà
câblé dans le gabarit — ne le retire pas en modifiant la structure des lignes.

## Ce qui reste ouvert

Rien de graphique pour l'instant — voir « Identité visuelle » ci-dessus. Si un scan révèle un vrai
angle mort du système (une donnée qu'aucun composant existant ne sait représenter), traite-le au cas
par cas plutôt que d'étendre silencieusement la palette ou la typographie.

## Cas de matière insuffisante

Aucun irritant n'atteint le niveau Probable : la page se réduit au titre, au bandeau de cadrage, au
constat d'ensemble, aux signaux faibles et à la méthode et limites. Ni cartes, ni tableau, ni légende.
Supprime ces blocs du gabarit plutôt que de les laisser vides.
