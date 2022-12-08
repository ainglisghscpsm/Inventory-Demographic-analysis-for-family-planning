# -*- coding: utf-8 -*-
# core libraries
import streamlit as st
import pandas as pd

# plotly libraries
import plotly.express as px
import plotly.figure_factory as ff

# supporting files
from multiapp import MultiApp
import threshold_tab, scoring_tab, dashboard_tab

################ Model ################
class Model:
   def __init__(self):
      self.df = pd.DataFrame(px.data.gapminder())
      self.ylist = [int(i) for i in self.df['year'].unique()]
      self.yearStart = self.ylist[0]
      self.yearEnd = self.ylist[-1]
      self.yearStep = self.ylist[1]-self.ylist[0]

   def chart(self,year):
      return px.scatter(self.df[self.df['year'] == year],
         x = 'lifeExp', y = 'gdpPercap', 
         title = f'Year: {year}',
         color='continent',size='pop')

   header = 'Global Statistics from Gapminder'

   description ='''
      See how life expectancy changes over time 
      and in relation to GDP.
      Move the slider to change the year to display.
   '''

   sliderCaption='Select the year for the chart'


################ View ################
def view(model):

   app = MultiApp()
   app.add_app("Demographic Parameters", threshold_tab.app)
   app.add_app("Indicator Priorities", scoring_tab.app)
   app.add_app("Dashboard",dashboard_tab.app)
   app.run()

################ Start ################
view(Model())