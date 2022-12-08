# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_auth
from  dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import plotly.figure_factory as ff
import plotly.graph_objects as go
import plotly.express as px

import dash_table
from dash_table.Format import Format, Scheme, Sign, Symbol

from datetime import datetime

import pandas as pd
import numpy as np
import json
import urllib

import sqlalchemy as sql
from sqlalchemy import create_engine


import transformation
import query

external_stylesheet = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
URI = 'postgresql://dbadmin:Bigdata2020@psm-to3-lx1.eastus2.cloudapp.azure.com/bigdata'


USERNAME_PASSWORD_PAIRS = {
    'bigdataadmin': 'bigdataadmin2020'
}

server = Flask(__name__)
app = dash.Dash(__name__, server=server, routes_pathname_prefix='/dash/', external_stylesheets= external_stylesheet)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
app.config.suppress_callback_exceptions = True



server.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
server.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://dbadmin:Bigdata2020@psm-to3-lx1.eastus2.cloudapp.azure.com/bigdata'
db = SQLAlchemy(server)
engine=create_engine(URI  , echo=True)

indicator_threshold = transformation.indicator_threshold
test_gdf = transformation.test_gdf
raster_df = transformation.raster_df
priority = transformation.input_use
priority_score = transformation.priority_score
facility_demo = transformation.facility_demo


score_itr_table = transformation.score_itr_table
facility_itr_table = transformation.facility_itr_table
hist_turn_pivot = transformation.hist_turn_pivot

def new_priority(priority_df):
    cols = ["preg_th_low_med","preg_th_med_high","umm_th_low_med","umm_th_med_high","ds_th_low_med","ds_th_med_high","umn_th_low_med","umn_th_med_high","pop_th_low_med","pop_th_med_high","creator_id","last_modified_by","source_id","current_ind"]
    temp_df = pd.DataFrame(columns = cols)
    temp_df['creator_id'] = "admin"
    temp_df['last_modified_by'] = "admin"
    temp_df['source_id'] = "webapp"
    temp_df['current_ind'] = "A"
    temp_df.fillna(0, inplace = True)
    return temp_df

new_input = new_priority(priority)

app.layout = html.Div([
        html.H1('Mali Family Planning Big Data Dashboard'),
        html.Div([
            dcc.Tabs(
                id = "tabs",
                value = 'dashboard_tab',
                vertical = False,
                children = [
                    dcc.Tab(label = 'Demographic Parameters', value = 'threshold_tab'),
                    dcc.Tab(label = 'Indicator Priorities', value = 'scoring_tab'),
                    dcc.Tab(label = 'Dashboard', value = 'dashboard_tab'),]
            ), 
            html.Div(id = 'tabs-content')
        ]),
        html.Div(id='data-json-dump-thres'),
])

@app.callback(Output('tabs-content', 'children'),
             [Input('tabs', 'value')])
              
def render_content(tab):
    if tab == 'threshold_tab':
        return threshold_tab_layout
    
    elif tab == 'scoring_tab':
       return scoring_tab_layout
    
    elif tab == 'dashboard_tab':
       return dashboard_tab_layout

    else:
        html.Div()

