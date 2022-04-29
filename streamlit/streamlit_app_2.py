#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from vega_datasets import data
from streamlit_vega_lite import altair_component



@st.cache
def load_yelp_data():
    yelp_df = pd.read_csv('yelp_cleaned.csv')
    #To Remove Unnamed Columns
    yelp_df.loc[:, ~yelp_df.columns.str.contains('^Unnamed')]
    # yelp_df.set_index("county", drop=True,inplace=True)
    return yelp_df


def load_pop_data():
    pop_df = pd.read_csv('population_density_data.csv')
    #To Remove Unnamed Columns
    pop_df.drop(pop_df.columns[pop_df.columns.str.contains('unnamed',case = False)],axis = 1, inplace = True)
    # pop_df.set_index("county",drop=True, inplace=True)
    return pop_df


# LOADS THE DATA
yelp_df = load_yelp_data()
#yelp_df = yelp_df.reset_index()
pop_df = load_pop_data()
#pop_df = pop_df.reset_index()
chains_df = yelp_df[yelp_df['chain'] == True]
locals_df = yelp_df[yelp_df['chain'] == False]


# DISPLAYS APP TITLE AND DESCRIPTION
row1, row2 = st.columns((2, 3))

with row1:
    st.title("Yelp Restaurant Preferences")

with row2:
    st.write(
        """
        ##
        Examine the restaurant preferences based on urban, suburban, and rural preferences across the United States based on the Yelp dataset! Click on filters on the side to view the data.
    """)

# SHOWS SIDEBAR FUNCTIONS
# show the data in a table
if st.sidebar.checkbox('Show Yelp Dataset'):
    st.subheader('Yelp Dataset')
    st.write(yelp_df)
if st.sidebar.checkbox('Show Population Density Dataset'):
    st.subheader('Population Density Dataset')
    st.write(pop_df)

# show charts
if st.sidebar.checkbox('Compare Ratings by Pop. Type in the US'):
    st.subheader('Ratings by Population Type (US)')
    c = alt.Chart(yelp_df).mark_bar().encode(
        x='chain:N',
        y='count(stars):Q',
        color='chain:N',
        column='stars:Q'
    ).configure_mark(
        color='white'
    )

    st.altair_chart(c)
    st.write('Chain Average: ' + str(chains_df['stars'].mean()) + ' ★')
    st.write('Local Average: ' + str(locals_df['stars'].mean()) + ' ★')

if st.sidebar.checkbox('Compare Ratings by Pop. Type by State'):
    st.subheader('Ratings by Population Type (State)')
    # state_abv =['AL','AK','AZ','AR','CA','CO','CT','DE','FL','GA','HI','ID','IL','IN','IA','KS','KY','LA','ME','MD','MA','MI','MN','MS','MO','MT','NE','NV','NH','NJ','NM','NY','NC','ND','OH','OK','OR','PA','RI','SC','SD','TN','TX','UT','VT','VA','WA','WV','WI','WY']
    states = yelp_df['state'].unique()
    option = st.selectbox('Select a state', states)
    by_State = alt.Chart(yelp_df).mark_bar().encode(
        x='chain:N',
        y='count(stars):Q',
        color='chain:N',
        column='stars:Q'
    ).configure_mark(
        color='white'   
    )
    
    st.altair_chart(by_State)
    st.write('Chain Average: ' + str(chains_df['stars'].mean()) + ' ★')
    st.write('Local Average: ' + str(locals_df['stars'].mean()) + ' ★')

if st.sidebar.checkbox('View Chloropleth Map'):
    counties = alt.topo_feature(data.us_10m.url, 'counties')
    selector = alt.selection_single(name="selector")

    ch_map = alt.Chart(counties).mark_geoshape(stroke='white').encode(
        color=alt.condition(selector, 'DENSITY(C):N', alt.value('lightgray')),
        tooltip=['NAME:N', 'DENSITY(N):Q', 'DENSITY(C):N', 'State:N']
    ).transform_lookup(
        lookup='id',
        from_=alt.LookupData(pop_df, 'id', [
            'NAME', 'DENSITY(N)', 'DENSITY(C)', 'State'])
    ).project(
        type='albersUsa'
    ).properties(
        width=600,
        height=400
    ).add_selection(
        selector
    )


    event_dict = altair_component(altair_chart=ch_map)

    r = event_dict.get('x')

    # st.write(event_dict)
    # if r:
    #     print('test', r)
    #     st.write(r)

    st.altair_chart(ch_map)
    


if st.sidebar.checkbox('View Scatterplot of Pop. Density Ratings'):
    #fig, ax = plt.subplots()
    #pop_df.loc[pop_df[2]:pop_df[11]].plot(ax=ax)
    #st.write(fig)
    
    #Creating a scatterplot for DENSITY(N) vs Stars
    result_df = pd.concat([yelp_df, pop_df], axis=1)
    result_df.plot.scatter(x='DENSITY(N)',y='stars')

    # Creating a scatterplot for city vs stars 
    yelp_df.plot.scatter(x='city',y='stars')

    # Creating a scatterplot for city vs stars 
    yelp_df.plot.scatter(x='county',y='stars')

    