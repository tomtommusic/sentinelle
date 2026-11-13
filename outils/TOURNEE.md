# Tournée Sentinelle : marche à suivre

Ce document décrit la tournée automatique du matin (lundi au vendredi). Elle se fait dans le Chrome de l'ordinateur où l'extension Claude est installée et où les sessions LinkedIn et Indeed sont ouvertes.

## 0. Préparation

1. Cloner le dépôt `tomtommusic/sentinelle` (ou faire `git pull`), puis travailler dans un dossier de travail à part pour les fichiers bruts (`brut.txt`, `frais.txt`, `fermees.txt`, `ouvertes.txt`). Ces fichiers ne vont pas dans le dépôt.
2. Charger les outils Chrome et ouvrir **un nouvel onglet**. Le fermer à la fin.
3. Si Chrome ne répond pas (ordinateur éteint ou en veille), réessayer une fois 30 minutes plus tard. Après ça, abandonner la tournée du jour et le dire dans le compte rendu.

## 1. Ce qu'on cherche

- **Postes :**
  - génie mécanique, ingénierie et production;
  - RH (directeur, conseiller, partenaire d'affaires);
  - finance (contrôleur financier, contrôleur adjoint, comptable, analyste financier);
  - vice-président et direction générale;
  - gérant et chargé de projet.
- **Période :** offres des 60 derniers jours. Celles de 7 à 60 jours sont les plus utiles.
- **Secteurs suivis de près (depuis le 9 novembre 2026) :** énergie (Hydro-Québec, éolien, lignes de transport), défense et construction navale (Davie et ses fournisseurs), mines et métallurgie, agroalimentaire, environnement, santé et pharma, et direction générale d'organisations (municipalités, MRC, coopératives, OBNL). Chaque offre et chaque prospect reçoit un secteur (`outils/secteurs.py`, appelé par `tournee.py` et `decouvrir.py`), qui alimente le filtre « Secteur d'activité ».
- **Territoire :** Estrie, Centre-du-Québec, Mauricie, Lanaudière, Montérégie, Chaudière-Appalaches, Laurentides, Québec (Capitale-Nationale), Montréal et Laval. **Depuis le 9 novembre 2026, aussi :** Abitibi-Témiscamingue, Nord-du-Québec, Côte-Nord, Saguenay–Lac-Saint-Jean et Bas-Saint-Laurent. La liste des villes par région est dans `outils/commun.py` (`REG`, `REGIONS_SUD`, `REGIONS_RESSOURCES`).
- **Exclusions :**
  - les agences de recrutement, qui sont des concurrentes : la liste est dans `commun.py` (`AGENCES`), à compléter au besoin;
  - les offres « Confidentiel ».

## 2. Indeed (toutes les régions, chaque jour)

Deux requêtes, pour chaque ville pivot avec son rayon :

- **Générale** (`QG`) : `ingénieur OR contrôleur OR comptable OR "ressources humaines" OR "chargé de projet" OR "vice-président" OR "directeur financier" OR "directeur général" OR "directeur des opérations"`
- **Ingénierie** (`QE`) : `"ingénieur mécanique" OR "ingénieur de projets" OR "ingénieur industriel" OR "ingénieur de procédés" OR "directeur de production" OR "directeur d'usine"`
- **Opérations, qualité, maintenance, SST** (`QO`) : `"directeur d'usine" OR "directeur de production" OR surintendant OR "directeur de maintenance" OR "planificateur de maintenance" OR fiabilité OR "directeur qualité" OR "ingénieur qualité" OR "coordonnateur qualité" OR "amélioration continue" OR automatisation OR automates OR "santé et sécurité" OR SST OR salubrité OR HACCP`
- **Achats, ventes, TI, finance et RH spécialisés** (`QA`) : `"directeur des achats" OR approvisionnement OR logistique OR "directeur des ventes" OR "développement des affaires" OR "directeur TI" OR ERP OR trésorier OR fiscaliste OR "relations de travail" OR "acquisition de talents" OR rémunération OR "directeur administratif" OR "directeur général adjoint" OR "coût de revient" OR "FP&A" OR "chef comptable" OR "contrôleur corporatif" OR "directeur de la paie" OR "partenaire d'affaires"`
- **Spécialités techniques** (`QT`) : `"concepteur mécanique" OR dessinateur OR CVAC OR réfrigération OR "centre de données" OR "ingénieur méthodes" OR "agent méthodes" OR robotique OR photonique OR "conception de produits" OR emballage OR estimateur OR "directeur de projets" OR "ingénieur électrique" OR "infrastructures municipales" OR "chargé de projets"`

- **Secteurs**, en trois requêtes courtes (une longue liste de termes donne des résultats sans rapport, vérifié le 9 novembre 2026) :
  - `QS1` énergie et défense : `éolien OR "énergie renouvelable" OR "postes électriques" OR "construction navale" OR défense`
  - `QS2` mines : `"ingénieur minier" OR géologue OR métallurgiste OR "directeur de mine" OR "surintendant de mine"`
  - `QS3` agroalimentaire, environnement, pharma : `"transformation alimentaire" OR "assurance qualité alimentaire" OR "traitement des eaux" OR "affaires réglementaires"`

**Régions ressources (lundi et jeudi) :** QG, plus QS2 en Abitibi et sur la Côte-Nord et QS1 au Bas-Saint-Laurent et au Saguenay, une page chacune, pour Rouyn-Noranda (50), Val-d'Or (40), Chibougamau (80), Sept-Îles (40), Baie-Comeau (40), Saguenay (40), Alma (40), Rimouski (50) et Rivière-du-Loup (50). Avec `fromage=7` le lundi et `fromage=3` le jeudi. Garder les pauses de 10 à 15 secondes entre les pages.

**QS1 et QS3 dans le sud :** une page par jour, en alternance entre Sherbrooke, Trois-Rivières, Québec, Lévis, Montréal et Saint-Jean-sur-Richelieu.

QO, QA et QT : une page chacune, chaque jour, pour Sherbrooke (60), Drummondville (50), Trois-Rivières (50), Joliette (40), Saint-Hyacinthe (40), Saint-Jean-sur-Richelieu (30), Montréal (15), Saint-Jérôme (35), Québec (35) et Saint-Georges (50). Ne garder que les postes de professionnels, de spécialistes et de cadres : pas de techniciens, d'opérateurs, de journaliers, de gens de métier (soudeur, mécanicien, électricien) ni de représentants de commerce de détail.

| Ville (rayon en km) | Pages QG | Pages QE |
|---|---|---|
| Sherbrooke (50), Trois-Rivières (40), Drummondville (40), Québec (30), Montréal (15) | 2 | 1 |
| Victoriaville (40), Joliette (40), Saint-Hyacinthe (30), Granby (30), Saint-Jean-sur-Richelieu (25), Lévis (25), Saint-Georges (50), Saint-Jérôme (35) | 1 | 1 |

**Adresse de recherche :**

```
https://ca.indeed.com/jobs?q=<QG ou QE encodé>&l=<Ville>%2C+QC&radius=<r>&lang=fr[&start=10]
```

**Extraction** (à lancer après le chargement de la page) :

```js
await new Promise(r=>setTimeout(r,2200));window.__r=[...document.querySelectorAll('a[data-jk]')].map(a=>{const card=a.closest('li')||a.closest('td')||a.parentElement;const co=(card.querySelector('[data-testid="company-name"]')||{}).innerText||'';const lo=(card.querySelector('[data-testid="text-location"]')||{}).innerText||'';return [a.getAttribute('data-jk'),(a.innerText||'').trim().slice(0,60),co.trim().slice(0,40),lo.replace(/, QC.*$/,'').trim()].join('¦')}).filter(s=>!/^(0123|1234|2345|3456|4567|5678|6789|789a|890a|89ab|9abc|abcd|bcde|cdef|0f1e|a1b2|fedc|f1e2)/.test(s));'n='+window.__r.length
```

Garder la colonne lieu telle quelle (sans `, QC`) : Indeed écrit « Télétravail hybride à Sherbrooke » ou « Télétravail à Montréal ». `tournee.py` en tire le mode de travail. Ne pas utiliser le filtre « télétravail » d'Indeed (`sc=0kf:attr(...)`) : il renvoie aussi des offres sur place.

Lire ensuite le résultat par tranches : `window.__r.slice(0,8).join('\n')`, puis `slice(8,16)`. Les sorties de plus de 1000 caractères sont tronquées. Les identifiants en suite hexadécimale (abcdef0123…) sont des leurres, il faut les ignorer.

**Offres récentes :** relancer QG et QE avec `&fromage=7` (une page chacune), récupérer seulement les identifiants et les ajouter à `frais.txt`. Indeed ne donne pas de date : une offre récente est datée d'environ 3 jours, les autres d'environ 14 jours.

## 3. LinkedIn (rotation, au plus 12 pages par jour)

Le compte LinkedIn utilisé est personnel. Il ne faut **jamais dépasser 12 pages de résultats par jour**.

| Jour | Villes |
|---|---|
| Lundi | Sherbrooke, Granby, Drummondville, Victoriaville |
| Mardi | Trois-Rivières, Shawinigan, Joliette, Saint-Hyacinthe |
| Mercredi | Saint-Jean-sur-Richelieu, Longueuil, Laval |
| Jeudi | Québec, Lévis |
| Vendredi | Montréal (6 pages) et régions ressources (6 pages) : Rouyn-Noranda et Sept-Îles les semaines paires, Saguenay et Rimouski les semaines impaires |

**Termes**, sous la forme « terme à Ville » (rayon de 80 km automatique) : `ingénieur`, `directeur`, `contrôleur financier`, `ressources humaines`, `chargé de projets`. Pour les régions ressources : `ingénieur`, `directeur`, `surintendant`. Il faut ajuster pour rester sous 12 pages.

Saint-Georges et Saint-Jérôme sont mal reconnues par LinkedIn : on les fait seulement par Indeed.

**Adresse de recherche** :

```
https://www.linkedin.com/jobs/search-results/?keywords=<terme à Ville encodé>&f_TPR=r5184000
```

**Extraction.** On calcule d'abord, en retournant seulement le nombre d'offres :

```js
await new Promise(r=>setTimeout(r,2500));let sc=document.querySelector('[componentkey^="job-card-component-ref-"]');while(sc&&sc!==document.body){const s=getComputedStyle(sc);if(/(auto|scroll)/.test(s.overflowY)&&sc.scrollHeight>sc.clientHeight+20)break;sc=sc.parentElement;}for(let i=0;i<8;i++){if(sc&&sc!==document.body)sc.scrollTop=sc.scrollHeight;await new Promise(r=>setTimeout(r,450));}const V=/ \(offre d’emploi vérifiée\)$/;window.__r=[...document.querySelectorAll('[componentkey^="job-card-component-ref-"]')].map(d=>{const id=d.getAttribute('componentkey').replace('job-card-component-ref-','');let l=d.innerText.split('\n').map(s=>s.trim()).filter(Boolean);if(V.test(l[0]))l=l.slice(1);if(l[1]===l[0])l=l.slice(1);const pub=(l.find(x=>/^Publication /.test(x))||'').replace(/^Publication il y a /,'');return [id,l[0].slice(0,60),l[1],(l[2]||'').replace(/, QC( \(|$)/,'$1'),pub].join('¦')});'n='+window.__r.length
```

On lit ensuite les tranches `slice(0,8)`, `slice(8,16)` et `slice(16,25)`.

**Garder la mention du mode de travail.** LinkedIn ajoute au lieu « (Hybride) », « (À distance) » ou « (Sur site) ». Il faut la laisser dans la colonne ville du fichier brut (ex. `Sherbrooke (Hybride)`) : `tournee.py` la retire du lieu et l'enregistre dans le champ `modalite`, qui alimente l'onglet Télétravail.

**Télétravail :** le filtre `f_WT` n'est plus pris en compte par la nouvelle page de recherche de LinkedIn (vérifié le 5 novembre 2026). La mention « (Hybride) » ou « (À distance) » sur chaque carte suffit : elle est captée par toutes les recherches.

## 4. Jobillico (facultatif, si le temps le permet)

```
https://www.jobillico.com/recherche-emploi/<terme>/<ville>/quebec
```

Format des lignes : `id¦titre¦entreprise¦ville¦âge¦chemin`. L'âge s'écrit par exemple « 5 jour(s) », « 2 semaines » ou « 1 mois ».

## 5. Fichier brut

Il faut écrire `brut.txt` en gardant seulement les postes visés et en retirant le bruit (restauration, techniciens, stagiaires, ventes, etc.) :

```
#SRC Indeed
#ALL
3c4bfb6b294da0f8¦Contrôleur financier¦Quadra Plast¦Sainte-Thérèse
#SRC LinkedIn
#Génie mécanique
4481904321¦Ingénieur.e en conception mécanique¦Robotiq¦Saint-Nicolas¦4 jours
#Ressources humaines
...
```

La ligne `#MODE Télétravail` ou `#MODE Hybride` (puis `#MODE` seul) force le mode de travail des lignes qui suivent, quand on l'a vérifié dans l'offre.

Les étiquettes de domaine possibles sont :
- `#ALL` (domaine deviné d'après le titre);
- `#Génie mécanique`;
- `#Ingénierie et production`;
- `#Finance et comptabilité`;
- `#Ressources humaines`;
- `#Direction`;
- `#Gestion de projets`.

## 6. Fusion

```
python3 <dépôt>/outils/tournee.py fusion brut.txt frais.txt
```

La commande ajoute les nouvelles offres, met à jour celles qui ont été revues et écrit `nouvelles-offres.json` dans le dossier courant.

## 7. Offres terminées

1. `python3 <dépôt>/outils/tournee.py averifier 40` liste les offres qui n'ont pas été revues pendant la tournée.
2. Ouvrir chaque offre Indeed et Jobillico de la liste. Pour LinkedIn, au plus 10 offres par jour.
   - **Fermée** si la page indique « Cette offre d'emploi a expiré », « n'est plus disponible », « N'accepte plus les candidatures », « No longer accepting applications », ou si elle renvoie vers une page de recherche ou d'erreur. Mettre l'identifiant (ex. `jb-…`, `li-…`) dans `fermees.txt`.
   - **Ouverte** sinon. Mettre l'identifiant dans `ouvertes.txt`.
3. Enregistrer le résultat :
   ```
   python3 <dépôt>/outils/tournee.py fermer fermees.txt
   python3 <dépôt>/outils/tournee.py ouvertes ouvertes.txt
   ```

Règles automatiques, appliquées à chaque enregistrement :
- une offre ni revue ni confirmée ouverte depuis 30 jours devient « terminée ». Les recherches ne montrent que les premières pages : une offre absente des résultats n'est pas forcément fermée, d'où la vérification de l'étape 7, à faire chaque jour sur les 40 offres les plus anciennement vues;
- une offre publiée il y a plus de 60 jours est retirée;
- une offre terminée depuis plus de 30 jours est retirée.

Dans Sentinelle, les offres terminées sont cachées par défaut. Une case à cocher permet de les afficher, avec la mention « Terminée le … ».

## 8. Prospects, publication et compte rendu

```
python3 <dépôt>/outils/decouvrir.py
cd <dépôt> && git add -A && git commit -m "Tournée du <date>" && git push
```

Il faut aussi fermer l'onglet Chrome.

**Compte rendu en français**, court :
- nombre de nouvelles offres par région;
- les 5 à 10 plus intéressantes (PME, postes spécialisés);
- nombre d'offres terminées;
- nouveaux prospects;
- problèmes rencontrés (connexion, pages bloquées).

Ne jamais inscrire d'adresse courriel personnelle dans ce dépôt public.

## 9. Si le push est refusé

Une autre tournée a peut-être publié entre-temps. Dans ce cas :
1. `git fetch && git reset --hard origin/main`;
2. relancer `tournee.py fusion` avec les mêmes fichiers bruts, puis `fermer` et `ouvertes`;
3. relancer `decouvrir.py`;
4. refaire le commit et le push.

## 10. Signaux d'affaires (le lundi seulement)

Le lundi, en plus de la tournée, chercher les nouvelles des 7 derniers jours qui annoncent des embauches : agrandissements, nouvelles usines, investissements ou prêts publics (Investissement Québec, quebec.ca, DEC), acquisitions, campagnes d'embauche, nominations ou départs de dirigeants. Couvrir les 10 régions du territoire.

**Recherches utiles :** WebSearch « agrandissement usine <région> <mois année> », « investissement emplois <ville> », « acquiert <ville> », puis vérifier chaque article avec WebFetch : date, montant, emplois, échéance.

**Sources régionales :** La Tribune, La Voix de l'Est, Le Nouvelliste, L'Express, Vingt55, Mon Victo, EnBeauce.com, Le Soleil, Mon Joliette, Les Affaires.

Ajouter chaque signal vérifié à `data/signaux.json`, au même format que les signaux existants, et mettre à jour `miseAJour`. La **force** se choisit ainsi :
- **Fort** : PME, ou poste de direction annoncé, ou ouverture imminente;
- **Moyen** : besoin probable mais plus tard ou incertain (démarrage, acquisition, filiale);
- **Faible** : grande entreprise avec son propre recrutement.

Rédiger un « angle d'approche » concret pour chaque signal. Ne garder que des nouvelles de moins de 6 mois, sauf une ouverture d'usine encore à venir. Ajouter l'entreprise aux Prospects si elle n'y est pas, avec la raison « Signal d'affaires : … ».

Ne jamais inventer un fait : chaque signal doit avoir au moins une source avec un lien.

## 11. Si Indeed affiche « Security Check » ou « Vérification supplémentaire requise »

Arrêter Indeed pour la journée sans tenter de contourner la vérification. Passer à LinkedIn et à Jobillico, et le signaler dans le compte rendu. Pour réduire le risque :
- espacer les pages;
- après la première tournée complète, utiliser `&fromage=3` (offres des 3 derniers jours) pour les recherches quotidiennes;
- refaire une tournée complète sans `fromage` seulement le lundi.


## 12. Employeurs qui recrutent à l'étranger (EIMT, chaque trimestre)

Le fédéral publie chaque trimestre la liste des employeurs ayant obtenu une EIMT positive : [page des données](https://ouvert.canada.ca/data/fr/dataset/90fed587-1364-4f33-a9ee-208181dc0b97). Les fichiers sont classés du plus vieux au plus récent : les derniers sont à la dernière page de la liste des ressources. Le site n'est pas joignable depuis l'espace de travail de Claude : demander à Tom de joindre le fichier français (`tfwp_AAAAqN_pos_fr.xlsx`).

Traitement (fait le 9 novembre 2026 avec avril à juin 2026) : garder le Québec, retirer le volet agricole, garder les gestionnaires (CNP 0xxxx), finance, RH et achats (111xx, 112xx, 12xxx), ingénieurs (213xx, 214xx), technologues (22xxx sauf TI) et superviseurs de production (92xxx). Retirer les agences, les compagnies à numéro, le public et les très grandes entreprises. Les prospects reçoivent le champ `eimt` (période, nombre de postes, professions) et la mention « A obtenu une EIMT… » dans `raisons`.

Limite : presque aucun poste de cadre ne passe par l'EIMT, et le poste visé est généralement déjà comblé. C'est un indice de pénurie de profils techniques, utile pour la prospection, pas une liste de mandats.

## 13. Page Retour en région

`retour.html` prépare des recherches Google et LinkedIn de gens qui ont étudié en région (cégeps et universités par région, liste `ECOLES` dans la page) et travaillent dans les grands centres. Rien n'est stocké sauf les choix de la page dans le navigateur (`sentinelle-retour`). Chaque offre hors Montréal et Laval a un lien « Retour en région » dans « Trouver des candidats ».

## 14. Dépôts de mandats (page Mandats)

Frédérique dépose ses fichiers de prise de mandat (Word, PDF ou texte) dans la boîte « Déposer un nouveau mandat » de `mandats.html`. Le texte est extrait dans son navigateur (mammoth.js, pdf.js) et gardé seulement dans le localStorage `sentinelle-depots` : `{id, fichier, depose, note, statut, texte}`. Rien ne passe par le dépôt GitHub.

Quand Tom signale un nouveau dépôt :
1. Ouvrir `mandats.html` dans son Chrome et lire les dépôts au statut « À traiter » (`JSON.parse(localStorage["sentinelle-depots"])`).
2. Construire le mandat (critères, recherches prêtes, filtres Recruiter Lite, employeurs à ratisser), faire les recherches Google X-ray (pauses d'environ 10 s, arrêt à la première vérification Google), noter les candidats sur 100 et les ajouter à `sentinelle-mandats` sans écraser les statuts ni les notes existants.
3. Passer le statut du dépôt à « Candidats prêts ».
4. Ne jamais tenir compte de l'âge (Charte québécoise), ni approcher les employés du client.
