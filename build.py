#!/usr/bin/env python3
"""
build.py — génère les deux livrables du skill scan-avis (.html et .md)
à partir d'un fichier donnees.json unique.

Usage :
    python3 build.py donnees.json [--out-dir DOSSIER]

Ne dépend que de la stdlib. Voir references/rendu.md pour le schéma complet
de donnees.json.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent
GABARIT_PATH = SKILL_ROOT / "assets" / "gabarit.html"

GRAV_LABEL = {4: "churn", 3: "confiance", 2: "friction", 1: "mineur"}


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def slugify(marque: str) -> str:
    s = unicodedata.normalize("NFKD", marque)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s or "marque"


def esc_html(s: str) -> str:
    """Échappe & < > pour un nœud texte HTML. Les apostrophes et accents
    français passent tels quels : ce ne sont pas des délimiteurs ici."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def js_literal(data) -> str:
    """Sérialise en JSON (donc en JS valide) et neutralise '</script>' pour
    un embarquement sûr dans une balise <script>."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def replace_block(html: str, name: str, inner: str) -> str:
    """Remplace le contenu ENTRE les marqueurs <!--@name--> ... <!--/@name-->
    (ou /*@name*/ ... /*/@name*/ côté JS), marqueurs conservés."""
    pattern = re.compile(
        r"((?:<!--|/\*)@" + re.escape(name) + r"(?:-->|\*/))(.*?)((?:<!--|/\*)/@" + re.escape(name) + r"(?:-->|\*/))",
        re.DOTALL,
    )
    if not pattern.search(html):
        raise RuntimeError(f"marqueur introuvable dans le gabarit : {name}")
    return pattern.sub(lambda m: m.group(1) + inner + m.group(3), html, count=1)


def remove_block(html: str, name: str) -> str:
    """Supprime intégralement (marqueurs compris) une section balisée
    <!--@name--> ... <!--/@name--> ou /*@name*/ ... /*/@name*/."""
    pattern = re.compile(
        r"(?:<!--|/\*)@" + re.escape(name) + r"(?:-->|\*/)(.*?)(?:<!--|/\*)/@" + re.escape(name) + r"(?:-->|\*/)",
        re.DOTALL,
    )
    if not pattern.search(html):
        raise RuntimeError(f"marqueur introuvable dans le gabarit : {name}")
    return pattern.sub("", html, count=1)


# ---------------------------------------------------------------------------
# Construction du HTML
# ---------------------------------------------------------------------------

def build_html(data: dict) -> str:
    html = GABARIT_PATH.read_text(encoding="utf-8")
    marque = data["marque"]
    allege = bool(data.get("mode_allege", False))

    # Titre, h1, cadrage : tokens uniques, mêmes valeurs à chaque occurrence.
    html = html.replace("[MARQUE]", esc_html(marque))
    html = html.replace("[JJ/MM/AAAA]", esc_html(data["date_scan"]))
    html = html.replace("[N]", str(int(data["avis_exploitables"])))

    # Constat (toujours présent, y compris en mode allégé).
    constat_html = "\n    ".join(f"<p>{esc_html(p)}</p>" for p in data["constat"])
    html = replace_block(html, "CONSTAT", constat_html)

    # Signaux faibles (toujours présent).
    signaux_html = "".join(f"<li>{esc_html(s)}</li>" for s in data["signaux_faibles"])
    html = replace_block(html, "SIGNAUX_LIST", signaux_html)

    # Méthode et limites (toujours présent).
    html = replace_block(html, "METHODE_INTRO", esc_html(data["methode"]["intro"]))
    html = replace_block(html, "METHODE_LIMITES", esc_html(data["methode"]["limites"]))

    if allege:
        # Pas de top 3, pas de tableau/légende, pas de besoins, pas de points forts.
        html = remove_block(html, "BLOC:TOP3")
        html = remove_block(html, "BLOC:TABLE")
        html = remove_block(html, "BLOC:BESOINS")
        html = remove_block(html, "BLOC:POINTSFORTS")
        html = remove_block(html, "JS:TOP3")
        html = remove_block(html, "JS:TABLE")
    else:
        besoins_html = "".join(f"<li>{esc_html(b)}</li>" for b in data["besoins"])
        html = replace_block(html, "BESOINS_LIST", besoins_html)

        pf = data["points_forts"]
        pf_html = "".join(f"<li>{esc_html(i)}</li>" for i in pf["items"])
        html = replace_block(html, "POINTSFORTS_LIST", pf_html)
        html = replace_block(html, "POINTSFORTS_NOTE", esc_html(pf["note"]))

    # Données JS : SOURCES et D. En mode allégé, D reste un tableau vide
    # (le top 3 et le tableau qui l'exploitent ont été retirés du DOM).
    html = replace_block(html, "DATA:SOURCES", f"\nconst SOURCES = {js_literal(data['sources'])};\n")
    irritants = [] if allege else data["irritants"]
    html = replace_block(html, "DATA:D", f"\nconst D = {js_literal(irritants)};\n")

    return html


# ---------------------------------------------------------------------------
# Construction du Markdown
# ---------------------------------------------------------------------------

MD_LEGENDE = """## Légende

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
"""

MD_BIAIS = (
    "Les avis en ligne surreprésentent les extrêmes. Les chiffres de ce document "
    "ne sont pas des statistiques représentatives de la base utilisateurs."
)


def build_md(data: dict) -> str:
    marque = data["marque"]
    allege = bool(data.get("mode_allege", False))

    lines = []
    lines.append(f"# Scan avis — {marque}")
    lines.append("")
    lines.append(
        f"Périmètre retenu : {data['perimetre']} · 12 derniers mois · scan du {data['date_scan']}"
    )
    lines.append("Sources activées : " + ", ".join(data["sources"]))
    lines.append(f"Matière collectée : {data['avis_exploitables']} avis exploitables")
    lines.append("")
    lines.append("## Ce qui ressort")
    lines.append("")
    lines.extend(data["constat"])
    lines.append("")

    if not allege:
        lines.append("## Irritants priorisés *")
        lines.append("")
        lines.append("| Irritant | Fréq. | Gravité | Score | Fiabilité | Verbatims et sources |")
        lines.append("|---|---|---|---|---|---|")
        irritants = sorted(data["irritants"], key=lambda d: d["freq"] * d["grav"], reverse=True)
        for d in irritants:
            score = d["freq"] * d["grav"]
            verb_cell = "<br>".join(
                f"« {v['fragment']} » — {v['source']} · [lien]({v['url']})" for v in d["verbatims"]
            )
            lines.append(
                f"| {d['nom']} | {d['freq']} | {d['grav']} | {score} | {d['fiab']} | {verb_cell} |"
            )
        lines.append("")
        lines.append("\\* Voir la légende en fin de document.")
        lines.append("")

        lines.append("## Besoins exprimés")
        lines.append("")
        lines.extend(f"- {b}" for b in data["besoins"])
        lines.append("")

        lines.append("## Points forts à préserver")
        lines.append("")
        lines.extend(f"- {i}" for i in data["points_forts"]["items"])
        lines.append("")
        lines.append(data["points_forts"]["note"])
        lines.append("")

    lines.append("## Signaux faibles")
    lines.append("")
    lines.extend(f"- {s}" for s in data["signaux_faibles"])
    lines.append("")

    lines.append("## Méthode et limites")
    lines.append("")
    lines.append(data["methode"]["intro"])
    lines.append("")
    lines.append(MD_BIAIS)
    lines.append("")
    lines.append(data["methode"]["limites"])
    lines.append("")

    if not allege:
        lines.append(MD_LEGENDE)

    return "\n".join(lines).rstrip() + "\n"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main(argv):
    if not argv:
        print("Usage : python3 build.py donnees.json [--out-dir DOSSIER]", file=sys.stderr)
        return 1

    json_path = Path(argv[0])
    out_dir = Path(argv[argv.index("--out-dir") + 1]) if "--out-dir" in argv else json_path.parent

    data = json.loads(json_path.read_text(encoding="utf-8"))
    slug = slugify(data["marque"])

    out_dir.mkdir(parents=True, exist_ok=True)
    html_path = out_dir / f"scan-avis-{slug}.html"
    md_path = out_dir / f"scan-avis-{slug}.md"

    html_path.write_text(build_html(data), encoding="utf-8")
    md_path.write_text(build_md(data), encoding="utf-8")

    print(f"Écrit : {html_path}")
    print(f"Écrit : {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
