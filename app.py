"""Tableau de bord d'analyse des ventes (Streamlit)."""

import streamlit as st
import pandas as pd

from ventes.nettoyage import charger_csv, nettoyer
from ventes import indicateurs as ind
from ventes import graphiques as g

st.set_page_config(page_title="AnalyseVentes", layout="wide")
st.title("Analyse des ventes")

# Chargement des données : fichier téléversé ou jeu d'exemple
fichier = st.sidebar.file_uploader("Fichier CSV de ventes", type="csv")
if fichier is not None:
    brut = pd.read_csv(fichier, sep=";")
    st.sidebar.success("Fichier chargé, nettoyage appliqué.")
else:
    st.sidebar.info("Jeu de données d'exemple utilisé.")
    brut = charger_csv("donnees/ventes.csv")

df, rapport = nettoyer(brut)
st.sidebar.write(
    f"{rapport['lignes_ecartees']} lignes écartées au nettoyage "
    f"({rapport['doublons_supprimes']} doublons)."
)

# Filtres
st.sidebar.header("Filtres")
regions = st.sidebar.multiselect("Régions", sorted(df["region"].unique()),
                                 default=sorted(df["region"].unique()))
categories = st.sidebar.multiselect("Catégories", sorted(df["categorie"].unique()),
                                    default=sorted(df["categorie"].unique()))
date_min, date_max = df["date"].min().date(), df["date"].max().date()
debut, fin = st.sidebar.date_input("Période", value=(date_min, date_max))

filtre = df[df["region"].isin(regions) & df["categorie"].isin(categories)]
filtre = filtre[(filtre["date"].dt.date >= debut) & (filtre["date"].dt.date <= fin)]

if filtre.empty:
    st.warning("Aucune vente ne correspond aux filtres choisis.")
    st.stop()

# Indicateurs clés
synthese = ind.resume(filtre)
col1, col2, col3, col4 = st.columns(4)
col1.metric("Chiffre d'affaires", f"{synthese['chiffre_affaires']:,.0f} €".replace(",", " "))
col2.metric("Panier moyen", f"{synthese['panier_moyen']:.2f} €")
col3.metric("Commandes", synthese["nb_commandes"])
col4.metric("Produits", synthese["nb_produits"])

# Graphiques
st.subheader("Évolution mensuelle")
st.pyplot(g.courbe_ca_mensuel(ind.ca_par_mois(filtre)))

col_g1, col_g2 = st.columns(2)
with col_g1:
    st.subheader("CA par catégorie")
    st.pyplot(g.barres_categories(ind.ca_par_categorie(filtre)))
with col_g2:
    st.subheader("CA par région")
    st.pyplot(g.camembert_regions(ind.ca_par_region(filtre)))

st.subheader("Top produits")
top = ind.top_produits(filtre)
st.pyplot(g.barres_top_produits(top))
st.dataframe(top, use_container_width=True)

# Export des données nettoyées
st.download_button("Télécharger les données nettoyées (CSV)",
                   filtre.to_csv(index=False, sep=";").encode("utf-8"),
                   file_name="ventes_nettoyees.csv", mime="text/csv")
