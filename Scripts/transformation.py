import pandas as pd
import numpy as np
from shapely.geometry import LineString, MultiLineString
import random
import time
import sys

import query
from query import facility_df, priority_df, product_df, stock_df
import geopandas as gpd


#Create database connection

shapefile_path = r'/var/www/webapp/shapfiles' "//"
fp_path = r'/var/www/webapp' "//"
shp_path = shapefile_path + r'MAL.shp'
geodf = gpd.read_file(shp_path)
raster = fp_path + r'RasterData20200818.xlsx'
output_path = shapefile_path + r'MAL.json'
#geodf.to_file(output_path, driver = "GeoJSON")

df_reduced = geodf[['ID','ADM1','ADM2','geometry']]
df_reduced.loc[df_reduced['ADM1']=='Bamako','ADM2'] = 'Bamako'
df_reduced = df_reduced.sort_values(by = 'ID', ascending = False).reset_index()


df = df_reduced.dissolve(by = 'ADM2')
df = df.sort_values(by = 'ID', ascending = False).reset_index()


def shapefile_to_geojson(gdf, index_list, level = 2, tolerance=0.0025): 
    # gdf - geopandas dataframe containing the geometry column and values to be mapped to a colorscale
    # index_list - a sublist of list(gdf.index)  or gdf.index  for all data
    # level - int that gives the level in the shapefile
    # tolerance - float parameter to set the Polygon/MultiPolygon degree of simplification
    
    # returns a geojson type dict 
   
    #geo_names = list(gdf['ADM{level}'])
    geo_level = 'ADM'+str(level)
    geo_names = list(gdf[geo_level])
    geojson = {'type': 'FeatureCollection', 'features': []}
    for index in index_list:
        geo = gdf['geometry'][index].simplify(tolerance)
    
        if isinstance(geo.boundary, LineString):
            gtype = 'Polygon'
            bcoords = np.dstack(geo.boundary.coords.xy).tolist()
    
        elif isinstance(geo.boundary, MultiLineString):
            gtype = 'MultiPolygon'
            bcoords = []
            for b in geo.boundary:
                x, y = b.coords.xy
                coords = np.dstack((x,y)).tolist() 
                bcoords.append(coords) 
        else: pass
        
        
        feature = {'type': 'Feature', 
                   'id' : index,
                   'properties': {'name': geo_names[index]},
                   'geometry': {'type': gtype,
                                'coordinates': bcoords},
                    }
                                
        geojson['features'].append(feature)
    return geojson


def create_threshold(input_use):
    indicator_threshold = pd.DataFrame(columns = ['Indicator','Low_value','Low-Med_Threshold','Med-High_Threshold','High_value'])
    indicator_threshold['Indicator'] = demographic_ind
    for i in demographic_ind:
        indicator_threshold.loc[indicator_threshold['Indicator']==i,'Low_value'] = raster_df[i].min()
        indicator_threshold.loc[indicator_threshold['Indicator']==i, 'High_value'] = raster_df[i].max()
    indicator_threshold.loc[indicator_threshold['Indicator']=='Unmet Need - mean','Low-Med_Threshold'] = input_use['umn_th_low_med'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']=='Use Modern Methods - mean','Low-Med_Threshold'] = input_use['umm_th_low_med'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']== 'Pregnancies per 1,000','Low-Med_Threshold'] = input_use['preg_th_low_med'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']=='Demand Satisfied - mean','Low-Med_Threshold'] = input_use['ds_th_low_med'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']=='Population Density','Low-Med_Threshold'] = input_use['pop_th_low_med'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']=='Unmet Need - mean','Med-High_Threshold'] = input_use['umn_th_med_high'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']=='Use Modern Methods - mean','Med-High_Threshold'] = input_use['umm_th_med_high'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']== 'Pregnancies per 1,000','Med-High_Threshold'] = input_use['preg_th_med_high'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']=='Demand Satisfied - mean','Med-High_Threshold'] = input_use['ds_th_med_high'].iloc[0]
    indicator_threshold.loc[indicator_threshold['Indicator']=='Population Density','Med-High_Threshold'] = input_use['pop_th_med_high'].iloc[0]

    return indicator_threshold