dashboard_tab_layout = html.Div(
    
    html.Div([
        html.Div([

            html.H2(
                "Current Year Logistics and Demographic Data",
                className = 'twelve columns',
            ),

            html.H3(
                "Logistics and Priority Data",
                className = 'twleve columns'
            ),

            #Drop-down and filters for current period
           

            html.Label('Choose product from drop-down', style = {'marginTop':15}),
            
            dcc.Dropdown(
                id = 'prod-drop-down',
                options = [
                    #Need to figure out which table to pull from and update
                    {'label':'Collier du cycle', 'value':'FP008'},
                    {'label':'Condom feminin/ Protective','value':'FP002'},
                    {'label':'Condom masculin/ Protector', 'value':'FP001'},
                    {'label':'Depo-Provera','value':'FP005'},
                    {'label':'DIU T 380 A','value':'FP006'},
                    {'label':'implanon NXT','value':'FP009'},
                    {'label':'Implant Jadelle','value':'FP007'},
                    {'label':'Microgynon/ Pilplan d','value':'FP003'},
                    {'label':'Microlut/ Ovrette','value':'FP004'},
                    {'label':'Sayana press','value':'FP010'}
                ],
                value = ''
            ),

        ], className = 'row'),

        html.Div([
            html.Div([
                #priority quadrant chart
                dcc.Graph(id = 'priority-quadrant')
            ], className = 'six columns', style = {'marginRight':90}),

            html.Div(id = 'itr-table', className = 'five columns', style = {'marginTop':50}),
        ], className = 'row'),

        html.Div([
            html.Div([
                #turn rate distribution chart
                dcc.Graph(id = 'itr-bar')
            ], className = 'five columns', style = {'marginRight':20}),

            html.Div([
                #turn rate heat map
                dcc.Graph(id = 'itr-map'),
            ], className = 'six columns'),
        ], className = 'row'),

        html.Div([
            html.H2(
                "Historical Logistics Data (2019)",
                className = 'twelve columns',
                style = {'marginTop':30}
            ),

            html.Label('Choose a product from drop-down', style = {'marginTop':20}),

            dcc.Dropdown(
                id = 'hist-prod-dropdown',
                options = [
                    {'label':'Collier du cycle', 'value':'FP008'},
                    {'label':'Condom feminin/ Protective','value':'FP002'},
                    {'label':'Condom masculin/ Protector', 'value':'FP001'},
                    {'label':'Depo-Provera','value':'FP005'},
                    {'label':'DIU T 380 A','value':'FP006'},
                    {'label':'implanon NXT','value':'FP009'},
                    {'label':'Implant Jadelle','value':'FP007'},
                    {'label':'Microgynon/ Pilplan d','value':'FP003'},
                    {'label':'Microlut/ Ovrette','value':'FP004'},
                    {'label':'Sayana press','value':'FP010'}
                ],
                value = ''
            ),

            html.Label('Choose a region from drop-down', style = {'marginTop':20}),

            dcc.Dropdown(
                id = 'hist-prov-dropdown',
                options = [
                    {'label':'Bamako', 'value': 'Bamako'},
                    {'label':'Gao', 'value': 'Gao'},
                    {'label':'Kayes','value':'Kayes'},
                    {'label':'Kidal','value':'Kidal'},
                    {'label':'Koulikoro', 'value':'Koulikoro'},
                    {'label':'Mopti','value':'Mopti'},
                    {'label':'Segou','value':'Segou'},
                    {'label':'Sikasso','value':'Sikasso'},
                    {'label':'Tombouctou','value':'Tombouctou'}
                ],
                value = ""
            ),

            
            html.Div(id = 'selected_hist_prod', style = {'display':'none'}),
            html.Div(id = 'selected_adm1', style = {'display':'none'}),

        ], className = 'row',style = {'marginTop':20}),        
        
        html.Div([
            html.Div([
                dcc.Graph(id = 'hist-itr')
            ], className = 'row'),
            

        ], className = 'row'),

        html.Div([
            
            html.Div([
                #map/scatter
                dcc.Graph(id= 'hist-map-scatter')
            ], className = 'six columns'),
            html.Div(
                #data table
                id = 'hist-itr-table'
            , className = 'six columns'),
        ], className = 'row'),

        html.Div([html.H5("Maps priority score to facility inventory turn rate. Red dots indicate high turn rate facilities. Dark blue data point are low turn rate facilities.")
        ], className = 'row', style = {'marginTop':5,'marginLeft':20}),
        html.Div([

            html.H3(
                "Demographic Indicators",
                className = "twelve columns"
            ),
            
            html.Label('Choose indicator from drop-down', style = {'marginTop':20}),

            dcc.Dropdown(
                id = 'ind-drop-down',
                options = [
                    #Need to figure out which table from the db to pull from
                    {'label':'Unmet Need', 'value':'Unmet Need - mean'},
                    {'label':'Use of Modern Methods','value':'Use Modern Methods - mean'},
                    {'label':'Pregnancies per 1,000', 'value':'Pregnancies per 1,000'},
                    {'label':'Population','value':'Population Density'},
                    {'label':'Demand Satisfied', 'value': 'Demand Satisfied - mean'}
                ],
                value = ''
            ),
        ], className = 'row'),

        html.Div([
            html.Div([
                dcc.Graph(id = 'dashboard-cy-map')
            ], className = 'five columns'),
        ],className = 'row'),




        html.Div([
            
        ],style={'marginTop': 30}),

        

        html.Div(id = 'selected_ind',style = {'display': 'none'}),
        html.Div(id = 'selected_prod', style = {'display':'none'}),

    ], className = 'ten columns offset-by-one')
)


@app.callback(
    Output('selected_ind', 'children'),
    [Input('ind-drop-down', 'value')]
)
def update_selected_indicator(value):
    selected_ind = ''
    selected_ind = value
    return selected_ind

@app.callback(
    Output('selected_prod', 'children'),
    [Input('prod-drop-down', 'value')]
)
def update_selected_product(value):
    selected_prod = ''
    selected_prod = value
    return selected_prod

@app.callback(
    Output('selected_adm1', 'children'),
    [Input('hist-prov-dropdown',' value')]
)
def update_historical_prov(value):
    selected_adm1 = ''
    selected_adm1 = value
    return selected_adm1

@app.callback(
    Output('selected_hist_prod', 'children'),
    [Input('hist-prod-dropdown', 'value')]
)
def update_historical_prod(value):
    selected_hist_prod = ''
    selected_hist_prod = value
    print(selected_hist_prod)
    return selected_hist_prod

