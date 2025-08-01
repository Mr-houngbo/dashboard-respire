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


"""
# Menu bottom avec le même style que la sidebar
selected_bottom = option_menu(
    menu_title=None,
    options=["Contactez-nous", "Paramètres"],
    icons=["telephone-fill", "gear-fill", "trophy-fill"],
    default_index=0,
    orientation="horizontal",
    styles={
        "container": {
            "padding": "10px",
            "background": "linear-gradient(90deg, #e8f5e8, #c8e6c9, #a5d6a7)",
            "border-radius": "20px",
            "box-shadow": "0 4px 15px rgba(46, 125, 50, 0.2)",
            "margin": "20px 20"
        },
        "icon": {
            "color": "#2e7d32", 
            "font-size": "18px",
            "margin-right": "8px"
        },
        "nav-link": {
            "font-size": "15px",
            "text-align": "center",
            "margin": "0 5px",
            "padding": "12px 20px",
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
            "box-shadow": "0 4px 15px rgba(76, 175, 80, 0.4)",
            "transform": "translateY(-2px)"
        }
    
    }
)
"""









#=========================== SECTION PRISE DEPUIS PARENT.PY =================================
#=========================== SECTION PRISE DEPUIS PARENT.PY =================================
#=========================== SECTION PRISE DEPUIS PARENT.PY =================================





# CE QUE CE CODE FAIT PRINCIPALEMENT GRACE A LA FONCTION show_now , c'est d'afficher tous les indices recueillis now now directement sur le dashboard , le test pour le visualiser est tout en bas 
# Ton boulot sera de l'adapter aux parents plutard (Vu que c'est juste un copier-coller de la vue ecole)

def show():
    st.header("📊 Vue des parents")
    st.markdown("Données spécifiques aux Parents bientot ici.")

def show_header(nom_ecole: str = None, logo_path: str = None):
    """
    Affiche l'entête de la page École.
    :param nom_ecole: Nom de l'école à afficher (optionnel)
    :param logo_path: Chemin vers le logo de l'école (optionnel)
    """

    # Conteneur d'entête
    with st.container():
        col1, col2 = st.columns([4, 1])  # Titre à gauche, logo éventuel à droite

        with col1:
            st.markdown(
                "<h1 style='color:#2E7D32;'>Bienvenue dans ton espace santé – Respire 🌿</h1>",
                unsafe_allow_html=True
            )
            st.markdown(
                "<h4 style='color:#555;'>Découvre comment va l’air de ton école aujourd’hui !</h4>",
                unsafe_allow_html=True
            )

            if nom_ecole:
                st.markdown(f"<h5 style='color:#888;'>🏫 {nom_ecole}</h5>", unsafe_allow_html=True)

        with col2:
            if logo_path:
                st.image(logo_path, width=80)

        st.markdown("---")  # Ligne de séparation

"""
def show_air_quality(location_id: str):
    
    Affiche la qualité de l'air d'une école en se basant sur son IQA.
    :param location_id: ID de l'école (sert à lire son CSV)
    
    iqa, pollutant = calculer_iqa(location_id)

    if iqa is None:
        return

    # Déterminer la catégorie IQA
    if iqa < 50:
        couleur = "#4CAF50"  # Vert
        statut = "Bon 😃"
        message = "L’air est bon ! Tu peux jouer dehors."
    elif iqa < 100:
        couleur = "#FFC107"  # Jaune
        statut = "Moyennement dégradé 😐"
        message = "Pense à bien t’hydrater et à te laver les mains."
    elif iqa < 200:
        couleur = "#FF5722"  # Orange/Rouge
        statut = "Mauvais 😷"
        message = "Attention ! Il vaut mieux rester à l’intérieur aujourd’hui."
    else:
        couleur = "#6D4C41"  # Marron
        statut = "Très mauvais 🚫"
        message = "Ne joue pas dehors ! Il faut rester protégé."

    # Affichage
    with st.container():
        st.markdown("## 🟢 Qualité de l’air aujourd’hui")
        st.markdown(
            f""""""
            <div style="background-color:{couleur}; padding: 15px; border-radius: 10px; text-align:center; color:white;">
                <h2>IQA : {iqa}</h2>
                <h4>Polluant principal : {pollutant}</h4>
                <h3>Qualité : {statut}</h3>
            </div>
            ""","""
            unsafe_allow_html=True
        )

        st.info(f"💡 {message}")
"""