def create_scores(raster_df, input_use):

    input_use['temp'] = 1
    raster_df['temp'] = 1
    raster_df = raster_df.merge(input_use[[ 'id', 'preg_priority', 'preg_weight',
        'preg_score', 'preg_th_low_med', 'preg_th_med_high', 'umm_priority',
        'umm_weight', 'umm_score', 'umm_th_low_med', 'umm_th_med_high',
        'ds_priority', 'ds_weight', 'ds_score', 'ds_th_low_med',
        'ds_th_med_high', 'umn_priority', 'umn_weight', 'umn_score',
        'umn_th_low_med', 'umn_th_med_high', 'pop_priority', 'pop_weight',
        'pop_score', 'pop_th_low_med', 'pop_th_med_high','temp']], how = 'left', on = 'temp')
    raster_df.drop(columns = ['temp'], inplace= True)
    raster_df.fillna(0, inplace = True)
    raster_df['umm_cat'] = np.where(raster_df['Use Modern Methods - mean']<raster_df['umm_th_low_med'],1,
                                            np.where(raster_df['Use Modern Methods - mean']>raster_df['umm_th_med_high'],10,5))
    raster_df['umn_cat'] = np.where(raster_df['Unmet Need - mean']<raster_df['umn_th_low_med'],1,
                                            np.where(raster_df['Unmet Need - mean']>raster_df['umn_th_med_high'],10,5))
    raster_df['preg_cat'] = np.where(raster_df['Pregnancies per 1,000']<raster_df['preg_th_low_med'],1,
                                            np.where(raster_df['Pregnancies per 1,000']>raster_df['preg_th_med_high'],10,5))
    raster_df['ds_cat'] = np.where(raster_df['Demand Satisfied - mean']<raster_df['ds_th_low_med'],1,
                                            np.where(raster_df['Demand Satisfied - mean']>raster_df['ds_th_med_high'],10,5))
    raster_df['pop_cat'] = np.where(raster_df['Population Density']<raster_df['pop_th_low_med'],1,
                                            np.where(raster_df['Population Density']>raster_df['pop_th_med_high'],10,5))

    raster_df['umm_score'] = pd.to_numeric(raster_df['umm_score'])
    #raster_df['umm_score'] = np.where(raster_df['umm_score']>3,3,raster_df['umm_score'])
    raster_df['umn_score'] = pd.to_numeric(raster_df['umn_score'])
    #raster_df['umn_score'] = np.where(raster_df['umn_score']>3,3,raster_df['umn_score'])
    raster_df['preg_score'] = pd.to_numeric(raster_df['preg_score'])
    #raster_df['preg_score'] = np.where(raster_df['preg_score']>3,3,raster_df['preg_score'])
    raster_df['ds_score'] = pd.to_numeric(raster_df['ds_score'])
    #raster_df['ds_score'] = np.where(raster_df['ds_score']>3,3,raster_df['ds_score'])
    raster_df['pop_score'] = pd.to_numeric(raster_df['pop_score'])
    #raster_df['pop_score'] = np.where(raster_df['pop_score']>3,3,raster_df['pop_score'])


    raster_df['umm_calc_score'] = raster_df['umm_cat']* raster_df['umm_weight']

    raster_df['umn_calc_score'] = raster_df['umn_cat']* raster_df['umn_weight']

    raster_df['preg_calc_score'] = raster_df['preg_cat']* raster_df['preg_weight']

    raster_df['ds_calc_score'] = raster_df['ds_cat']* raster_df['ds_weight']

    raster_df['pop_calc_score'] = raster_df['pop_cat']* raster_df['pop_weight']

    raster_df['total_priority_score'] = raster_df['umm_calc_score'] + raster_df['umn_calc_score'] + raster_df['preg_calc_score'] + raster_df['ds_calc_score'] + raster_df['pop_calc_score']

    return raster_df

def fac_rolling_rates(df, window, unique_group):
    for col in unique_group:
        df[col] = df[col].map(str)
    df['group'] = df[unique_group].sum(1)
    
    grouped = df.groupby(['group','ADM1','demo_district','facility_code','product_code','calendar_year','month_number']).agg({
        'dispensed':'sum','closing_stock':'sum'}).sort_index(level = ['demo_district','facility_code','product_code','calendar_year','month_number']).groupby(level =0).rolling(window = window, min_periods = window).agg({
            'dispensed':['std','mean','sum','count'],'closing_stock':'mean'}).reset_index(level = 0, drop = True).reset_index()
    grouped.columns = grouped.columns.map('_'.join).str.strip('_')
    grouped['inventory_turn_rate'] = grouped['dispensed_sum']/grouped['closing_stock_mean']

    return grouped

def dist_rolling_rates(df, window, unique_group):
    df = df.copy()
    for col in unique_group:
        df[col] = df[col].map(str)
    df['group'] = df[unique_group].sum(1)
    df= df.sort_values(by = ['calendar_year','month_number'])
    
    grouped = df.groupby(['group','ADM1','demo_district','product_code','calendar_year', 'month_number']).agg({
        'dispensed':'sum','closing_stock':'sum'}).sort_index(level=['demo_district','product_code','calendar_year','month_number']).groupby(level =0).rolling(window = window, min_periods = window).agg({
            'dispensed':['std','mean','sum'],'closing_stock':'mean'}).reset_index(level = 0, drop = True).reset_index()
    grouped.columns = grouped.columns.map('_'.join).str.strip('_')
    #grouped['Consumption_COV'] = grouped['Issued_Qty_std']/grouped['Issued_Qty_mean']
    grouped['inventory_turn_rate'] = grouped['dispensed_sum']/grouped['closing_stock_mean']

    return grouped

#District boundaries
test_gdf = shapefile_to_geojson(df, list(df.index))


