#!/usr/bin/env python
# coding: utf-8

# In[34]:


import pandas as pd
import streamlit as st
import altair as alt
import plotly.express as px
import numpy as np


# In[37]:


# How do gun shootings quantity and gun shooting fatalities compare across states
# How do they evolve over time 
df = pd.read_csv('US_Mass_Shootings.csv')
df[['city', 'state']] = df['location'].str.split(',', expand=True)
df['state'] = df['state'].str.strip()

state_mapping = {
    # Handle abbreviations that are already correct
    'TX': 'TX', 'MT': 'MT', 'NY': 'NY', 'NV': 'NV',
    
    # Handle full state names
    'Georgia': 'GA', 'Arkansas': 'AR', 'Nevada': 'NV', 'Maine': 'ME',
    'Florida': 'FL', 'California': 'CA', 'Pennsylvania': 'PA', 
    'New Mexico': 'NM', 'Texas': 'TX', 'Kentucky': 'KY', 
    'Tennessee': 'TN', 'Michigan': 'MI', 'Virginia': 'VA', 
    'Colorado': 'CO', 'North Carolina': 'NC', 'Indiana': 'IN', 
    'Illinois': 'IL', 'Alabama': 'AL', 'Maryland': 'MD', 
    'Oklahoma': 'OK', 'New York': 'NY', 'Missouri': 'MO', 
    'Wisconsin': 'WI', 'New Jersey': 'NJ', 'Ohio': 'OH', 
    'Washington': 'WA', 'Kansas': 'KS', 'Oregon': 'OR', 
    'South Carolina': 'SC', 'Connecticut': 'CT', 'Minnesota': 'MN', 
    'Arizona': 'AZ', 'Nebraska': 'NE', 'Utah': 'UT', 
    'Mississippi': 'MS', 'Massachusetts': 'MA', 'Hawaii': 'HI', 
    'Iowa': 'IA',
    
    # Handle misspelling
    'Lousiana': 'LA',  # Corrected spelling
    'Louisiana': 'LA', # In case you fix the spelling
    
    # Handle D.C.
    'D.C.': 'DC',
    'Washington D.C.': 'DC',
    'District of Columbia': 'DC'
}
df['state'] = df['state'].map(state_mapping)

new_df = df[['fatalities', 'year', 'state']]


# In[36]:


fatalities_df = new_df.groupby(['year', 'state'])['fatalities'].sum() 
fatalities_df = fatalities_df.reset_index()

year = fatalities_df['year'].unique()[::-1]
year = year.tolist()
st.set_page_config(
    page_title="US Gun Fatalities Dashboard",
    page_icon="💥",
    layout="wide",
    initial_sidebar_state="expanded")

st.markdown("""
<style>
    .stApp {
        background-color: #1a1a1a;  /* Dark but not pure black */
        color: #ffffff;
    }
    
    .main .block-container {
        background-color: #1a1a1a;
    }
    
    /* Accent color for headers - muted red */
    h1, h2 {
        color: #cc5555 !important;  /* Muted red for headers */
    }
</style>
""", unsafe_allow_html=True)

alt.themes.enable("dark")




# In[54]:


def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(
        input_df, 
        locations=input_id, 
        color=input_column,  # Could be 'fatalities', 'num_shootings', etc.
        locationmode="USA-states",
        color_continuous_scale=input_color_theme,
        range_color=(0, max(input_df[input_column])),  # Use the actual column
        scope="usa",
        labels={input_column: input_column.replace('_', ' ').title()}  # Dynamic label
    )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth
    
with st.sidebar:
    st.title('💥 US Gun Fatalities Dashboard')
    
    selected_year = st.selectbox('Select a year', year, index=0)
    df_selected_year = fatalities_df[fatalities_df['year'] == selected_year]
    df_selected_year_sorted = fatalities_df.sort_values(by="fatalities", ascending=False)


    choropleth = make_choropleth(df_selected_year, 'state', 'fatalities', 'reds')


# In[ ]:


def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
        y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
        x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
        color=alt.Color(f'{input_color}:Q',
                         legend=None,
                         scale=alt.Scale(scheme=input_color_theme)),
        stroke=alt.value('black'),
        strokeWidth=alt.value(0.25),
    ).properties(width=900).configure_axis(
        labelFontSize=12,
        titleFontSize=12
    ) 
    return heatmap

# Correct function call:
heatmap = make_heatmap(fatalities_df, 'year', 'state', 'fatalities', 'reds')


# In[ ]:
col1, col2 = st.columns(2)

with col1:
    st.subheader("Fatalities by State and Year")
    st.plotly_chart(choropleth, use_container_width=True)

with col2:
    st.subheader("Fatalities Heatmap")
    st.altair_chart(heatmap, use_container_width=True)




