# AnalyseVentes

Tableau de bord d'analyse de ventes en Python : nettoyage automatique des
données, calcul d'indicateurs clés (chiffre d'affaires, panier moyen, top
produits…) et graphiques, avec une interface web interactive.

Chargez votre propre fichier CSV ou utilisez le jeu de données d'exemple
fourni (12 mois de ventes d'une boutique fictive).

## Fonctionnalités

- **Nettoyage** : suppression des doublons, gestion des valeurs manquantes et
  des dates illisibles, calcul du montant par ligne, avec rapport de nettoyage.
- **Indicateurs** : chiffre d'affaires, panier moyen, CA par mois / catégorie /
  région, top produits.
- **Tableau de bord Streamlit** : filtres par région, catégorie et période,
  graphiques matplotlib, export CSV des données nettoyées.
- **Générateur de données** : `generer_donnees.py` produit un CSV réaliste
  pour les démos.

## Stack

Python 3.12, pandas, matplotlib, Streamlit, Docker, pytest, GitHub Actions.

## Installation

```bash
pip install -r requirements.txt
```

## Utilisation

Lancer le tableau de bord :

```bash
streamlit run app.py
```

Puis ouvrir http://localhost:8501. Le tableau de bord utilise le jeu
d'exemple (`donnees/ventes.csv`) par défaut ; vous pouvez téléverser votre
propre CSV (mêmes colonnes, séparateur `;`) depuis la barre latérale.

Régénérer les données d'exemple :

```bash
python generer_donnees.py
```

### Avec Docker

```bash
docker build -t analyse-ventes .
docker run -p 8501:8501 analyse-ventes
```

## Structure du projet

```
AnalyseVentes/
├── app.py                  # tableau de bord Streamlit
├── generer_donnees.py      # génération du jeu de données d'exemple
├── donnees/ventes.csv      # données d'exemple (12 mois de ventes)
├── ventes/
│   ├── nettoyage.py        # chargement + nettoyage des données
│   ├── indicateurs.py      # calcul des indicateurs clés
│   └── graphiques.py       # graphiques matplotlib
├── tests/                  # tests pytest
├── Dockerfile
└── .github/workflows/ci.yml
```

## Tests

```bash
pytest
```

## Licence

MIT — voir le fichier [LICENSE](LICENSE).
