import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import altair as alt


path2020 = "C:\\Users\\Aicha Nzeket\\Desktop\\streamlit-dataset\\df2020.csv"
data2020 = pd.read_csv(path2020)


st.header('Dashboard Agence')
st.success ('Bienvenu.e.s sur votre espace personnel, vous avez ici un résumé des informations les plus importantes')

container1 = st.container()
col1, col2 = st.columns(2)

with container1:
    with col1:
        #histogramme de la nature des transactions
        st.header('Les transactions les plus fréquentes')
        transactions_type = pd.DataFrame(data2020["nature_mutation"].value_counts())
        st.bar_chart(transactions_type)

    with col2:
        fig = go.Figure(
        go.Pie(
        labels = data2020["nom_commune"],
        values = data2020["nom_commune"].value_counts()[:20],
        hoverinfo = "label+percent",
        textinfo = "value"
        
))     
        st.header("Les communes les plus prisées")
        st.plotly_chart(fig)

    


container2 = st.container()
col3, col4 = st.columns(2)

with container2:
    with col3:
        st.header('Le nombre de pièces moyen sur le marché')
        transactions_locations = pd.DataFrame(data2020["nombre_pieces_principales"].value_counts())
        st.bar_chart(transactions_locations)


        
    with col4:
        st.header('Les types de locaux')
        transactions_locations = pd.DataFrame(data2020["type_local"].value_counts())
        st.bar_chart(transactions_locations)


with st.expander("See explanation"):
    st.write("Voir ici l'analyse utile pour les agences")

if st.button('Retourner à la page précédente'):
    st.write('On va aller ')
    