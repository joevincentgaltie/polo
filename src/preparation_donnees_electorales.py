import pandas as pd

bv_cols = ['Code du département', 'Libellé du département',
       'Code de la circonscription', 'Libellé de la circonscription',
       'Code de la commune', 'Libellé de la commune', 'Code du b.vote',
       'Inscrits', 'Abstentions', '% Abs/Ins', 'Votants', '% Vot/Ins',
       'Blancs', '% Blancs/Ins', '% Blancs/Vot', 'Nuls', '% Nuls/Ins',
       '% Nuls/Vot', 'Exprimés', '% Exp/Ins', '% Exp/Vot']
candidat_cols_pres= [ 'N°Panneau', 'Sexe','Nom', 'Prénom', 'Voix', '% Voix/Ins', '% Voix/Exp']


candidat_cols_leg= ['N°Panneau',
            'Sexe',
            'Nom',
            'Prénom',
            'Nuance',
            'Voix',
            '% Voix/Ins',
            '% Voix/Exp']




def preparation_donnees_electorales_brutes(tableau_donnees_brutes : pd.DataFrame, tour : int, cat_elec : str, annee : int) -> pd.DataFrame :
    """"Prend en entrée la donnée éléctorale brute et ressort un tableau de données nettoyées et prêtes à être utilisées pour l'analyse. 
    Les opérations réalisées sont les suivantes :
    - Isole la base bureau 
    - Renomme et concatène en ligne les colonnes candidats
    - Remplit les valeurs manquantes par la méthode ffill
    - Supprime les colonnes inutiles 
"

    Args:
        tableau_donnees_brutes (pd.DataFrame): tableau de données brutes. nb : s'applique aux bases suivantes :
        - PR_2022_T1
        - PR_2017_T1
        - PR_2022_T2
        - PR_2017_T2
        - LG_2022_T1
        - LG_2022_T2
        tour (str): tour de l'élection
        cat_election : "pres", "leg"
    

    Returns:
        pd.DataFrame: tableau de données prêt à l'analyse
    """

    if cat_elec=='pres' : 
        tmp_candidat_cols =candidat_cols_pres 
    elif cat_elec=='leg':
        tmp_candidat_cols=candidat_cols_leg
    # définition des colonnes à garder
    
    nb_max_candidats = (tableau_donnees_brutes.shape[1] - len(bv_cols))/len(tmp_candidat_cols)
    
    assert round(nb_max_candidats) == nb_max_candidats   
    colonnes_dataframe = bv_cols + tmp_candidat_cols
    base_bureau_de_vote = tableau_donnees_brutes.loc[:,:len(bv_cols)-1]
    base_bureau_de_vote.columns = bv_cols
    tableau_donnees_preparees = pd.DataFrame()
  #iterating over 7 columns of candidates data starting from 19th column
    for i in range(base_bureau_de_vote.shape[1], tableau_donnees_brutes.shape[1], len(tmp_candidat_cols)):
        temp_candidat = tableau_donnees_brutes.loc[:,i:i+len(tmp_candidat_cols)-1]
        temp_candidat.columns = tmp_candidat_cols
        temp_candidat = pd.concat([base_bureau_de_vote, temp_candidat], axis=1)
        tableau_donnees_preparees = pd.concat([tableau_donnees_preparees, temp_candidat], axis=0)
    tableau_donnees_preparees.drop(['N°Panneau', 'Sexe'], axis=1, inplace=True)
    tableau_donnees_preparees.reset_index(drop=True, inplace=True)
    tableau_donnees_preparees['Tour'] = tour
    tableau_donnees_preparees['Election'] = cat_elec
    tableau_donnees_preparees['Annee'] = annee
    return tableau_donnees_preparees