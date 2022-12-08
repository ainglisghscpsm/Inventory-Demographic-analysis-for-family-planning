import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px


def update_demo_map(selected_ind):
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
    figure = go.Figure(data = data, layout = layout)

    return figure

def update_histogram(df): #selected_row, rows, data
    #df = pd.DataFrame(px.data.gapminder())

    figure = go.Figure()
    figure.add_trace(go.Histogram(
        x = df['gdpPercap'],
        histnorm = 'probability',
        name = 'GDP Per Capita',
        nbinsx = 80))
    figure.add_shape(go.layout.Shape(type='line', xref='x', x0=10000, y0=0, x1=10000,y1=0.5, line={'dash': 'dash'}))
    figure.add_shape(go.layout.Shape(type='line', xref='x', x0=20000, y0=0, x1=20000,y1=0.5, line={'dash': 'dash'}))
    figure.update_layout(paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)')
    '''
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
        figure = px.histogram(height = 700)'''

    return figure

def app():
    st.title('Demographic Parameters')

    st.markdown("### Set Priority Score Threshold:")

    st.write('Click on the indicator to edit threshold')

    df = pd.DataFrame(px.data.gapminder())

    st.table(df.head(10))

    col1, col2 = st.columns(2)

    hist_fig = update_histogram(df)
    map_fig = update_histogram(df)

    col1.plotly_chart(hist_fig, use_container_width=True)
    col2.plotly_chart(map_fig, use_container_width=True)