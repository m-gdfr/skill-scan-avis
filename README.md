# Scan-avis

Scanne les avis publiés en ligne sur une marque pour en extraire les irritants utilisateurs, les besoins exprimés et les points forts à préserver.

Il produit systématiquement **deux livrables** :
- un Markdown (lecture machine 🤖)
- une page HTML (lecture humaine 🙋‍♂️).

Le skill se déclenche via `/scan-avis` ou toute intention naturelle d'analyse produit à partir d'avis
("que disent les utilisateurs de X", "les irritants de X"...). 

Méthode complète dans [skill-scan-avis/SKILL.md](skill-scan-avis/SKILL.md).

## Téléchargement

[Télécharger le skill (zip)](https://github.com/m-gdfr/skill-scan-avis/archive/refs/heads/main.zip)

## Étapes préliminaires

**Config Exa (recommandé).** Le skill privilégie la recherche **sémantique** Exa pour la collecte d'avis.
- Connecter le connecteur/MCP Exa avant de lancer un scan. 

> Sinon la collecte retombe sur une recherche web classique.
