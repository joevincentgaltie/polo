import pandas as pd 

def filter_liste_electorale(code_insee_commmune : int, base : pd.DataFrame) : 
    """_summary_

    Args:
        code_insee_commmune (int): code insee de la commune que l'on veut afficher 
        base (pd.DataFrame): base table-adresses-reu.csv

    Returns:
        _type_: dataframe
    """
    return base[base.code_commune_ref == code_insee_commmune]

def points_to_poly(x, voronois):
    """
    Args:
        x (shapely.geometry.point.Point): point
        voronois (gpd.GeoDataFrame): dataframe avec une colonne geometry
        
    Returns:
        _type_: shapely.geometry.polygon.Polygon
        """
    for i in range(voronois.shape[0]):
        if x.within(voronois.loc[i,'geometry']) == True:
            return voronois.loc[i,'geometry']

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
        return df[df["Code Postal"]==valeur_filtre]

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