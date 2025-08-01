import streamlit as st
from components.calculer_iqa import calculer_iqa
import pandas as pd
import os
from urllib.parse import urlencode
import requests
from datetime import datetime
import random


#=============================================================================================================

BASE_URL = "https://api.airgradient.com/public/api/v1"
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data/now')
token = "77a25676-a9ec-4a99-9137-f33e6776b590"
location_id = "164928"

#=============================================================================================================

# Valeurs limites (à ajuster selon normes locales)
VALEURS_LIMITE = {
    "rco2_corrected": 1000,    # ppm - Qualité d'air intérieur acceptable
    "tvoc": 500,               # µg/m³ - Limite indicative pour COV
    "pm01_corrected": 15,      # µg/m³ - PM1 (proche de PM2.5 mais plus stricte)
    "pm02_corrected": 25,      # µg/m³ - PM2.5 (norme OMS)
    "pm10_corrected": 50,      # µg/m³ - PM10 (norme OMS)
    "noxIndex": 100       # µg/m³ - Limite pour NOx
}

#=============================================================================================================

def show_header(nom_ecole: str = None, logo_path: str = None):
    """
    Affiche un en-tête moderne et attractif pour la page École.
    :param nom_ecole: Nom de l'école à afficher (optionnel)
    :param logo_path: Chemin vers le logo de l'école (optionnel)
    """
    
    # CSS personnalisé pour l'animation et le style
    st.markdown("""
    <style>
    .header-container {
        background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 50%, #a5d6a7 100%);
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px rgba(46, 125, 50, 0.1);
        border: 2px solid rgba(46, 125, 50, 0.1);
        backdrop-filter: blur(10px);
    }
    
    .title-main {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1b5e20;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 10px;
        animation: fadeInUp 1s ease-out;
    }
    
    .subtitle {
        font-size: 1.3rem;
        color: #2e7d32;
        margin-bottom: 15px;
        font-weight: 500;
        animation: fadeInUp 1.2s ease-out;
    }
    
    .school-name {
        font-size: 1.1rem;
        color: #4caf50;
        background: rgba(255,255,255,0.7);
        padding: 8px 15px;
        border-radius: 25px;
        display: inline-block;
        margin-top: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        animation: fadeInUp 1.4s ease-out;
    }
    
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
    }
    
    .logo-image {
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        border: 3px solid white;
        animation: bounce 2s infinite;
    }
    
    .air-emoji {
        font-size: 2rem;
        animation: float 3s ease-in-out infinite;
        margin: 0 10px;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes bounce {
        0%, 20%, 50%, 80%, 100% {
            transform: translateY(0);
        }
        40% {
            transform: translateY(-10px);
        }
        60% {
            transform: translateY(-5px);
        }
    }
    
    @keyframes float {
        0%, 100% {
            transform: translateY(0px);
        }
        50% {
            transform: translateY(-10px);
        }
    }
    
    .decorative-line {
        height: 4px;
        background: linear-gradient(90deg, #4caf50, #81c784, #a5d6a7, #4caf50);
        border-radius: 2px;
        margin: 20px 0;
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200px 0;
        }
        100% {
            background-position: 200px 0;
        }
    }
    </style>
    """, unsafe_allow_html=True)

    # Conteneur principal avec design moderne
    with st.container():
        st.markdown('<div class="header-container">', unsafe_allow_html=True)
        
        col1, col2 = st.columns([4, 1])
        
        with col1:
            # Titre principal avec emojis animés
            st.markdown(
                """
                <div class="title-main">
                    Bienvenue , cher ecolier.e dans ton espace  – Respire
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Sous-titre engageant
            st.markdown(
                '<div class="subtitle"> Découvre comment va l\'air de ton école aujourd\'hui ! </div>',
                unsafe_allow_html=True
            )
            
            # Nom de l'école avec style modernisé
            if nom_ecole:
                st.markdown(
                    f'<div class="school-name">🏫 {nom_ecole}</div>',
                    unsafe_allow_html=True
                )
        
        with col2:
            if logo_path:
                st.markdown('<div class="logo-container">', unsafe_allow_html=True)
                try:
                    st.image(logo_path, width=100, use_container_width=False)
                except:
                    # Fallback si l'image ne se charge pas
                    st.markdown(
                        '<div style="font-size: 60px; text-align: center;">🏫</div>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                # Logo par défaut si aucun logo fourni
                st.markdown(
                    '<div class="logo-container"><div style="font-size: 60px; text-align: center;">🏫</div></div>',
                    unsafe_allow_html=True
                )
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Ligne décorative animée
        st.markdown('<div class="decorative-line"></div>', unsafe_allow_html=True)

#=============================================================================================================


def fetch_current_data(location_id: str, token: str) -> pd.DataFrame:
    """
    Récupère la mesure  actuelle à partir de l'endpoint /measures/current.
    """

    endpoint = f"/locations/{location_id}/measures/current"
    
    params = {
        "token": token
    }

    full_url = f"{BASE_URL}{endpoint}?{urlencode(params)}"

    try:
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()

        # Vérification du format de réponse
        if isinstance(data, dict):
            # Si les mesures sont directement dans "measures"
            if "measures" in data:
                return pd.DataFrame([data["measures"]])  # ✅ Encapsulation dans une liste
            else:
                return pd.DataFrame([data])  # ✅ On transforme le dict en DataFrame ligne unique
        elif isinstance(data, list):
            return pd.DataFrame(data)  # Si API renvoie déjà une liste d'objets

        print(f"⚠️ Format inattendu de la réponse API pour {location_id} : {data}")
        return pd.DataFrame()

    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur réseau pour {location_id} : {e}")
        return pd.DataFrame()
    except ValueError as e:
        print(f"❌ Erreur lors du parsing JSON pour {location_id} : {e}")
        return pd.DataFrame()
#=============================================================================================================

def calculer_iqa(df: pd.DataFrame):
    """
    Calcule l'IQA global de l'école à partir du df des données actuelles obtenues plus haut.
    :param df : Le DataFrame des données courantes de l'école
    :return: dict avec 'iqa_principal', 'polluant_principal', 'iqa_moyen'
    """

    # Calculer l'IQA pour chaque polluant
    iqa_values = {}
    for pollutant, limite in VALEURS_LIMITE.items():
        if pollutant in df.columns:
            concentration = df[pollutant].mean()  # moyenne du polluant
            iqa_values[pollutant] = (concentration / limite) * 100

    if not iqa_values:
        st.error("❌ Aucun polluant valide trouvé dans le fichier.")
        return None

    # Polluant le plus critique
    pollutant_principal = max(iqa_values, key=iqa_values.get)
    iqa_principal = iqa_values[pollutant_principal]

    # Moyenne des IQA
    iqa_moyen = sum(iqa_values.values()) / len(iqa_values)

    return {
        "iqa_principal": round(iqa_principal, 2),
        "polluant_principal": pollutant_principal,
        "iqa_moyen": round(iqa_moyen, 2)
    }

#=============================================================================================================


def show_air_quality(location_id: str = "164928", token: str = "77a25676-a9ec-4a99-9137-f33e6776b590"):
    st.markdown("## 🌬️ Comment va l'air de notre école ?")

    df = fetch_current_data(location_id, token)
    resultats = calculer_iqa(df)

    if not resultats:
        st.error("Impossible de calculer l'IQA.")
        return

    iqa = resultats["iqa_principal"]
    polluant = resultats["polluant_principal"]
    iqa_moyen = resultats["iqa_moyen"]

    # Détermination du niveau avec emojis plus grands
    if iqa < 50:
        niveau = "EXCELLENT"
        emoji = "😊"
        message = "Super! L’air est bon ! Tu peux jouer dehors sans souci !"
        couleur_bg = "#e8f5e8"
        couleur_border = "#4caf50"
    elif 50<= iqa < 100:
        niveau = "CORRECT"
        emoji = "😐"
        message = "C'est bien, mais pense à aérer la classe !"
        couleur_bg = "#fff8e1"
        couleur_border = "#ff9800"
    else:
        niveau = "ATTENTION"
        emoji = "😷"
        message = "L’air est très pollué . Mieux vaut rester à l'intérieur aujourd'hui"
        couleur_bg = "#ffebee"
        couleur_border = "#f44336"

    # Affichage plus visuel pour les élèves
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown(
            f"""
            <div style='
                background: {couleur_bg};
                border: 3px solid {couleur_border};
                border-radius: 20px;
                padding: 30px;
                text-align: center;
                margin: 20px 0;
            '>
                <div style='font-size: 80px; margin-bottom: 10px;'>{emoji}</div>
                <h1 style='color: {couleur_border}; font-size: 28px; margin: 10px 0;'>{niveau}</h1>
                <h3 style='color: #555; font-size: 18px;'>{message}</h3>
                <p style='color: #777; margin-top: 15px;'>Dernière mesure : {datetime.now().strftime("%H:%M")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Option : Afficher détails supplémentaires si l'utilisateur le souhaite
    with st.expander("🧪 Voir les détails de l'IQA"):
        st.markdown(f"**📊 Moyenne des IQA (tous polluants)** : {iqa_moyen}")
        st.markdown("---")
        st.markdown("### 🧬 Détail par polluant :")
        for pollutant, limite in VALEURS_LIMITE.items():
            if pollutant in df.columns:
                concentration = df[pollutant].mean()
                iqa_polluant = (concentration / limite) * 100
                nom_affiche = pollutant.replace("_corrected", "").upper()
                st.markdown(f"- {nom_affiche} : {round(iqa_polluant, 2)}")

#=============================================================================================================

def show_animation(video_url: str = None):
    """
    Affiche le bloc de sensibilisation avec une vidéo ou, à défaut, une image et un texte explicatif.
    :param video_url: URL de la vidéo YouTube ou intégrée. Si None, affiche une alternative statique.
    """
    st.markdown("## 🎬 Tu veux savoir comment l’air devient pollué ?")

    if video_url:
        st.video(video_url)
    else:
        st.image(
            "assets/images/bad_air_quality.png",  # Image illustrative générique, à remplacer si besoin
            caption="Même quand l'air paraît propre... il peut cacher des choses invisibles 👀",
            use_container_width =True
        )
    st.markdown(
            """
            <div style="font-size:18px; line-height:1.6">
            🌬️ L'air autour de nous peut transporter des petites choses qu'on ne voit pas : fumées, poussières, ou gaz.<br><br>
            🧪 Le capteur installé dans ta classe les détecte, un peu comme un super-nez scientifique !<br><br>
            🛡️ Quand l'air est mauvais, on peut se protéger :<br>
            — en aérant la pièce 🍃<br>
            — en se lavant les mains 🧼<br>
            — ou en restant à l’intérieur 📚<br><br>
            Ensemble, on peut respirer mieux 🤝
            </div>
            """,
            unsafe_allow_html=True
        )
 
 
 
 
#=============================================================================================================

 
def show_daily_tips():
    """
    Affiche des conseils adaptatifs selon la qualité de l'air actuelle
    """
    st.markdown("## 🌱 Mes super-pouvoirs du jour ( Conseils )!")
    
    # Récupérer l'IQA actual
    df = fetch_current_data(location_id, token)
    resultats = calculer_iqa(df)
    
    if not resultats:
        st.warning("Impossible de récupérer les conseils du jour")
        return
        
    iqa = resultats["iqa_principal"]
    
    # Conseils par niveau
    if iqa < 50:
        conseils = [
            {"icon": "🏃‍♂️", "titre": "Sport dehors", "desc": "C'est parfait pour courir et jouer !"},
            {"icon": "🌼", "titre": "Jardinage", "desc": "Arrose les plantes de la classe"},
            {"icon": "🪟", "titre": "Aération", "desc": "Ouvre grand les fenêtres !"}
        ]
        couleur = "#e8f5e8"
    elif 50<= iqa < 100:
        conseils = [
            {"icon": "🌬️", "titre": "Aération courte", "desc": "5 minutes de fenêtres ouvertes"},
            {"icon": "🧼", "titre": "Hygiène", "desc": "Lave-toi bien les mains"},
            {"icon": "💧", "titre": "Hydratation", "desc": "Bois de l'eau régulièrement"}
        ]
        couleur = "#fff8e1"
    else:
        conseils = [
            {"icon": "😷", "titre": "Protection", "desc": "Porte ton masque si nécessaire"},
            {"icon": "🏠", "titre": "Reste dedans", "desc": "Évite les activités extérieures"},
            {"icon": "📚", "titre": "Activités calmes", "desc": "Lecture ou jeux de société"}
        ]
        couleur = "#ffebee"

    # Affichage des conseils en colonnes
    cols = st.columns(len(conseils))
    for i, conseil in enumerate(conseils):
        with cols[i]:
            st.markdown(
                f"""
                <div style='
                    background: {couleur};
                    padding: 20px;
                    border-radius: 15px;
                    text-align: center;
                    height: 180px;
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                '>
                    <div style='font-size: 40px; margin-bottom: 10px;'>{conseil["icon"]}</div>
                    <h4 style='color: #333; margin: 8px 0;'>{conseil["titre"]}</h4>
                    <p style='color: #666; font-size: 12px;'>{conseil["desc"]}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

 
#=============================================================================================================

            
def show_educational_cards():
    st.markdown("## 📚 Le coin des savants !")
    
    cards = [
        {
            "title": "C'est quoi le PM2.5 ?",
            "icon": "🔬",
            "content": "Ce sont des particules si petites qu'on en mettrait 30 sur l'épaisseur d'un cheveu !",
            "color": "#e3f2fd"
        },
        {
            "title": "Pourquoi le CO₂ nous fatigue ?",
            "icon": "😴",
            "content": "Quand il y a trop de CO₂, il y a moins d'oxygène pour notre cerveau !",
            "color": "#f3e5f5"
        },
        {
            "title": "L'humidité et nous",
            "icon": "💧",
            "content": "45-55% d'humidité, c'est parfait ! Trop sec ou trop humide peut gêner notre respiration.",
            "color": "#e8f5e8"
        }
    ]
    
    cols = st.columns(len(cards))
    for i, card in enumerate(cards):
        with cols[i]:
            if st.button(f"{card['icon']} {card['title']}", key=f"card_{i}"):
                st.info(card['content'])
                
#=============================================================================================================

def show_quiz():
    st.markdown("## 🧠 Quiz du jour !")
    
    quiz_questions = [
        {
            "question": "Que mesure PM2.5 ?",
            "options": ["La température", "Les particules fines", "L'humidité"],
            "correct": 1,
            "explanation": "PM2.5 mesure les particules fines de moins de 2,5 micromètres !"
        },
        {
            "question": "Pourquoi trop de CO₂ fatigue ?",
            "options": ["Il fait chaud", "Il manque d'oxygène", "Il est lourd"],
            "correct": 1,
            "explanation": "Trop de CO₂ signifie moins d'oxygène frais pour notre cerveau !"
        }
    ]
    
    question = random.choice(quiz_questions)
    
    with st.container():
        st.markdown(f"### {question['question']}")
        
        answer = st.radio("Choisis ta réponse :", question["options"], key="quiz_daily")
        
        if st.button("Vérifier ma réponse !"):
            if question["options"].index(answer) == question["correct"]:
                st.success(f"🎉 Bravo ! {question['explanation']}")
            else:
                st.info(f"🤔 Pas tout à fait... {question['explanation']}")
                
                
#=============================================================================================================



#=============================================================================================================



#=============================================================================================================