@app.callback(
    Output('priority-quadrant','figure'),
    [Input('selected_prod','children')]
)
def update_quadrant(selected_prod):
    if((selected_prod== "ITR ")|(selected_prod == "")|(selected_prod == None)):
        raise PreventUpdate
    selected_prod = "ITR " + selected_prod
    print(score_itr_table.columns)
    print(score_itr_table[selected_prod])
    print(score_itr_table['Total Priority Score'])
    filtered_itr = score_itr_table[['Total Priority Score', selected_prod, "ADM1", "District"]]
    filtered_itr.rename(columns = {selected_prod: "Inventory Turn Rate"}, inplace = True)
    max_rate = filtered_itr['Inventory Turn Rate'].max()
    y_max = min(max_rate, 20)
    fig = px.scatter(filtered_itr, x = "Total Priority Score", y = "Inventory Turn Rate", color = "ADM1", hover_data = ['ADM1'], width = 700, height = 700, template = "ggplot2", hover_name = "District")
    fig.update_traces(marker = dict(size = 18, opacity = 0.5, line = dict(width = 1, color = 'DarkSlateGrey')))
    fig.update_yaxes(range=[0, y_max])
    fig.add_trace(go.Scatter(
    x=[100],
    y=[3.3],
    text=["Target Area"],
    mode="text",showlegend = False))
    fig.add_trace(go.Scatter(
    x = [100],
    y = [5.5],
    text = ["Understock"],
    mode = "text", showlegend=False
    ))
    fig.add_trace(go.Scatter(
    x = [100],
    y = [2.5],
    text = ["Overstock"],
    mode = "text", showlegend=False
    ))

    fig.update_xaxes(range=[0, 108])
    fig.update_layout(title = 'Priority Score vs Inventory Turn Rate',
    paper_bgcolor='rgba(0,0,0,0)',
    #plot_bgcolor='rgba(0,0,0,0)',
    shapes=[
        #target zone
        dict(
            type="rect",
            # x-reference is assigned to the x-values
            xref="x",
            yref="y",
            x0=50,
            y0=3,
            x1=100,
            y1=5,
            fillcolor='rgba(127, 191, 63, 0.5)',
            opacity=0.38,
            layer="below",
            line_width=0,
        )])
    #fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)')
    fig.update_traces(marker= dict(size = 12))

    #add reference lines
    reference_line1 = go.Scatter(x=[10, 100],
                            y=[3, 3],
                            mode="lines",
                            line=go.scatter.Line(color="gray"),
                            text=["", "Turn Rate Ideal Lower Bound"],
                            textposition="bottom center",
                            showlegend=False)

    reference_line2 = go.Scatter(x=[10, 100],
                            y=[5, 5],
                            mode="lines",
                            line=go.scatter.Line(color="gray"),
                            text=["", "Turn Rate Ideal Upper Bound"],
                            textposition="bottom center",
                            showlegend=False)
    y_max = score_itr_table[selected_prod].max()
    reference_line3 = go.Scatter(x=[50, 50],
                        y=[0, max(5,y_max)],
                        mode="lines",
                        line=go.scatter.Line(color="gray"),
                        text=["", "Median Priority Separator"],
                            textposition="middle center",
                        showlegend=False)
    fig.add_trace(reference_line1)
    fig.add_trace(reference_line2)
    fig.add_trace(reference_line3)
    
    return fig
                    

@app.callback(
    [Output('itr-table', 'children')],
    [Input('selected_prod','children')]
)
def update_score_dt(selected_prod):
    if((selected_prod== "ITR ")|(selected_prod == "")):
        raise PreventUpdate
    col_string = "ITR " + selected_prod
    col_list = ['ADM1','District','Total Priority Score', col_string]
    df_use = score_itr_table[col_list]
    
    new_dt = [
                dash_table.DataTable(
                id = 'priority-quad-table',
                columns=[
                    #{"name": i, "id": i, 'editable': False, 'selectable':False} 
                    #for i in ['Year','ADM1','District','Total Priority Score','Inventory Turn Rate']],
                    {
                        'id': "ADM1",
                        'name':'ADM1',
                        'type':'text'
                    },{
                        'id':'District',
                        'name':'District',
                        'type':'text'
                    },{
                        'id':'Total Priority Score',
                        'name':'Total Priority Score',
                        'type':'numeric',
                        'format': Format(precision=2,scheme=Scheme.fixed),
                    },{
                        'id':col_string,
                        'name':'Inventory Turn Rate',
                        'type':'numeric',
                        'format':Format(precision=2,scheme=Scheme.fixed),
                    }],
                data = (df_use.sort_values(by = 'Total Priority Score', ascending = False).to_dict("records")),
                sort_action='native',
                
                style_cell = {'textAlign':'center','padding':'3px', 'font_size':'14px'},
                style_as_list_view = True,
                style_header = {'backgroundColor':'white','fontWeight':'bold'},
                style_table = {'height':700,'width':600 ,'overflowY': 'auto'}
            ),
            ]
    return new_dt


@app.callback(
    Output('itr-bar','figure'),
    [Input('selected_prod', 'children')]
)
def update_hist(selected_prod):
    if((selected_prod== "ITR ")|(selected_prod == "")):
        raise PreventUpdate
    if(selected_prod != ''):
        selected_prod = "ITR " + selected_prod
        #plot for each region
        y_kayes = score_itr_table[score_itr_table['ADM1']=='Kayes'][selected_prod]
        y_kou = score_itr_table[score_itr_table['ADM1']=='Koulikoro'][selected_prod]
        y_mopti = score_itr_table[score_itr_table['ADM1']=='Mopti'][selected_prod]
        y_segou = score_itr_table[score_itr_table['ADM1']=='Segou'][selected_prod]
        y_sik = score_itr_table[score_itr_table['ADM1']=='Sikasso'][selected_prod]
        #y_bam = score_itr_table[score_itr_table['ADM1']=='Bamako'][selected_prod]
        hist_data = [y_kayes, y_kou, y_mopti, y_segou, y_sik]
        group_labels = ['Kayes','Koulikoro','Mopti','Segou','Sikasso']
        colors = ["#1F77B4","#FF7F0E","#2CA02C","#D62728","#9467BD"]
        fig = ff.create_distplot(hist_data, group_labels, colors = colors, bin_size = .25, show_rug = False)
        fig.update_layout(title_text = "Inventory Rate Distribution by Region",width=700,height=700, xaxis_title_text='Turn Rate', yaxis_title_text="Count/Percentage")
        return fig

