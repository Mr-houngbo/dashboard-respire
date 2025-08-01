import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from plotly.subplots import make_subplots
import os
import requests
from urllib.parse import urlencode,quote_plus
import json
from twilio.rest import Client
import time



# Configuration (à adapter selon vos données)
BASE_URL = "https://api.airgradient.com/public/api/v1"
token = "77a25676-a9ec-4a99-9137-f33e6776b590"
location_id = "164928"
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data/air_quality')


# CSS personnalisé pour un design moderne
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(45deg, #81c784, #aed581, #c5e1a5, #dcedc8);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
    }
    
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
        margin-bottom: 1rem;
    }
    
    .status-excellent { border-left-color: #22c55e !important; }
    .status-good { border-left-color: #84cc16 !important; }
    .status-moderate { border-left-color: #eab308 !important; }
    .status-poor { border-left-color: #f97316 !important; }
    .status-dangerous { border-left-color: #ef4444 !important; }
    
    .prediction-card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #cbd5e1;
    }
    
    .action-button {
        background: linear-gradient(90deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .alert-banner {
        background: linear-gradient(90deg, #fef3c7 0%, #fde68a 100%);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #f59e0b;
        margin-bottom: 1rem;
    }
    
    .stMetric > div > div > div > div {
        font-size: 2rem !important;
    }
</style>
""", unsafe_allow_html=True)

# Valeurs limites (à ajuster selon normes locales)
VALEURS_LIMITE = {
"pm03_count": 100000, # particules de 0.3μm - pas de norme OMS, seuil indicatif élevé
"pm01_corrected": 15, # µg/m³ - Particules fines PM1 (plus sévère que PM2.5)
"pm02_corrected": 25, # µg/m³ - PM2.5 - norme OMS 2021
"pm10_corrected": 50, # µg/m³ - PM10 - norme OMS 2021
"rco2_corrected": 1000, # ppm - qualité de l'air intérieur acceptable (OMS + ASHRAE)
"atmp_corrected": 27, # °C - Température intérieure maximale conseillée
"rhum_corrected": 60, # % - Humidité relative recommandée : 40-60%
"tvoc": 500, # µg/m³ - Limite indicative (sensibilité à 150-300 selon source)
"noxIndex": 100 # µg/m³ - Limite OMS pour NO₂ sur 1h
}

#=============================================================================================================

def show_header(nom_ecole: str = "Ecole Multinationnale de Telecoms ", logo_path: str = None):
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
                    Bienvenue sur l'espace Autorité de Respire
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Sous-titre engageant
            st.markdown(
                '<div class="subtitle">Découvrez comment va l\'air de l\'école dans les ecoles de votre ville aujourd\'hui et prenez des décisions !</div>',
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


def show_line():
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

    return round(iqa_principal, 2)

#=============================================================================================================

def alerts(aqi_global = calculer_iqa(fetch_current_data(location_id, token))):
    if aqi_global > 100:
        st.markdown("""
        <div class="alert-banner">
            <strong>⚠️ ALERTE QUALITÉ DE L'AIR</strong><br>
            Niveau préoccupant détecté. Actions recommandées : ventilation renforcée, réduction des activités extérieures.
        </div>
        """, unsafe_allow_html=True)
#=============================================================================================================

def descript(aqi_global = calculer_iqa(fetch_current_data(location_id, token))):
    """
    Décrit la signification de l'AQI et interprète la valeur donnée
    Args:
        aqi_global (int/float): Valeur de l'Air Quality Index
    
    Returns:
        str: Description de l'AQI et interprétation de la valeur
    """
    
    # Description générale de l'AQI
    description_generale = "L'AQI (Air Quality Index) est un indicateur standardisé qui mesure la qualité de l'air sur une échelle de 0 à 500,en combinant plusieurs polluants atmosphériques."
    
    # Interprétation selon la valeur
    if aqi_global <= 50:
        interpretation = f"Avec un AQI de {aqi_global}, l'air est de qualité excellente. <br> Aucun risque pour la santé, toutes les activités peuvent se dérouler normalement. <br>L'environnement est idéal pour les élèves et le personnel."
        
    elif aqi_global <= 100:
        interpretation = f"Votre AQI de {aqi_global} indique une qualité d'air acceptable.<br> La plupart des personnes peuvent vaquer à leurs activités sans restriction, <br>seules les personnes très sensibles pourraient ressentir un léger inconfort."
        
    elif aqi_global <= 150:
        interpretation = f"L'AQI de {aqi_global} révèle une qualité d'air modérément dégradée.<br> Les personnes sensibles (enfants, personnes âgées, asthmatiques) peuvent ressentir des symptômes légers.<br> Il est recommandé de limiter les activités physiques intenses à l'extérieur."
        
    elif aqi_global <= 200:
        interpretation = f"Avec un AQI de {aqi_global}, la qualité de l'air est préoccupante pour la santé.<br> Tous peuvent commencer à ressentir des effets, les groupes sensibles étant plus affectés.<br> Les activités extérieures prolongées sont déconseillées."
        
    else:
        interpretation = f"L'AQI de {aqi_global} signale une qualité d'air dangereuse.<br> Risques sanitaires importants pour tous, particulièrement les enfants et personnes vulnérables.<br> Mesures d'urgence recommandées : fermeture des fenêtres, report des activités extérieures, port du masque si nécessaire."
    
    # st.markdown(f"{description_generale} {interpretation}")
    st.markdown(f"""
        <div class="metric-card">
            <p>{description_generale}</p>
            <p>{interpretation}</p>
        </div>
        """, unsafe_allow_html=True)
    
#=============================================================================================================

def get_aqi_status(aqi = calculer_iqa(fetch_current_data(location_id, token))):
    """Retourne le statut et la couleur selon l'AQI"""
    if aqi <= 50:
        return "Excellent", "#22c55e", "😊"
    elif aqi <= 100:
        return "Bon", "#84cc16", "🙂"
    elif aqi <= 150:
        return "Modéré", "#eab308", "😐"
    elif aqi <= 200:
        return "Préoccupant", "#f97316", "😟"
    else:
        return "Dangereux", "#ef4444", "😷"
#=============================================================================================================

def create_gauge_chart(title, max_val=200,value = calculer_iqa(fetch_current_data(location_id, token))):
    """Crée un graphique en forme de jauge"""
    status, color, emoji = get_aqi_status(value)
    
    fig = go.Figure(go.Indicator(
        mode = "gauge+number+delta",
        value = value,
        domain = {'x': [0, 1], 'y': [0, 1]},
        title = {'text': f"{title} {emoji}"},
        delta = {'reference': 50},
        gauge = {
            'axis': {'range': [None, max_val]},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 50], 'color': "rgba(34, 197, 94, 0.3)"},
                {'range': [50, 100], 'color': "rgba(132, 204, 22, 0.3)"},
                {'range': [100, 150], 'color': "rgba(234, 179, 8, 0.3)"},
                {'range': [150, 200], 'color': "rgba(249, 115, 22, 0.3)"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 150
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
    return fig
#=============================================================================================================

def create_indicator_bars():
    """Crée les barres d'indicateurs actuels"""
    # Données simulées pour les indicateurs
    indicators = {
        'PM2.5': {'value': 18.2, 'unit': 'μg/m³', 'max': 50, 'status': 'good'},
        'PM0.3': {'value': 4580, 'unit': 'count', 'max': 10000, 'status': 'moderate'},
        'PM1': {'value': 12.1, 'unit': 'μg/m³', 'max': 40, 'status': 'good'},
        'PM10': {'value': 24.5, 'unit': 'μg/m³', 'max': 80, 'status': 'moderate'},
        'CO₂': {'value': 420, 'unit': 'ppm', 'max': 1000, 'status': 'good'},
        'Temp': {'value': 24.8, 'unit': '°C', 'max': 35, 'status': 'good'},
        'Humidité': {'value': 65, 'unit': '%', 'max': 100, 'status': 'moderate'},
        'TVOC': {'value': 180, 'unit': 'Ind40', 'max': 500, 'status': 'good'},
        'NOx': {'value': 45, 'unit': 'Ind41', 'max': 100, 'status': 'good'}
    }
    
    names = list(indicators.keys())
    values = [indicators[name]['value'] for name in names]
    colors = ['#22c55e' if indicators[name]['status'] == 'good' 
              else '#eab308' if indicators[name]['status'] == 'moderate' 
              else '#ef4444' for name in names]
    
    fig = go.Figure(data=[
        go.Bar(
            x=names,
            y=values,
            marker_color=colors,
            text=[f"{val} {indicators[name]['unit']}" for name, val in zip(names, values)],
            textposition='auto',
            hovertemplate='<b>%{x}</b><br>Valeur: %{y}<br><extra></extra>'
        )
    ])
    
    fig.update_layout(
        title="📊 Indicateurs en Temps Réel",
        xaxis_title="Paramètres",
        yaxis_title="Valeurs",
        height=400,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig
#=============================================================================================================

def create_prediction_chart():
    """Crée le graphique de prédictions"""
    hours = ['00h', '06h', '12h', '18h', '23h']
    pm25_pred = [16, 22, 28, 24, 18]
    co2_pred = [400, 450, 580, 520, 420]
    temp_pred = [22, 24, 28, 26, 23]
    
    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('PM2.5 (μg/m³)', 'CO₂ (ppm)', 'Température (°C)'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )
    
    fig.add_trace(go.Scatter(x=hours, y=pm25_pred, mode='lines+markers', 
                            name='PM2.5', line=dict(color='#ef4444', width=3)), row=1, col=1)
    fig.add_trace(go.Scatter(x=hours, y=co2_pred, mode='lines+markers', 
                            name='CO₂', line=dict(color='#3b82f6', width=3)), row=1, col=2)
    fig.add_trace(go.Scatter(x=hours, y=temp_pred, mode='lines+markers', 
                            name='Température', line=dict(color='#22c55e', width=3)), row=1, col=3)
    
    fig.update_layout(height=300, showlegend=False, title_text="🔮 Prédictions pour Demain")
    return fig
#=============================================================================================================

def create_school_ranking():
    """Crée le classement des écoles"""
    schools_data = {
        'École': ['École Primaire Almadies', 'Lycée John F. Kennedy', 'Lycée Blaise Diagne', 
                  'École Sacré-Cœur', 'Lycée Seydou Nourou Tall'],
        'AQI': [45, 58, 68, 82, 95],
        'Statut': ['Excellent', 'Bon', 'Modéré', 'Préoccupant', 'Mauvais']
    }
    
    df = pd.DataFrame(schools_data)
    colors = ['#22c55e', '#84cc16', '#eab308', '#f97316', '#ef4444']
    
    fig = go.Figure(data=[
        go.Bar(
            y=df['École'],
            x=df['AQI'],
            orientation='h',
            marker_color=colors,
            text=df['Statut'],
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title="📍 Classement des Écoles par AQI",
        xaxis_title="Air Quality Index",
        height=400,
        showlegend=False
    )
    
    return fig


def calculate_air_quality_status(df):
    """Calcule le statut global de la qualité de l'air pour les autorités avec tous les indicateurs"""
    if df.empty:
        return None

    
    # Récupération des valeurs avec valeurs par défaut
    pm25 = df.get('pm02_corrected', [0]).iloc[0] if 'pm02_corrected' in df.columns else 0
    co2 = df.get('rco2_corrected', [400]).iloc[0] if 'rco2_corrected' in df.columns else 400
    temp = df.get('atmp_corrected', [25]).iloc[0] if 'atmp_corrected' in df.columns else 25
    humidity = df.get('rhum_corrected', [50]).iloc[0] if 'rhum_corrected' in df.columns else 50
    pm10 = df.get('pm10_corrected', [0]).iloc[0] if 'pm10_corrected' in df.columns else 0
    pm1 = df.get('pm01_corrected', [0]).iloc[0] if 'pm01_corrected' in df.columns else 0
    pm03 = df.get('pm03', [0]).iloc[0] if 'pm03' in df.columns else 0
    tvoc = df.get('tvoc', [0]).iloc[0] if 'tvoc' in df.columns else 0
    nox = df.get('noxIndex', [0]).iloc[0] if 'noxIndex' in df.columns else 0

    # Logique de classification simplifiée initalement pensee pour les parents

    # Score de risque global (seulement basé sur PM2.5 et CO2 ici)
    risk_level = 0
    
    # PM2.5 (particules fines)
    if pm25 > 35:
        risk_level += 3
    elif pm25 > 15:
        risk_level += 2
    elif pm25 > 10:
        risk_level += 1

    # CO2 (ventilation)
    if co2 > 1000:
        risk_level += 2
    elif co2 > 800:
        risk_level += 1

    # Statut qualitatif
    if risk_level == 0:
        status = "Excellente"
        color = "#4caf50"
        icon = "😊"
        message = "L'air est pur ! Environnement optimal."
        advice = "Aucune action requise."
    elif risk_level <= 2:
        status = "Bonne"
        color = "#8bc34a"
        icon = "🙂"
        message = "Qualité de l'air acceptable."
        advice = "Surveillance normale."
    elif risk_level <= 4:
        status = "Moyenne"
        color = "#ff9800"
        icon = "😐"
        message = "Qualité de l'air moyenne."
        advice = "Réduire l’activité physique en intérieur."
    elif risk_level <= 6:
        status = "Mauvaise"
        color = "#f44336"
        icon = "😷"
        message = "Pollution notable détectée."
        advice = "Renforcer l’aération ou installer purificateur."
    else:
        status = "Très mauvaise"
        color = "#d32f2f"
        icon = "😨"
        message = "Air fortement pollué !"
        advice = "Action urgente recommandée."

    # Résultat complet
    return {
        "status": status,
        "color": color,
        "icon": icon,
        "message": message,
        "advice": advice,
        "pm25": pm25,
        "co2": co2,
        "temp": temp,
        "humidity": humidity,
        "pm10": pm10,
        "pm1": pm1,
        "pm03": pm03,
        "tvoc": tvoc,
        "nox": nox,
        "last_update": datetime.now().strftime("%H:%M")
    }


def show_air_status_summary():
    """
    BLOC I: Affiche l'état de l'air aujourd'hui - Version autorite
    Grande carte récap' simplifiée, compréhensible en 5 secondes
    """
    
    st.markdown("## État de l'air aujourd'hui à l'école")
    
    # Récupération des données
    df = fetch_current_data(location_id, token)
    air_status = calculate_air_quality_status(df)
    
    if not air_status:
        st.error("❌ Impossible de récupérer les données de qualité de l'air")
        return
    
    # CSS pour la grande carte
    st.markdown("""
    <style>
    .air-status-card {{
        background: linear-gradient(135deg, {color}15, {color}08);
        border: 3px solid {color}40;
        border-radius: 25px;
        padding: 30px;
        text-align: center;
        margin: 20px 0;
        box-shadow: 0 10px 30px {color}20;
        position: relative;
        overflow: hidden;
    }}
    
    .status-icon {{
        font-size: 4rem;
        margin-bottom: 15px;
        animation: pulse 2s ease-in-out infinite;
    }}
    
    .status-title {{
        font-size: 2.5rem;
        font-weight: bold;
        color: {color};
        margin-bottom: 10px;
    }}
    
    .status-message {{
        font-size: 1.3rem;
        color: #333;
        margin-bottom: 15px;
        line-height: 1.5;
    }}
    
    .status-advice {{
        font-size: 1.1rem;
        color: #666;
        font-style: italic;
        margin-bottom: 20px;
    }}
    
    .school-info {{
        background: inherit;
        padding: 15px;
        border-radius: 15px;
        margin-top: 20px;
    }}
    
    .last-update {{
        font-size: 0.9rem;
        color: #888;
        margin-top: 10px;
    }}
    
    @keyframes pulse {{
        0%%, 100%% {{ transform: scale(1); }}
        50%% {{ transform: scale(1.1); }}
    }}
    </style>
    """.format(color=air_status["color"]), unsafe_allow_html=True)
    
    
    # Indicateurs rapides en bas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pm25_color = "#4caf50" if air_status["pm25"] <= 15 else "#ff9800" if air_status["pm25"] <= 35 else "#f44336"
        st.markdown(f'''
        <div style="background: {pm25_color}20; padding: 15px; border-radius: 15px; text-align: center;">
            <div style="font-size: 1.5rem;">🌫️</div>
            <div style="font-weight: bold; color: {pm25_color};">PM2.5</div>
            <div style="font-size: 1.2rem; font-weight: bold;">{air_status["pm25"]:.1f}</div>
            <div style="font-size: 0.8rem; color: #666;">µg/m³</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        co2_color = "#4caf50" if air_status["co2"] <= 800 else "#ff9800" if air_status["co2"] <= 1000 else "#f44336"
        st.markdown(f'''
        <div style="background: {co2_color}20; padding: 15px; border-radius: 15px; text-align: center;">
            <div style="font-size: 1.5rem;">💨</div>
            <div style="font-weight: bold; color: {co2_color};">CO₂</div>
            <div style="font-size: 1.2rem; font-weight: bold;">{air_status["co2"]:.0f}</div>
            <div style="font-size: 0.8rem; color: #666;">ppm</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        temp_color = "#4caf50" if 18 <= air_status["temp"] <= 26 else "#ff9800"
        st.markdown(f'''
        <div style="background: {temp_color}20; padding: 15px; border-radius: 15px; text-align: center;">
            <div style="font-size: 1.5rem;">🌡️</div>
            <div style="font-weight: bold; color: {temp_color};">Temp.</div>
            <div style="font-size: 1.2rem; font-weight: bold;">{air_status["temp"]:.1f}°C</div>
            <div style="font-size: 0.8rem; color: #666;">intérieur</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col4:
        humidity_color = "#4caf50" if 40 <= air_status["humidity"] <= 60 else "#ff9800"
        st.markdown(f'''
        <div style="background: {humidity_color}20; padding: 15px; border-radius: 15px; text-align: center;">
            <div style="font-size: 1.5rem;">💧</div>
            <div style="font-weight: bold; color: {humidity_color};">Humidité</div>
            <div style="font-size: 1.2rem; font-weight: bold;">{air_status["humidity"]:.0f}%</div>
            <div style="font-size: 0.8rem; color: #666;">relative</div>
        </div>
        ''', unsafe_allow_html=True)
        
        
    col5, col6, col7, col8, col9 = st.columns(5)

    with col5:
        pm10_color = "#4caf50" if air_status["pm10"] <= 30 else "#ff9800" if air_status["pm10"] <= 50 else "#f44336"
        st.markdown(f'''
        <div style="background: {pm10_color}20; padding: 15px; border-radius: 15px; text-align: center;">
        <div style="font-size: 1.5rem;">🌁</div>
        <div style="font-weight: bold; color: {pm10_color};">PM10</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{air_status["pm10"]:.1f}</div>
        <div style="font-size: 0.8rem; color: #666;">µg/m³</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col6:
        tvoc_color = "#4caf50" if air_status["tvoc"] <= 220 else "#ff9800" if air_status["tvoc"] <= 500 else "#f44336"
        st.markdown(f'''
        <div style="background: {tvoc_color}20; padding: 15px; border-radius: 15px; text-align: center;">
        <div style="font-size: 1.5rem;">🧪</div>
        <div style="font-weight: bold; color: {tvoc_color};">TVOC</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{air_status["tvoc"]:.0f}</div>
        <div style="font-size: 0.8rem; color: #666;">indice (μg/m³)</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col7:
        nox_color = "#4caf50" if air_status["nox"] <= 50 else "#ff9800" if air_status["nox"] <= 100 else "#f44336"
        st.markdown(f'''
        <div style="background: {nox_color}20; padding: 15px; border-radius: 15px; text-align: center;">
        <div style="font-size: 1.5rem;">🚛</div>
        <div style="font-weight: bold; color: {nox_color};">NOx</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{air_status["nox"]:.0f}</div>
        <div style="font-size: 0.8rem; color: #666;">indice (μg/m³)</div>
        </div>
        ''', unsafe_allow_html=True)
        
    with col8:
        pm1_color = "#4caf50" if air_status["pm1"] <= 10 else "#ff9800" if air_status["pm1"] <= 15 else "#f44336"
        st.markdown(f'''
        <div style="background: {pm1_color}20; padding: 15px; border-radius: 15px; text-align: center;">
        <div style="font-size: 1.5rem;">🌁</div>
        <div style="font-weight: bold; color: {pm1_color};">PM1</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{air_status["pm1"]:.1f}</div>
        <div style="font-size: 0.8rem; color: #666;">µg/m³</div>
        </div>
        ''', unsafe_allow_html=True)
    with col9:
        pm03_color = "#4caf50" if air_status["pm03"] <= 10000 else "#ff9800" if air_status["pm03"] <= 30000 else "#f44336"
        st.markdown(f'''
        <div style="background: {pm03_color}20; padding: 15px; border-radius: 15px; text-align: center;">
        <div style="font-size: 1.5rem;">🌬️</div>
        <div style="font-weight: bold; color: {pm03_color};">PM0.3</div>
        <div style="font-size: 1.2rem; font-weight: bold;">{air_status["pm03"]:.0f}</div>
        <div style="font-size: 0.8rem; color: #666;">compte particules</div>
        </div>
        ''', unsafe_allow_html=True)
        

def show_air_quality(location_id: str = "164928", token: str = "77a25676-a9ec-4a99-9137-f33e6776b590"):
    st.markdown("## Comment va l'air de notre école ?")

    df = fetch_current_data(location_id, token)
    iqa = calculer_iqa(df)
    resultats = iqa
    
    if not resultats:
        st.error("Impossible de calculer l'IQA.")
        return

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