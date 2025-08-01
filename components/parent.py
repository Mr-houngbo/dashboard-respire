import streamlit as st
from components.parent_ import *

def show():
    """Fonction principale pour afficher la page parents"""
    show_header(logo_path="assets/images/logo_esmt.jpeg")
    
    show_air_status_summary()
        
    show_health_parameters()

    render_bloc_tendances()
    
    render_bloc_conseils()
    
    show_sms_sytem()
    
    
    
# Test de la fonction
if __name__ == "__main__":
    show()



































#=========================== SECTION TOUT EN BAS RESERVEE AU FOOTER =================================

# show_footer()