import streamlit as st
from src.footer import show_footer
from components.autorite_ import *


def show():
    
    show_header(logo_path="assets/images/logo_esmt.jpeg")
    
    # Alerte si nécessaire
    alerts()
    
    # Bloc I AQI
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Gauge AQI principal

        st.plotly_chart(create_gauge_chart(title="Indice de la qualite de l'air "), use_container_width=True)
        
    with col2:
        #Description de l'aqi
        descript()
    
    show_line()
    
    # Bloc II Indicateurs cles actuels 
    
    show_air_status_summary()
    show_air_quality()
    
    show_line()
    # 2. BLOC ANALYTIQUE CENTRAL
    st.markdown("## Analyse Détaillée en Temps Réel")
    st.plotly_chart(create_indicator_bars(), use_container_width=True)
    
    # 3. PRÉDICTIONS
    st.markdown("## Prédictions pour Demain")
    
    col_pred1, col_pred2 = st.columns([2, 1])
    
    with col_pred1:
        st.plotly_chart(create_prediction_chart(), use_container_width=True)
    
    with col_pred2:
        st.markdown("""
        <div class="prediction-card">
            <h4>🧠 Recommandations IA</h4>
            <ul>
                <li>📈 Pic de CO₂ prévu à 12h</li>
                <li>🌡️ Température élevée l'après-midi</li>
                <li>💨 Ventilation recommandée 10h-14h</li>
                <li>🌱 Activités extérieures favorisées le matin</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # 4. CLASSEMENT ET CARTE
    st.markdown("## Vue d'Ensemble Régionale")
    
    col_rank1, col_rank2 = st.columns([1, 1])
    
    with col_rank1:
        st.plotly_chart(create_school_ranking(), use_container_width=True)
    
    with col_rank2:
        st.markdown("### 🗺️ Carte Interactive")
        # Simulation d'une carte (vous pourrez intégrer folium ici)
        st.info("🚧 Carte interactive en développement")
        
        # Tableau des écoles
        schools_df = pd.DataFrame({
            'École': ['École Primaire Almadies', 'Lycée John F. Kennedy', 'Lycée Blaise Diagne'],
            'AQI': [45, 58, 68],
            'Statut': ['Excellent 😊', 'Bon 🙂', 'Modéré 😐'],
            'Action': ['Aucune', 'Surveillance', 'Ventilation']
        })
        st.dataframe(schools_df, use_container_width=True)
    
    # 5. GÉNÉRATION DE RAPPORT
    show_line()
    st.markdown("## Gestion des Rapports")
    
    col_report1, col_report2, col_report3 = st.columns(3)
    
    with col_report1:
        st.markdown("""
        <div class="metric-card">
            <h4>📊 Rapport Hebdomadaire</h4>
            <p>Généré automatiquement chaque dimanche</p>
            <p><strong>Prochain envoi :</strong> Dimanche 3 Nov, 20h00</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_report2:
        st.markdown("""
        <div class="metric-card">
            <h4>📧 Liste de Diffusion</h4>
            <p>12 destinataires configurés</p>
            <p><strong>Derniers envois :</strong> 100% livrés</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_report3:
        st.markdown("""
        <div class="metric-card">
            <h4>📈 Historique</h4>
            <p>24 rapports générés ce mois</p>
            <p><strong>Taux d'ouverture :</strong> 87%</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Options avancées dans un expander
    with st.expander("Configuration Avancée"):
        col_config1, col_config2 = st.columns(2)
        
        with col_config1:
            st.markdown("### 🎯 Seuils d'Alerte Personnalisés")
            pm25_threshold = st.slider("Seuil PM2.5 (μg/m³)", 0, 50, 25)
            co2_threshold = st.slider("Seuil CO₂ (ppm)", 400, 1000, 600)
        
        with col_config2:
            st.markdown("### 📧 Configuration Email")
            email_frequency = st.selectbox("Fréquence d'envoi", 
                                         ["Quotidien", "Hebdomadaire", "Sur alerte uniquement"])
            include_predictions = st.checkbox("Inclure les prédictions", True)
    
 
    show_line()

    st.markdown("### Actions Rapides")
    if st.button("📧 Générer Rapport", key="generate_report"):
        st.success("Rapport en cours de génération...")
    
    if st.button("📥 Télécharger CSV", key="download_csv"):
        st.info("Téléchargement démarré...")
    
    if st.button("⚙️ Seuils d'Alerte", key="alert_settings"):
        st.info("Configuration des seuils...")
    





























#=========================== SECTION TOUT EN BAS RESERVEE AU FOOTER =================================

# show_footer()