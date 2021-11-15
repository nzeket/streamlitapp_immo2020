import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import datetime
import numpy as np
import plotly.graph_objects as go
import seaborn as sns

path2020 = "C:\\Users\\Aicha Nzeket\\Desktop\\streamlit-dataset\\df2020.csv"
data2020 = pd.read_csv(path2020)

st.header('Dashboard Agence')
st.success ('Bienvenu.e.s sur votre espace personnel, vous avez ici un résumé des informations les plus importantes')

data2020["prix/m^2"] = data2020.valeur_fonciere/data2020.surface_terrain

@st.cache
def type_location_by_communs(values):
    df, commune = values
    vals = df[df.nom_commune == commune].type_local.value_counts()
    labels = vals.index
    return (vals,labels)

def get_communs(df):
    return df.nom_commune.value_counts().index

@st.cache
def lowest_square_meters_prices(values):
    df, limits = values
    b = df[(df.surface_terrain >= limits[0]) & (df.surface_terrain <= limits[1]) & ~(df["prix/m^2"].isna())]
    b = b[["nom_commune","prix/m^2"]].groupby("nom_commune").mean().sort_values(by="prix/m^2", ascending=True)[:15]
    b["nom_commune"] = b.index
    return b

def get_types_local(df):
    return df.type_local.value_counts().index



st.header('Le type de local par commune')
fig, ax = plt.subplots(figsize=(10,6))
commune=st.selectbox(
    "Sélectionnez votre commune",
            tuple(get_communs(data2020))
        )
data, labels = type_location_by_communs((data2020,commune))
ax = plt.pie(data, labels=labels, autopct="%.0f%%")
st.pyplot(fig)
        

st.header('Les fluctuations des prix sur le marché')
transactions_type = pd.DataFrame((data2020["valeur_fonciere"][:20]))
st.area_chart(transactions_type)

col1 , col2 = st.columns (2)       
 
st.subheader("Le prix au m2 par commune")
location = col1.selectbox("Choissisez un type de logement", tuple(get_types_local(data2020)))
subdf = data2020[data2020.type_local == location]
limits = (subdf.surface_terrain.min(), subdf.surface_terrain.max())
limits = col2.slider('Sélectionnez un intervalle de valeurs',limits[0],limits[1], (20.0, 10000.0))
data = lowest_square_meters_prices((subdf, limits))
fig, ax = plt.subplots(figsize=(10,6))
ax = sns.barplot(data=data, x="nom_commune", y="prix/m^2")
ax.set_xticklabels(ax.get_xticklabels(),rotation = 50)
st.pyplot(fig)
