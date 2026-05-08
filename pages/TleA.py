# =========================================================
# TERMINAL A (VERSION CORRIGÉE + UNIVERSITÉS)
# =========================================================
import streamlit as st
import pandas as pd
import joblib
from PIL import Image

# --------- SESSION STATE ---------
if "career" not in st.session_state:
    st.session_state["career"] = None

if "show_univ" not in st.session_state:
    st.session_state["show_univ"] = False

# --------- CSS ---------
st.markdown("""
<style>
body, .stApp { background-color: black !important; color: white !important; }
</style>
""", unsafe_allow_html=True)

# --------- IMAGE ---------
st.image(Image.open("IMG-20260412-WA0041.jpg"), width=500)

# --------- CHARGEMENT MODELE ---------
try:
    model = joblib.load("modele_metier.pkl")
    encoders = joblib.load("label_encoder.pkl")
except Exception as e:
    st.error(f"Erreur chargement modèle : {e}")
    st.stop()

# --------- BASE UNIVERSITÉS ---------
universites = {
    "Diplomate international": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Magistrat": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm")
    ],
    "Avocat": [
        ("Université de Yaoundé II", "https://www.univ-yaounde2.org"),
        ("Université de Douala", "https://www.univ-douala.cm")
    ],
    "Journaliste international": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Traducteur / Interprète": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm")
        ("Université de Buea", "https://www.ubuea.cm"),
    ],
    "Professeur de lettres": [
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm")

    ],
    "Analyste politique": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm")
    ],
    "Assistant administratif": [
        ("Université de Douala", "https://www.univ-douala.cm")
    ],
    "Banker": [
        ("École Polytechnique", "https://www.polytechnique.edu"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),

    ],
    "Business Owner": [
        ("École Polytechnique", "https://www.polytechnique.edu"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),

    ],
}

# --------- FORMULAIRE ---------
with st.form("form_A"):
    part_time_job = st.selectbox("🧑‍💼 Job à temps partiel ?", [0, 1])
    absence_days = st.number_input("📅 Jours d'absence", 0, 10)
    weekly_self_study_hours = st.number_input("📚 Étude perso / semaine", 0, 20)

    math = st.slider("📐 Mathématiques", 0, 20)
    philo = st.slider("⚛ Philosophie", 0, 20)
    litterature = st.slider("📚 Littérature", 0, 20)
    langue = st.slider("🌐 Langue", 0, 20)
    english = st.slider("📖 Anglais", 0, 20)
    history = st.slider("📜 Histoire", 0, 20)
    geography = st.slider("🌍 Géographie", 0, 20)

    submit_A = st.form_submit_button("🔮 Prédire ma carrière")

# --------- REGLES ---------
def apply_a_rules(math, philo, litterature, langue, english, history, geography,
                 absence_days, weekly_self_study_hours):

    avg = (philo + litterature + langue + english + history + geography) / 6
    discipline = 20 - absence_days

    if avg >= 17 and english >= 16 and weekly_self_study_hours >= 10:
        return "Diplomate international"

    if history >= 16 and philo >= 15:
        return "Magistrat"

    if history >= 14 and philo >= 14:
        return "Avocat"

    if litterature >= 15 and english >= 14:
        return "Journaliste international"

    if english >= 17 or langue >= 17:
        return "Traducteur / Interprète"

    if avg >= 13:
        return "Professeur de lettres"

    if avg >= 10:
        return "Assistant administratif"

    return None

# --------- PREDICTION ---------
if submit_A:

    input_data = pd.DataFrame([[
        math, philo, litterature, langue, english, history
    ]], columns=[
        "math", "physics", "chemistry",
        "biology", "english", "history"
    ])

    career_rule = apply_a_rules(
        math, philo, litterature, langue,
        english, history, geography,
        absence_days, weekly_self_study_hours
    )

    if career_rule:
        career = career_rule
    else:
        prediction = model.predict(input_data)
        career = encoders["career_aspiration"].inverse_transform(prediction)[0]

    # ✅ STOCKAGE
    st.session_state["career"] = career
    st.session_state["show_univ"] = False

    st.success(f"💼 Métier prédit : **{career}**")
    st.balloons()

# --------- BOUTON UNIVERSITÉS ---------
career = st.session_state["career"]

if career:
    if st.button("🎓 Voir les universités recommandées"):
        st.session_state["show_univ"] = True

# --------- AFFICHAGE UNIVERSITÉS ---------
if st.session_state["show_univ"]:

    career = st.session_state["career"]

    if career in universites:

        st.markdown("## 🎓 Universités recommandées")

        for nom, lien in universites[career]:
            st.markdown(f"""
            <div style="background: #1e1e1e; padding:15px; border-radius:10px; margin-bottom:10px;">
                <p style="color:white; font-size:18px;"><b>{nom}</b></p>
                <a href="{lien}" target="_blank">
                    <button style="
                        background-color:#00bcd4;
                        color:black;
                        border:none;
                        padding:8px 15px;
                        border-radius:8px;
                        cursor:pointer;">
                        Accéder au site
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

# --------- RETOUR ---------
if st.button("⬅️ Retour accueil"):
    st.switch_page("app.py")
