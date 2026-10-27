# Sentinelle

Tableau de veille des offres d'emploi LinkedIn récentes (72 dernières heures), regroupées par entreprise, avec coordonnées publiques et suivi.

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

## Pages carrières surveillées

`data/surveillance.json` contient :
- `pagesCarrieres` : les pages carrières vérifiées directement à chaque tournée ;
- `entreprises` : 200 employeurs de l'Estrie, de la Mauricie et du Centre-du-Québec susceptibles de recruter (onglet « Entreprises surveillées »), avec la raison de leur présence dans la liste.
