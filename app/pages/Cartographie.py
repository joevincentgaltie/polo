import streamlit as st
from pomme.carto_resultats import filtre_geo, filtre_election, filtre_annee, filtre_tour, process_results, plot_results
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
import folium 
import time
import json
import numpy as np


#Load dictionary with paths for carto and results
with open("../db/carto/departement_fichiers_carto.json") as f:
    departements_fichiers_carto=json.load(f)
with open("../db/results/departement_fichiers.json") as f:
    departements_fichiers_results=json.load(f)
with open("../db/results/villes_par_dep.json") as f:
    villes_par_dep=json.load(f)

st.title("Popol")
st.markdown("## Cartographie des résultats des élections à l'échelle départementale")
dep = st.selectbox("Choisissez un département", departements_fichiers_results.keys(), index=1)

gdf = gpd.read_file(f"../db/carto/{departements_fichiers_carto[dep]}",crs="epsg:4326")

results = pd.read_csv(f'../db/results/{departements_fichiers_results[dep]}')
election = st.radio("Choisissez une éléction",options= ["législative", "présidentielle"])
tour = st.radio("Choisissez un tour",options= ["1", "2"])
if election == "législative":
    annee = st.slider("Choisissez une année", 2017, 2022, 2022, step=5)
else :
    annee = st.slider("Choisissez une année", 2012, 2022, 2012, step=5)
type_election = {"présidentielle" : "pres", "législative" : "leg"}

params= {
    "filtre_geo_cat" : "dep",
    "filtre_geo_val" : dep,
    "filtre_election_val" : type_election[election],
    "filtre_annee_val" : int(annee),
    "filtre_tour_val" : int(tour), 
    "Nuance": "CENTRE-DROIT"}

resultat_elections_cible = process_results(params, results, gdf)
nuance = st.selectbox("Choisissez une nuance", np.unique(resultat_elections_cible["Nuance"]) )

params= {
    "filtre_geo_cat" : "dep",
    "filtre_geo_val" : dep,
    "filtre_election_val" : type_election[election],
    "filtre_annee_val" : int(annee),
    "filtre_tour_val" : int(tour), 
    "Nuance": nuance}
#ville = st.selectbox("Choisissez une ville", villes_par_dep[dep])
st.write("### Cartographie des résultats des élections")


#beginn streamlit 

# # allow choice of paremeters
# st.write("# Quel département souhaitez vous afficher ?")
# dep = st.selectbox("Choisissez un département", ["94","93","92"])
# params["filtre_geo_val"] = dep
col1, col2, col3, col4 = st.columns(4)
col1.metric("Nombre de bureaux de vote", f"{resultat_elections_cible['id_bv'].nunique()}", "bureaux de vote")
col2.metric("Nombre total de voix ", f"{int(resultat_elections_cible[resultat_elections_cible.Nuance==params['Nuance']]['Voix'].sum())}", "pour la nuance")
col3.metric("% d'abstention", f"{int((resultat_elections_cible['Abstentions'].sum()/resultat_elections_cible['Inscrits'].sum())*100)}")
col4.metric("% votes ", f"{int(((resultat_elections_cible[resultat_elections_cible.Nuance==params['Nuance']]['Voix'].sum()/resultat_elections_cible['Voix'].sum())*100))}", "pour la nuance")
tmp_to_plot = process_results(params, results, gdf)
m = plot_results(tmp_to_plot, params)
tableau_voix = tmp_to_plot[['Voix',"Nuance"]].groupby("Nuance").sum().sort_values("Voix",ascending=False)
tableau_voix["%"]= tableau_voix['Voix'].apply(lambda x : round(x/tmp_to_plot['Voix'].sum()*100))

st_data = st_folium(m, width=725)
st.markdown("### Récapitulatif des résultats par nuance")

st.dataframe(tableau_voix, use_container_width=True)

st.markdown("## Focus à l'échelle municipale")
villes = tmp_to_plot["Libellé de la commune"].unique()
ville = st.selectbox("Choisissez une ville", villes)
tmp_to_plot_ville = tmp_to_plot[tmp_to_plot["Libellé de la commune"]==ville]
m = plot_results(tmp_to_plot_ville, params)
col11, col21, col31, col41 = st.columns(4)
col11.metric("Nombre de bureaux de vote", f"{tmp_to_plot_ville['id_bv'].nunique()}", "bureaux de vote")
col21.metric("Nombre total de voix ", f"{int(tmp_to_plot_ville[tmp_to_plot_ville.Nuance==params['Nuance']]['Voix'].sum())}", "pour la nuance")
col31.metric("% d'abstention", f"{int((tmp_to_plot_ville['Abstentions'].sum()/tmp_to_plot_ville['Inscrits'].sum())*100)}")
col41.metric("% votes ", f"{int(((tmp_to_plot_ville[tmp_to_plot_ville.Nuance==params['Nuance']]['Voix'].sum()/tmp_to_plot_ville['Voix'].sum())*100))}", "pour la nuance")
st_data_ville = st_folium(m, width=725)
tableau_voix_ville = tmp_to_plot_ville[['Voix',"Nuance"]].groupby("Nuance").sum().sort_values("Voix",ascending=False)
tableau_voix_ville["%"]= tableau_voix_ville['Voix'].apply(lambda x : round(x/tmp_to_plot_ville['Voix'].sum()*100))
st.markdown("### Récapitulatif des résultats par nuance")

st.dataframe(tableau_voix_ville, use_container_width=True)