@app.callback(
    Output('itr-map','figure'),
    [Input('selected_prod', 'children')]
)
def update_itr_map(selected_prod):
    if((selected_prod== "ITR ")|(selected_prod == "")):
        raise PreventUpdate
    if(selected_prod != ''):
        selected_prod = "ITR " + selected_prod
        
        all_dist = score_itr_table.merge(raster_df[['ADM2']], how = 'outer', left_on = 'District', right_on = 'ADM2')
        print(all_dist)

        data1 = go.Choroplethmapbox(geojson=test_gdf, locations=all_dist['ADM2'],featureidkey="properties.name",
                                    z=all_dist[selected_prod],
                                    colorscale="Viridis",
                                    #zmid = median_value,
                                    #text = raster_df['text'],
                                    marker_opacity=1, marker_line_color='white'
                                    )
        
        filledna = all_dist[pd.isnull(all_dist).any(axis=1)]
        filledna.fillna(0, inplace = True)
        
        data2 = go.Choroplethmapbox(geojson=test_gdf, locations=filledna['ADM2'],featureidkey="properties.name",
                                    z=filledna[selected_prod],
                                    colorscale="gray",
                                    zmid=0,
                                    #zmid = median_value,
                                    text = "No Data",
                                    marker_opacity=1, marker_line_color='white'
                                    )
        data2.update(showscale=False)

        layout1 = go.Layout(width = 700, height=700,
                        mapbox_style="carto-positron",
                        mapbox_zoom=4.5, mapbox_center = {"lat": 17.0750, "lon": -3.0615},title_text = "Inventory Turn Rate by District")
        itr_map = go.Figure(data = [data2, data1], layout = layout1)

        return itr_map

@app.callback(
    Output('dashboard-cy-map','figure'),
    [Input('selected_ind','children')]
)
def update_demo_map(selected_ind):
    #raster_df = raster_df.copy()
    #raster_df = raster_df[raster_df['ADM2']!='Bamako']
    if (selected_ind == ''):
        data = go.Choroplethmapbox(geojson=test_gdf, locations=raster_df['ADM2'],featureidkey="properties.name",
                                    colorscale="Viridis",
                                    visible=False)
    else:
        data = go.Choroplethmapbox(geojson=test_gdf, locations=raster_df['ADM2'],featureidkey="properties.name",
                                    z=raster_df[selected_ind],
                                    colorscale="Viridis",
                                    #zmid = median_value,
                                    text = raster_df['text'],
                                    marker_opacity=1, marker_line_color='white'
                                    )
    
    layout = go.Layout(width = 700, height=700,
                  mapbox_style="carto-positron",
                  mapbox_zoom=4.0, mapbox_center = {"lat": 17.3750, "lon": -2.8615})
    fig = go.Figure(data = data, layout = layout)
    return fig


@app.callback(
    Output('dashboard-dist-scores','figure'),
    [Input('selected_ind','children')]
)
def update_histogram(selected_ind):
    figure = px.histogram(height = 700)
    return figure

@app.callback(
    Output('hist-itr', 'figure'),
    [Input('hist-prod-dropdown', 'value'),
    Input('hist-prov-dropdown','value')]
)
def update_hist_itr(selected_hist_prod, selected_adm1):
    if(((selected_adm1 != '')&(selected_adm1 != None))&((selected_hist_prod != '')&(selected_hist_prod != 'ITR ')&(selected_hist_prod != None))):
        print(selected_hist_prod)
        selected_prod = "ITR " + selected_hist_prod
        df_use = hist_turn_pivot[(hist_turn_pivot['ADM1']==selected_adm1)&(hist_turn_pivot['Year']==2019)]
        df_use = df_use[['Month','District',selected_prod]]
        df_use.rename(columns = {selected_prod: "Inventory Turn Rate"}, inplace = True)
        print(df_use.columns)
        print(df_use)
        figure = px.line(df_use, x = 'Month', y = "Inventory Turn Rate", line_group = "District", color = "District")
        return figure
    else:
        raise PreventUpdate

@app.callback(
    Output('hist-map-scatter','figure'),
    [Input('hist-prod-dropdown', 'value')]
)
def update_hist_map(selected_hist_prod):
    if((selected_hist_prod != '')&(selected_hist_prod != None)):
        facility_use = facility_itr_table[facility_itr_table['Month']==12]
        selected_prod = "ITR " + selected_hist_prod
        facility_use['text'] = facility_use['facility_name'] + ', Turn Rate: '+ facility_use[selected_prod].round(decimals = 2).astype(str)
        facility_use.rename(columns = {selected_prod: "Inventory Turn Rate"}, inplace = True)

        choro = go.Choroplethmapbox(geojson=test_gdf, locations=facility_demo['ADM2'],featureidkey="properties.name",
                                    z=facility_demo['total_priority_score'],
                                    colorscale="tempo",
                                    #zmid = median_value,
                                    text = facility_demo['ADM2'],
                                    marker_opacity=1, marker_line_color='white',
                                    colorbar = dict(title = dict(text="Priority Score",side = "right"))
                                    )
        #choro.update(showscale=False)

        scatter = go.Scattermapbox(lat = facility_use['latitude'], 
                                    lon = facility_use['longitude'],
                                    mode = 'markers',
                                    marker = dict(size = 9, color = facility_use['Inventory Turn Rate'], opacity = 0.7, cmin = 0, colorscale = "RdYlBu", cmid = 4, cmax =20, reversescale=True, colorbar = dict(x = 1.2,title = dict(text="Inventory Turn Rate",side = "right"))),
                                    text = facility_use['text'],
                                    hoverinfo="text")
        layout = go.Layout(title_text = "Priority Score and Facility Turn Rate Category",
                    width = 900, height=700,
                    mapbox_style="carto-positron",
                    mapbox_zoom=4.0, mapbox_center = {"lat": 17.3750, "lon": -2.8615})
        fig = go.Figure(data = [choro, scatter], layout = layout)
        fig.update_layout()
        return fig
    else:
        raise PreventUpdate


