import streamlit as st
from pomme.carto_resultats import filtre_geo, filtre_election, filtre_annee, filtre_tour, process_results, plot_results
import pandas as pd
import geopandas as gpd
from streamlit_folium import st_folium, folium_static
import folium 
import time
import json

st.title(" Bienvenue !")

# Présentation de Polo
st.subheader("Mon nom est Popol et grâce à moi, même la plus obscure des mairies ne te résistera pas.")

# Lien vers la page Cartographie
st.write("Sur la page cartographie, tu trouveras les résultats par bureau de vote. Tu pourras visualiser à l'échelle des villes les résultats des nuances électorales qui t'intéressent.")

# Lien vers la page Rapport
st.write("Sur la page rapport, tu trouveras des données sur les rapports de force dans chaque ville.")

st.write("Au fait, j'utilise streamlit. C'est un outil super beaucoup trop cool (et mieux que Dash). <span style='font-family:Cambria; font-size:24px; color:green;'> et je peux même suivre une charte particulièrement moche ...</span>", unsafe_allow_html=True)