def show_now(df: pd.DataFrame):

    # Exemple de DataFrame (à remplacer par ton fetch_current_data)
    # df = fetch_current_data(location_id, token)

    # Icônes et unités pour affichage
    POLLUTANTS_INFO = {
        "rco2_corrected": {"label": "CO₂", "unit": "ppm", "icon": "🌬️"},
        "tvoc": {"label": "TVOC", "unit": "µg/m³", "icon": "🧪"},
        "pm01_corrected": {"label": "PM1.0", "unit": "µg/m³", "icon": "🌫️"},
        "pm02_corrected": {"label": "PM2.5", "unit": "µg/m³", "icon": "🌁"},
        "pm10_corrected": {"label": "PM10", "unit": "µg/m³", "icon": "🏭"},
        "noxIndex": {"label": "NOx", "unit": "µg/m³", "icon": "🚗"},
    }

    st.subheader("🔬 Polluants mesurés actuellement")

    if df.empty:
        st.warning("Aucune donnée disponible.")
        return

    cols = st.columns(3)  # Crée 3 colonnes pour affichage

    index = 0
    for key, info in POLLUTANTS_INFO.items():
        if key in df.columns:
            value = df[key].mean()
            if pd.isna(value):
                continue

            col = cols[index % 3]
            with col:
                st.markdown(f"""
                    <div style="background-color: #f0f9ff; padding: 1rem; border-radius: 0.5rem; text-align: center; box-shadow: 2px 2px 5px rgba(0,0,0,0.05);">
                        <h4 style="margin-bottom: 0.5rem;">{info['icon']} {info['label']}</h4>
                        <p style="font-size: 24px; font-weight: bold; margin: 0;">{round(value, 1)} {info['unit']}</p>
                    </div>
                """, unsafe_allow_html=True)
            index += 1
        else:
            st.info(f"🛈 Donnée manquante pour {info['label']}")

    # Exemple d’appel
    # afficher_polluants(df)



#===============================================================================   TEST   ============================================================================

import streamlit as st
from components.ecole_ import show_header,show_now
from components.calculer_iqa import calculer_iqa,fetch_current_data
import pandas as pd 


location_id = "164928"
token = "77a25676-a9ec-4a99-9137-f33e6776b590"


def show():
    # Bloc I - Titre
    show_header(nom_ecole="École Multinationale des Telecommunications de Dakar", logo_path="assets/images/logo_esmt.jpeg")

    # Bloc II - Qualité de l'air (valeur fictive pour test)
    # show_air_quality(pm25_value=76)


# Test pour voir si les donnees actuellees recues sont justes

df = fetch_current_data(location_id,token)
show_now(df)


#=========================== SECTION PRISE DEPUIS PARENT.PY =================================












def send_sms_orange_senegal(self, phone_number, message):
    """Envoie SMS via API Orange Sénégal (à adapter selon l'API réelle)"""
    try:
        # Exemple d'implémentation - à adapter selon l'API Orange
        url = "https://api.orange.sn/sms/v1/send"  # URL exemple
        headers = {
            'Authorization': f'Bearer {self.config["orange_api_key"]}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'to': phone_number,
            'message': message,
            'from': 'RESPiRE'  # Nom expéditeur
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=10)
        
        if response.status_code == 200:
            return True, "SMS envoyé via Orange"
        else:
            return False, f"Erreur Orange API: {response.status_code}"
            
    except Exception as e:
        return False, f"Erreur Orange: {str(e)}"

def send_sms_free(self, phone_number, message):
    """Envoie SMS via service gratuit (pour tests uniquement)"""
    try:
        # Service SMS gratuit pour tests - attention aux limitations
        url = "https://textbelt.com/text"
        data = {
            'phone': phone_number,
            'message': message,
            'key': 'textbelt'  # Clé gratuite limitée
        }
        
        response = requests.post(url, data=data, timeout=10)
        result = response.json()
        
        if result.get('success'):
            return True, "SMS envoyé (service test)"
        else:
            return False, f"Erreur service SMS: {result.get('error', 'Inconnu')}"
            
    except Exception as e:
        return False, f"Erreur SMS gratuit: {str(e)}"









