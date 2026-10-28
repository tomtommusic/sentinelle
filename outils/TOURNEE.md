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
- **Territoire :** Estrie, Centre-du-Québec, Mauricie, Lanaudière, Montérégie, Chaudière-Appalaches, Laurentides, Québec (Capitale-Nationale), Montréal et Laval. La liste des villes par région est dans `outils/commun.py`.
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
| Vendredi | Montréal |

**Termes**, sous la forme « terme à Ville » (rayon de 80 km automatique) : `ingénieur mécanique`, `ingénieur de projets`, `contrôleur financier`, `directeur ressources humaines`, `vice-président`. Il faut ajuster pour rester sous 12 pages.

Saint-Georges et Saint-Jérôme sont mal reconnues par LinkedIn : on les fait seulement par Indeed.

**Adresse de recherche** :

```
https://www.linkedin.com/jobs/search-results/?keywords=<terme à Ville encodé>&f_TPR=r5184000
```

**Extraction.** On calcule d'abord, en retournant seulement le nombre d'offres :

```js
await new Promise(r=>setTimeout(r,2500));let sc=document.querySelector('[componentkey^="job-card-component-ref-"]');while(sc&&sc!==document.body){const s=getComputedStyle(sc);if(/(auto|scroll)/.test(s.overflowY)&&sc.scrollHeight>sc.clientHeight+20)break;sc=sc.parentElement;}for(let i=0;i<8;i++){if(sc&&sc!==document.body)sc.scrollTop=sc.scrollHeight;await new Promise(r=>setTimeout(r,450));}const V=/ \(offre d’emploi vérifiée\)$/;window.__r=[...document.querySelectorAll('[componentkey^="job-card-component-ref-"]')].map(d=>{const id=d.getAttribute('componentkey').replace('job-card-component-ref-','');let l=d.innerText.split('\n').map(s=>s.trim()).filter(Boolean);if(V.test(l[0]))l=l.slice(1);if(l[1]===l[0])l=l.slice(1);const pub=(l.find(x=>/^Publication /.test(x))||'').replace(/^Publication il y a /,'');return [id,l[0].slice(0,60),l[1],(l[2]||'').replace(/ \(.*\)$/,'').replace(/, QC$/,''),pub].join('¦')});'n='+window.__r.length
```

On lit ensuite les tranches `slice(0,8)`, `slice(8,16)` et `slice(16,25)`.

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
- une offre qui n'est plus vue depuis 14 jours devient « terminée »;
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
