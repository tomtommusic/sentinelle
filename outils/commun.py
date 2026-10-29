"""Fonctions communes aux tournées Sentinelle : régions, agences exclues, dates, domaines."""
import json, re, unicodedata, datetime
now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-4))).replace(second=0, microsecond=0)
def slug(s):
    s = unicodedata.normalize('NFD', (s or '').lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', '-', s).strip('-')
REG = {
 "Estrie": ["Sherbrooke","Magog","Valcourt","Windsor","Coaticook","Lac-Mégantic","East Angus","Val-des-Sources","Asbestos","Richmond","Stanstead","Compton","Eastman","Mansonville","Bolton-Ouest","Marbleton","Stoke","Cookshire","Waterville","Ascot","Orford","North Hatley","Lennoxville","Rock Forest","Weedon","Dudswell","Saint-François-Xavier-de-Brompton","Racine","Kingsbury","Estrie","Lac-Drolet","Saint-Sébastien-de-Frontenac","Ayer's Cliff","Saint-Sébastien"],
 "Centre-du-Québec": ["Drummondville","Victoriaville","Bécancour","Nicolet","Plessisville","Princeville","Warwick","Kingsey Falls","Saint-Germain-de-Grantham","St-Germain-de-Grantham","Sainte-Brigitte-des-Saults","Wickham","Baie-du-Febvre","St-François-du-Lac","Saint-François-du-Lac","Aston Junction","Daveluyville","Saint-Cyrille-de-Wendover","Villeroy","Saint-Léonard-d'Aston","Chesterville","Tingwick","Saint-Albert","Centre-du-Québec","Saint-Bonaventure","Notre-Dame-du-Bon-Conseil","Sainte-Eulalie","Saint-Valère","Saint-Félix-de-Kingsey"],
}
REG["Mauricie"] = ["Trois-Rivières","Shawinigan","La Tuque","Louiseville","Yamachiche","Saint-Boniface","Sainte-Geneviève-de-Batiscan","Saint-Tite","Sainte-Anne-de-la-Pérade","Saint-Étienne-des-Grès","Proulxville","Champlain","Saint-Stanislas","Saint-Maurice","Notre-Dame-du-Mont-Carmel","Wemotaci","Grand-Mère","Saint-Narcisse","Batiscan","Saint-Luc-de-Vincennes","Maskinongé","Saint-Paulin","Mauricie"]
REG["Lanaudière"] = ["Joliette","Repentigny","Terrebonne","Mascouche","L'Assomption","Lavaltrie","Berthierville","Saint-Jacques","Sainte-Julienne","Rawdon","Saint-Lin","Crabtree","Saint-Charles-Borromée","Sainte-Mélanie","Saint-Félix-de-Valois","Notre-Dame-des-Prairies","Saint-Gabriel","Chertsey","Lanoraie","L'Épiphanie","Lanaudière"]
REG["Montérégie"] = ["Granby","Bromont","Cowansville","Knowlton","Lac-Brome","Dunham","Sutton","Farnham","Waterloo","Saint-Hyacinthe","Saint-Damase","Sainte-Rosalie","Upton","Acton Vale","Saint-Pie","Saint-Liboire","Saint-Valérien-de-Milton","Sorel-Tracy","Contrecoeur","Varennes","Boucherville","Longueuil","Brossard","Saint-Lambert","Saint-Bruno","Sainte-Julie","Beloeil","Mont-Saint-Hilaire","Chambly","Marieville","Rougemont","Saint-Césaire","Saint-Jean-sur-Richelieu","La Prairie","Candiac","Châteauguay","Salaberry-de-Valleyfield","Vaudreuil","Saint-Robert","Mercier","Beauharnois","Saint-Rémi","Rive-Sud de Montréal","Saint-Alphonse-de-Granby","Saint-Ours","Saint-Denis-sur-Richelieu","Massueville","Saint-Joseph-de-Sorel","Saint-Hubert","Sainte-Catherine","Delson","Sherrington","Saint-Basile-le-Grand","Saint-Mathias-sur-Richelieu","Montérégie"]
REG["Chaudière-Appalaches"] = ["Lévis","Saint-Nicolas","Saint-Romuald","Charny","Pintendre","Saint-Lambert-de-Lévis","Saint-Georges","Beauceville","Sainte-Marie","Saint-Joseph-de-Beauce","Saint-Éphrem-de-Beauce","Saint-Victor","Vallée-Jonction","Tring-Jonction","Saint-Elzéar","Sainte-Claire","Saint-Henri","Saint-Apollinaire","Saint-Agapit","Laurier-Station","Thetford Mines","Disraeli","Black Lake","Montmagny","L'Islet","Saint-Jean-Port-Joli","Saint-Pamphile","Lac-Etchemin","Saint-Prosper","Saint-Côme-Linière","Saint-Martin","Saint-Isidore","Scott","Saint-Bernard","Sainte-Hénédine","Saint-Anselme","Saint-Gervais","Saint-Raphaël","Armagh","Saint-Just-de-Bretenières","East Broughton","Saint-Gédéon-de-Beauce","Saint-Évariste","Notre-Dame-des-Pins","Saint-Zacharie","Lotbinière","Saint-Lambert-de-Lauzon","Saint-Damien-de-Buckland","Chaudière-Appalaches"]
REG["Laurentides"] = ["Saint-Jérôme","Mirabel","Blainville","Boisbriand","Saint-Eustache","Sainte-Thérèse","Rosemère","Bois-des-Filion","Lorraine","Deux-Montagnes","Sainte-Marthe-sur-le-Lac","Pointe-Calumet","Saint-Joseph-du-Lac","Oka","Saint-Placide","Lachute","Brownsburg","Mont-Tremblant","Sainte-Agathe","Saint-Sauveur","Sainte-Adèle","Prévost","Saint-Colomban","Sainte-Sophie","Sainte-Anne-des-Plaines","Saint-Hippolyte","Val-David","Mont-Laurier","Rivière-Rouge","Labelle","Morin-Heights","Saint-Lin–Laurentides-X","Saint-Janvier","Saint-Canut","Saint-Benoît","Laurentides"]
REG["Capitale-Nationale"] = ["Ville de Québec","Québec","Quebec","Sainte-Foy","Sillery","Beauport","Charlesbourg","Cap-Rouge","Val-Bélair","Loretteville","L'Ancienne-Lorette","Ancienne-Lorette","Saint-Augustin-de-Desmaures","Lac-Beauport","Stoneham","Shannon","Wendake","Boischatel","L'Ange-Gardien","Château-Richer","Sainte-Anne-de-Beaupré","Pont-Rouge","Donnacona","Saint-Raymond","Neuville","Portneuf","Saint-Marc-des-Carrières","Baie-Saint-Paul","La Malbaie","Lac-Saint-Charles","Sainte-Brigitte-de-Laval","Stoneham","Deschambault","Saint-Tite-des-Caps","Capitale-Nationale"]
REG["Montréal"] = ["Montréal","Montreal","Saint-Laurent","Dorval","Pointe-Claire","Lachine","LaSalle","Anjou","Kirkland","Dollard-des-Ormeaux","Mont-Royal","Ville Mont-Royal","Westmount","Verdun","Saint-Léonard","Pierrefonds","Baie-D'Urfé","Sainte-Anne-de-Bellevue","Beaconsfield","Côte-Saint-Luc","Hampstead","Rivière-des-Prairies","Outremont"]
REG["Laval"] = ["Laval"]
def _n(x):
    x = unicodedata.normalize('NFD', x.lower()); x = ''.join(c for c in x if unicodedata.category(c) != 'Mn')
    x = re.sub(r"^st-", "saint-", x); x = re.sub(r"^ste-", "sainte-", x)
    return x
def region(city):
    c = _n(city)
    best = None
    for r, cs in REG.items():
        for v in cs:
            if c.startswith(_n(v)) and (best is None or len(v) > best[0]): best = (len(v), r)
    return best[1] if best else None
AGENCES = {"hays","recruscope","selekktus","agence-charlie","emergence","brh","jobsmedia-io","go-rh","jump-recruteurs","proforce-personnel","immigrant-quebec","hudson-rpo","fed-finance","metier-plus","randstad","cabinet-joyal-chasseurs-de-tetes","l-orientheque","alevo-talents","professional-staffing","totem-recruteur-de-talent","simetra-recrutement","claude-grenier-ressources-humaines","pur-rh","alinov-entreprise-de-developpement-professionnel","fed-manutech","recrute-action-inc","horus-ressources","randstad","bedard-ressources-humaines-human-resources","defisrh","coefficient-rh","totem-recrutement","azimut-management","henri-talent-culture","vision-ressources-humaines-inc","confidentiel","kassen-recruitment","jobsmedia-io","jobsmedia","otus-rh","extra-multi-ressources","express-employment-professionals","express-employment-profess","hera-ressources-humaines","azimut-management","aerotek","bedard-ressources","larouche-raymond","quantum-management-services","talentworld","artemis","adecco","manpower","kelly-services","lambert","korn-ferry","kenova","robert-half","michael-page","totem","professional-staffing","randstad-canada","michael-page","jump-recruteurs","kenova-recrutement-humain","akkodis","gestion-de-personnel-10-04-inc","pcv-group-inc-personnel-chez-vous-recruitment-services","technogenie-chasseurs-de-talents","cote-personnel","alevo-talents","confidential","artemis","cristalrh","robert-half","recrutement-precision","odgers","aleanza-recrutement-durable","technogenie","cote-personnel","technogenie-inc","groupe-technogenie"}
def to_iso(age):
    m = re.match(r"(\d+)\s*(minute|heure|jour|semaine|mois)", age or "")
    if not m: return None
    n = int(m.group(1)); u = m.group(2)
    d = {"minute": datetime.timedelta(minutes=n), "heure": datetime.timedelta(hours=n), "jour": datetime.timedelta(days=n),
         "semaine": datetime.timedelta(weeks=n), "mois": datetime.timedelta(days=30 * n)}[u]
    return (now - d).isoformat()
def domaine(titre, tag):
    T = titre.lower()
    if tag == "ALL":
        if re.search(r"qualit|maintenance|fiabilit|salubrit|haccp|\bsst\b|sant[ée].{0,4}s[ée]curit|\bhse\b|\behs\b", T): return "Qualité, maintenance et SST"
        if re.search(r"m[ée]cani|mechanical|cvac|hvac|r[ée]frig[ée]ration", T): return "Génie mécanique"
        if re.search(r"contr[ôo]l|comptab|financ|cpa|tr[ée]sor|fiscal|co[uû]t de revient|fp&a|\bpaie\b", T): return "Finance et comptabilité"
        if re.search(r"ressources humaines|\brh\b|talent|recrut|relations de travail|r[ée]mun[ée]ration|human resources|\bhr\b", T): return "Ressources humaines"
        if re.search(r"achat|approvision|logisti|cha[iî]ne d|supply|procurement", T): return "Approvisionnement et logistique"
        if re.search(r"vente|d[ée]veloppement des affaires|business development|comptes industriels|\bsales\b", T): return "Ventes et développement des affaires"
        if re.search(r"\bti\b|\berp\b|informatique|technologies de l.information|\bit director", T): return "Technologies de l'information"
        if re.search(r"ing[ée]nieur|engineer|concepteur|dessinateur|designer|agent m[ée]thodes|programmeur d.automates|\bplc\b", T): return "Ingénierie et production"
        if re.search(r"usine|production|surintendant|op[ée]rations|carri[èe]re|am[ée]lioration continue|lean", T): return "Opérations et production"
        if re.search(r"projet|estimat", T): return "Gestion de projets"
        return "Direction"
    if tag in ("Génie mécanique", "Ingénierie et production"):
        if re.search(r"m[ée]cani|mechanical|tuyauterie|piping|m[ée]cano|cvac|hvac", titre, re.I): return "Génie mécanique"
        return "Ingénierie et production"
    return tag

def est_agence(cie):
    s = slug(cie)
    return any(s == a or s.startswith(a + "-") for a in AGENCES)
BRUIT = re.compile(r"(salle à manger|restauration|restaurant|hébergement touristique|auberge|entretien ménager|ferme d'élevage|succursale|planification préalable|candidature spontanée|étudiant|stagiaire|stage\b|technicien|personnel enseignant|professeur|enseignant|adjoint(e)? (administrati|de direction))", re.I)

STOP_CIE = {"groupe", "group", "les", "le", "la", "l", "industries", "industrie", "inc", "canada", "ltee", "ltd", "corporation", "corp",
            "compagnie", "cie", "entreprises", "entreprise", "produits", "services", "the", "company", "de", "du", "des", "et", "s", "e", "c"}
def coeur_cie(nom):
    t = [w for w in slug(re.split(r" – | \(", nom or "")[0]).split("-") if w and w not in STOP_CIE]
    return t[0] if t else slug(nom)
def titre_norm(t):
    t = re.sub(r"\(.*?\)", " ", (t or "").lower()).strip()      # (e), (H/F), (Trois-Rivières)…
    if "/" in t:                                                   # forme masculine/féminine
        a, b = [x.strip() for x in t.split("/", 1)]
        if a[:4] and b[:4] == a[:4]:
            t = a + b[len(b.split(" ")[0]):] if " " not in a else a
    m = re.search(r"\s[-–|]\s*([^-–|]+)$", t)                     # « … - Longueuil » : retirer la ville
    if m and region(m.group(1).strip()): t = t[:m.start()]
    t = re.sub(r"[·.](e|ne|trice|rice|euse|ère|ere|eure)s?\b", "", t)
    t = re.sub(r"\b(h/f|f/h|senior|sénior|junior|temporaire|hybride)\b", " ", t)
    return slug(t)[:40]
def cle_offre(o):
    """Même poste, même entreprise : un seul doublon, quelle que soit la ville ou la source."""
    return (titre_norm(o["titre"]), coeur_cie(o["entreprise"]))
