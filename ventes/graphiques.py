"""Graphiques matplotlib pour l'analyse des ventes."""

import matplotlib
matplotlib.use("Agg")  # pas d'affichage, adapté au serveur et aux tests

import matplotlib.pyplot as plt
import pandas as pd

plt.rcParams["figure.figsize"] = (9, 5)


def courbe_ca_mensuel(ca_mois: pd.Series) -> plt.Figure:
    """Courbe d'évolution du chiffre d'affaires mois par mois."""
    fig, ax = plt.subplots()
    ax.plot(ca_mois.index, ca_mois.values, marker="o")
    ax.set_title("Chiffre d'affaires mensuel")
    ax.set_xlabel("Mois")
    ax.set_ylabel("CA (€)")
    ax.tick_params(axis="x", rotation=45)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    return fig


def barres_categories(ca_categories: pd.Series) -> plt.Figure:
    """Barres du chiffre d'affaires par catégorie."""
    fig, ax = plt.subplots()
    ax.bar(ca_categories.index, ca_categories.values)
    ax.set_title("Chiffre d'affaires par catégorie")
    ax.set_ylabel("CA (€)")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()
    return fig


def barres_top_produits(top: pd.DataFrame) -> plt.Figure:
    """Barres horizontales des produits les plus vendus."""
    fig, ax = plt.subplots()
    ax.barh(top["produit"], top["chiffre_affaires"])
    ax.set_title("Produits les plus vendus")
    ax.set_xlabel("CA (€)")
    ax.invert_yaxis()
    fig.tight_layout()
    return fig


def camembert_regions(ca_regions: pd.Series) -> plt.Figure:
    """Répartition du chiffre d'affaires par région."""
    fig, ax = plt.subplots()
    ax.pie(ca_regions.values, labels=ca_regions.index, autopct="%1.0f%%",
           startangle=90)
    ax.set_title("Répartition du CA par région")
    fig.tight_layout()
    return fig
