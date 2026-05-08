# =========================================================
# TERMINAL D (VERSION PRO)
# =========================================================
import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# --------- STYLE ---------
st.markdown("""
<style>
body, .stApp { background-color: black !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

st.image(Image.open("notebook_2312_cover.jpg"), width=500)

# --------- CHARGEMENT MODELE ---------
try:
    mode = joblib.load("modele_metier.pkl")
    encoders = joblib.load("label_encoder.pkl")
except Exception as e:
    st.error(f"Erreur chargement modèle : {e}")
    st.stop()

# --------- FORMULAIRE ---------
with st.form("form_D"):
    part_time_job = st.selectbox("🧑‍💼 Job à temps partiel ?", [0, 1])
    absence_days = st.number_input("📅 Jours d'absence", 0, 10)
    weekly_self_study_hours = st.number_input("📚 Heures d'étude perso / semaine", 0, 20)

    math = st.slider("📐 Mathématiques", 0, 20)
    physics = st.slider("⚛ Physique", 0, 20)
    chemistry = st.slider("🧪 Chimie", 0, 20)
    biology = st.slider("🧬 Biologie", 0, 20)
    english = st.slider("📖 Anglais", 0, 20)
    education_moral = st.slider("📜 Education morale", 0, 20)
    geography = st.slider("🌍 Géographie", 0, 20)

    submit_D = st.form_submit_button("🔮 Prédire ma carrière")

# =========================================================
# 🔥 REGLES INTELLIGENTES AMÉLIORÉES
# =========================================================
def apply_d_rules(math, physics, chemistry, biology, absence_days, weekly_self_study_hours):

    score_bio = biology*0.4 + chemistry*0.3 + physics*0.2 + math*0.1

    # 🏥 MÉDECINE HAUT NIVEAU
    if biology >= 18 and chemistry >= 17 and weekly_self_study_hours >= 12:
        return "Médecin spécialiste"

    if biology >= 17 and chemistry >= 15:
        return "Médecin généraliste"

    # 💊 PHARMACIE
    if chemistry >= 17:
        return "Pharmacien"

    # 🧬 BIOTECH / GÉNÉTIQUE
    if biology >= 16 and physics >= 14:
        return "Biotechnologiste"

    if biology >= 17:
        return "Généticien"

    # 🧪 RECHERCHE
    if biology >= 15 and weekly_self_study_hours >= 8:
        return "Chercheur en Biologie"

    # 🩺 PARAMEDICAL
    if score_bio >= 15:
        return "Infirmier spécialisé"

    if score_bio >= 13:
        return "Infirmier diplômé d'État"

    # 🌱 AGRONOMIE
    if biology >= 14 and chemistry >= 13:
        return "Ingénieur agronome"

    # 🐾 VETERINAIRE
    if biology >= 15:
        return "Vétérinaire"

    # 🔬 LABO
    if score_bio >= 11:
        return "Technicien de laboratoire"

    if score_bio >= 9:
        return "Assistant sanitaire"

    # 🔥 fallback
    if score_bio >= 8:
        return "Aide-soignant"

    return None

# =========================================================
# 🎓 UNIVERSITES (RICHE + REELLES)
# =========================================================
universites = {

    "Médecin spécialiste": [
        ("Université de Yaoundé I - Faculté de Médecine", "https://uy1.uninet.cm"),
        ("Université de Douala - Faculté de Médecine", "https://www.univ-douala.cm"),

    ],
    "Banker": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://uy1.uninet.cm"),

    ],
    "Business Owner": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://uy1.uninet.cm"),

    ],
    "Médecin généraliste": [
        ("Université de Buea", "https://www.ubuea.cm"),
        ("polytechnique", "https://polytechnique.cm/")
    ],

    "Pharmacien": [
        ("Université de Yaoundé I", "https://uy1.uninet.cm"),

    ],

    "Biotechnologiste": [
        ("Université de Dschang", "https://www.univ-dschang.org"),
        ("MIT Biotechnology", "https://www.mit.edu")
    ],

    "Chercheur en Biologie": [
        ("Universite yaounde1","https://uy1.uninet.cm")
    ],

    "Infirmier diplômé d'État": [
        ("École des Infirmiers Yaoundé", ""),
        ("Croix Rouge", "https://isss-croixrouge.optsolution.net")
    ],

    "Infirmier spécialisé": [
        ("Institut Supérieur de Santé", "#"),

    ],

    "Ingénieur agronome": [
        ("Université de Dschang", "https://www.univ-dschang.org"),

    ],

    "Vétérinaire": [
        ("Université de Ngaoundéré", "https://www.univ-ndere.cm"),

    ],

    "Technicien de laboratoire": [
        ("Institut Pasteur", "https://pasteur-yapunde.org"),
        ("Université de Douala", "https://www.univ-douala.cm")
    ],

    "Assistant sanitaire": [

    ]
}

# =========================================================
# 🚀 PREDICTION
# =========================================================
if submit_D:

    career = None

    # 🔥 règles d'abord
    career_rule = apply_d_rules(
        math, physics, chemistry, biology,
        absence_days, weekly_self_study_hours
    )

    if career_rule:
        career = career_rule

    else:
        input_data = pd.DataFrame([[ 
            math, physics, chemistry, biology, english, education_moral
        ]], columns=[
            "math", "physics", "chemistry", "biology", "english", "history"
        ])

        prediction = mode.predict(input_data)

        try:
            if isinstance(encoders, dict):
                career = encoders["career_aspiration"].inverse_transform(prediction)[0]
            else:
                career = encoders.inverse_transform(prediction)[0]
        except:
            career = str(prediction[0])

    # --------- RESULTAT ---------
    st.session_state["career_acd"] = career
    st.session_state["show_unis_acd"] = False

    st.success(f"💼 Métier prédit : **{career}**")
    st.balloons()

# =========================================================
# 🎓 AFFICHAGE UNIVERSITES
# =========================================================
if "career_acd" in st.session_state and st.session_state["career_acd"]:

    if st.button("📚 Voir les universités conseillées"):
        st.session_state["show_unis_acd"] = True

    if st.session_state.get("show_unis_acd"):

        career = st.session_state["career_acd"]

        if career in universites:
            st.markdown(f"### 🎓 Universités pour {career}")

            for nom, lien in universites[career]:
                st.markdown(f"**{nom}**")
                st.link_button("📎 Accéder à la formation", lien)

        else:
            st.warning("Aucune université spécifique trouvée.")

# --------- RETOUR ---------
if st.button("⬅️ Retour accueil"):
    st.switch_page("app.py")