threshold_tab_layout= html.Div(
    html.Div([
        html.Div([
            html.H3(
                "Set Priority Score Threshold: ",
                className = 'twelve columns',
            ),
            html.P(
                "Click on the indicator to edit threshold.",
                className = 'twelve columns',

            )
        ], className = 'row'),

        html.Div([
            #Editable datatable for user to enter threshold
            dash_table.DataTable(
                id = 'ind-threshold',
                columns=[{"name": i, "id": i, 'editable': False, 'selectable':True, 'type':'text'}
                if (i == 'Indicator') else
                    {"name": i, "id": i, 'editable': False, 'selectable':True,
                        'type':'numeric',
                        'format': Format(precision=2,scheme=Scheme.fixed),} 
                    if (i != 'Low-Med_Threshold') & (i != 'Med-High_Threshold') else
                    {"name": i, "id": i, 'editable': True, 'selectable':True,
                        'type':'numeric',
                        'format': Format(precision=2,scheme=Scheme.fixed),}
                    for i in indicator_threshold.columns],
                data = indicator_threshold.to_dict('records'),
                row_selectable = "single",
                selected_rows = []                
            ),
            #html.Div(id = 'threshold-interactive-container')
        ], className = 'row'),

        html.Div([
            #Div for histogram and map
            html.Div([
                #Div for histogram
                dcc.Graph(id = 'threshold-hist')
            ], className = 'six columns'
            ),

            html.Div([
                #Div for map
                dcc.Graph(
                    id = 'threshold_map', 
                )
            ], className = 'six columns'
            ),

        ], className = 'row'),

        html.Div([
            html.Button('Save and Continue', id = 'save-threshold', n_clicks = 0)
        ]),

        html.Div(id = 'selected_row',style = {'display': 'none'}),
        html.Div(id = 'modified_table', style = {'display':'none'}),
        html.Div(id = 'hidden_df_update')


    ], className = 'ten columns offset-by-one')
)
#Add call back to highight row when data table is selected and columns in row is only editable when selected
@app.callback(
    Output('selected_row', 'children'),
    [Input('ind-threshold', 'selected_rows')]
)
def update_selected_row(selected_rows):
    selected_row = []
    selected_row = selected_rows
    return selected_row

@app.callback(
    Output('ind-threshold','style_data_conditional'),
    [Input('selected_row','children')]
)
def update_style(selected_row):
    return [{
        'if': {'row_index': i},
        'background_color': '#D2F3FF',
    } for i in selected_row]


#Callbak to update map
@app.callback(
    Output('threshold_map','figure'),
    [Input('selected_row','children')]
)
def update_map(selected_row):
    #raster_df = raster_df.copy()
    #raster_df = raster_df[raster_df['ADM2']!='Bamako']
    if len(selected_row) > 0:
        
        indicator_index = selected_row[0]
        output_ind = indicator_threshold.loc[indicator_index, 'Indicator']
        median_value = raster_df[output_ind].median()
        data = go.Choroplethmapbox(geojson=test_gdf, locations=raster_df['ADM2'],featureidkey="properties.name",
                                    z=raster_df[output_ind],
                                    colorscale="Viridis",
                                    zmid = median_value,
                                    text = raster_df['text'],
                                    marker_opacity=1, marker_line_color='white'
                                    )
    else:
        data = go.Choroplethmapbox(geojson=test_gdf, locations=raster_df['ADM2'],featureidkey="properties.name",
                                    colorscale="Viridis",
                                    #text = raster_df['text'],
                                    marker_opacity=1, marker_line_width=0,
                                    visible=False)
    
    layout = go.Layout(width = 700, height=700,
                  mapbox_style="carto-positron",
                  mapbox_zoom=3.8, mapbox_center = {"lat": 17.3750, "lon": -4.2615})
    fig = go.Figure(data = data, layout = layout)
    return fig




@app.callback(
    Output('threshold-hist','figure'),
    [Input('selected_row','children'),
    Input('ind-threshold','data'),
    Input('ind-threshold','rows')]
)
def update_histogram(selected_row, rows, data):
    if len(selected_row) > 0:
        indicator_index = selected_row[0]
        selected_data = rows[indicator_index]
        low_threshold = selected_data['Low-Med_Threshold']
        high_threshold = selected_data['Med-High_Threshold']
        output_ind = indicator_threshold.loc[indicator_index, 'Indicator']
        #new_df = raster_df[raster_df['ADM2']!='Bamako']
        figure = go.Figure()
        figure.add_trace(go.Histogram(
            x = raster_df[output_ind],
            histnorm = 'probability',
            name = output_ind,
            nbinsx = 80,
        )),
        figure.add_shape(go.layout.Shape(type='line', xref='x',
                                x0=low_threshold, y0=0, x1=low_threshold,y1=0.5, line={'dash': 'dash'}))
        figure.add_shape(go.layout.Shape(type='line', xref='x',
                                x0=high_threshold, y0=0, x1=high_threshold,y1=0.5, line={'dash': 'dash'}))
        figure.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    else:
        figure = px.histogram(height = 700)
    return figure

@app.callback(Output('data-json-dump-thres', 'children'),
              [Input('ind-threshold','columns'),
              Input('ind-threshold','data'),
              Input('save-threshold','n_clicks')])     
