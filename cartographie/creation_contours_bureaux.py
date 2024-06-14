from pomme.utils import filter_liste_electorale,points_to_poly

import pandas as pd 
import numpy as np 
from  scipy.spatial import Voronoi, voronoi_plot_2d
import matplotlib.pyplot as plt
import shapely

import geopandas as gpd
from tqdm import tqdm 

from shapely.ops import cascaded_union


print("Importation des contours de communes")

commune_shapes_path = "http://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2022/geojson/communes-5m.geojson"
communes_france = gpd.read_file(commune_shapes_path)
communes_france = communes_france.rename(
    {'code': 'insee'}, axis=1
)[['insee', 'geometry']]

print("Importation de la base REU")
base_insee= pd.read_csv('../../db/carto/table-adresses-reu.csv')

print("creation des contours")


for i, code_insee in tqdm(enumerate(communes_france.insee.unique())) :
    if i ==0 : 
        bv_carto=[]


    df = filter_liste_electorale(code_insee_commmune=int(code_insee), base = base_insee)
    gdf = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.longitude, df.latitude))
    x = gdf.geometry.x.values
    y = gdf.geometry.y.values
    coords = np.vstack((x, y)).T
    vor = Voronoi(coords)

    boundary = gpd.GeoDataFrame(geometry = gpd.GeoSeries(communes_france[communes_france.insee==code_insee].geometry ))

    lines = [shapely.geometry.LineString(vor.vertices[line]) for line in vor.ridge_vertices if -1 not in line]
    polys = shapely.ops.polygonize(lines)
    voronois = gpd.GeoDataFrame(geometry=gpd.GeoSeries(polys))
    voronois=gpd.overlay(voronois, boundary, how='intersection')

    gdf['poly'] = gdf.apply(lambda x: points_to_poly(x.geometry, voronois), axis=1)


    tmp_bv_carto={}
    for  bv in gdf.id_brut_bv_reu.unique(): 
        tmp_carto=gdf[gdf.id_brut_bv_reu == bv]
        voronois_polygons = gpd.GeoSeries(cascaded_union(tmp_carto.poly))
        tmp_bv_carto[bv] = voronois_polygons

    
    tmp_bv_carto = pd.DataFrame.from_dict(tmp_bv_carto, orient='index').rename(columns={0:'geometry'}).reset_index().rename(columns={'index':'id_brut_bv_reu'})

    bv_carto.append(tmp_bv_carto) 

    if (i%1000==0)&(i!=0) : 
        pd.concat(bv_carto,axis=0).to_csv(f'../db/carto/tmp/bv_carto_from_{i-1000}_to_{i}.csv')
        bv_carto=[]