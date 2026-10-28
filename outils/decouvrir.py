"""Ajoute aux prospects les employeurs trouvés dans les offres qui n'y sont pas encore."""
import json, re, unicodedata, datetime
from collections import defaultdict
import os
R = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data') + '/'
def slug(s):
    s = unicodedata.normalize('NFD', (s or '').lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
STOP = {"groupe", "group", "les", "le", "la", "l", "industries", "industrie", "inc", "canada", "ltee", "ltd", "corporation", "corp", "compagnie", "cie", "entreprises", "entreprise", "produits", "services", "the", "company", "de", "du", "des", "et", "s", "e", "c"}
def coeur(nom):
    t = [w for w in slug(nom.split(" – ")[0]).split("-") if w and w not in STOP]
    return "".join(t[:1]) if t else slug(nom)
pros = json.load(open(R + 'prospects.json'))
offres = [o for o in json.load(open(R + "offres.json"))["offres"] if not o.get("terminee")]
connus = {coeur(c["nom"]) for c in pros["entreprises"]}

par = defaultdict(list)
for o in offres:
    par[coeur(o["entreprise"])].append(o)

PUBLIC = re.compile(r"(centre de services scolaire|c[ée]gep|minist[èe]re|municipalit|ville de|sant[ée] qu[ée]bec|f[ée]d[ée]ration qu[ée]b[ée]coise|canmet|[ée]cole|universit|gouvernement|hydro-qu[ée]bec|spec du|\bmrc\b|investissement qu[ée]bec|forces arm[ée]es|centre d.h[ée]bergement|chambre de commerce|soquij|ceriu|mus[ée]e|fondation|f[ée]d[ée]ration|conseil des industriels)", re.I)
GRANDS = {"siemens", "rolls", "bombardier", "airbus", "amazon", "artelia", "edf", "kiewit", "dra", "genetec", "bnp", "agropur", "saputo", "cascades", "future", "fiera", "ubisoft", "sysco", "maple", "pratt", "wsp", "englobe", "ametek", "fives", "volvo", "cima", "canac", "kerry", "davie", "prevost", "realtruck", "kinaxis", "sofina", "newly", "cyient", "sogeclair", "halo", "migso", "aon", "banque", "ville", "5n", "malvern", "kpmg", "stantec", "investissement", "hcltech", "mda", "epiq", "air", "andritz", "celanese", "systra", "nordex", "mckesson", "multi", "mty", "transdev", "american", "cellcom", "uap", "ge", "samsic", "deloitte", "pwc", "desjardins", "pepsico", "couche", "stantec", "steris", "atkinsrealis", "sika", "amrize", "trane", "beneva", "harris", "compugen", "wipro", "carrier", "nova", "vinci", "lion", "mallette", "mnp", "bain", "biscuits", "leclerc", "coveo", "h2o", "alcoa", "arcelormittal", "bridgestone", "cibc", "cpkc", "desjardins", "general", "home", "honeywell", "kpmg", "mnp", "metro", "pomerleau",
          "pratt", "sysco", "tetra", "hatch", "hcltech", "cyient", "teledyne", "lactalis", "gordon", "eurovia", "expleo", "bunge", "essity", "rheinmetall",
          "wajax", "valmet", "owens", "mallette", "bba", "colliers", "graymont", "guillevin", "nova", "mda", "arjo", "chart", "bel", "broan", "bridor", "nortek"}
MULTI = {"siemens", "rolls", "airbus", "amazon", "artelia", "edf", "kiewit", "dra", "bnp", "future", "sysco", "maple", "pratt", "wsp", "ametek", "fives", "volvo", "kerry", "prevost", "realtruck", "kinaxis", "sofina", "newly", "cyient", "sogeclair", "halo", "migso", "malvern", "flying", "air", "andritz", "celanese", "systra", "nordex", "mckesson", "multi", "transdev", "ge", "samsic", "deloitte", "pwc", "pepsico", "stantec", "steris", "atkinsrealis", "sika", "amrize", "trane", "harris", "wipro", "carrier", "vinci", "alcoa", "arcelormittal", "bridgestone", "cpkc", "general", "home", "honeywell", "kpmg", "sysco", "tetra", "hatch", "hcltech", "cyient", "teledyne",
         "lactalis", "gordon", "eurovia", "expleo", "bunge", "essity", "rheinmetall", "valmet", "owens", "colliers", "graymont", "nova", "mda", "arjo", "chart",
         "bel", "broan", "bridor", "nortek", "litostroj", "artelia", "intersand", "vins"}
AGENCES = {"mesar", "larouche", "artemis", "cristalrh", "robert", "recrutement", "odgers", "aleanza", "confidential"}

aujourd = datetime.date.today().isoformat()
ajout = []
for k, L in par.items():
    if k in connus or k in AGENCES: continue
    nom = L[0]["entreprise"]
    villes = sorted({o["lieu"].replace(", QC", "") for o in L})
    n = len(L)
    dom = sorted({o["domaine"] for o in L})
    signal = f"{n} offre{'s' if n > 1 else ''} en cours dans Sentinelle ({', '.join(dom)}), découverte le {aujourd}"
    raisons = []
    if PUBLIC.search(nom):
        d = dict(taille="", type="Public / parapublic", score=-5, categorie="Peu probable",
                 raisons=["Employeur public : embauche encadrée par des conventions et des règles d'attribution de contrats", signal])
    else:
        score = 0; taille = "1000+" if k in GRANDS else ""
        if taille: score -= 2; raisons.append("Très grande organisation : équipe d'acquisition de talents interne")
        else: score += 1; raisons.append("Taille à confirmer (probablement une PME)")
        typ = "Privé"
        if k in MULTI: score -= 1; typ = "Filiale d'un groupe international"; raisons.append("Filiale d'une multinationale : recrutement souvent centralisé au siège")
        score += 2; raisons.append("Recrute des profils spécialisés (" + ", ".join(dom) + ")")
        score += 1; raisons.append("Recrute en ce moment : " + signal)
        if n >= 3: score += 1; raisons.append("Plusieurs postes ouverts en même temps")
        cat = "Mandats de cadres" if taille == "1000+" else ("Fort probable" if score >= 6 else "Probable" if score >= 3 else "Peu probable")
        d = dict(taille=taille, type=typ, score=score, categorie=cat, raisons=raisons)
    ajout.append(dict(id=slug(nom), nom=nom, region=L[0]["region"], ville=" / ".join(villes[:3]),
                      secteur="À préciser", decouvert=aujourd, **d))
ids = {e["id"] for e in pros["entreprises"]}
ajout = [a for a in ajout if a["id"] not in ids]
pros["entreprises"].extend(ajout)
pros["miseAJour"] = aujourd
pros["territoire"] = "Estrie (Cantons-de-l'Est), Centre-du-Québec, Mauricie, Lanaudière, Montérégie, Chaudière-Appalaches, Laurentides, Québec, Montréal et Laval"
json.dump(pros, open(R + 'prospects.json', 'w'), ensure_ascii=False, indent=1)
from collections import Counter
print(len(ajout), Counter(a["categorie"] for a in ajout), "total", len(pros["entreprises"]))
