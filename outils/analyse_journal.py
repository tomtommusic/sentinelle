"""Analyse du journal d'utilisation de Sentinelle.

Le journal vit seulement dans le navigateur de l'utilisatrice (clé localStorage « sentinelle-journal »).
Pour l'analyser : ouvrir Sentinelle dans son Chrome, copier localStorage.getItem("sentinelle-journal")
dans un fichier (jamais dans ce dépôt public), puis :

  python3 outils/analyse_journal.py journal.json
"""
import json, os, sys, datetime
from collections import Counter

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = json.load(open(sys.argv[1], encoding="utf-8"))
offres = {o["id"]: o for o in json.load(open(os.path.join(RACINE, "data", "offres.json"), encoding="utf-8"))["offres"]}
tz = datetime.timezone(datetime.timedelta(hours=-4))
for e in J:
    e["dt"] = datetime.datetime.fromisoformat(e["t"].replace("Z", "+00:00")).astimezone(tz)

# Séances : une pause de plus de 30 minutes commence une nouvelle séance
seances, cur = [], []
for e in J:
    if cur and (e["dt"] - cur[-1]["dt"]).total_seconds() > 1800:
        seances.append(cur); cur = []
    cur.append(e)
if cur: seances.append(cur)
print(f"{len(J)} événements, {len(seances)} séances")
for s in seances:
    duree = (s[-1]["dt"] - s[0]["dt"]).total_seconds() / 60
    print(f"  {s[0]['dt']:%a %d %b %H:%M} · {duree:.0f} min · pages : {', '.join(sorted({e['p'] for e in s}))}")

print("\nJours et heures d'utilisation :", Counter(f"{e['dt']:%A}" for e in J if e["e"] == "visite").most_common(),
      Counter(e["dt"].hour for e in J if e["e"] == "visite").most_common())
print("Pages visitées :", Counter(e["p"] for e in J if e["e"] == "visite").most_common())
print("Recherches :", Counter(e.get("valeur") for e in J if e["e"] == "recherche").most_common(20))
print("Filtres choisis :", Counter(f"{e.get('champ')}={e.get('valeur')}" for e in J if e["e"] == "choix" and e.get("champ") not in ("q",)).most_common(25))
print("Boutons et liens :", Counter(e.get("quoi", "").split("\n")[0] for e in J if e["e"] == "clic").most_common(25))
vus = [offres[e["id"]] for e in J if e["e"] == "clic" and e.get("id") in offres]
print("Offres touchées par domaine :", Counter(o["domaine"] for o in vus).most_common())
print("Offres touchées par région :", Counter(o["region"] for o in vus).most_common())
print("Offres touchées par âge (jours) :", Counter(min(60, ((datetime.datetime.now(datetime.timezone.utc) - datetime.datetime.fromisoformat(o["publieLe"])).days // 7) * 7) for o in vus if o.get("publieLe")).most_common())
print("Notes écrites :", sum(1 for e in J if e["e"] == "note"))
