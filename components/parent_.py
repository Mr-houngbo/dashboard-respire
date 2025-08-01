import streamlit as st
import pandas as pd
import requests
from urllib.parse import urlencode,quote_plus
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np
import os
import json
from twilio.rest import Client
import time



# Configuration (à adapter selon vos données)
BASE_URL = "https://api.airgradient.com/public/api/v1"
token = "77a25676-a9ec-4a99-9137-f33e6776b590"
location_id = "164928"
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data/air_quality')



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
                    Bienvenue sur l'espace parents de Respire
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Sous-titre engageant
            st.markdown(
                '<div class="subtitle">Découvrez comment va l\'air de l\'école de votre enfant aujourd\'hui !</div>',
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
    """Récupère les données actuelles de qualité de l'air"""
    endpoint = f"/locations/{location_id}/measures/current"
    params = {"token": token}
    full_url = f"{BASE_URL}{endpoint}?{urlencode(params)}"
    
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        data = response.json()
        
        if isinstance(data, dict):
            if "measures" in data:
                return pd.DataFrame([data["measures"]])
            else:
                return pd.DataFrame([data])
        elif isinstance(data, list):
            return pd.DataFrame(data)
        
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur lors de la récupération des données: {e}")
        return pd.DataFrame()


def calculate_air_quality_status(df):
    """Calcule le statut global de la qualité de l'air pour les parents"""
    if df.empty:
        return None
    
    # Récupération des valeurs principales
    pm25 = df.get('pm02_corrected', [0]).iloc[0] if 'pm02_corrected' in df.columns else 0
    co2 = df.get('rco2_corrected', [400]).iloc[0] if 'rco2_corrected' in df.columns else 400
    temp = df.get('atmp_corrected', [25]).iloc[0] if 'atmp_corrected' in df.columns else 25
    humidity = df.get('rhum_corrected', [50]).iloc[0] if 'rhum_corrected' in df.columns else 50
    
    # Logique de classification simplifiée pour les parents
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
    
    # Classification finale
    if risk_level == 0:
        status = "Excellente"
        color = "#4caf50"
        icon = "😊"
        message = "L'air est pur ! Votre enfant respire dans de bonnes conditions."
        advice = "Parfait pour toutes les activités à l'école."
    elif risk_level <= 2:
        status = "Bonne"
        color = "#8bc34a"
        icon = "🙂"
        message = "La qualité de l'air est satisfaisante."
        advice = "Conditions normales, rien à signaler."
    elif risk_level <= 4:
        status = "Moyenne"
        color = "#ff9800"
        icon = "😐"
        message = "L'air pourrait être mieux. Surveillez les symptômes chez votre enfant."
        advice = "Encouragez votre enfant à bien s'hydrater."
    elif risk_level <= 6:
        status = "Mauvaise"
        color = "#f44336"
        icon = "😷"
        message = "Air pollué. Soyez vigilant aux signes de gêne respiratoire."
        advice = "Contactez l'école si votre enfant tousse ou a du mal à respirer."
    else:
        status = "Très mauvaise"
        color = "#d32f2f"
        icon = "😨"
        message = "Air très pollué ! Surveillez attentivement votre enfant."
        advice = "Consultez un médecin si votre enfant présente des symptômes."
    
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
        "last_update": datetime.now().strftime("%H:%M")
    }


