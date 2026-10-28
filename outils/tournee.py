"""Tournée Sentinelle : ajoute les nouvelles offres à data/offres.json sans tout reconstruire,
et gère les offres terminées.

  python3 outils/tournee.py fusion brut.txt [frais.txt]   ajoute / met à jour les offres vues
  python3 outils/tournee.py averifier [N]                 liste les offres à vérifier (pas revues aujourd'hui)
  python3 outils/tournee.py fermer fermees.txt            marque ces identifiants comme terminés
  python3 outils/tournee.py ouvertes ouvertes.txt         ces offres vérifiées sont encore ouvertes
  python3 outils/tournee.py menage                        applique seulement les règles automatiques

Format de brut.txt (un champ par ¦) :
  #SRC LinkedIn | #SRC Indeed | #SRC Jobillico     source des lignes suivantes
  #ALL | #Génie mécanique | #Ressources humaines …  domaine des lignes suivantes (#ALL = deviné d'après le titre)
  LinkedIn  : id¦titre¦entreprise¦ville¦âge (ex. « 2 semaines »)
  Indeed    : id¦titre¦entreprise¦ville          (les id récents vont dans frais.txt)
  Jobillico : id¦titre¦entreprise¦ville¦âge¦chemin-de-l-offre

Règles des offres terminées :
  - confirmée fermée en ouvrant l'offre (commande fermer)      -> « terminee » avec la date
  - plus vue dans aucune tournée depuis 14 jours               -> « terminee » (probablement fermée)
  - publiée il y a plus de 60 jours                            -> retirée (hors de la fenêtre suivie)
  - terminée depuis plus de 30 jours                           -> retirée
"""
import json, os, re, sys, datetime
sys.path.insert(0, os.path.dirname(__file__))
from commun import slug, region, est_agence, to_iso, domaine, BRUIT, now

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F = os.path.join(RACINE, "data", "offres.json")
AUJ = now.date().isoformat()
TAGS = {"meca": "Génie mécanique", "rh": "Ressources humaines"}


def charger():
    d = json.load(open(F, encoding="utf-8"))
    for o in d["offres"]:
        o.setdefault("premiereVue", (o.get("publieLe") or now.isoformat())[:10])
        o.setdefault("vuLe", AUJ)
    return d


def cle(o):
    return (slug(o["titre"])[:30], slug(o["entreprise"]).split("-")[0], slug(o["lieu"].replace(", QC", "")))


def jours(iso):
    return (now - datetime.datetime.fromisoformat(iso)).total_seconds() / 86400 if iso else None


def menage(d):
    garde = []
    for o in d["offres"]:
        if o.get("dateApprox"):  # Indeed : tranche recalculée chaque jour
            o["dateApprox"] = "Moins de 7 jours" if (jours(o["publieLe"]) or 99) < 7 else "Plus de 7 jours"
        a = jours(o.get("publieLe"))
        if a is not None and a > 60: continue
        if o.get("terminee"):
            if (now.date() - datetime.date.fromisoformat(o["terminee"])).days > 30: continue
        elif (now.date() - datetime.date.fromisoformat(o["vuLe"])).days >= 14:
            o["terminee"] = AUJ; o["termineeRaison"] = "Plus affichée depuis 14 jours"
        garde.append(o)
    d["offres"] = sorted(garde, key=lambda o: o.get("publieLe") or "", reverse=True)