#Demographic data
raster_df = pd.read_excel(raster)
raster_df = raster_df.drop_duplicates()
raster_df.loc[raster_df['ADM2']=='Dissolved','ADM2'] = 'Bamako'
raster_df['text'] = raster_df['ADM2']
raster_df['Pregnancies per 1,000'] = raster_df['Pregnancies - sum'] / (raster_df['Population - sum'] / 1000)
#raster_df = raster_df[raster_df['ADM2']!='Bamako']

#Indicator used
demographic_ind = ['Unmet Need - mean', 'Use Modern Methods - mean', 'Pregnancies per 1,000', 'Demand Satisfied - mean', 'Population Density']

#Indicator threshold
if(priority_df.empty == False):
    priority_df.sort_values(by = ['id'], inplace = True)
    input_use = priority_df.tail(1)

indicator_threshold = create_threshold(input_use)

raster_df = create_scores(raster_df, input_use)
facility_df = facility_df.dropna()
facility_df.loc[facility_df['demo_district'].str.contains('Commune'),'demo_district'] = 'Bamako' 
facility_df.loc[facility_df['demo_district'].str.contains('COMMUNE'),'demo_district'] = 'Bamako'
facility_df.loc[facility_df['demo_district'].str.contains('Dissolved'),'demo_district'] = 'Bamako' 
facility_demo = facility_df[['facility_code','demo_district','facility_name']].merge(raster_df, how = 'left', left_on = 'demo_district',right_on = 'ADM2')


stock_df.fillna(0, inplace= True)
stock_detail =  stock_df.merge(facility_demo, how = 'left', on = 'facility_code')
stock_detail = stock_detail.merge(product_df, how = 'left', on = 'product_code')


stock_detail['calendar_year'] = pd.to_numeric(stock_detail['calendar_year'])

stock_detail_cy = stock_detail[stock_detail['calendar_year']>=2018]
stock_detail_py = stock_detail[stock_detail['calendar_year']<2020]

stock_detail_now = stock_detail_cy[stock_detail_cy['calendar_year']==2020]
priority_score = stock_detail_now[['calendar_year','ADM1','demo_district','total_priority_score']]
priority_score = priority_score.drop_duplicates()
def monthly_average(stock_df):
    return stock_df


district_turn_rate = dist_rolling_rates(stock_detail_cy, 12, ['demo_district','product_code'])

hist_turn = district_turn_rate[district_turn_rate['calendar_year']==2019]

district_turn_rate = district_turn_rate[district_turn_rate['calendar_year']==2020]
district_turn_rate = district_turn_rate[district_turn_rate['month_number']==district_turn_rate['month_number'].max()]
district_turn_rate = district_turn_rate.drop(columns = ['dispensed_sum','dispensed_mean','dispensed_std','closing_stock_mean','group','month_number'])
input_df = priority_score.merge(district_turn_rate, on = ['calendar_year','ADM1','demo_district'], how = 'left')
input_df.dropna(inplace = True)

score_itr_table = input_df.copy()
score_itr_table = input_df.pivot_table(index = ['calendar_year','demo_district','ADM1', 'total_priority_score'], columns = 'product_code', values = ['inventory_turn_rate']).reset_index()
score_itr_table.columns = score_itr_table.columns.map('_'.join).str.strip('_')

score_itr_table.columns = ['Year','District','ADM1','Total Priority Score','ITR FP001','ITR FP002','ITR FP003','ITR FP004','ITR FP005','ITR FP006','ITR FP007','ITR FP008','ITR FP009','ITR FP010']

facility_turn = fac_rolling_rates(stock_detail_py, 12, ['demo_district','product_code'])
#facility_turn = priority_score[['ADM1','demo_district','total_priority_score']].merge(facility_turn, on = ['ADM1','demo_district'], how = 'left')
facility_itr_table = facility_turn.pivot_table(index = ['calendar_year','month_number','demo_district','ADM1','facility_code'], columns= 'product_code', values = ['inventory_turn_rate']).reset_index()
facility_itr_table.columns = facility_itr_table.columns.map('_'.join).str.strip('_')
facility_itr_table.columns = ['Year','Month','District','ADM1','facility_code','ITR FP001','ITR FP002','ITR FP003','ITR FP004','ITR FP005','ITR FP006','ITR FP007','ITR FP008','ITR FP009','ITR FP010']
facility_use = facility_df[['facility_code','facility_name','facility_type','latitude','longitude']]
facility_itr_table = facility_itr_table.merge(facility_use, on = ['facility_code'],how = 'left')
facility_itr_table.loc[facility_itr_table['ADM1']=='Bamako','District'] = 'Bamako'

hist_turn = hist_turn.drop(columns = ['dispensed_sum','dispensed_mean','dispensed_std','closing_stock_mean','group'])
hist_turn_pivot = hist_turn.pivot_table(index = ['calendar_year','month_number','demo_district','ADM1'], columns = 'product_code', values = ['inventory_turn_rate']).reset_index()
hist_turn_pivot.columns = ['Year','Month','District','ADM1','ITR FP001','ITR FP002','ITR FP003','ITR FP004','ITR FP005','ITR FP006','ITR FP007','ITR FP008','ITR FP009','ITR FP010']

