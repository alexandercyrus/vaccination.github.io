#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import requests


response = requests.get('https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/vaccination_metrics-v3.json')


df = response.json()



data_dict = []
for postcode in df.keys():
    for date in df[postcode].keys():
        data_dict.append([postcode,date]+[value  for stat_name,value in df[postcode][date].items()]) 



df_f = pd.DataFrame(data_dict, columns=['postcode','date','totalVaccinations','firstDoses','fullyVaccinated',"ageUnder50Years","age50YearsAndOver","eligiblePopulation","percPopFullyVaccinatedRange",
"percPopFullyVaccinated10WidthRange","percPopAtLeastFirstDoseRange","percPopAtLeastFirstDose10WidthRange"])



response = requests.get('https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/geojson/postcode_2016_nsw_simplified.json')


geojson = response.json()


import geopandas
url = "https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/geojson/postcode_2016_nsw_simplified.json"
postcode_geo = geopandas.read_file(url)
#display(postcode_geo.head(5))


#display(postcode_geo.head(5))


postcode_geo.columns = ['POA_CODE16', 'POA_NAME16', 'AREASQKM16', 'geometry']


postcode_geo.dropna(inplace=True)


df_f=df_f[df_f['date'] == df_f['date'].max()]



df_merged = pd.merge(postcode_geo,df_f,how='left',left_on='POA_CODE16',right_on='postcode');


df_merged.shape



df_merged = df_merged[df_merged['geometry']!=None]


url = "https://nswdac-covid-19-postcode-heatmap.azurewebsites.net/datafiles/population.json"



suburbs = pd.read_json(url)


suburbs['POA_NAME16'] = suburbs['POA_NAME16'].astype('str')


df_merged = pd.merge(df_merged,suburbs,how='left',left_on='postcode',right_on='POA_NAME16') 


df_merged['Suburbs'] = df_merged['Combined']


df_merged.dropna(subset=['percPopFullyVaccinatedRange'],inplace=True)

import keplergl;


# note that to manually change config, need to remove read_only
w1 = keplergl.KeplerGl(height=500);


w1.add_data(data=df_merged, name='Vaccination Rates')


config = {'version': 'v1',
 'config': {'visState': {'filters': [],
   'layers': [{'id': 'h7zmhd',
     'type': 'geojson',
     'config': {'dataId': 'Vaccination Rates',
      'label': 'Vaccination Rates',
      'color': [179, 173, 158],
      'columns': {'geojson': 'geometry'},
      'isVisible': True,
      'visConfig': {'opacity': 0.8,
       'strokeOpacity': 0.8,
       'thickness': 0.5,
       'strokeColor': [106, 187, 107],
       'colorRange': {'name': 'ColorBrewer YlGn-6',
        'type': 'sequential',
        'category': 'ColorBrewer',
        'colors': ['#ffffcc',
         '#d9f0a3',
         '#addd8e',
         '#78c679',
         '#31a354',
         '#006837']},
       'strokeColorRange': {'name': 'Global Warming',
        'type': 'sequential',
        'category': 'Uber',
        'colors': ['#5A1846',
         '#900C3F',
         '#C70039',
         '#E3611C',
         '#F1920E',
         '#FFC300']},
       'radius': 10,
       'sizeRange': [0, 10],
       'radiusRange': [0, 50],
       'heightRange': [0, 500],
       'elevationScale': 5,
       'enableElevationZoomFactor': True,
       'stroked': True,
       'filled': True,
       'enable3d': False,
       'wireframe': False},
      'hidden': False,
      'textLabel': [{'field': None,
        'color': [255, 255, 255],
        'size': 18,
        'offset': [0, 0],
        'anchor': 'start',
        'alignment': 'center'}]},
     'visualChannels': {'colorField': {'name': 'percPopFullyVaccinatedRange',
       'type': 'string'},
      'colorScale': 'ordinal',
      'strokeColorField': None,
      'strokeColorScale': 'quantile',
      'sizeField': None,
      'sizeScale': 'linear',
      'heightField': None,
      'heightScale': 'linear',
      'radiusField': None,
      'radiusScale': 'linear'}}],
   'interactionConfig': {'tooltip': {'fieldsToShow': {'Vaccination Rates': [{'name': 'postcode',
        'format': None},
       {'name': 'date', 'format': None},
       {'name': 'percPopFullyVaccinatedRange', 'format': None},
       {'name': 'Suburbs', 'format': None}]},
     'compareMode': False,
     'compareType': 'absolute',
     'enabled': True},
    'brush': {'size': 0.5, 'enabled': False},
    'geocoder': {'enabled': True},
    'coordinate': {'enabled': False}},
   'layerBlending': 'normal',
   'splitMaps': [],
   'animationConfig': {'currentTime': None, 'speed': 1}},
  'mapState': {'bearing': 0,
   'dragRotate': False,
   'latitude': -33.84416836886649,
   'longitude': 151.0122575699062,
   'pitch': 0,
   'zoom': 8.38911043038418,
   'isSplit': False},
  'mapStyle': {'styleType': 'dark',
   'topLayerGroups': {},
   'visibleLayerGroups': {'label': True,
    'road': False,
    'border': False,
    'building': True,
    'water': True,
    'land': True,
    '3d building': False},
   'threeDBuildingColor': [9.665468314072013,
    17.18305478057247,
    31.1442867897876],
   'mapStyles': {}}}}



w1.config = config


# In[32]:


# to display the map in the notebook run the name of the map
#w1


# To get the config of the map w1.config

# In[33]:


w1.save_to_html(file_name='C:/Users/sesk2281/DataWarehouse/Personal Web Projects/vaccination.github.io/docs/index.html',read_only = True)

  