import streamlit as st
import datetime


def parametre():
    st.markdown("## ⚙️ Paramètres du Dashboard")
    st.write("Configure ici les paramètres de visualisation et de données du tableau de bord RESPiRE.")

    # Sélection de l'école à afficher
    st.markdown("### 🏫 Choix de l’école")
    ecole = st.selectbox(
        "Sélectionne une école à afficher dans les visualisations :",
        ["École A – Dakar", "École B – Pikine", "École C – Guédiawaye", "École D – Rufisque"],
        index=0
    )
    st.success(f"📌 École sélectionnée : {ecole}")

    # Choix de la langue
    st.markdown("### 🌍 Langue d’affichage")
    langue = st.radio("Langue", ["Français", "Wolof"], horizontal=True)
    st.info(f"Langue actuelle : {langue}")

    # Rafraîchissement manuel des données
    st.markdown("### 🔄 Mettre à jour les données")
    if st.button("🔁 Rafraîchir les données maintenant"):
        st.success("✅ Données mises à jour avec succès à " + datetime.datetime.now().strftime("%H:%M"))

    # Informations système
    st.markdown("---")
    st.markdown("### ℹ️ Informations système")
    col1, col2 = st.columns(2)

    with col1:
        st.metric("Version du dashboard", "v1.2.3")
        st.metric("Dernière mise à jour", datetime.datetime.now().strftime("%d/%m/%Y %H:%M"))

    with col2:
        st.metric("Capteurs actifs", "10")
        st.metric("Écoles suivies", "4")

    st.markdown("---")
    st.caption("Les paramètres sont locaux à cette session.")











