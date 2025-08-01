import streamlit as st
from streamlit_option_menu import option_menu
from src.header import show_header_playful
from src.footer import show_footer

# Configuration générale de la page
st.set_page_config(page_title="RESPiRE – Accueil", layout="wide", initial_sidebar_state="expanded")


st.markdown("""
            <style> 
                .st-emotion-cache-zy6yx3 {
                    width: 100%;
                    padding: 1rem 3rem 0rem;
                    margin-bottom : 0rem;
                    max-width: initial;
                    min-width: auto;
                    }
            </style>
            """,unsafe_allow_html=True)



#  tab1, tab2, tab3, tab4, tab5 = st.tabs(["Threat Model", "Attack Tree", "Mitigations", "DREAD", "Test Cases"])

st.markdown("""
    <style>
        section[data-testid="stSidebar"] {
            background-color: #2E7D32;  /* vert  */
        }
        .block-container {
            padding-top: 1rem;
            margin-bottom: 0rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

# --------------------- HEADER ---------------------
#st.markdown("<h1 style='text-align: left;'>Dashboard RESPiRE</h1>", unsafe_allow_html=True)

# --------- SIDEBAR PERSONNALISÉE ---------

# CSS personnalisé pour la sidebar (à ajouter en début de votre fichier principal)
st.markdown("""
<style>
/* Styling global de la sidebar */
.css-1d391kg {
    background: linear-gradient(180deg, #e8f5e8 0%, #c8e6c9 50%, #a5d6a7 100%) !important;
    border-radius: 20px !important;
}

/* Container de la sidebar */
.css-1cypcdb {
    background: linear-gradient(180deg, #e8f5e8 0%, #c8e6c9 100%) !important;
    border-right: 3px solid rgba(46, 125, 50, 0.2) !important;
    
}

/* Style pour le menu option_menu */
.nav-link {
    background-color: white !important;
    color: #2e7d32 !important;
    border-radius: 20px !important;
    margin: 8px 5px !important;
    padding: 12px 20px !important;
    transition: all 0.3s ease !important;
    border: 2px solid transparent !important;
    font-weight: 600 !important;
    backdrop-filter: blur(10px) !important;
    
}

.nav-link:hover {
    background-color: rgba(46, 125, 50, 0.1) !important;
    color: #1b5e20 !important;
    border: 2px solid rgba(46, 125, 50, 0.3) !important;
    transform: translateX(5px) !important;
    box-shadow: 0 4px 15px rgba(46, 125, 50, 0.2) !important;
}

.nav-link-selected {
    background: linear-gradient(135deg, #4caf50, #66bb6a) !important;
    color: white !important;
    border: 2px solid rgba(255, 255, 255, 0.3) !important;
    box-shadow: 0 6px 20px rgba(76, 175, 80, 0.4) !important;
    transform: translateX(8px) !important;
}

/* Animation pour les icônes */
.nav-link i {
    transition: transform 0.3s ease !important;
}

.nav-link:hover i {
    transform: scale(1.2) !important;
}

.nav-link-selected i {
    transform: scale(1.1) !important;
}


@keyframes breathe {
    0%, 100% { transform: scale(1); }
    50% { transform: scale(1.1); }
}



</style>
""", unsafe_allow_html=True)

#===================================================================================================

#===================================================================================================

# Version améliorée de votre sidebar
with st.sidebar:
    # Logo 
    # Affichage du logo cool (remplace la ligne avec les emojis)
        
    st.image("assets/images/logo_vert.png",output_format="auto")
    
    #    # Titre stylisé
    #    st.markdown(
    #        '<div class="nav-title"> Breath4Life 🌱</div>', 
    #        unsafe_allow_html=True
    #    )
    
    # Menu principal avec style personnalisé
    selected_main = option_menu(
        menu_title=None,  # On enlève le titre car on en a mis un stylisé
        options=["Accueil", "Écoles", "Parents", "Autorité"],
        icons=["house-fill", "building", "people-fill", "shield-fill"],
        default_index=0,
        orientation="vertical",
        styles={
            "container": {
                "padding": "10px",
                "background-color": "inherit",
                "border-radius": "20px"
            },
            "icon": {
                "color": "#2e7d32", 
                "font-size": "18px",
                "margin-right": "10px"
            },
            "nav-link": {
                "font-size": "16px",
                "text-align": "left",
                "margin": "8px 0px",
                "padding": "12px 15px",
                "border-radius": "15px",
                "background-color": "rgba(255, 255, 255, 0.7)",
                "color": "#2e7d32",
                "border": "2px solid transparent",
                "transition": "all 0.3s ease",
                "backdrop-filter": "blur(10px)"
            },
            "nav-link-selected": {
                "background": "linear-gradient(135deg, #4caf50, #66bb6a)",
                "color": "white",
                "border": "2px solid rgba(255, 255, 255, 0.3)",
                "box-shadow": "0 6px 20px rgba(76, 175, 80, 0.4)",
                "transform": "translateX(5px)"
            }
        }
    )
    
    # Séparateur décoratif
    st.markdown(
        """
        <div style="
            height: 3px; 
            background: linear-gradient(90deg, #4caf50, #81c784, #a5d6a7, #4caf50);
            border-radius: 2px; 
            margin: 25px 10px;
            animation: shimmer 2s infinite;
        "></div>
        """, 
        unsafe_allow_html=True
    )
    
    # Section informative
    st.markdown(
        """
        <div style="
            background: rgba(255, 255, 255, 0.8);
            padding: 15px;
            border-radius: 15px;
            margin: 20px 5px;
            text-align: center;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        ">
            <div style="font-size: 2rem; margin-bottom: 10px;">📊</div>
            <div style="color: #2e7d32; font-weight: bold; font-size: 0.9rem;">
                Données en temps réel
            </div>
            <div style="color: #666; font-size: 0.8rem;">
                Capteurs AirGradient
            </div>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    st.markdown("""
        <div style="
            background: rgba(255,255,255,0.85);
            border-radius: 12px;
            padding: 15px;
            margin-top: 20px;
            font-size: 0.85rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            color: #2e7d32;
        ">
            🌬️ <b>Respirer, c’est vivre.</b><br>
            Chaque souffle compte. <br>Agissons aujourd’hui pour un air plus pur demain.
        </div>
        """, unsafe_allow_html=True)




# ---------------------- SECTIONS FIXES POUR LA PAGE D'ACCUEIL -------------------------------

if selected_main == "Accueil":
    show_header_playful()

    tab1,tab2,tab3,tab4 = st.tabs(["Home","Parametres", "A Propos ","KaiKai"])

    with tab1:
        st.markdown("### Suivi de la qualité de l’air dans les écoles au Sénégal")


        # Carte du Sénégal (à remplacer plus tard par vraie carte interactive)
        st.markdown("### 🗺️ Carte du Sénégal")
        st.info("Ici s’affichera la carte interactive avec les zones de pollution.")
        st.image("assets/images/carte_senegal.png", caption="Carte du senegal placeholder", use_container_width=True)

        # KPIs ou indicateurs en bas
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        col1.metric("PM2.5", "35 µg/m³", "+5")
        col2.metric("CO₂", "480 ppm", "-20")
        col3.metric("Température", "31°C", "+1")
    with tab2:
        # Onglet : Parametres 
        from components import parametres
        parametres.parametre()

    with tab3 :
        
        # Onglet : A propos

        st.markdown("## 👥 Qui sommes-nous ?")
        st.write(
            "Nous sommes l’équipe **Breath4Life**, un collectif de jeunes passionnés par l’environnement, la technologie "
            "et la santé publique. Dans le cadre du hackathon Kaikai, nous avons conçu **RESPiRE**, un projet visant "
            "à rendre visible et compréhensible la qualité de l’air dans les écoles au Sénégal."
        )

        st.markdown("### Notre équipe")
        col1, col2 = st.columns(2)

        with col1:
            st.image("assets/images/equipe.jpg", use_container_width=True, caption="L'équipe Breath4Life")
        with col2:
            st.write("""
            - 👨🏽‍💻 **Data & Dev** : Analyse, visualisation, traitement automatique des données AirGradient
            - 🌱 **Environnement & Éducation** : Création de contenus de sensibilisation en Wolof, formation des élèves
            - 📲 **Design & Interface** : Conception d’un tableau de bord adapté aux élèves, parents et autorités
            - 🤝 **Coordination & Communication** : Structuration du projet, pilotage agile, communication institutionnelle
            """)

        st.info("Notre objectif : un air plus sain, une génération plus consciente 🌍")
        
            
        
    with tab4 :

        # Onglet : KaiKai

        st.markdown("## 💡 À propos de Kaikai")
        st.write(
            "**Kaikai** est une entreprise sociale sénégalaise qui met l’innovation au service de l’environnement, "
            "de la santé et du développement durable. Elle accompagne des initiatives à impact à travers des programmes, "
            "des partenariats et des événements structurants comme ce hackathon."
        )

        st.image("assets/images/kaikai_logo.png", width=200)

        st.markdown("### Le Hackathon RESPiRE")
        st.write(
            "Ce hackathon est organisé par Kaikai avec l’ambition de concevoir des solutions concrètes, locales et durables "
            "pour améliorer la qualité de l’air dans les écoles. Des équipes de jeunes innovateurs comme la nôtre "
            "travaillent à proposer des outils basés sur les données pour protéger la santé des enfants."
        )

        st.success("Un grand merci à Kaikai pour son accompagnement et son engagement 🌿")

        st.markdown("---")
        st.markdown("[🔗 En savoir plus sur Kaikai](https://www.kaikai.dev)")



# --------------------- CONTENU PRINCIPAL -----------------------------------

# ---------------------- ACTIONS DES MENUS PRINCIPAUX -----------------------
        
if selected_main == "Écoles":
    from components import ecole
    ecole.show()

elif selected_main == "Parents":
    from components import parent
    parent.show()

elif selected_main == "Autorité":
    from components import autorite
    autorite.show()



































#=========================== SECTION TOUT EN BAS RESERVEE AU FOOTER =================================


show_footer()