def continue_tab2(columns, rows,n_clicks):
    
    temp_df = pd.DataFrame()
    if(n_clicks > 0):
        
        global new_input
        threshold = pd.DataFrame(rows, columns=[c['name'] for c in columns])
        print(threshold)
        #latest_priority = pd.read_sql(query.priority_query.statement, query.session.bind)
        #max_priority = pd.to_numeric(latest_priority['id'],errors = 'coerce').max()
        #print(max_priority)
        #new_input['id'] = max_priority + 1   

        
        temp_df.loc[0,'umn_th_low_med'] = threshold.iloc[0,2]
        #print(threshold.iloc[0,2])
        temp_df.loc[0,'umn_th_med_high'] = threshold.iloc[0,3]
        temp_df.loc[0,'umm_th_low_med'] = threshold.iloc[1,2]
        temp_df.loc[0,'umm_th_med_high'] = threshold.iloc[1,3]
        temp_df.loc[0,'preg_th_low_med'] = threshold.iloc[2,2]
        temp_df.loc[0,'preg_th_med_high'] = threshold.iloc[2,3]
        temp_df.loc[0,'ds_th_low_med'] = threshold.iloc[3,2]
        temp_df.loc[0,'ds_th_med_high'] = threshold.iloc[3,3]
        temp_df.loc[0,'pop_th_low_med'] = threshold.iloc[4,2]
        temp_df.loc[0,'pop_th_med_high'] = threshold.iloc[4,3]
	#print(new_input)
        #for col in new_input.columns:
		#print(new_input.loc[0,col])
        #print(temp_df)
        return temp_df.to_json(orient = 'split')


scoring_tab_layout = html.Div(
    html.Div([
        html.Div([
            html.H3(
                "Set Priority Score Ordering: ",
                className = 'twelve columns',
            ),
            html.P(
                "Select from the drop-down menu to rank the indicators in descending criticality, "+
                "then click on the value range that should receive highest priority in each indicator. For example, if higher Unmet Need should higher priority, choose max for that category.",
                className = 'twelve columns',
            ),
           html.Div([
               html.H5(
                   "Step 1: In descending order, prioritize the demographic indicators. ",
                   className = 'five columns',
               ),
               html.H5(
                   "Step 2: Decide what level of indicator should drive action. ",
                   className = 'six columns',
               ),
           ], className = 'row'),
           html.Div([
               html.P("Priority 1 will receive highest priority score.", className = 'five columns'),
               html.P("For example, should low levels of demand satisfied trigger an action, or higher? If high is selected, higher levels of the indicator will receive higher priority score.", className = 'six columns'),
           ], className = 'row'),


        ], className = 'row', style = {'marginBottom':50}),

        html.Div([
            #Radio items 1
            html.Div([
                dcc.Dropdown(
                    id = 'priority-1-dropdown',
                    options = [
                        {'label':'Unmet Need','value':'umn'},
                        {'label':'Use of Modern Methods','value':'umm'},
                        {'label':'Pregnancies','value':'preg'},
                        {'label':'Population','value':'pop'},
                        {'label':'Demand Satisfied','value':'ds'}
                    ],
                    placeholder = "Select Priority 1..."
                ),
            ], className = 'three columns',
            ),
            html.Div([
                dcc.RadioItems(
                    id = 'priority-1-radio',
                    options = [{'label': 'High', 'value':3},
                        {'label': 'Med', 'value':2},
                        {'label':'Low', 'value':1}],
                        labelStyle={'display': 'inline-block'}
                ),
            ], className = 'nine columns')
        ], className = 'row',style={'marginTop': 25}),

        html.Div([
            #Radio items 2
            html.Div([
                dcc.Dropdown(
                    id = 'priority-2-dropdown',
                    options = [
                        {'label':'Unmet Need','value':'umn'},
                        {'label':'Use of Modern Methods','value':'umm'},
                        {'label':'Pregnancies','value':'preg'},
                        {'label':'Population','value':'pop'},
                        {'label':'Demand Satisfied','value':'ds'}
                    ],
                    placeholder = "Select Priority 2..."
                ),
            ], className = 'three columns',
            ),
            html.Div([
                dcc.RadioItems(
                    id = 'priority-2-radio',
                    options = [{'label': 'High', 'value':3},
                        {'label': 'Med', 'value':2},
                        {'label':'Low', 'value':1}],
                        labelStyle={'display': 'inline-block'}
                ),
            ], className = 'nine columns')
        ], className = 'row',style={'marginTop': 25}),

        html.Div([
            #Radio items 3
            html.Div([
                dcc.Dropdown(
                    id = 'priority-3-dropdown',
                    options = [
                        {'label':'Unmet Need','value':'umn'},
                        {'label':'Use of Modern Methods','value':'umm'},
                        {'label':'Pregnancies','value':'preg'},
                        {'label':'Population','value':'pop'},
                        {'label':'Demand Satisfied','value':'ds'}
                    ],
                    placeholder = "Select Priority 3..."
                ),
            ], className = 'three columns',
            ),
            html.Div([
                dcc.RadioItems(
                    id = 'priority-3-radio',
                    options = [{'label': 'High', 'value':3},
                        {'label': 'Med', 'value':2},
                        {'label':'Low', 'value':1}],
                        labelStyle={'display': 'inline-block'}
                ),
            ], className = 'nine columns')
        ], className = 'row',style={'marginTop': 25}),

        html.Div([
            #Radio items 4
            html.Div([
                dcc.Dropdown(
                    id = 'priority-4-dropdown',
                    options = [
                        {'label':'Unmet Need','value':'umn'},
                        {'label':'Use of Modern Methods','value':'umm'},
                        {'label':'Pregnancies','value':'preg'},
                        {'label':'Population','value':'pop'},
                        {'label':'Demand Satisfied','value':'ds'}
                    ],
                    placeholder = "Select Priority 4..."
                ),
            ], className = 'three columns',
            ),
            html.Div([
                dcc.RadioItems(
                    id = 'priority-4-radio',
                    options = [{'label': 'High', 'value':3},
                        {'label': 'Med', 'value':2},
                        {'label':'Low', 'value':1}],
                        labelStyle={'display': 'inline-block'}
                ),
            ], className = 'nine columns')
        ], className = 'row',style={'marginTop': 25}),

        html.Div([
            #Radio items 4
            html.Div([
                dcc.Dropdown(
                    id = 'priority-5-dropdown',
                    options = [
                        {'label':'Unmet Need','value':'umn'},
                        {'label':'Use of Modern Methods','value':'umm'},
                        {'label':'Pregnancies','value':'preg'},
                        {'label':'Population','value':'pop'},
                        {'label':'Demand Satisfied','value':'ds'}
                    ],
                    placeholder = "Select Priority 5..."
                ),
            ], className = 'three columns',
            ),
            html.Div([
                dcc.RadioItems(
                    id = 'priority-5-radio',
                    options = [{'label': 'High', 'value':3},
                        {'label': 'Med', 'value':2},
                        {'label':'Low', 'value':1}],
                        labelStyle={'display': 'inline-block'}
                ),
            ], className = 'nine columns')
        ], className = 'row',style={'marginTop': 25}),


        html.Div([
            html.Button('Save and Submit', id = 'save-submit', n_clicks = 0)
        ],style={'marginTop': 30}),

        html.Div(id = 'sql-push',style = {'display': 'none'}),
        html.Div(id = 'dropdown1',style = {'display': 'none'}),
        html.Div(id = 'radio1',style = {'display': 'none'}),
        html.Div(id = 'dropdown2',style = {'display': 'none'}),
        html.Div(id = 'radio2',style = {'display': 'none'}),
        html.Div(id = 'dropdown3',style = {'display': 'none'}),
        html.Div(id = 'radio3',style = {'display': 'none'}),
        html.Div(id = 'dropdown4',style = {'display': 'none'}),
        html.Div(id = 'radio4',style = {'display': 'none'}),
        html.Div(id = 'dropdown5',style = {'display': 'none'}),
        html.Div(id = 'radio5',style = {'display': 'none'}),
	html.Div(id = 'hidden_push',style = {'display': 'none'}),


    ], className = 'ten columns offset-by-one')
)

