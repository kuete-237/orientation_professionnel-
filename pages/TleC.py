# =========================================================
# TERMINAL C (VERSION CORRIGÉE + UNIVERSITÉS)
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
st.image(Image.open("notebook_2312_cover_6sn8YXk.jpg"), width=500)

# --------- CHARGEMENT MODELE ---------
try:
    mod = joblib.load("modele_metier.pkl")
    encoders = joblib.load("label_encoder.pkl")
except Exception as e:
    st.error(f"Erreur chargement modèle/encodeur : {e}")
    st.stop()

# --------- UNIVERSITÉS ---------
universites = {
    "Ingénieur en Génie Aéronautique": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
        ("MIT", "https://www.mit.edu"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Ingénieur en Génie Civil": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Actuaire": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Chercheur en Physique": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Architecte": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
        ("Université de Dschang", "https://www.univ-dschang.org"),
    ],
    "Ingénieur chimiste": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Technicien supérieur en industrie": [
        ("IUT de Douala", "https://www.univ-douala.cm"),
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
    ],
    "Technicien industriel": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),
        ("Université de Douala", "https://www.univ-douala.cm"),
        ("ENSET Douala", "https://www.univ-douala.cm"),
    ],
    "Banker": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://www.univ-yaounde1.cm"),

    ],
    "Business Owner": [
        ("École Polytechnique", "https://polytechnique.cm/"),
        ("Université de Yaoundé I", "https://univ-yaounde1.cm"),

    ],
}

# --------- FORMULAIRE ---------
with st.form("form_C"):
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

    submit_C = st.form_submit_button("🔮 Prédire ma carrière")

# --------- RÈGLES ---------
def apply_c_rules(math, physics, chemistry, biology, absence_days, weekly_self_study_hours):

    score_science = math*0.4 + physics*0.3 + chemistry*0.2 + biology*0.1
    discipline_score = 20 - absence_days

    if math >= 18 and physics >= 17 and weekly_self_study_hours >= 12:
        return "Ingénieur en Génie Aéronautique"

    if math >= 17 and physics >= 16:
        return "Ingénieur en Génie Civil"

    if math >= 16 and discipline_score >= 15:
        return "Actuaire"

    if physics >= 16 and weekly_self_study_hours >= 8:
        return "Chercheur en Physique"

    if score_science >= 15:
        return "Architecte"

    if chemistry >= 15:
        return "Ingénieur chimiste"

    if score_science >= 13:
        return "Technicien supérieur en industrie"

    if score_science >= 10:
        return "Technicien industriel"

    return None

# --------- PREDICTION ---------
if submit_C:

    career_rule = apply_c_rules(
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

        prediction = mod.predict(input_data)

        try:
            if isinstance(encoders, dict):
                career = encoders["career_aspiration"].inverse_transform(prediction)[0]
            else:
                career = encoders.inverse_transform(prediction)[0]
        except:
            career = str(prediction[0])

    # ✅ stockage
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

    if career in universites:

        st.markdown("## 🎓 Universités recommandées")

        for nom, lien in universites[career]:
            st.markdown(f"""
            <div style="background:#1e1e1e; padding:15px; border-radius:10px; margin-bottom:10px;">
                <p style="color:white; font-size:18px;"><b>{nom}</b></p>
                <a href="{lien}" target="_blank">
                    <button style="
                        background-color:#00bcd4;
                        color:black;
                        border:none;
                        padding:8px 15px;
                        border-radius:8px;">
                        Accéder au site
                    </button>
                </a>
            </div>
            """, unsafe_allow_html=True)

# --------- RETOUR ---------
if st.button("⬅️ Retour accueil"):
    st.switch_page("app.py")