def show_air_status_summary(school_name="École Multinationale des Télécommunications"):
    """
    BLOC I: Affiche l'état de l'air aujourd'hui - Version parents
    Grande carte récap' simplifiée, compréhensible en 5 secondes
    """
    
    st.markdown("## 🏫 État de l'air aujourd'hui à l'école")
    
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
    
    # Grande carte de statut
    st.markdown(f'''
    <div class="air-status-card" style="
        background: linear-gradient(135deg, {air_status["color"]}15, {air_status["color"]}08);
        border: 3px solid {air_status["color"]}40;
        box-shadow: 0 10px 30px {air_status["color"]}20;
    ">
        <div class="status-icon">{air_status["icon"]}</div>
        <div class="status-title" style="color: {air_status["color"]};">
            Qualité: {air_status["status"]}
        </div>
        <div class="status-message">
            {air_status["message"]}
        </div>
        <div class="status-advice">
            💡 {air_status["advice"]}
        </div>
        <div class="school-info">
            <div style="font-size: 1.1rem; color: #333; font-weight: 600;">
                📍 {school_name}
            </div>
            <div class="last-update">
                🕐 Dernière mesure: {air_status["last_update"]}
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
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


def show_health_parameters():
    """
    BLOC II: Paramètres de santé critiques
    Indicateurs clés avec seuils explicites et explications pour les parents
    """
    
    st.markdown("## Paramètres de santé à surveiller")
    st.markdown("*Comprendre les indicateurs qui affectent la santé de votre enfant*")
    
    # Récupération des données
    df = fetch_current_data(location_id, token)
    if df.empty:
        st.warning("Données non disponibles pour le moment")
        return
    
    # Extraction des valeurs
    pm25 = df.get('pm02_corrected', [0]).iloc[0] if 'pm02_corrected' in df.columns else 0
    co2 = df.get('rco2_corrected', [400]).iloc[0] if 'rco2_corrected' in df.columns else 400
    temp = df.get('atmp_corrected', [25]).iloc[0] if 'atmp_corrected' in df.columns else 25
    humidity = df.get('rhum_corrected', [50]).iloc[0] if 'rhum_corrected' in df.columns else 50
    
    # CSS pour les cartes de paramètres
    st.markdown("""
    <style>
    .health-param-card {
        background: white;
        border-radius: 20px;
        padding: 25px;
        margin: 15px 0;
        box-shadow: 0 6px 25px rgba(0,0,0,0.1);
        border-left: 6px solid;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .health-param-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.15);
    }
    
    .param-header {
        display: flex;
        align-items: center;
        margin-bottom: 15px;
    }
    
    .param-icon {
        font-size: 2.5rem;
        margin-right: 15px;
    }
    
    .param-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin: 0;
    }
    
    .param-value {
        font-size: 2rem;
        font-weight: 900;
        margin: 10px 0;
    }
    
    .param-status {
        font-size: 1.1rem;
        font-weight: 600;
        padding: 8px 15px;
        border-radius: 25px;
        display: inline-block;
        margin: 10px 0;
    }
    
    .param-explanation {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        font-size: 0.95rem;
        line-height: 1.5;
    }
    
    .param-advice {
        background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
        padding: 15px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid #2196f3;
    }
    
    .threshold-indicator {
        display: flex;
        justify-content: space-between;
        background: #f5f5f5;
        padding: 10px;
        border-radius: 10px;
        margin: 10px 0;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Fonction pour déterminer le statut d'un paramètre
    def get_param_status(value, thresholds, unit=""):
        if value <= thresholds[0]:
            return {"status": "Excellent", "color": "#4caf50", "bg": "#e8f5e8"}
        elif value <= thresholds[1]:
            return {"status": "Bon", "color": "#8bc34a", "bg": "#f1f8e9"}
        elif value <= thresholds[2]:
            return {"status": "Moyen", "color": "#ff9800", "bg": "#fff3e0"}
        else:
            return {"status": "Préoccupant", "color": "#f44336", "bg": "#ffebee"}
    
    # 1. PM2.5 - Particules fines
    pm25_status = get_param_status(pm25, [12, 25, 35])
    st.markdown(f'''
    <div class="health-param-card" style="border-left-color: {pm25_status["color"]};">
        <div class="param-header">
            <div class="param-icon">🌫️</div>
            <div>
                <div class="param-title" style="color: {pm25_status["color"]};">PM2.5 - Particules fines</div>
                <div style="color: #666; font-size: 0.9rem;">Poussières invisibles dans l'air</div>
            </div>
        </div>
        <div class="param-value" style="color: {pm25_status["color"]};">
            {pm25:.1f} µg/m³
        </div>
        <div class="param-status" style="background: {pm25_status["bg"]}; color: {pm25_status["color"]};">
            {pm25_status["status"]}
        </div>
        <div class="param-explanation">
            <h4> Qu'est-ce que c'est ?</h4>
            Les PM2.5 sont des particules si petites qu'elles peuvent pénétrer profondément dans les poumons de votre enfant. 
            Elles proviennent de la pollution des véhicules, de la poussière, ou des fumées.
            <h4>⚠️ Effets sur la santé</h4>
            <b>Exposition faible:</b> Aucun problème<br>
            <b>Exposition moyenne:</b> Peut causer toux, irritation des yeux<br>
            <b>Exposition élevée:</b> Difficultés respiratoires, fatigue
        </div>
        <div class="threshold-indicator">
            <span style="color: #4caf50;">🟢 Excellent: 0-12</span>
            <span style="color: #ff9800;">🟡 Moyen: 12-35</span>
            <span style="color: #f44336;">🔴 Élevé: >35</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Conseil spécifique PM2.5
    if pm25 > 35:
        advice = "🚨 <b>Action recommandée:</b> Gardez votre enfant à l'intérieur, fermez les fenêtres. Consultez un médecin s'il tousse."
    elif pm25 > 25:
        advice = "⚠️ <b>Conseil:</b> Limitez les activités extérieures intenses. Surveillez si votre enfant tousse ou a les yeux qui piquent."
    else:
        advice = " <b>Parfait:</b> Votre enfant peut faire toutes ses activités normalement."
    
    st.markdown(f'<div class="param-advice">{advice}</div>', unsafe_allow_html=True)
    
    # st.markdown("---")
    
    # 2. CO₂ - Qualité de l'air intérieur
    co2_status = get_param_status(co2, [600, 800, 1000])
    st.markdown(f'''
    <div class="health-param-card" style="border-left-color: {co2_status["color"]};">
        <div class="param-header">
            <div class="param-icon">💨</div>
            <div>
                <div class="param-title" style="color: {co2_status["color"]};">CO₂ - Dioxyde de carbone</div>
                <div style="color: #666; font-size: 0.9rem;">Indicateur de ventilation en classe</div>
            </div>
        </div>
        <div class="param-value" style="color: {co2_status["color"]};">
            {co2:.0f} ppm
        </div>
        <div class="param-status" style="background: {co2_status["bg"]}; color: {co2_status["color"]};">
            {co2_status["status"]}
        </div>
        <div class="param-explanation">
            <h4> Qu'est-ce que c'est ?</h4>
            Le CO₂ nous indique si la classe est bien aérée. Quand il y a beaucoup d'élèves dans une pièce fermée, 
            le taux de CO₂ augmente et l'oxygène diminue.
            <h4>⚠️ Effets sur la santé</h4>
            <b>Taux normal:</b> Concentration et apprentissage optimaux<br>
            <b>Taux élevé:</b> Fatigue, somnolence, difficultés de concentration<br>
            <b>Taux très élevé:</b> Maux de tête, sensation d'étouffement
        </div>
        <div class="threshold-indicator">
            <span style="color: #4caf50;">🟢 Excellent: <600</span>
            <span style="color: #ff9800;">🟡 Moyen: 600-1000</span>
            <span style="color: #f44336;">🔴 Élevé: >1000</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Conseil spécifique CO₂
    if co2 > 1000:
        advice = "🚨 <b>Action recommandée:</b> La classe manque d'air frais. Contactez l'école pour améliorer la ventilation."
    elif co2 > 800:
        advice = "⚠️ <b>Conseil:</b> La ventilation pourrait être améliorée. Votre enfant pourrait être plus fatigué que d'habitude."
    else:
        advice = " <b>Parfait:</b> La classe est bien aérée, conditions idéales pour l'apprentissage."
    
    st.markdown(f'<div class="param-advice">{advice}</div>', unsafe_allow_html=True)
    
    # st.markdown("---")
    
    # 3. Température
    temp_status = get_param_status(abs(temp - 22), [2, 4, 6])  # Écart par rapport à 22°C idéal
    st.markdown(f'''
    <div class="health-param-card" style="border-left-color: {temp_status["color"]};">
        <div class="param-header">
            <div class="param-icon">🌡️</div>
            <div>
                <div class="param-title" style="color: {temp_status["color"]};">Température intérieure</div>
                <div style="color: #666; font-size: 0.9rem;">Confort thermique en classe</div>
            </div>
        </div>
        <div class="param-value" style="color: {temp_status["color"]};">
            {temp:.1f}°C
        </div>
        <div class="param-status" style="background: {temp_status["bg"]}; color: {temp_status["color"]};">
            {temp_status["status"]}
        </div>
        <div class="param-explanation">
            <h4> Pourquoi c'est important ?</h4>
            Une température appropriée aide votre enfant à rester concentré et confortable. 
            Trop chaud ou trop froid peut affecter son attention et son bien-être.
            <h4>⚠️ Effets sur le confort</h4>
            <b>18-24°C:</b> Température idéale pour l'apprentissage<br>
            <b>Trop chaud (>26°C):</b> Fatigue, somnolence<br>
            <b>Trop froid (<18°C):</b> Difficultés de concentration
        </div>        
        <div class="threshold-indicator">
            <span style="color: #4caf50;">🟢 Idéal: 20-24°C</span>
            <span style="color: #ff9800;">🟡 Acceptable: 18-26°C</span>
            <span style="color: #f44336;">🔴 Inconfortable: <18 ou >26°C</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # st.markdown("---")
    
    # 4. Humidité
    humidity_status = get_param_status(abs(humidity - 50), [10, 20, 30])  # Écart par rapport à 50% idéal
    st.markdown(f'''
    <div class="health-param-card" style="border-left-color: {humidity_status["color"]};">
        <div class="param-header">
            <div class="param-icon">💧</div>
            <div>
                <div class="param-title" style="color: {humidity_status["color"]};">Humidité relative</div>
                <div style="color: #666; font-size: 0.9rem;">Taux d'humidité dans l'air</div>
            </div>
        </div>
        <div class="param-value" style="color: {humidity_status["color"]};">
            {humidity:.0f}%
        </div>        
        <div class="param-status" style="background: {humidity_status["bg"]}; color: {humidity_status["color"]};">
            {humidity_status["status"]}
        </div>
        <div class="param-explanation">
            <h4> Qu'est-ce que c'est ?</h4>
            L'humidité influence la propagation des virus et le confort respiratoire. 
            Un air trop sec ou trop humide peut causer des problèmes.
            <h4>⚠️ Effets sur la santé</h4>
            <b>40-60%:</b> Idéal pour la santé respiratoire<br>
            <b>Trop sec (<40%):</b> Irritation des voies respiratoires, nez sec<br>
            <b>Trop humide (>60%):</b> Favorise moisissures et virus
        </div>
        <div class="threshold-indicator">
            <span style="color: #4caf50;">🟢 Idéal: 40-60%</span>
            <span style="color: #ff9800;">🟡 Acceptable: 30-70%</span>
            <span style="color: #f44336;">🔴 Problématique: <30% ou >70%</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)


def render_bloc_tendances(location_id: str = location_id, school_name="ESMT"):
    """
    Bloc III - Tendances pour la page Parent
    Utilise les fonctions existantes et les données CSV locales
    """
    
    st.markdown("### **Évolution cette semaine**")
    
    # Container principal avec style
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); 
                    padding: 20px; border-radius: 15px; margin-bottom: 20px; 
                    border: 1px solid #dee2e6;">
        """, unsafe_allow_html=True)
        
        # === RÉCUPÉRATION DES DONNÉES ===
        csv_filename = f"{DATA_DIR}/{location_id}.csv"
        
        # Vérifier si le fichier CSV existe
        if os.path.exists(csv_filename):
            try:
                df_historical = pd.read_csv(csv_filename)
                df_historical['date'] = pd.to_datetime(df_historical['Local Date/Time'])
                
                # Prendre les 7 derniers jours
                recent_data = df_historical.tail(7).copy()
                
                if len(recent_data) == 0:
                    st.warning("Aucune donnée historique disponible pour cette école.")
                    st.markdown("</div>", unsafe_allow_html=True)
                    return
                    
            except Exception as e:
                st.error(f"Erreur lors du chargement des données : {e}")
                st.markdown("</div>", unsafe_allow_html=True)
                return
        else:
            st.warning(f"Fichier de données non trouvé : {csv_filename}")
            st.markdown("</div>", unsafe_allow_html=True)
            return
        
        # Colonnes pour organiser l'affichage
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # === MINI GRAPHIQUE D'ÉVOLUTION ===
            st.markdown("#### **Qualité de l'air - 7 derniers jours**")
            
            # Utiliser les vraies colonnes de tes données
            pm25_col = 'PM2.5 (μg/m³) corrected' if 'PM2.5 (μg/m³) corrected' in recent_data.columns else 'pm25'
            co2_col = 'CO2 (ppm) corrected' if 'CO2 (ppm) corrected' in recent_data.columns else 'co2'
            temp_col = 'Temperature (°C) corrected' if 'Temperature (°C) corrected' in recent_data.columns else 'temperature'
            humidity_col = 'Humidity (%) corrected' if 'Humidity (%) corrected' in recent_data.columns else 'humidity'
            
            # Fonction pour déterminer le statut (utilise ta logique existante)
            def get_air_quality_status_from_pm25(pm25):
                if pm25 <= 10:
                    return "Excellente", "#4caf50"
                elif pm25 <= 15:
                    return "Bonne", "#8bc34a"
                elif pm25 <= 35:
                    return "Moyenne", "#ff9800"
                elif pm25 <= 55:
                    return "Mauvaise", "#f44336"
                else:
                    return "Très mauvaise", "#d32f2f"
            
            # Vérifier que la colonne PM2.5 existe
            if pm25_col in recent_data.columns:
                # Calcul des statuts pour chaque jour
                recent_data['status'], recent_data['color'] = zip(*recent_data[pm25_col].apply(get_air_quality_status_from_pm25))
                
                # Graphique sparkline avec Plotly
                fig = go.Figure()
                
                # Ligne principale
                fig.add_trace(go.Scatter(
                    x=recent_data['date'],
                    y=recent_data[pm25_col],
                    mode='lines+markers',
                    line=dict(color='#007bff', width=3),
                    marker=dict(size=8, color=recent_data['color']),
                    name='PM2.5 (µg/m³)',
                    hovertemplate='<b>%{x|%d/%m}</b><br>' +
                                 'PM2.5: %{y:.1f} µg/m³<br>' +
                                 '<extra></extra>'
                ))
                
                # Zones de seuils (selon ta logique)
                fig.add_hline(y=10, line_dash="dash", line_color="#4caf50", 
                             annotation_text="Seuil Excellent", annotation_position="right")
                fig.add_hline(y=15, line_dash="dash", line_color="#8bc34a", 
                             annotation_text="Seuil Bon", annotation_position="right")
                fig.add_hline(y=35, line_dash="dash", line_color="#ff9800", 
                             annotation_text="Seuil Moyen", annotation_position="right")
                
                fig.update_layout(
                    height=300,
                    margin=dict(l=0, r=0, t=20, b=0),
                    showlegend=False,
                    xaxis=dict(
                        showgrid=True,
                        gridcolor='lightgray',
                        tickformat='%d/%m'
                    ),
                    yaxis=dict(
                        title="PM2.5 (µg/m³)",
                        showgrid=True,
                        gridcolor='lightgray'
                    ),
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # === RÉSUMÉ DE LA SEMAINE ===
                st.markdown("#### **Résumé de la semaine**")
                
                # Calculs statistiques sur les vraies données
                avg_pm25 = recent_data[pm25_col].mean()
                max_pm25 = recent_data[pm25_col].max()
                days_over_threshold = len(recent_data[recent_data[pm25_col] > 35])
                
                # Affichage en colonnes
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                with col_stat1:
                    status_avg = "Correct" if avg_pm25 <= 25 else "Élevé"
                    delta_color = "normal" if avg_pm25 <= 25 else "inverse"
                    st.metric(
                        label="📊 Moyenne PM2.5", 
                        value=f"{avg_pm25:.1f} µg/m³",
                        delta=status_avg,
                        delta_color=delta_color
                    )
                
                with col_stat2:
                    status_max = "Acceptable" if max_pm25 <= 35 else "Préoccupant"
                    delta_color = "normal" if max_pm25 <= 35 else "inverse"
                    st.metric(
                        label="📈 Pic maximum", 
                        value=f"{max_pm25:.1f} µg/m³",
                        delta=status_max,
                        delta_color=delta_color
                    )
                
                with col_stat3:
                    status_days = "Aucun souci" if days_over_threshold == 0 else "À surveiller"
                    delta_color = "normal" if days_over_threshold == 0 else "inverse"
                    st.metric(
                        label="⚠️ Jours d'alerte", 
                        value=f"{days_over_threshold} jour(s)",
                        delta=status_days,
                        delta_color=delta_color
                    )
            else:
                st.error(f"Colonne PM2.5 non trouvée dans les données. Colonnes disponibles : {list(recent_data.columns)}")
        
        with col2:
            
            # === PLAGES HORAIRES CRITIQUES ===
            st.markdown("#### **Analyse par jour**")
            
            # Analyser chaque jour des données réelles
            if pm25_col in recent_data.columns:
                for idx, row in recent_data.iterrows():
                    
                    jours_fr = {                                      # Pour la convertion du Nom du jour en francais 
                            "Monday": "Lundi",
                            "Tuesday": "Mardi",
                            "Wednesday": "Mercredi",
                            "Thursday": "Jeudi",
                            "Friday": "Vendredi",
                            "Saturday": "Samedi",
                            "Sunday": "Dimanche"
                            }
                    date_str = jours_fr[row['date'].strftime('%A')]   # Nom du jour
                                                
                    
                    pm25_val = row[pm25_col]
                    # Déterminer le statut du jour
                    if pm25_val <= 15:
                        icon = ""
                        level = "Bon"
                        color = "#28a745"
                        message = f"{date_str} : {icon} Journée saine (PM2.5: {pm25_val:.1f})"
                    elif pm25_val <= 35:
                        icon = "⚡"
                        level = "Moyen"
                        color = "#ffc107"
                        message = f"{date_str} : {icon} Qualité correcte (PM2.5: {pm25_val:.1f})"
                    else:
                        icon = "⚠️"
                        level = "Élevé"
                        color = "#dc3545"
                        message = f"{date_str} : {icon} Pollution détectée (PM2.5: {pm25_val:.1f})"
                    st.markdown(f"""
                    <div style="background-color: {color}15; 
                               border-left: 4px solid {color}; 
                               padding: 8px 12px; margin: 5px 0; border-radius: 5px;">
                        {message}
                    </div>
                    """, unsafe_allow_html=True)
            
            # === ALERTES AUTOMATIQUES ===
            st.markdown("#### 🔔 Alertes de la semaine")
            
            if pm25_col in recent_data.columns:
                days_over_threshold = len(recent_data[recent_data[pm25_col] > 35])
                
                if days_over_threshold > 0:
                    max_pollution_day = recent_data.loc[recent_data[pm25_col].idxmax()]
                    st.markdown(f"""
                    <div style="background-color: #dc354520; border: 1px solid #dc3545; 
                               border-radius: 8px; padding: 15px; margin: 10px 0;">
                        <strong>⚠️ {days_over_threshold} jour(s) avec dépassement de seuil</strong><br>
                        <small>Pic de {max_pollution_day[pm25_col]:.1f} µg/m³ le {max_pollution_day['date'].strftime('%d/%m')}. 
                        Surveillez les symptômes respiratoires.</small>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div style="background-color: #28a74520; border: 1px solid #28a745; 
                               border-radius: 8px; padding: 15px; margin: 10px 0;">
                        <strong> Aucune alerte cette semaine</strong><br>
                        <small>La qualité de l'air est restée dans les normes acceptables.</small>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # === INTERPRÉTATION AUTOMATIQUE (utilise ta logique existante) ===
        st.markdown("#### **Ce que cela signifie pour votre enfant**")
        
        if pm25_col in recent_data.columns:
            avg_pm25 = recent_data[pm25_col].mean()
            
            # Générer des conseils basés sur ta logique calculate_air_quality_status
            if avg_pm25 <= 15:
                interpretation = """
                🧠 Excellente nouvelle ! L'air à l'école a été globalement de très bonne qualité cette semaine. 
                Votre enfant peut participer à toutes les activités sans contrainte particulière.
                """
                advice_color = "#4caf50"
            elif avg_pm25 <= 35:
                interpretation = """
                ⚠️ Qualité correcte mais à surveiller. Quelques variations ont été observées. 
                Encouragez votre enfant à bien s'hydrater et surveillez d'éventuels symptômes (toux, fatigue).
                """
                advice_color = "#ff9800"
            else:
                interpretation = """
                🚨 Attention requise. La qualité de l'air a été préoccupante plusieurs jours. 
                Consultez un médecin si votre enfant présente toux persistante, maux de tête ou fatigue inhabituelle.
                """
                advice_color = "#f44336"
            st.markdown(f"""
            <div style="background-color: {advice_color}15; border: 2px solid {advice_color}; 
                       border-radius: 10px; padding: 20px; margin: 15px 0;">
                {interpretation}
            </div>
            """, unsafe_allow_html=True)


def render_bloc_conseils(location_id: str = location_id, token: str = token, school_name="ESMT"):
    """
    Bloc IV - Conseils/Actions préventives pour la page Parent
    Conseils personnalisés selon la qualité de l'air à l'école de l'enfant
    """
    
    st.markdown("### 🧩 **Conseils & Actions préventives**")
    
    # Récupérer les données actuelles de l'école
    current_data = fetch_current_data(location_id, token)
    air_status = calculate_air_quality_status(current_data) if not current_data.empty else None
    
    # Container principal
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f0f8ff 0%, #e6f3ff 100%); 
                    padding: 25px; border-radius: 15px; margin-bottom: 20px; 
                    border: 1px solid #b3d9ff;">
        """, unsafe_allow_html=True)
        
        if air_status:
            # === SECTION 1: QUE PUIS-JE FAIRE À LA MAISON ? ===
            st.markdown("#### 🏠 **Que puis-je faire à la maison ?**")
            
            # Conseils personnalisés selon la qualité de l'air à l'école
            pm25 = air_status['pm25']
            co2 = air_status['co2']
            status = air_status['status']
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.markdown("##### 🌅 **Préparation du matin**")
                
                if pm25 <= 15:  # Air de bonne qualité à l'école
                    morning_tips = [
                        "✅ <strong>Petit-déjeuner copieux</strong> - Votre enfant peut dépenser son énergie normalement",
                        "🚪 <strong>Fenêtres ouvertes</strong> - Aérez sa chambre avant le départ pour l'école",
                        "👕 <strong>Habits légers</strong> - Pas de protection particulière nécessaire",
                        "💧 <strong>Gourde d'eau</strong> - Hydratation normale suffit"
                    ]
                    tips_color = "#d4edda"
                    border_color = "#28a745"
                elif pm25 <= 35:  # Air moyen à l'école
                    morning_tips = [
                        "⚠️ <strong>Petit-déjeuner riche</strong> - Donnez-lui des forces pour la journée",
                        "🏠 <strong>Aération matinale</strong> - Ouvrez 5-10 min quand l'air extérieur est plus frais",
                        "🧥 <strong>Veste légère</strong> - Au cas où l'école limite les sorties",
                        "💧 <strong>Grande gourde</strong> - Encouragez à boire plus que d'habitude"
                    ]
                    tips_color = "#fff3cd"
                    border_color = "#ffc107"
                else:  # Air pollué à l'école
                    morning_tips = [
                        "🚨 <strong>Petit-déjeuner énergétique</strong> - Fruits, céréales pour renforcer ses défenses",
                        "🚪 <strong>Fenêtres fermées</strong> - Gardez l'air intérieur propre avant le départ",
                        "😷 <strong>Masque dans le sac</strong> - Si l'école le demande ou si trajet à pied",
                        "💧 <strong>Double hydratation</strong> - Prévoyez une grande gourde + thermos"
                    ]
                    tips_color = "#f8d7da"
                    border_color = "#dc3545"
                
                # Affichage des conseils
                for tip in morning_tips:
                    st.markdown(f"""
                    <div style="background-color: {tips_color}; border-left: 4px solid {border_color}; 
                               padding: 10px; margin: 8px 0; border-radius: 5px;">
                        {tip}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                st.markdown("##### 🌆 **Après l'école**")
                
                if pm25 <= 15:  # Air de bonne qualité
                    evening_tips = [
                        "🏃 <strong>Activités extérieures</strong> - Parfait pour jouer dehors après l'école",
                        "🛁 <strong>Douche normale</strong> - Pas de précautions particulières",
                        "🥗 <strong>Repas équilibré</strong> - Alimentation normale suffit",
                        "😴 <strong>Coucher habituel</strong> - Son organisme n'est pas stressé"
                    ]
                    tips_color = "#d4edda"
                    border_color = "#28a745"
                elif pm25 <= 35:  # Air moyen
                    evening_tips = [
                        "🏠 <strong>Activités à l'intérieur</strong> - Privilégiez les jeux calmes en rentrant",
                        "🛁 <strong>Douche rapide</strong> - Rincez le visage et les mains",
                        "🍊 <strong>Fruits vitaminés</strong> - Oranges, kiwis pour renforcer l'immunité",
                        "👂 <strong>Écoutez-le</strong> - Demandez s'il a ressenti de la fatigue ou gêne"
                    ]
                    tips_color = "#fff3cd"
                    border_color = "#ffc107"
                else:  # Air pollué
                    evening_tips = [
                        "🚪 <strong>Rentrez vite</strong> - Évitez les détours et jeux extérieurs",
                        "🛁 <strong>Douche obligatoire</strong> - Cheveux et visage pour éliminer les particules",
                        "🥕 <strong>Alimentation anti-oxydante</strong> - Légumes colorés, thé léger",
                        "🩺 <strong>Surveillance</strong> - Vérifiez toux, maux de tête ou fatigue inhabituelle"
                    ]
                    tips_color = "#f8d7da"
                    border_color = "#dc3545"
                
                # Affichage des conseils du soir
                for tip in evening_tips:
                    st.markdown(f"""
                    <div style="background-color: {tips_color}; border-left: 4px solid {border_color}; 
                               padding: 10px; margin: 8px 0; border-radius: 5px;">
                        {tip}
                    </div>
                    """, unsafe_allow_html=True)
            
            # === SECTION 2: QUAND DOIS-JE M'INQUIÉTER ? ===
            st.markdown("---")
            st.markdown("#### 🩺 **Quand dois-je m'inquiéter ?**")
            
            # Seuils d'alerte personnalisés selon l'école
            col_alert1, col_alert2 = st.columns([1, 1])
            
            with col_alert1:
                st.markdown("##### ⚠️ **Symptômes à surveiller**")
                
                if pm25 <= 15:
                    alert_message = """
                    <div style="background-color: #d4edda; border: 2px solid #28a745; 
                               border-radius: 10px; padding: 15px;">
                        <strong>😊 Situation rassurante</strong><br>
                        L'air à l'école est de bonne qualité. Les symptômes suivants sont peu probables 
                        mais restez attentif à :
                        <ul>
                            <li>Toux persistante (+ de 2 jours)</li>
                            <li>Fatigue inhabituelle</li>
                            <li>Maux de tête fréquents</li>
                        </ul>
                    </div>
                    """
                elif pm25 <= 35:
                    alert_message = """
                    <div style="background-color: #fff3cd; border: 2px solid #ffc107; 
                               border-radius: 10px; padding: 15px;">
                        <strong>⚠️ Vigilance modérée</strong><br>
                        L'air à l'école est correct mais surveillez ces signaux :
                        <ul>
                            <li><strong>Toux sèche</strong> en rentrant de l'école</li>
                            <li><strong>Yeux qui piquent</strong> ou nez qui coule</li>
                            <li><strong>Fatigue</strong> après les récréations</li>
                            <li><strong>Difficultés de concentration</strong> en classe</li>
                        </ul>
                    </div>
                    """
                else:
                    alert_message = """
                    <div style="background-color: #f8d7da; border: 2px solid #dc3545; 
                               border-radius: 10px; padding: 15px;">
                        <strong>🚨 Surveillance renforcée</strong><br>
                        L'air à l'école est pollué. Consultez un médecin si votre enfant présente :
                        <ul>
                            <li><strong>Toux persistante</strong> (surtout le soir)</li>
                            <li><strong>Essoufflement</strong> inhabituel</li>
                            <li><strong>Maux de tête</strong> fréquents</li>
                            <li><strong>Irritation des yeux/gorge</strong></li>
                            <li><strong>Fatigue extrême</strong> au retour</li>
                        </ul>
                    </div>
                    """
                
                st.markdown(alert_message, unsafe_allow_html=True)
            
            with col_alert2:
                st.markdown("##### 📞 **Actions à entreprendre**")
                
                # Actions spécifiques selon le niveau de pollution à l'école
                if pm25 <= 15:
                    action_items = [
                        ("💬", "<strong>Dialogue avec l'enfant</strong>", "Demandez-lui comment il se sent à l'école"),
                        ("📚", "<strong>Suivi scolaire normal</strong>", "Aucune restriction d'activité nécessaire"),
                        ("🏥", "<strong>Médecin si nécessaire</strong>", "Seulement si symptômes inhabituels persistent pendant plusieurs jours ")
                    ]
                    action_color = "#28a745"
                elif pm25 <= 35:
                    action_items = [
                        ("📞", "<strong>Contact avec l'école</strong>", "Demandez si d'autres enfants ont des symptômes"),
                        ("💧", "<strong>Hydratation renforcée</strong>", "Encouragez à boire plus pendant les pauses"),
                        ("👨‍⚕️", "<strong>Médecin si symptoms</strong>", "Consultation si toux + fatigue > 3 jours"),
                        ("📝", "<strong>Journal des symptômes</strong>", "Notez les moments où l'enfant tousse")
                    ]
                    action_color = "#ffc107"
                else:
                    action_items = [
                        ("🚨", "<strong>Contact école immédiat</strong>", "Signalez les symptômes à l'enseignant"),
                        ("🏥", "<strong>Médecin rapidement</strong>", "Consultation si symptômes > 24h"),
                        ("📱", "<strong>Alertes pollution</strong>", "Installez une app météo avec qualité de l'air"),
                        ("🏠", "<strong>Adaptation à domicile</strong>", "Purificateur d'air si possible"),
                        ("📋", "<strong>Suivi quotidien</strong>", "Température, toux, énergie de l'enfant")
                    ]
                    action_color = "#dc3545"
                
                for icon, title, description in action_items:
                    st.markdown(f"""
                    <div style="border-left: 4px solid {action_color}; padding: 10px; margin: 8px 0;">
                        <strong>{icon} {title}</strong><br>
                        <small>{description}</small>
                    </div>
                    """, unsafe_allow_html=True)
            
            # === SECTION 3: RESSOURCES ET CONTACTS ===
            st.markdown("---")
            st.markdown("#### 📚 **Ressources utiles**")
            
            col_resource1, col_resource2 = st.columns([1, 1])
            
            with col_resource1:
                st.markdown("""
                ##### 📖 **En savoir plus**
                
                - 🫁 **Qu'est-ce que le PM2.5 ?** → Particules fines qui pénètrent dans les poumons
                - 🏫 **Pourquoi surveiller à l'école ?** → Les enfants y passent 6-8h par jour
                - 💨 **CO₂ et concentration** → Trop de CO₂ fatigue et réduit l'attention
                - 🌡️ **Température et confort** → Impact sur l'apprentissage
                """)
            
            with col_resource2:
                st.markdown(f"""
                ##### 📞 **Contacts d'urgence**
                
                - 🏫 <strong>École</strong> : {school_name}
                - 📞 <strong>Direction</strong> : [Ici on mets le numero de Bernard T.]
                - 🚑 <strong>SAMU</strong> : 15 (urgences médicales)
                - 🏥 <strong>Centre de santé local</strong> : [Ici on mets le numero de M. Laminou S L.]
                
                <div style="background-color: #e3f2fd; padding: 10px; border-radius: 5px; margin-top: 10px;">
                <strong>💡 Conseil :</strong> Gardez ces numéros dans votre téléphone !
                </div>
                """, unsafe_allow_html=True)
        
        else:
            # Si pas de données disponibles
            st.warning("⚠️ Données de qualité de l'air non disponibles pour le moment.")
            st.markdown("""
            **En attendant, voici quelques conseils généraux :**
            - 💧 Encouragez votre enfant à bien s'hydrater à l'école
            - 🧼 Rappellez-lui de se laver les mains régulièrement
            - 👂 Demandez-lui comment il se sent après l'école
            - 📞 Contactez l'école si vous avez des préoccupations
            """)
        
        st.markdown("</div>", unsafe_allow_html=True)




#================================================ SECTION D'ENVOI DE SMS AUTO ==============================================

class SMSAlertSystem:
    """
    Système d'alertes SMS pour les parents
    Gère l'envoi automatique de notifications selon la qualité de l'air à l'école
    """
    
    def __init__(self, contacts_file="parents_contacts.txt", config_file="sms_config.json"):
        self.contacts_file = contacts_file
        self.config_file = config_file
        self.sent_alerts_file = "sent_alerts.json"
        
        # Configuration par défaut
        self.default_config = {
            "sms_provider": "twilio",  # ou "orange_sms_senegal", "free_sms"
            "twilio_account_sid": "ACabfcb37ffd779fca3dfdb47a028352a7",
            "twilio_auth_token": "8699c97724e7c3458fb5a0f79dffbc5e",
            "twilio_phone_number": "+17754297649",
            "orange_api_key": "",
            "max_sms_per_day": 5,
            "quiet_hours_start": "21:00",
            "quiet_hours_end": "07:00",
            "pm25_alert_threshold": 35,
            "pm25_danger_threshold": 55,
            "co2_alert_threshold": 1000,
            "enabled": True
        }
        
        self.load_config()
        self.load_sent_alerts()
    
    def load_config(self):
        """Charge la configuration SMS"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = self.default_config.copy()
                self.save_config()
        except Exception as e:
            st.error(f"Erreur chargement config SMS : {e}")
            self.config = self.default_config.copy()
    
    def save_config(self):
        """Sauvegarde la configuration"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Erreur sauvegarde config : {e}")
    
    def load_sent_alerts(self):
        """Charge l'historique des alertes envoyées"""
        try:
            if os.path.exists(self.sent_alerts_file):
                with open(self.sent_alerts_file, 'r', encoding='utf-8') as f:
                    self.sent_alerts = json.load(f)
            else:
                self.sent_alerts = {}
        except:
            self.sent_alerts = {}
    
    
    
    def save_sent_alerts(self):
        """Sauvegarde l'historique des alertes"""
        try:
            with open(self.sent_alerts_file, 'w', encoding='utf-8') as f:
                json.dump(self.sent_alerts, f, indent=2, ensure_ascii=False)
        except Exception as e:
            st.error(f"Erreur sauvegarde alertes : {e}")
    
    
    
    def load_parent_contacts(self):
        """
        Charge la liste des contacts parents depuis le fichier txt
        Format attendu : nom,telephone,enfant,classe
        """
        contacts = []
        try:
            if os.path.exists(self.contacts_file):
                with open(self.contacts_file, 'r', encoding='utf-8') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):  # Ignorer lignes vides et commentaires
                            parts = line.split(',')
                            if len(parts) >= 4:
                                contacts.append({
                                    'nom': parts[0].strip(),
                                    'telephone': parts[1].strip(),
                                    'enfant': parts[2].strip(),
                                    'classe': parts[3].strip(),
                                    'line_num': line_num
                                })
                            else:
                                st.warning(f"Ligne {line_num} mal formatée : {line}")
            else:
                st.warning(f"Fichier {self.contacts_file} non trouvé")
        except Exception as e:
            st.error(f"Erreur lecture contacts : {e}")
        
        return contacts
    
    
    
    
    def is_quiet_hours(self):
        """Vérifie si on est dans les heures de silence"""
        now = datetime.now().time()
        start_time = datetime.strptime(self.config['quiet_hours_start'], '%H:%M').time()
        end_time = datetime.strptime(self.config['quiet_hours_end'], '%H:%M').time()
        
        if start_time <= end_time:
            return start_time <= now <= end_time
        else:  # Cas où les heures passent minuit
            return now >= start_time or now <= end_time
    
    
    
    
    def can_send_alert(self, alert_type, phone_number):
        """Vérifie si on peut envoyer une alerte (anti-spam)"""
        today = datetime.now().strftime('%Y-%m-%d')
        key = f"{phone_number}_{alert_type}_{today}"
        
        # Vérifier si déjà envoyé aujourd'hui
        if key in self.sent_alerts:
            return False
        
        # Vérifier le nombre total d'SMS envoyés aujourd'hui
        daily_count = sum(1 for k in self.sent_alerts.keys() 
                         if k.startswith(f"{phone_number}_") and k.endswith(f"_{today}"))
        
        return daily_count < self.config['max_sms_per_day']
    
    
    
    
    def generate_alert_message(self, alert_type, air_data, school_name, child_name):
        """Génère le message d'alerte personnalisé"""
        pm25 = air_data.get('pm25', 0)
        co2 = air_data.get('co2', 400)
        status = air_data.get('status', 'Inconnue')
        
        messages = {
            'pollution_high': f"""🚨 ALERTE POLLUTION - {school_name}
                Bonjour, l'air à l'école de {child_name} est très pollué (PM2.5: {pm25:.1f}).
                Surveillez: toux, fatigue, irritations.
                Hydratation++ recommandée.
                Dashboard: [lien]""",
                            
            'pollution_moderate': f"""⚠️ Air dégradé - {school_name}
                L'air à l'école de {child_name} s'est dégradé (PM2.5: {pm25:.1f}).
                Surveillez son état en rentrant.
                Plus d'infos: [lien dashboard]""",
                            
            'co2_high': f"""💨 Ventilation insuffisante - {school_name}
                Le CO2 est élevé dans la classe de {child_name} ({co2:.0f} ppm).
                Peut causer fatigue/difficultés de concentration.
                L'école a été informée.""",
                            
            'back_to_normal': f"""✅ Air redevenu sain - {school_name}
                Bonne nouvelle ! L'air à l'école de {child_name} est redevenu bon.
                Activités normales possibles.
                Merci de votre vigilance.""",
                            
            'daily_report': f"""📊 Rapport quotidien - {school_name}
                Air aujourd'hui: {status}
                PM2.5 moyen: {pm25:.1f}
                {child_name} a respiré dans de {'bonnes' if pm25 <= 15 else 'moyennes' if pm25 <= 35 else 'mauvaises'} conditions.
                Détails: [lien]""",
                            
            'weekly_summary': f"""📈 Résumé de la semaine - {school_name}
                L'air à l'école de {child_name} cette semaine:
                - Qualité moyenne: {status}
                - Jours d'alerte: [à calculer]
                Consultez le dashboard pour plus de détails."""
        }
        
        return messages.get(alert_type, f"Alerte qualité air - {school_name}: {status}")
    
    
    
    
    def send_sms_twilio(self, phone_number, message):
        """Envoie SMS via Twilio"""
        try:
            account_sid = self.default_config['twilio_account_sid']
            auth_token = self.default_config['twilio_auth_token']
            from_number = self.default_config['twilio_phone_number']

            client = Client(account_sid, auth_token)

            if not phone_number.startswith('+'):
                phone_number = f"+221{phone_number.lstrip('0')}"

            sms = client.messages.create(
                body=message,
                from_=from_number,
                to=phone_number
            )

            print(sms.body)
            return True, f"SMS envoyé (SID: {sms.sid})"
        except Exception as e:
            return False, f"Erreur Twilio: {str(e)}"

    
    
    
    
    
    def send_sms(self, phone_number, message):
        """Envoie SMS selon le provider configuré"""
        if not self.config['enabled']:
            return False, "Système SMS désactivé"
        
        if self.is_quiet_hours():
            return False, "Heures de silence"
        
        provider = self.config['sms_provider']
        
        if provider == 'twilio':
            return self.send_sms_twilio(phone_number, message)
        elif provider == 'orange_sms_senegal':
            return self.send_sms_orange_senegal(phone_number, message)
        elif provider == 'free_sms':
            return self.send_sms_free(phone_number, message)
        else:
            return False, f"Provider SMS inconnu: {provider}"
        
        
        
    
    def send_alert_to_parents(self, alert_type, air_data, school_name, selected_classes=None):
        """
        Envoie une alerte à tous les parents concernés
        """
        contacts = self.load_parent_contacts()
        results = []
        sent_count = 0
        
        for contact in contacts:
            # Filtrer par classe si spécifié
            if selected_classes and contact['classe'] not in selected_classes:
                continue
            
            phone = contact['telephone']
            child_name = contact['enfant']
            parent_name = contact['nom']
            
            # Vérifier si on peut envoyer
            if not self.can_send_alert(alert_type, phone):
                results.append({
                    'parent': parent_name,
                    'phone': phone,
                    'status': 'Ignoré',
                    'reason': 'Limite quotidienne atteinte'
                })
                continue
            
            # Générer le message personnalisé
            message = self.generate_alert_message(alert_type, air_data, school_name, child_name)
            
            # Envoyer le SMS
            success, reason = self.send_sms(phone, message)
            
            if success:
                # Marquer comme envoyé
                today = datetime.now().strftime('%Y-%m-%d')
                key = f"{phone}_{alert_type}_{today}"
                self.sent_alerts[key] = {
                    'timestamp': datetime.now().isoformat(),
                    'parent': parent_name,
                    'child': child_name,
                    'message': message[:100] + '...'  # Extrait du message
                }
                sent_count += 1
            
            results.append({
                'parent': parent_name,
                'phone': phone,
                'child': child_name,
                'status': 'Envoyé' if success else 'Échec',
                'reason': reason
            })
        
        # Sauvegarder l'historique
        self.save_sent_alerts()
        
        return results, sent_count
    
    
    
    
    
    def check_and_send_automatic_alerts(self, location_id, token, school_name):
        """
        Vérifie les conditions et envoie automatiquement des alertes si nécessaire
        """
                
        # Récupérer les données actuelles
        current_data = fetch_current_data(location_id, token)
        if current_data.empty:
            return [], 0
        
        air_status = calculate_air_quality_status(current_data)
        if not air_status:
            return [], 0
        
        pm25 = air_status['pm25']
        co2 = air_status['co2']
        
        alerts_sent = []
        total_sent = 0
        
        # Alerte pollution élevée
        if pm25 > self.config['pm25_danger_threshold']:
            results, count = self.send_alert_to_parents('pollution_high', air_status, school_name)
            alerts_sent.extend(results)
            total_sent += count
        
        # Alerte pollution modérée
        elif pm25 > self.config['pm25_alert_threshold']:
            results, count = self.send_alert_to_parents('pollution_moderate', air_status, school_name)
            alerts_sent.extend(results)
            total_sent += count
        
        # Alerte CO2 élevé
        if co2 > self.config['co2_alert_threshold']:
            results, count = self.send_alert_to_parents('co2_high', air_status, school_name)
            alerts_sent.extend(results)
            total_sent += count
        
        return alerts_sent, total_sent




def render_bloc_messages_alertes(location_id: str, token: str, school_name="École Primaire Mamadou Dia"):
    """
    Interface Streamlit pour le système d'alertes SMS
    """
    
    st.markdown("### 📬 **Messages & Alertes SMS**")
    
    # Initialiser le système SMS
    sms_system = SMSAlertSystem()
    
    with st.container():
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fff5f5 0%, #ffe6e6 100%); 
                    padding: 25px; border-radius: 15px; margin-bottom: 20px; 
                    border: 1px solid #ffb3b3;">
        """, unsafe_allow_html=True)
        
        # === ONGLETS ===
        tab1, tab2, tab3, tab4 = st.tabs(["📱 Envoi Manuel", "⚙️ Configuration", "📊 Historique", "🔄 Auto-Check"])
        
        with tab1:
            st.markdown("#### 📱 **Envoi manuel d'alertes**")
            
            # Sélection du type d'alerte
            col1, col2 = st.columns([1, 1])
            with col1:
                alert_type = st.selectbox(
                    "Type d'alerte",
                    options=['pollution_high', 'pollution_moderate', 'co2_high', 'back_to_normal', 'daily_report'],
                    format_func=lambda x: {
                        'pollution_high': '🚨 Pollution élevée',
                        'pollution_moderate': '⚠️ Pollution modérée',
                        'co2_high': '💨 CO2 élevé',
                        'back_to_normal': '✅ Retour normal',
                        'daily_report': '📊 Rapport quotidien'
                    }[x]
                )
            
            with col2:
                # Charger les contacts pour sélection
                contacts = sms_system.load_parent_contacts()
                if contacts:
                    classes = list(set(c['classe'] for c in contacts))
                    selected_classes = st.multiselect(
                        "Classes à alerter",
                        options=classes,
                        default=classes
                    )
                else:
                    st.warning("Aucun contact trouvé")
                    selected_classes = []
            
            # Aperçu du message
            if contacts:
                current_data = fetch_current_data(location_id, token)
                air_status = calculate_air_quality_status(current_data) if not current_data.empty else None
                
                if air_status:
                    sample_message = sms_system.generate_alert_message(
                        alert_type, air_status, school_name, "Exemple Enfant"
                    )
                    st.markdown("**Aperçu du message :**")
                    st.info(sample_message)
                    
                    # Bouton d'envoi
                    if st.button("📤 Envoyer les alertes", type="primary"):
                        with st.spinner("Envoi en cours..."):
                            results, sent_count = sms_system.send_alert_to_parents(
                                alert_type, air_status, school_name, selected_classes
                            )
                            
                            st.success(f"✅ {sent_count} SMS envoyés avec succès !")
                            
                            # Afficher les résultats
                            if results:
                                df_results = pd.DataFrame(results)
                                st.dataframe(df_results, use_container_width=True)
                else:
                    st.warning("Données de qualité de l'air non disponibles")
        
        with tab2:
            st.markdown("#### ⚙️ **Configuration du système SMS**")
            
            # Configuration générale
            col1, col2 = st.columns([1, 1])
            
            with col1:
                
                st.markdown("##### 📡 **Provider SMS**")

                options = ['twilio', 'orange_sms_senegal', 'free_sms']
                default = sms_system.config.get('sms_provider', 'twilio')
                default_index = options.index(default) if default in options else 0

                sms_system.config['sms_provider'] = st.selectbox(
                    "Service SMS",
                    options=options,
                    index=default_index,
                    help="Twilio: Fiable mais payant | Orange: Local Sénégal | Free: Tests uniquement"
                )

                
                if sms_system.config['sms_provider'] == 'twilio':
                    sms_system.config['twilio_account_sid'] = st.text_input(
                        "Twilio Account SID", 
                        value=sms_system.config.get('twilio_account_sid', ''),
                        type="password"
                    )
                    sms_system.config['twilio_auth_token'] = st.text_input(
                        "Twilio Auth Token", 
                        value=sms_system.config.get('twilio_auth_token', ''),
                        type="password"
                    )
                    sms_system.config['twilio_phone_number'] = st.text_input(
                        "Numéro Twilio", 
                        value=sms_system.config.get('twilio_phone_number', ''),
                        placeholder="+221xxxxxxxxx"
                    )
                
                elif sms_system.config['sms_provider'] == 'orange_sms_senegal':
                    sms_system.config['orange_api_key'] = st.text_input(
                        "Clé API Orange", 
                        value=sms_system.config.get('orange_api_key', ''),
                        type="password"
                    )
            
            with col2:
                st.markdown("##### ⏰ **Paramètres d'envoi**")
                sms_system.config['max_sms_per_day'] = st.number_input(
                    "Max SMS par parent/jour", 
                    min_value=1, max_value=20, 
                    value=sms_system.config['max_sms_per_day']
                )
                
                sms_system.config['quiet_hours_start'] = st.time_input(
                    "Début heures de silence", 
                    value=datetime.strptime(sms_system.config['quiet_hours_start'], '%H:%M').time()
                ).strftime('%H:%M')
                
                sms_system.config['quiet_hours_end'] = st.time_input(
                    "Fin heures de silence", 
                    value=datetime.strptime(sms_system.config['quiet_hours_end'], '%H:%M').time()
                ).strftime('%H:%M')
                
                st.markdown("##### 🎯 **Seuils d'alerte**")
                sms_system.config['pm25_alert_threshold'] = st.number_input(
                    "PM2.5 Alerte (µg/m³)", 
                    min_value=10, max_value=100, 
                    value=sms_system.config['pm25_alert_threshold']
                )
                
                sms_system.config['pm25_danger_threshold'] = st.number_input(
                    "PM2.5 Danger (µg/m³)", 
                    min_value=30, max_value=200, 
                    value=sms_system.config['pm25_danger_threshold']
                )
                
                sms_system.config['enabled'] = st.checkbox(
                    "Système SMS activé", 
                    value=sms_system.config['enabled']
                )
            
            # Sauvegarder la configuration
            if st.button("💾 Sauvegarder la configuration"):
                sms_system.save_config()
                st.success("Configuration sauvegardée !")
            
            # Gestion des contacts
            st.markdown("---")
            st.markdown("##### 👥 **Gestion des contacts parents**")
            
            # Upload du fichier contacts
            uploaded_file = st.file_uploader(
                "Importer fichier contacts (CSV/TXT)", 
                type=['txt', 'csv'],
                help="Format: nom,telephone,enfant,classe"
            )
            
            if uploaded_file:
                content = uploaded_file.read().decode('utf-8')
                with open(sms_system.contacts_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                st.success("Fichier contacts importé !")
            
            # Afficher les contacts actuels
            contacts = sms_system.load_parent_contacts()
            if contacts:
                st.markdown(f"**{len(contacts)} contacts trouvés :**")
                df_contacts = pd.DataFrame(contacts)[['nom', 'telephone', 'enfant', 'classe']]
                st.dataframe(df_contacts, use_container_width=True)
            
        with tab3:
            st.markdown("#### 📊 **Historique des envois**")
            
            # Afficher l'historique
            if sms_system.sent_alerts:
                history_data = []
                for key, data in sms_system.sent_alerts.items():
                    phone, alert_type, date = key.split('_', 2)
                    history_data.append({
                        'Date': date,
                        'Type': alert_type,
                        'Parent': data.get('parent', 'Inconnu'),
                        'Enfant': data.get('child', 'Inconnu'),
                        'Téléphone': phone,
                        'Heure': data.get('timestamp', '').split('T')[1][:5] if 'T' in data.get('timestamp', '') else '',
                        'Message': data.get('message', '')
                    })
                
                df_history = pd.DataFrame(history_data)
                
                # Filtres
                col1, col2 = st.columns([1, 1])
                with col1:
                    date_filter = st.date_input("Filtrer par date", value=datetime.now().date())
                with col2:
                    type_filter = st.selectbox("Filtrer par type", options=['Tous'] + list(set(df_history['Type'])))
                
                # Appliquer les filtres
                filtered_df = df_history.copy()
                if date_filter:
                    filtered_df = filtered_df[filtered_df['Date'] == date_filter.strftime('%Y-%m-%d')]
                if type_filter != 'Tous':
                    filtered_df = filtered_df[filtered_df['Type'] == type_filter]
                
                st.dataframe(filtered_df, use_container_width=True)
                
                # Statistiques
                st.markdown("##### 📈 **Statistiques**")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total SMS envoyés", len(history_data))
                with col2:
                    today_count = len([d for d in history_data if d['Date'] == datetime.now().strftime('%Y-%m-%d')])
                    st.metric("SMS aujourd'hui", today_count)
                with col3:
                    unique_parents = len(set(d['Parent'] for d in history_data))
                    st.metric("Parents contactés", unique_parents)
            else:
                st.info("Aucun SMS envoyé pour le moment")
        
        with tab4:
            st.markdown("#### 🔄 **Vérification automatique**")
            
            # Statut du système
            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown("##### 📡 **Statut système**")
                if sms_system.config['enabled']:
                    st.success("✅ Système activé")
                else:
                    st.error("❌ Système désactivé")
                
                if sms_system.is_quiet_hours():
                    st.warning("🔇 Heures de silence")
                else:
                    st.info("🔊 Envois autorisés")
            
            with col2:
                st.markdown("##### 🎯 **Configuration actuelle**")
                st.text(f"Provider: {sms_system.config['sms_provider']}")
                st.text(f"Seuil PM2.5: {sms_system.config['pm25_alert_threshold']} µg/m³")
                st.text(f"Max SMS/jour: {sms_system.config['max_sms_per_day']}")
            
            # Test de vérification manuelle
            if st.button("🔍 Vérifier maintenant", type="primary"):
                with st.spinner("Vérification en cours..."):
                    results, sent_count = sms_system.check_and_send_automatic_alerts(
                        location_id, token, school_name
                    )
                    
                    if sent_count > 0:
                        st.success(f"✅ {sent_count} alertes automatiques envoyées !")
                        df_results = pd.DataFrame(results)
                        st.dataframe(df_results)
                    else:
                        st.info("ℹ️ Aucune alerte nécessaire pour le moment")
        
        st.markdown("</div>", unsafe_allow_html=True)




# === FONCTION POUR AUTOMATISER LES ALERTES ===
def setup_automatic_alerts(location_id, token, school_name, check_interval_minutes=30):
    """
    Configure un système d'alertes automatiques
    À intégrer dans un scheduler (cron, celery, etc.)
    """

    def check_alerts_loop():
        sms_system = SMSAlertSystem()
        
        while True:
            try:
                # Vérifier seulement pendant les heures ouvrables
                current_hour = datetime.now().hour
                if 7 <= current_hour <= 18:  # Entre 7h et 18h
                    results, sent_count = sms_system.check_and_send_automatic_alerts(
                        location_id, token, school_name
                    )
                    
                    if sent_count > 0:
                        print(f"[{datetime.now()}] {sent_count} alertes automatiques envoyées")
                    
                # Attendre l'intervalle suivant
                time.sleep(check_interval_minutes * 60)
                
            except Exception as e:
                print(f"[{datetime.now()}] Erreur check automatique: {e}")
                time.sleep(300)  # Attendre 5 min en cas d'erreur
    
    # Lancer en arrière-plan
    alert_thread = threading.Thread(target=check_alerts_loop, daemon=True)
    alert_thread.start()
    
    return alert_thread

# === INTÉGRATION AVEC STREAMLIT SCHEDULER ===
def setup_streamlit_scheduler():
    """
    Configure les tâches automatiques pour Streamlit
    """
    import streamlit as st
    
    # Vérifier si le scheduler est déjà en cours
    if 'alert_scheduler_running' not in st.session_state:
        st.session_state.alert_scheduler_running = False
    
    if not st.session_state.alert_scheduler_running:
        # Démarrer le scheduler
        location_id = st.session_state.get('location_id', 'default')
        token = st.session_state.get('api_token', 'default')
        school_name = st.session_state.get('school_name', 'École par défaut')
        
        setup_automatic_alerts(location_id, token, school_name)
        st.session_state.alert_scheduler_running = True

# === WEBHOOK POUR INTÉGRATIONS EXTERNES ===
def create_webhook_handler():
    """
    Créer un endpoint webhook pour recevoir des alertes externes
    Exemple d'usage avec Flask ou FastAPI
    """
    webhook_code = '''
    from flask import Flask, request, jsonify
    from datetime import datetime

    app = Flask(__name__)
    sms_system = SMSAlertSystem()

    @app.route('/webhook/air-quality-alert', methods=['POST'])
    def handle_air_quality_webhook():
        """
        Endpoint pour recevoir des alertes de qualité d'air
        
        Payload attendu:
        {
            "location_id": "school_001",
            "school_name": "École Primaire XYZ",
            "alert_type": "pollution_high",
            "air_data": {
                "pm25": 45.2,
                "co2": 800,
                "status": "Mauvaise",
                "timestamp": "2024-01-01T12:00:00Z"
            },
            "classes": ["CM1", "CM2"]  # Optionnel
        }
        """
        try:
            data = request.json
            
            location_id = data.get('location_id')
            school_name = data.get('school_name', 'École inconnue')
            alert_type = data.get('alert_type')
            air_data = data.get('air_data', {})
            selected_classes = data.get('classes')
            
            # Validation
            if not all([location_id, alert_type, air_data]):
                return jsonify({"error": "Données manquantes"}), 400
            
            # Envoyer les alertes
            results, sent_count = sms_system.send_alert_to_parents(
                alert_type, air_data, school_name, selected_classes
            )
            
            return jsonify({
                "success": True,
                "sent_count": sent_count,
                "timestamp": datetime.now().isoformat(),
                "results": results
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/webhook/test-sms', methods=['POST'])
    def test_sms_endpoint():
        """Test endpoint pour vérifier la configuration SMS"""
        try:
            data = request.json
            phone = data.get('phone')
            message = data.get('message', 'Test SMS depuis RESPiRE Dashboard')
            
            if not phone:
                return jsonify({"error": "Numéro de téléphone requis"}), 400
            
            success, reason = sms_system.send_sms(phone, message)
            
            return jsonify({
                "success": success,
                "reason": reason,
                "timestamp": datetime.now().isoformat()
            }), 200
            
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    if __name__ == '__main__':
        app.run(host='0.0.0.0', port=5000, debug=True)
        '''
        
    return webhook_code

# === DOCUMENTATION D'UTILISATION ===
def render_sms_documentation():
    """
    Affiche la documentation du système SMS
    """
    st.markdown("""
    ## 📚 **Documentation - Système d'Alertes SMS**
    
    ### 🚀 **Installation et Configuration**
    
    #### 1. **Prérequis**
    ```bash
    pip install twilio requests streamlit pandas
    ```
    
    #### 2. **Fichier de contacts (parents_contacts.txt)**
    ```
    # Format: nom,telephone,enfant,classe
    Aminata Diallo,771234567,Fatou Diallo,CP
    Moussa Ndiaye,775678901,Omar Ndiaye,CP
    ```
    
    #### 3. **Configuration Twilio**
    1. Créer un compte sur [twilio.com](https://twilio.com)
    2. Obtenir Account SID et Auth Token
    3. Acheter un numéro de téléphone Twilio
    4. Configurer dans l'interface
    
    ### 📱 **Types d'Alertes Disponibles**
    
    | Type | Déclencheur | Message type |
    |------|-------------|--------------|
    | `pollution_high` | PM2.5 > 55 µg/m³ | 🚨 Alerte rouge |
    | `pollution_moderate` | PM2.5 > 35 µg/m³ | ⚠️ Alerte orange |
    | `co2_high` | CO2 > 1000 ppm | 💨 Ventilation |
    | `back_to_normal` | Retour normal | ✅ Rassurance |
    | `daily_report` | Rapport quotidien | 📊 Résumé |
    
    ### ⚙️ **Configuration Avancée**
    
    #### **Seuils personnalisables**
    - PM2.5 alerte: 35 µg/m³ (modifiable)
    - PM2.5 danger: 55 µg/m³ (modifiable)
    - CO2 alerte: 1000 ppm (modifiable)
    
    #### **Limitations anti-spam**
    - Max 5 SMS par parent/jour (configurable)
    - Heures de silence: 21h-7h (configurable)
    - Pas de doublon sur même alerte/jour
    
    ### 🔧 **Intégrations**
    
    #### **Webhook automatique**
    ```python
    import requests
    
    # Envoyer alerte via webhook
    data = {
        "location_id": "school_001",
        "school_name": "École XYZ",
        "alert_type": "pollution_high",
        "air_data": {"pm25": 45, "status": "Mauvaise"}
    }
    
    response = requests.post("http://localhost:5000/webhook/air-quality-alert", json=data)
    ```
    
    #### **Scheduler automatique**
    ```python
    # Vérification toutes les 30 minutes
    setup_automatic_alerts("location_id", "token", "École XYZ", 30)
    ```
    
    ### 💡 **Bonnes Pratiques**
    
    1. **Tester d'abord** avec le provider `free_sms`
    2. **Vérifier les numéros** au format international (+221...)
    3. **Surveiller les coûts** avec Twilio
    4. **Backup des contacts** régulier
    5. **Messages courts** (max 160 caractères recommandé)
    
    ### 🆘 **Dépannage**
    
    | Problème | Solution |
    |----------|----------|
    | SMS non reçus | Vérifier numéro format +221... |
    | Erreur Twilio | Vérifier crédits et tokens |
    | Heures silence | Changer config quiet_hours |
    | Limite quotidienne | Augmenter max_sms_per_day |
    
    ### 📞 **Support**
    
    - **Twilio Support**: [support.twilio.com](https://support.twilio.com)
    - **Orange Sénégal**: 8080 (numéro gratuit)
    - **Documentation**: [docs.twilio.com](https://docs.twilio.com)
    """)


# === FONCTION D'UTILISATION PRINCIPALE ===
def show_sms_sytem():
    """Fonction principale pour tester le système SMS"""
    
    st.title("📱 **RESPiRE - Système d'Alertes SMS**")
    
    # Rendu du bloc principal
    school_name = "ESMT"
    render_bloc_messages_alertes(location_id, token, school_name)
    
    # Documentation
    with st.expander("📚 Voir la documentation complète"):
        render_sms_documentation()





















#=========================== SECTION TOUT EN BAS RESERVEE AU FOOTER =================================

# show_footer()