#Callback functions for radio items and dropdowns

@app.callback(
    Output('dropdown1', 'children'),
    [Input('priority-1-dropdown', 'value')]
)
def get_priority_1(input):
    if(input != None):
        #json_df = pd.read_json(json_dump)
        column_name = input + "_priority"
        col_name2 = input + "_weight"
        #global new_input
        #new_input[column_name] = 1
        #new_input[col_name2] = 3.0
        #json_df[column_name] = 1
        #json_df[col_name2] = 3.0
	#print(new_input)
        #print(json_df)
        d = {column_name: [1], col_name2: [3.0]}
        new_df = pd.DataFrame(data = d)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('dropdown2','children'),
    [Input('priority-2-dropdown','value')]
)
def get_priority_2(input):
    if(input != None):
        #json_df = pd.read_json(json_dump)
        column_name = input + "_priority"
        col_name2 = input + "_weight"
        #global new_input
        #new_input[column_name] = 2
        #new_input[col_name2] = 2.5
        #json_df[column_name] = 2
        #json_df[col_name2] = 2.5
        d = {column_name: [2], col_name2: [2.5]}
        new_df = pd.DataFrame(data = d)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('dropdown3','children'),
    [Input('priority-3-dropdown','value')]
)
def get_priority_3(input):
    if(input != None):
        column_name = input + "_priority"
        col_name2 = input + "_weight"
        #global new_input
        #new_input[column_name] = 3
        #new_input[col_name2] = 2.0
        d = {column_name: [3], col_name2: [2.0]}
        new_df = pd.DataFrame(data = d)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('dropdown4','children'),
    [Input('priority-4-dropdown','value')]
)
def get_priority_4(input):
    if(input != None):
        column_name = input + "_priority"
        col_name2 = input + "_weight"
        global new_input
        new_input[column_name] = 4
        new_input[col_name2] = 1.5
        d = {column_name: [4], col_name2: [1.5]}
        new_df = pd.DataFrame(data = d)

    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('dropdown5','children'),
    [Input('priority-5-dropdown','value')]
)
def get_priority_5(input):
    if(input != None):
        column_name = input + "_priority"
        col_name2 = input + "_weight"
        global new_input
        new_input[column_name] = 5
        new_input[col_name2] = 1.0
        d = {column_name: [5], col_name2: [1.0]}
        new_df = pd.DataFrame(data = d)

    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('radio1','children'),
    [Input('priority-1-radio', 'value'),
    Input('priority-1-dropdown','value')]
)
def priority1_score(input, ind):
    if((input != None)&(ind != None)):
        column_name = ind + "_score"
        global new_input
        new_input[column_name] = input
        d = {column_name: [input]}
        new_df = pd.DataFrame(data = d)
        print(column_name)
        print(new_df)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('radio2','children'),
    [Input('priority-2-radio', 'value'),
    Input('priority-2-dropdown','value')]
)
def priority2_score(input, ind):
    if((input != None)&(ind != None)):
        column_name = ind + "_score"
        global new_input
        new_input[column_name] = input
        d = {column_name: [input]}
        new_df = pd.DataFrame(data = d)
        print(column_name)
        print(new_df)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('radio3','children'),
    [Input('priority-3-radio', 'value'),
    Input('priority-3-dropdown','value')]
)
def priority3_score(input, ind):
    if((input != None)&(ind != None)):
        column_name = ind + "_score"
        global new_input
        new_input[column_name] = input
        d = {column_name: [input]}
        new_df = pd.DataFrame(data = d)
        print(column_name)
        print(new_df)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('radio4','children'),
    [Input('priority-4-radio', 'value'),
    Input('priority-4-dropdown','value')]
)
def priority4_score(input, ind):
    if((input != None)&(ind != None)):
        column_name = ind + "_score"
        global new_input
        new_input[column_name] = input
        d = {column_name: [input]}
        new_df = pd.DataFrame(data = d)
        print(column_name)
        print(new_df)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('radio5','children'),
    [Input('priority-5-radio', 'value'),
    Input('priority-5-dropdown','value')]
)
def priority5_score(input, ind):
    if((input != None)&(ind != None)):
        column_name = ind + "_score"
        global new_input
        new_input[column_name] = input
        d = {column_name: [input]}
        new_df = pd.DataFrame(data = d)
        print(column_name)
        print(new_df)
    	return new_df.to_json(orient = 'split')

