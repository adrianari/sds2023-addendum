import streamlit as st
st.set_page_config(layout="wide")

import pandas as pd
import colorcet as cc
import matplotlib.pyplot as plt

import bokeh
from bokeh.plotting import figure
from bokeh.transform import factor_cmap
from bokeh.models import Circle, ColumnDataSource, Line, LinearAxis, Range1d, LabelSet, HoverTool
from bokeh.palettes import d3
import bokeh.models as bmo
from bokeh.plotting import figure, output_file, show
from bokeh.core.properties import value


tab1, tab2 = st.tabs(["Topic Modelling", "Words per topic"])

with tab1: 
    label_dict = {

    'topics_updated': 'Topic',
    "1":"01: Corona pandemic - Vaccination",
    "2":"02: Radio broadcasting",
    "3":"03: (Public) Transportation",
    "4":"04: Corona pandemic - Precautions",
    "5":"05: Politics - conservatism",
    "6":"06: Corona pandemic - Transmission",
    "7":"07: Journalism",
    "8":"08: Gender",
    "9":"09: Aviation",
    "10":"10: Russia",
    "11":"11: Politics - Framework-agreement EU-Switzerland",
    "12":"12: (Swiss-)German language",
    "13":"13: Politics - Voting",
    "14":"14: Corona pandemic - Testing",
    "15":"15: Education",
    "16":"16: Taxation",
    "17":"17: Entertainment industry",
    "18":"18: Politics",
    "19":"19: Employment",
    "20":"20: Hospital",
    "21":"21: Pension plan",
    "22":"22: Climate change",
    "23":"23: Age & generations",
    "24":"24: Gastronomy",
    "25":"25: Television broadcasting",
    "26":"26: Dietary choices",
    "27":"27: Banking industry",
    "28":"28: Sports",
    "29":"29: Law enforcement",
    'Brand': "Brand", 
    'SRF': 'SRF', 
    'Tages Anzeiger': 'Tages Anzeiger', 
    'Aargauer Zeitung':'Aargauer Zeitung', 
    'Weltwoche':'Weltwoche',
    '0.1':"(Noise)"
    }

    inv_map = {v: k for k, v in label_dict.items()}

    mapli = ['1: Corona pandemic - Vaccination','2: Radio broadcasting','3: (Public) Transportation', '5: Politics - conservatism','4: Corona pandemic - Precautions','6: Corona pandemic – Transmission','7: Journalism', '8: Gender','9: Aviation','10: Russia',
    '11: Politics - Framework-agreement EU-Switzerland','12: (Swiss-)German language','13: Politics - Voting', '14: Corona pandemic - Testing','15: Education','16: Taxation',
    '17: Entertainment industry', '18: Politics',
    '19: Employment','20: Hospital','21: Pension plan','22: Climate change', 
    '23: Age & generations','24: Gastronomy','25: Television broadcasting',
    '26: Dietary choices','27: Banking industry','28: Sports','29: Law enforcement']

    st.write("## Interactive graphic to 'Assessing polarisation in brand-related comments on three Swiss online media portals with Natural Language Processing'")

    dfx = pd.read_csv("df_for_pub.csv")
    all_brands = dfx["Brand"].unique().tolist()
    all_topics = dfx["topics_updated"].unique().tolist()

    all_topics_labeled = sorted([label_dict[str(x)] for x in all_topics])


    selectbox_topics = st.multiselect("Topics to include in graphic", all_topics_labeled, all_topics_labeled)
    selectbox_topics = [int(inv_map[x]) for x in selectbox_topics]


    st.write("Medium to include")
    aargauer = st.checkbox("Aargauer Zeitung", value = True)
    if aargauer:
        m1 = "Aargauer Zeitung"
    else:
        m1 = None

    srf = st.checkbox("SRF", value = True)
    if srf:
        m2 = "SRF"
    else:
        m2 = None

    tagi = st.checkbox("Tages Anzeiger", value = True)
    if tagi:
        m3 = "Tages Anzeiger"
    else:
        m3 = None

    weltwoche = st.checkbox("Weltwoche", value = True)
    if weltwoche:
        m4 = "Weltwoche"
    else:
        m4 = None

    mediums = [m1, m2, m3, m4]


    dfa = dfx[(dfx["Brand"].isin(mediums)) & (dfx["topics_updated"].isin(selectbox_topics))]
    dfa['topics_updated'] = dfa['topics_updated'].astype(str)

    fig, ax = plt.subplots()

    source = ColumnDataSource(data=dict(x=dfa["x"], 
                                        y=dfa["y"], 
                                        keys=dfa['topics_updated'],
                                        keys_right = dfa["topics_updated"].apply(lambda x: label_dict[str(x)]),
                                        brands =dfa['Brand'],
                                    ))

    palette = cc.glasbey_dark[:dfa['topics_updated'].nunique()]
    color_map = bmo.CategoricalColorMapper(factors=dfa['topics_updated'].unique().tolist(), palette=palette)

    marker_mapper = bmo.CategoricalMarkerMapper(factors=["SRF", "Aargauer Zeitung", "Tages Anzeiger", "Weltwoche"], markers = ["diamond", "square", "triangle", "plus"])

    hover = HoverTool(tooltips=[('Topic', '@keys_right'), ('Medium', '@brands')])

    TOOLS = ['pan', 'wheel_zoom', 'reset', hover]
    p = figure(title='UMAP representation of commens to articles', tools=TOOLS, plot_width=1000 )
    p.scatter(x='x', 
                y='y', 
                size=2, 
                source=source,
                color={'field': 'keys', 'transform': color_map},
                marker={'field': 'brands', 'transform': marker_mapper},
                )

    st.bokeh_chart(p)


with tab2:
    HtmlFile = open("topic-word-scores.html", 'r', encoding='utf-8')
    source_code = HtmlFile.read() 
    st.components.v1.html(source_code, height = 1200)  
    