"""Génère un jeu de données de ventes réaliste pour les démos.

Le fichier produit (`donnees/ventes.csv`) couvre 12 mois de ventes d'une
boutique fictive, avec quelques défauts volontaires (doublons, valeurs
manquantes) pour montrer le nettoyage.
"""

import random
from datetime import date, timedelta
from pathlib import Path

# Graine fixe pour que le jeu de données soit toujours identique
random.seed(42)

CATALOGUE = {
    "Épicerie": [("Café arabica 250g", 8.90), ("Thé vert bio 100g", 6.50),
                 ("Chocolat noir 70% 200g", 4.20), ("Miel d'acacia 500g", 9.80)],
    "Boissons": [("Jus d'orange 1L", 2.90), ("Limonade artisanale 75cl", 3.40),
                 ("Sirop de grenadine 75cl", 4.90)],
    "Maison": [("Bougie parfumée", 12.90), ("Savon de Marseille", 3.80),
               ("Torchon en lin", 7.50)],
    "Beauté": [("Crème hydratante 50ml", 14.90), ("Huile d'argan 100ml", 11.50)],
}

REGIONS = ["Île-de-France", "Auvergne-Rhône-Alpes", "Nouvelle-Aquitaine",
           "Occitanie", "Hauts-de-France", "Provence-Alpes-Côte d'Azur",
           "Bretagne", "Grand Est"]

DEBUT = date(2025, 1, 1)


def generer(nb_lignes: int = 1500) -> list[dict]:
    """Construit la liste des lignes de vente."""
    lignes = []
    for i in range(1, nb_lignes + 1):
        categorie = random.choice(list(CATALOGUE.keys()))
        produit, prix = random.choice(CATALOGUE[categorie])
        jour = DEBUT + timedelta(days=random.randint(0, 364))
        # Pic d'activité en fin d'année
        quantite = random.randint(1, 6) + (2 if jour.month in (11, 12) else 0)
        lignes.append({
            "commande_id": f"CMD-{i:05d}",
            "date": jour.isoformat(),
            "produit": produit,
            "categorie": categorie,
            "region": random.choice(REGIONS),
            "quantite": quantite,
            "prix_unitaire": prix,
        })
    # Quelques doublons volontaires
    lignes += random.sample(lignes, 25)
    # Quelques valeurs manquantes volontaires
    for ligne in random.sample(lignes, 20):
        ligne["quantite"] = ""
    random.shuffle(lignes)
    return lignes


def main() -> None:
    lignes = generer()
    colonnes = ["commande_id", "date", "produit", "categorie",
                "region", "quantite", "prix_unitaire"]
    sortie = Path(__file__).resolve().parent / "donnees" / "ventes.csv"
    sortie.parent.mkdir(exist_ok=True)
    with sortie.open("w", encoding="utf-8") as f:
        f.write(";".join(colonnes) + "\n")
        for ligne in lignes:
            f.write(";".join(str(ligne[c]) for c in colonnes) + "\n")
    print(f"{len(lignes)} lignes écrites dans {sortie}")


if __name__ == "__main__":
    main()
