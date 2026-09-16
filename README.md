# skill-scan-avis

Skill qui scanne les avis publiés en ligne sur une marque pour en extraire les irritants
utilisateurs, les besoins exprimés et les points forts à préserver. Il produit systématiquement deux
livrables : un Markdown (lecture machine, reprise par un autre agent) et une page HTML autonome
(lecture humaine, sans commentaire oral d'accompagnement).

Le skill se déclenche via `/scan-avis` ou toute intention naturelle d'analyse produit à partir d'avis
("que disent les utilisateurs de X", "les irritants de X"...). Il ne réclame jamais d'informations
complémentaires : une fois lancé, il tourne d'un bout à l'autre sans pause de validation.

Méthode complète dans [skill-scan-avis/SKILL.md](skill-scan-avis/SKILL.md).

## Téléchargement

[Télécharger le skill (zip)](https://github.com/m-gdfr/skill-scan-avis/archive/refs/heads/main.zip)

## Étapes préliminaires

- **Config Exa (recommandé).** Le skill privilégie la recherche sémantique Exa pour la collecte
  d'avis (formulations d'irritants trop variables pour des mots-clés rigides). Connecter le
  connecteur/MCP Exa avant de lancer un scan, sinon la collecte retombe sur une recherche web classique.
