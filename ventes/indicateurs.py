"""Calcul des indicateurs clés à partir des ventes nettoyées."""

import pandas as pd


def chiffre_affaires(df: pd.DataFrame) -> float:
    """Chiffre d'affaires total."""
    return float(df["montant"].sum())


def panier_moyen(df: pd.DataFrame) -> float:
    """Montant moyen par commande."""
    if df["commande_id"].nunique() == 0:
        return 0.0
    return float(df["montant"].sum() / df["commande_id"].nunique())


def ca_par_mois(df: pd.DataFrame) -> pd.Series:
    """Chiffre d'affaires regroupé par mois (format 'YYYY-MM')."""
    mois = df["date"].dt.to_period("M").astype(str)
    return df.groupby(mois)["montant"].sum().sort_index()


def ca_par_categorie(df: pd.DataFrame) -> pd.Series:
    """Chiffre d'affaires par catégorie, trié décroissant."""
    return df.groupby("categorie")["montant"].sum().sort_values(ascending=False)


def ca_par_region(df: pd.DataFrame) -> pd.Series:
    """Chiffre d'affaires par région, trié décroissant."""
    return df.groupby("region")["montant"].sum().sort_values(ascending=False)


def top_produits(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Les n produits les plus vendus en chiffre d'affaires."""
    top = (df.groupby("produit")["montant"].sum()
             .sort_values(ascending=False).head(n)
             .reset_index())
    top.columns = ["produit", "chiffre_affaires"]
    return top


def resume(df: pd.DataFrame) -> dict:
    """Synthèse des indicateurs principaux dans un dictionnaire."""
    return {
        "chiffre_affaires": round(chiffre_affaires(df), 2),
        "panier_moyen": round(panier_moyen(df), 2),
        "nb_commandes": int(df["commande_id"].nunique()),
        "nb_produits": int(df["produit"].nunique()),
        "periode": (df["date"].min().strftime("%d/%m/%Y"),
                    df["date"].max().strftime("%d/%m/%Y")),
    }
