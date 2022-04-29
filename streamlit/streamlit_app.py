#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data
from streamlit_vega_lite import altair_component


@st.cache
def load_yelp_data():
    yelp_df = pd.read_csv('yelp_cleaned.csv')
    # yelp_df.set_index("county", drop=True,inplace=True)
    return yelp_df


def load_pop_data():
    pop_df = pd.read_csv('population_density_data.csv')
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
    st.write(yelp_df)
if st.sidebar.checkbox('Show Population Density Dataset'):
    st.write(pop_df)


# show charts
if st.sidebar.checkbox('Compare Ratings by Pop. Type in the US'):
    c = alt.Chart(yelp_df).mark_bar().encode(
        x='chain:N',
        y='count(stars):Q',
        color='chain:N',
        column='stars:Q'
    )

    st.altair_chart(c)
    st.write('Chain Average: ' + str(chains_df['stars'].mean()) + ' ★')
    st.write('Local Average: ' + str(locals_df['stars'].mean()) + ' ★')

if st.sidebar.checkbox('Compare Ratings by Pop. Type by State'):
    rateState_df = yelp_df['stars'].value_counts()
    st.bar_chart(data=rateState_df)

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

    st.write(event_dict)
    if r:
        print('test', r)
        st.write(r)

    st.altair_chart(ch_map)
    


if st.sidebar.checkbox('View Scatterplot of Pop. Density Ratings'):
    fig, ax = plt.subplots()
    pop_df.loc[pop_df[2]:pop_df[11]].plot(ax=ax)
    st.write(fig)
