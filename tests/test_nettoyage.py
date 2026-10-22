"""Tests du nettoyage des données."""

import pandas as pd
import pytest

from ventes.nettoyage import nettoyer


@pytest.fixture
def ventes_sales():
    return pd.DataFrame([
        {"commande_id": "CMD-1", "date": "2025-03-01", "produit": "Café",
         "categorie": "Épicerie", "region": "Bretagne", "quantite": 2,
         "prix_unitaire": 8.9},
        # doublon exact du précédent
        {"commande_id": "CMD-1", "date": "2025-03-01", "produit": "Café",
         "categorie": "Épicerie", "region": "Bretagne", "quantite": 2,
         "prix_unitaire": 8.9},
        # quantité manquante
        {"commande_id": "CMD-2", "date": "2025-03-02", "produit": "Thé",
         "categorie": "Épicerie", "region": "Bretagne", "quantite": None,
         "prix_unitaire": 6.5},
        # date illisible
        {"commande_id": "CMD-3", "date": "pas une date", "produit": "Thé",
         "categorie": "Épicerie", "region": "Bretagne", "quantite": 1,
         "prix_unitaire": 6.5},
        # quantité négative
        {"commande_id": "CMD-4", "date": "2025-03-03", "produit": "Savon",
         "categorie": "Maison", "region": "Bretagne", "quantite": -1,
         "prix_unitaire": 3.8},
        {"commande_id": "CMD-5", "date": "2025-03-04", "produit": "Savon",
         "categorie": "Maison", "region": "Bretagne", "quantite": 3,
         "prix_unitaire": 3.8},
    ])


def test_nettoyer_supprime_doublons(ventes_sales):
    propre, rapport = nettoyer(ventes_sales)
    assert rapport["doublons_supprimes"] == 1
    assert len(propre) == 2


def test_nettoyer_ecarte_lignes_invalides(ventes_sales):
    propre, rapport = nettoyer(ventes_sales)
    assert rapport["lignes_ecartees"] == 4
    assert set(propre["commande_id"]) == {"CMD-1", "CMD-5"}


def test_nettoyer_calcule_montant(ventes_sales):
    propre, _ = nettoyer(ventes_sales)
    ligne = propre[propre["commande_id"] == "CMD-1"].iloc[0]
    assert ligne["montant"] == pytest.approx(17.8)


def test_nettoyer_trie_par_date(ventes_sales):
    propre, _ = nettoyer(ventes_sales)
    assert propre["date"].is_monotonic_increasing
