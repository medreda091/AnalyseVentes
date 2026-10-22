"""Tests des indicateurs et des graphiques."""

import matplotlib.pyplot as plt
import pandas as pd
import pytest

from ventes import graphiques as g
from ventes import indicateurs as ind


@pytest.fixture
def ventes_propres():
    df = pd.DataFrame([
        {"commande_id": "CMD-1", "date": "2025-01-10", "produit": "Café",
         "categorie": "Épicerie", "region": "Bretagne", "quantite": 2,
         "prix_unitaire": 10.0, "montant": 20.0},
        {"commande_id": "CMD-1", "date": "2025-01-10", "produit": "Thé",
         "categorie": "Épicerie", "region": "Bretagne", "quantite": 1,
         "prix_unitaire": 6.0, "montant": 6.0},
        {"commande_id": "CMD-2", "date": "2025-02-05", "produit": "Savon",
         "categorie": "Maison", "region": "Bretagne", "quantite": 3,
         "prix_unitaire": 4.0, "montant": 12.0},
    ])
    df["date"] = pd.to_datetime(df["date"])
    return df


def test_chiffre_affaires(ventes_propres):
    assert ind.chiffre_affaires(ventes_propres) == pytest.approx(38.0)


def test_panier_moyen(ventes_propres):
    # 38 € pour 2 commandes distinctes
    assert ind.panier_moyen(ventes_propres) == pytest.approx(19.0)


def test_ca_par_mois(ventes_propres):
    resultat = ind.ca_par_mois(ventes_propres)
    assert resultat["2025-01"] == pytest.approx(26.0)
    assert resultat["2025-02"] == pytest.approx(12.0)


def test_ca_par_categorie_trie(ventes_propres):
    resultat = ind.ca_par_categorie(ventes_propres)
    assert list(resultat.index) == ["Épicerie", "Maison"]
    assert resultat.iloc[0] == pytest.approx(26.0)


def test_top_produits(ventes_propres):
    top = ind.top_produits(ventes_propres, n=2)
    assert list(top["produit"]) == ["Café", "Savon"]
    assert top["chiffre_affaires"].iloc[0] == pytest.approx(20.0)


def test_resume(ventes_propres):
    synthese = ind.resume(ventes_propres)
    assert synthese["chiffre_affaires"] == pytest.approx(38.0)
    assert synthese["nb_commandes"] == 2
    assert synthese["nb_produits"] == 3


def test_graphiques_produisent_des_figures(ventes_propres):
    figures = [
        g.courbe_ca_mensuel(ind.ca_par_mois(ventes_propres)),
        g.barres_categories(ind.ca_par_categorie(ventes_propres)),
        g.barres_top_produits(ind.top_produits(ventes_propres)),
        g.camembert_regions(ind.ca_par_region(ventes_propres)),
    ]
    for fig in figures:
        assert isinstance(fig, plt.Figure)
        assert len(fig.axes) == 1
    plt.close("all")
