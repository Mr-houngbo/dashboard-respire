import streamlit as st
from components.ecole_ import *
from src.footer import show_footer

location_id = "164928"
token = "77a25676-a9ec-4a99-9137-f33e6776b590"


def show():
    # Bloc I - Titre
    show_header(nom_ecole="École Multinationale des Telecommunications de Dakar", logo_path="assets/images/logo_esmt.jpeg")
    st.markdown("---")
    
    # Bloc II - Qualité de l'air  -- Test effectuee avec ESMT comme location_id
    show_air_quality()
    st.markdown("---")
    # Aspect beaute de show_air_quality a revoir 
    
    # Bloc III
    show_animation("https://youtu.be/jeKPLNFDoHA?si=0zrmH7cfqyMQ3Osq")
    st.markdown("---")
    
    #BLOC IV
    show_daily_tips()
    st.markdown("---")

    # Bloc V - Quiz interactif (nouveau)
    show_quiz()
    
    st.markdown("---")
    
    # Bloc VI - Fiches pédagogiques (nouveau)
    
    show_educational_cards()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

#=========================== SECTION TOUT EN BAS RESERVEE AU FOOTER =================================

# show_footer()