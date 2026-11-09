"""Attribue un secteur d'activité aux offres et aux prospects (ajouté le 9 novembre 2026).

  python3 outils/secteurs.py        recalcule tout (appelé aussi par tournee.py et decouvrir.py)

Règles : un secteur saisi à la main dans prospects.json (autre que « À préciser ») est conservé.
Une offre prend le secteur de son entreprise dans les prospects quand il est connu, sinon il est deviné
d'après le nom de l'entreprise et le titre du poste (commun.secteur).
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from commun import secteur, coeur_cie

R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
F_OFF, F_PRO = os.path.join(R, "offres.json"), os.path.join(R, "prospects.json")
A_PRECISER = "À préciser"


def premier(s):
    return (s or "").split(" – ")[0].strip()


def prospects_secteurs(pros, offres):
    titres = {}
    for o in offres:
        titres.setdefault(coeur_cie(o["entreprise"]), []).append(o["titre"])
    n = 0
    for e in pros["entreprises"]:
        if e.get("secteur") and e["secteur"] != A_PRECISER and not e.get("secteurAuto"):
            continue
        s = secteur(e["nom"])
        if not s:
            for t in titres.get(coeur_cie(e["nom"]), []):
                s = secteur("", t)
                if s: break
        if s:
            e["secteur"] = s; e["secteurAuto"] = True; n += 1
        else:
            e["secteur"] = A_PRECISER; e.pop("secteurAuto", None)
    return n


def offres_secteurs(offres, pros):
    connus = {coeur_cie(e["nom"]): premier(e["secteur"]) for e in pros["entreprises"]
              if e.get("secteur") and e["secteur"] != A_PRECISER}
    for o in offres:
        s = connus.get(coeur_cie(o["entreprise"])) or secteur(o["entreprise"], o["titre"])
        if s: o["secteur"] = s
        else: o.pop("secteur", None)


def tout():
    pros = json.load(open(F_PRO, encoding="utf-8"))
    d = json.load(open(F_OFF, encoding="utf-8"))
    n = prospects_secteurs(pros, d["offres"])
    offres_secteurs(d["offres"], pros)
    json.dump(pros, open(F_PRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump(d, open(F_OFF, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return n, sum(1 for o in d["offres"] if o.get("secteur")), len(d["offres"])


if __name__ == "__main__":
    n, a, t = tout()
    print(f"{n} prospects avec un secteur deviné · {a}/{t} offres avec un secteur")
