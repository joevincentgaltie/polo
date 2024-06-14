import pandas as pd
import geopandas as gpd
import streamlit as st  

def filtre_geo(df:pd.DataFrame, cat_filtre : str, valeur_filtre : str) -> pd.DataFrame : 
    """_summary_

    Args:
        df (pd.DataFrame): dataframe avec une colonne Code Postal 
        cat_filtre (str): peut prendre la valeur "dep" ou "ville"
        valeur_filtre (str): si cat_filtre = "dep" : valeur_filtre prend le code du département (ex : 75); si cat_filtre = "ville" : valeur_filtre prend le code postal de la ville (ex : 75001)

    Returns:
        pd.DataFrame: dataframe filtré
    """
    if cat_filtre == "dep":
        return df[df["Code du département"]==int(valeur_filtre)]
    elif cat_filtre == "ville":
        return df[df["Libellé de la commune"]==valeur_filtre]

def filtre_election(df : pd.DataFrame, election : str) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): dataframe avec une colonne Election
        election (str): peut prendre la valeur "pres" ou "leg"

    Returns:
        pd.DataFrame: dataframe filtré
    
    """
    return df[df.Election == election]

def filtre_annee(df : pd.DataFrame, annee : int) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): dataframe avec une colonne Election
        annee(int): peut prendre la valeur 2017 ou 2022 ou 2012

    Returns:
        pd.DataFrame: dataframe filtré
    
    """
    return df[df.Annee == annee]

def filtre_tour(df : pd.DataFrame, tour : int) -> pd.DataFrame:
    """
    Args:
        df (pd.DataFrame): dataframe avec une colonne Election
        tour(int): peut prendre la valeur 1 ou 2

    Returns:
        pd.DataFrame: dataframe filtré
    
    """
    return df[df.Tour == tour]


#functions that takes params, results, and gdf and returns a gdf with the results merged
def process_results(params : dict, results : pd.DataFrame, gdf : gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """_summary_

    Args:
        params (dict): dictionnaire avec les paramètres de filtrage, 
        results (pd.DataFrame): dataframe avec les résultats des élections
        gdf (gpd.GeoDataFrame): dataframe avec les contours des bureaux de vote

    Returns:
        gpd.GeoDataFrame: dataframe avec les contours des bureaux de vote et les résultats des élections
    """
    tmp_results = filtre_geo(results, params["filtre_geo_cat"], params["filtre_geo_val"])
    tmp_results = filtre_election(tmp_results, params["filtre_election_val"])
    tmp_results = filtre_annee(tmp_results, params["filtre_annee_val"])
    tmp_results = filtre_tour(tmp_results, params["filtre_tour_val"])

    tmp_to_plot = gdf.merge(tmp_results, on='id_bv', how='inner')

    tmp_to_plot= pd.merge(tmp_to_plot, tmp_to_plot.groupby(['id_bv','Nuance'])['Voix'].sum().reset_index().rename({'Voix':'Voix_nuance'}, axis=1), on =['id_bv','Nuance'])
  

    tmp_to_plot['% Voix/Exp_nuance'] = tmp_to_plot['Voix_nuance']/tmp_to_plot['Exprimés']
    tmp_to_plot['% Voix/Ins_nuance'] = tmp_to_plot['Voix_nuance']/tmp_to_plot['Inscrits']
    return tmp_to_plot

def plot_results(tmp_to_plot, params):
    """Plot the map with the given parameters

    Args:
        tmp_to_plot (geopandas dataframe): dataframe with the results to plot
        params (dict): dictionnary with the parameters
    
    Returns:
        m (folium map): map with the results
    """
    tmp_to_plot = gpd.GeoDataFrame(tmp_to_plot, crs="EPSG:4326", geometry="geometry")
    m = tmp_to_plot[tmp_to_plot.Nuance==params['Nuance']].explore(column='% Voix/Exp_nuance', legend=True, tooltip=False,popup=['Adresse','Nom Bureau Vote','% Voix/Exp_nuance'], cmap='OrRd', tiles="CartoDB dark_matter")
    return m

def extract_villes(results: pd.DataFrame, dep: str):
    """Extrait les villes du département"""
    villes = list(results[results["dep"] == dep]["ville"].unique())
    return villes