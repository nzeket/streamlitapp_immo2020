import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px
import plotly.graph_objects as go
#import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image



path2020 = "df2020.csv"
data2020 = pd.read_csv(path2020)


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


def main():
    # Register your pages
    pages = {
        "Accueil/Infos Générales": page_accueil,
        "Agence": page_agence,
        "Particulier": page_particulier,
        
    }


    #ajouter toute la partie homepage
    st.warning('Visual Immo: Toute l actualité sur l immobilier en France')

    #image = Image.open('background2.jpg')
    #st.image(image)

    
    st.sidebar.header('Visual Immo: Mon compte')
    st.sidebar.write('Connectez-vous à votre profil')

    #mettre les cases pour entrer le nom et le code 
    title = st.sidebar.text_input(' Entrez votre identifiant', 'identifiant')
    title = st.sidebar.text_input(' Entrez votre mot de passe', 'Mot de Passe')
    #mettre les checkboxes 
    page = st.sidebar.selectbox("Selectionnez votre profil", tuple(pages.keys()))
        
    pages[page]()
    #st.write('The current movie title is', title)
    st.sidebar.success(' Ce site a été concu pour aider les amateurs en immobilier à se tenir au courant de toute l actualité dans le marché de l immobilier, vous pouvez vous abonner à notre newsletter, en entrant votre adresse-mail ci-dessous')
    
    
    title = st.sidebar.text_input('Entrez votre adresse e-mail', 'votrenom@gmail.com')
    
    
    #fin de l'ajout 

def page_agence():
    st.error ('Nous vous suggérons de fermer l onglet de coté pour avoir une meilleure vue sur votre tableau de bord, et d utiliser le mode plein écran')
    st.success ('Bienvenu.e.s sur votre espace personnel, vous avez ici un résumé des informations les plus importantes pour une agence')


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

def page_particulier():
    st.title('Dashboard Particulier')
    st.success ('Bienvenu.e.s sur votre espace personnel, vous avez ici un résumé des informations les plus importantes pour vendre ou acheter un logement')

    data2020["prix/m^2"] = data2020.valeur_fonciere/data2020.surface_terrain

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

def page_accueil():
    st.title('Accueil & Informations générales')
    st.header('Avec Visual Immo: l immobilier devient visuel')
    st.subheader('Restez informés sur votre et gagnez une longueur d avance grace à nos chiffres clés')
    image = Image.open('background2.jpg')
    st.image(image)

if __name__ == "__main__":
    main()