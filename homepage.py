import streamlit as st
import pandas as pd
from PIL import Image


st.set_page_config(layout="wide")
#début ajout

#fin ajout

st.warning('Visual Immo: Toute l actualité sur l immobilier en France')

col1, col2 = st.columns((1, 2))

with col1:
    st.header('Visual Immo: Mon compte')
    st.write('Connectez-vous à votre profil')

    #mettre les cases pour entrer le nom et le code 
    title = st.text_input(' Entrez votre identifiant', 'identifiant')
    title = st.text_input(' Entrez votre mot de passe', 'Mot de Passe')
    #mettre les checkboxes 
    genre = st.radio( "Sélectionnez votre profil",
        ('Agence', 'Particulier'))

    #st.write('The current movie title is', title)
    st.success(' Ce site a été concu pour aider les amateurs en immobilier à se tenir au courant de toute l actualité dans le marché de l immobilier, vous pouvez vous abonner à notre newsletter, en cliquanr sur *see explanation* ci-dessous')
    
    
    title = st.text_input('Entrez votre adresse e-mail', 'votrenom@gmail.com')
    
with col2:
    image = Image.open('background2.jpg')
    st.image(image)


