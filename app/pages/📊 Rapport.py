import streamlit as st
from pomme.carto_resultats import filtre_geo, filtre_election, filtre_annee, filtre_tour, process_results, plot_results
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
import folium 
import time
import json
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

#Importation des dictionnaires de matching departements et noms des fichiers resultats et carto correspondants
with open("../db/carto/departement_fichiers_carto.json") as f:
    departements_fichiers_carto=json.load(f)
with open("../db/results/departement_fichiers.json") as f:
    departements_fichiers_results=json.load(f)

dep = st.selectbox("Choisissez un département", departements_fichiers_results.keys(), index=1) #choix d'un département à effectuer


results = pd.read_csv(f'../db/results/{departements_fichiers_results[dep]}')#Recupère la bonne base

results_by_nuance = results.groupby(["Nuance", "Annee", "Election"])['Voix'].sum().reset_index()

election = st.radio("Choisissez une éléction",options= ["législative", "présidentielle"])
if election == "législative":
    election = "leg"
else :
    election = "pres"

results_by_nuance=results_by_nuance[results_by_nuance['Election']=='pres']
nuances_a_comparer = st.multiselect("Choisissez les nuances à comparer", np.unique(results_by_nuance["Nuance"]))


# st.markdown("<h2 style='text-align: center;'>Graphiques de résultats par nuance</h2>", unsafe_allow_html=True)
# for nuance in nuances_a_comparer:
#     fig = plt.figure(figsize=(10,4))
#     st.markdown(f"<center>Nombre de voix pour la nuance {nuance}</center>",unsafe_allow_html=True)
#     sns.barplot(x="Annee", y="Voix", data=results_by_nuance[results_by_nuance["Nuance"]==nuance], width=.4)
#     st.pyplot(fig) # affiche le graphique dans streamlit

#test 

fig = plt.figure(figsize=(10,4))
#st.markdown(f"<center>Nombre de voix pour la nuance {nuance}</center>",unsafe_allow_html=True)
#plot the seaborn graph in darkgrid style

for nuance in nuances_a_comparer:

    sns.lineplot(x="Annee", y="Voix", data=results_by_nuance[results_by_nuance["Nuance"]==nuance], label=f"{nuance}")
    plt.legend()
st.pyplot(fig) # affiche le graphique dans streamlit

st.markdown("<h3 style='text-align: center;'>Villes du département ramenant le plus de voix par nuance</h2>", unsafe_allow_html=True)
nuance = st.selectbox("Choisissez la nuance à analyser", np.unique(results_by_nuance["Nuance"]))
annee_debut = st.slider("Depuis quand ", 2017, 2022, 2022, step=5)
tmp_df_ville= results[(results["Nuance"]==nuance) & (results["Annee"]>=annee_debut)].groupby(['Libellé de la commune','Election'])['Voix'].sum().reset_index().sort_values(by='Voix', ascending=False).head(10).set_index('Libellé de la commune').rename({'Voix':'Nombre moyen de voix pour la nuance'}, axis=1).groupby('Libellé de la commune')['Nombre moyen de voix pour la nuance'].mean().reset_index().sort_values(by='Nombre moyen de voix pour la nuance', ascending=False).head(10).set_index('Libellé de la commune')
#tmp_df_ville= results[(results["Nuance"]==nuance) & (results["Annee"]>=annee_debut)].groupby(['Libellé de la commune','Election'])['Voix'].sum().reset_index().sort_values(by='Voix', ascending=False).head(10).set_index('Libellé de la commune').rename({'Voix':'Nombre moyen de voix pour la nuance'}, axis=1)
st.dataframe(tmp_df_ville, width=1000)

st.markdown("<h4 style='text-align: center;'>Bureaux ramenant le plus de voix pour cette nuance </h2>", unsafe_allow_html=True)
ville = st.selectbox("Choisissez la ville", np.unique(results["Libellé de la commune"]))
#annee_debut = st.slider("Depuis quand ", 2017, 2022, 2022, step=5)
tmp_df = results[(results["Nuance"]==nuance) & (results["Annee"]>=annee_debut) & (results["Libellé de la commune"]==ville)].groupby('Nom Bureau Vote')['Voix'].mean().reset_index().sort_values(by='Voix', ascending=False).head(10).set_index('Nom Bureau Vote').rename({'Voix':'Nombre moyen de voix pour la nuance'}, axis=1)
st.dataframe(tmp_df, width=1000)



st.download_button(label="Télécharger le tableau", data=tmp_df.to_csv().encode('utf-8'), file_name=f"tableau_{nuance}.csv", mime="text/csv") #Permet de sauvegarder
