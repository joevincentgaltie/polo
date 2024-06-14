import pandas as pd 
import geopandas as gpd 

commune_shapes_path = "http://etalab-datasets.geo.data.gouv.fr/contours-administratifs/2022/geojson/communes-5m.geojson"
communes_france = gpd.read_file(commune_shapes_path)
communes_france = communes_france.rename(
    {'code': 'insee'}, axis=1
)[['insee', 'geometry']]
#save communes_france as csv file in db
communes_france.to_csv('../db/carto/communes_france.csv')