@app.callback(
    Output('sql-push', 'children'),
    [Input('save-submit','n_clicks'),
    Input('data-json-dump-thres','children'),
    Input('dropdown1','children'),
    Input('radio1','children'),
    Input('dropdown2','children'),
    Input('radio2','children'),
    Input('dropdown3','children'),
    Input('radio3','children'),
    Input('dropdown4','children'),
    Input('radio4','children'),
    Input('dropdown5','children'),
    Input('radio5','children'),]
)
def push_db(n_clicks, json_dump, dd1, rb1, dd2, rb2, dd3, rb3, dd4, rb4, dd5, rb5):
    #dummy until df can be created with user input
    updated_df = pd.read_json(json_dump, orient='split')
    #updated_df['priority_id'] = updated_df['priority_id'] + 1
    for col in updated_df.columns:
        print(col)
        print(updated_df.loc[0, col])

    if((n_clicks > 0)):
                
        drop1 = pd.read_json(dd1, orient='split')
        radio1 = pd.read_json(rb1, orient='split')
        drop2 = pd.read_json(dd2, orient='split')
        radio2 = pd.read_json(rb2, orient='split')
        drop3 = pd.read_json(dd3, orient='split')
        radio3 = pd.read_json(rb3, orient='split')
        drop4 = pd.read_json(dd4, orient='split')
        radio4 = pd.read_json(rb4, orient='split')
        drop5 = pd.read_json(dd5, orient='split')
        radio5 = pd.read_json(rb5, orient='split')
	updated_df = pd.concat([updated_df, drop1, radio1, drop2, radio2, drop3, radio3, drop4, radio4, drop5, radio5], axis = 1, sort = False)
        
        #if(n_clicks > 1):
            #updated_df['priority_id'] = updated_df['priority_id'] + 1
	
        
        updated_df['create_date'] = datetime.now()
        updated_df['last_modified_date'] = datetime.now()
        updated_df['creator_id'] = "admin"
        updated_df['last_modified_by'] = "admin"
        updated_df['source_id'] = "webapp"
        updated_df['current_ind'] = "A"
        create_date = datetime.now()
        last_modified_date = datetime.now()
        source_id = "webapp"
        creator_id = "admin"

        
        for col in updated_df.columns:
            print(updated_df.loc[0,col])
        
        #update previous entries to inactive
        query.session.query(query.priority_input).filter_by(current_ind='A').update({"current_ind" : "N", "last_modified_date": last_modified_date})
        new_user_input = query.priority_input(preg_priority=updated_df.loc[0,'preg_priority'], preg_weight=updated_df.loc[0,'preg_weight'], preg_score=updated_df.loc[0,'preg_score'], preg_th_low_med=updated_df.loc[0,'preg_th_low_med'], preg_th_med_high=updated_df.loc[0,'preg_th_med_high'], umm_priority=updated_df.loc[0,'umm_priority'], umm_weight=updated_df.loc[0,'umm_weight'], umm_score=updated_df.loc[0,'umm_score'], umm_th_low_med=updated_df.loc[0,'umm_th_low_med'], umm_th_med_high=updated_df.loc[0,'umm_th_med_high'], ds_priority=updated_df.loc[0,'ds_priority'], ds_weight=updated_df.loc[0,'ds_weight'], ds_score=updated_df.loc[0,'ds_score'], ds_th_low_med=updated_df.loc[0,'ds_th_low_med'], ds_th_med_high=updated_df.loc[0,'ds_th_med_high'], umn_priority=updated_df.loc[0,'umn_priority'], umn_weight=updated_df.loc[0,'umn_weight'], umn_score=updated_df.loc[0,'umn_score'], umn_th_low_med=updated_df.loc[0,'umn_th_low_med'], umn_th_med_high=updated_df.loc[0,'umn_th_med_high'], pop_priority=updated_df.loc[0,'pop_priority'], pop_weight=updated_df.loc[0,'pop_weight'], pop_score=updated_df.loc[0,'pop_score'], pop_th_low_med=updated_df.loc[0,'pop_th_low_med'], pop_th_med_high=updated_df.loc[0,'pop_th_med_high'], create_date=updated_df.loc[0,'create_date'], creator_id=updated_df.loc[0,'creator_id'], last_modified_date=updated_df.loc[0,'last_modified_date'], last_modified_by=updated_df.loc[0,'last_modified_by'], source_id=updated_df.loc[0,'source_id'], current_ind=updated_df.loc[0,'current_ind'])
        query.session.add(new_user_input)
                
        query.session.commit()
        #json_dump = json.loads(json_dump)
        #json_dump_df = pd.DataFrame(json_dump['data'], columns=json_dump['columns'])
        #print(json_dump_df)
        global indicator_threshold
        indicator_threshold = transformation.create_threshold(updated_df)
        print("I got here.")
    return updated_df.to_json(orient = 'split')



if __name__ == '__main__':
     app.run_server()

