"""Nettoyage des données de ventes."""

import pandas as pd

COLONNES_ATTENDUES = ["commande_id", "date", "produit", "categorie",
                      "region", "quantite", "prix_unitaire"]


def charger_csv(chemin: str) -> pd.DataFrame:
    """Charge un fichier CSV de ventes (séparateur point-virgule)."""
    return pd.read_csv(chemin, sep=";")


def nettoyer(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Nettoie le DataFrame et renvoie (données propres, rapport de nettoyage).

    Étapes : suppression des doublons, conversion des dates, suppression des
    lignes avec quantité ou prix manquant/invalide, calcul du montant.
    """
    rapport = {"lignes_avant": len(df)}

    propre = df.copy()

    # Dates au format datetime (les lignes illisibles sont écartées)
    propre["date"] = pd.to_datetime(propre["date"], errors="coerce")
    propre = propre.dropna(subset=["date"])

    # Quantités et prix numériques
    propre["quantite"] = pd.to_numeric(propre["quantite"], errors="coerce")
    propre["prix_unitaire"] = pd.to_numeric(propre["prix_unitaire"], errors="coerce")
    propre = propre.dropna(subset=["quantite", "prix_unitaire"])
    propre = propre[(propre["quantite"] > 0) & (propre["prix_unitaire"] > 0)]

    # Doublons (même commande, même produit, même date)
    doublons = int(propre.duplicated(
        subset=["commande_id", "date", "produit"]).sum())
    propre = propre.drop_duplicates(subset=["commande_id", "date", "produit"])

    # Montant de chaque ligne
    propre["montant"] = propre["quantite"] * propre["prix_unitaire"]
    propre = propre.sort_values("date").reset_index(drop=True)

    rapport["doublons_supprimes"] = doublons
    rapport["lignes_apres"] = len(propre)
    rapport["lignes_ecartees"] = rapport["lignes_avant"] - len(propre)
    return propre, rapport