def sauver(d):
    menage(d)
    regs = sorted({o["region"] for o in d["offres"]})
    d["tournee"] = {"date": now.isoformat(), "regions": ", ".join(regs) + " · offres des 60 derniers jours",
                    "sources": sorted({s["nom"] for o in d["offres"] for s in o["sources"]})}
    json.dump(d, open(F, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def fusion(brut, frais_f=None):
    d = charger()
    frais = set(open(frais_f).read().split()) if frais_f and os.path.exists(frais_f) else set()
    par_id = {o["id"]: o for o in d["offres"]}
    par_cle = {cle(o): o for o in d["offres"]}
    src, tag, nouvelles, revues, ignorees = "LinkedIn", "ALL", [], 0, 0
    for line in open(brut, encoding="utf-8"):
        line = line.strip()
        if not line: continue
        if line.startswith("#SRC"): src = line[4:].strip(); continue
        if line.startswith("#"): tag = TAGS.get(line[1:], line[1:]); continue
        p = [x.strip() for x in line.split("¦")]
        if len(p) < 4: continue
        oid, titre, cie, ville = p[:4]
        age = p[4] if len(p) > 4 else ""
        r = region(ville)
        if not r or est_agence(cie) or BRUIT.search(titre): ignorees += 1; continue
        cie = re.sub(r",? (inc\.?|Inc\.?|INC\.?|ltée|Ltée|ULC|S\.E\.N\.C\.R\.L\..*)$", "", cie).strip()
        url = {"LinkedIn": f"https://www.linkedin.com/jobs/view/{oid}/",
               "Indeed": f"https://ca.indeed.com/viewjob?jk={oid}"}.get(src) or "https://www.jobillico.com/fr/offre-d-emploi/" + (p[5] if len(p) > 5 else "")
        k = ("li-" if src == "LinkedIn" else "jb-") + oid
        iso, approx = None, None
        if src == "Indeed":
            iso = (now - datetime.timedelta(days=3 if (age == "F" or oid in frais) else 14)).isoformat(); approx = True
        else:
            iso = to_iso(age)
        if iso and jours(iso) > 60: ignorees += 1; continue
        o = {"id": k, "titre": titre, "entreprise": cie, "lieu": ville + ", QC", "region": r, "domaine": domaine(titre, tag),
             "publieLe": iso, "urlOffre": url, "sources": [{"nom": src, "url": url}], "premiereVue": AUJ, "vuLe": AUJ}
        ex = par_id.get(k) or par_cle.get(cle(o))
        if ex:
            ex["vuLe"] = AUJ; revues += 1
            ex.pop("terminee", None); ex.pop("termineeRaison", None)
            if src not in [s["nom"] for s in ex["sources"]]: ex["sources"].append({"nom": src, "url": url})
            if iso and not approx and (not ex.get("publieLe") or ex.get("dateApprox") or iso < ex["publieLe"]):
                ex["publieLe"] = iso; ex.pop("dateApprox", None)
            continue
        if approx: o["dateApprox"] = "x"
        d["offres"].append(o); par_id[k] = o; par_cle[cle(o)] = o; nouvelles.append(o)
    sauver(d)
    json.dump(nouvelles, open("nouvelles-offres.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{len(nouvelles)} nouvelles · {revues} revues · {ignorees} ignorées (hors territoire, agences, bruit, >60 j) · total {len(d['offres'])}")
    print(f"terminées affichées : {sum(1 for o in d['offres'] if o.get('terminee'))}  (liste des nouvelles : ./nouvelles-offres.json)")


def averifier(n=40):
    d = charger()
    L = [o for o in d["offres"] if o["vuLe"] < AUJ and not o.get("terminee")]
    L.sort(key=lambda o: o["vuLe"])
    for o in L[:n]:
        print(o["id"], o["urlOffre"], "|", o["titre"][:50], "|", o["entreprise"])
    print(f"# {len(L)} offres non revues aujourd'hui ; {min(n, len(L))} listées")


def fermer(f):
    ids = set(open(f).read().split())
    d = charger(); n = 0
    for o in d["offres"]:
        if o["id"] in ids and not o.get("terminee"):
            o["terminee"] = AUJ; o["termineeRaison"] = "Offre fermée sur le site d'emploi"; n += 1
    sauver(d); print(f"{n} offres marquées terminées")


def revues(f):
    """Offres vérifiées et encore ouvertes : on les considère comme revues aujourd'hui."""
    ids = set(open(f).read().split())
    d = charger()
    for o in d["offres"]:
        if o["id"] in ids: o["vuLe"] = AUJ
    sauver(d); print(f"{len(ids)} offres confirmées encore ouvertes")


if __name__ == "__main__":
    c = sys.argv[1] if len(sys.argv) > 1 else ""
    if c == "fusion": fusion(sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
    elif c == "averifier": averifier(int(sys.argv[2]) if len(sys.argv) > 2 else 40)
    elif c == "fermer": fermer(sys.argv[2])
    elif c == "ouvertes": revues(sys.argv[2])
    elif c == "menage": d = charger(); sauver(d); print("ok", len(d["offres"]))
    else: print(__doc__)
