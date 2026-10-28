# Sentinelle

Tableau de veille des offres d'emploi récentes (60 derniers jours; affichage par défaut : 7 à 60 jours), regroupées par entreprise, avec coordonnées publiques et suivi.

- `index.html` : l'application (une seule page, aucune dépendance à installer).
- `data/offres.json` : les offres et les coordonnées, mis à jour après chaque tournée.

Les notes et statuts de suivi sont gardés dans le navigateur de la personne qui les écrit. Le bouton « Sauvegarder mes notes » permet d'en garder une copie et de les transférer sur un autre appareil.

## Format de `data/offres.json`

```json
{
  "tournee": { "date": "2026-10-28T08:30:00-04:00", "regions": "Montréal, Laval", "domaines": ["Génie mécanique"] },
  "entreprises": {
    "slug-entreprise": { "nom": "", "siteWeb": "", "pageCarrieres": "", "telephone": "", "courriel": "", "adresse": "", "linkedinUrl": "" }
  },
  "offres": [
    { "id": "linkedin-job-id", "titre": "", "entreprise": "", "lieu": "", "region": "", "domaine": "", "modalite": "", "publieLe": "ISO 8601", "urlOffre": "", "sources": [{ "nom": "LinkedIn", "url": "" }, { "nom": "Jobillico", "url": "" }], "recruteur": { "nom": "", "titre": "", "profilUrl": "" } }
  ]
}
```

## Pages carrières et sites surveillés

`data/surveillance.json` contient :
- `sitesEmploi` : les sites d'emploi consultés à chaque tournée, et s'ils exigent une session ouverte ;
- `pagesCarrieres` : les pages carrières vérifiées directement à chaque tournée.

## Prospects

`prospects.html` est un outil séparé : les entreprises entre Montréal et Québec (de Sorel-Tracy et Saint-Hyacinthe à Stanstead, jusqu'à Shawinigan), classées selon leur probabilité de faire appel à une firme de recrutement (Fort probable, Probable, Mandats de cadres, Peu probable). Les données sont dans `data/prospects.json`; la méthode de pointage est expliquée dans la page. Le suivi (statut et notes) est gardé dans le navigateur.

## Tournées automatiques

- `outils/TOURNEE.md` : la marche à suivre de la tournée du matin (sources, villes, extraction, offres terminées).
- `outils/tournee.py` : ajoute les nouvelles offres à `data/offres.json` et gère les offres terminées.
- `outils/decouvrir.py` : ajoute aux Prospects les employeurs trouvés dans les offres.
- `outils/commun.py` : régions et villes, agences exclues, classement par domaine.
