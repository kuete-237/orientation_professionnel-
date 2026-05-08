# =========================================================
# TERMINAL TI (VERSION AVANCÉE)
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

st.image(Image.open("notebook_2312_cover_VO1QyTl.jpg"), width=500)

# --------- CHARGEMENT MODELE ---------
try:
    modele = joblib.load("modele.pkl")
    le = joblib.load("label.pkl")
except Exception as e:
    st.error(f"Erreur chargement modèle : {e}")
    st.stop()

# --------- FORMULAIRE ---------
with st.form("form_TI"):

    moyenne = st.number_input("📊 Moyenne Générale", 0.0, 20.0, step=0.1)

    interested_domain = st.selectbox(
        "💡 Domaine d'intérêt",
        [
            "IA", "Web development", "Data Science", "Cybersecurity",
            "Cloud Computing+", "Robotique", "Software Development",
            "Machine Learning", "Database Management", "Computer Graphics",
            "Software Engineering", "Mobile App Development",
            "Network Security", "Game Development"
        ]
    )

    projects = st.number_input("🛠️ Projets réalisés", 0, 10)
    java = st.selectbox("☕ Java ?", ["Oui", "Non"])
    python = st.selectbox("🐍 Python ?", ["Oui", "Non"])

    submit_TI = st.form_submit_button("🔮 Prédire carrière informatique")

# --------- MAPPING ---------
domain_mapping = {
    "IA": 0, "Web development": 1, "Data Science": 2, "Cybersecurity": 3,
    "Cloud Computing+": 4, "Robotique": 5, "Software Development": 6,
    "Machine Learning": 7, "Database Management": 8, "Computer Graphics": 9,
    "Software Engineering": 10, "Mobile App Development": 11,
    "Network Security": 12, "Game Development": 13
}

# =========================================================
# 🔥 REGLES INTELLIGENTES (ULTRA AMÉLIORÉES)
# =========================================================
def apply_ti_rules(moyenne, projects, java, python, interested_domain):

    # 🧠 IA / ML
    if moyenne >= 16 and python == "Oui" and projects >= 4:
        return "AI Engineer"

    if moyenne >= 14 and python == "Oui" and interested_domain in ["IA", "Machine Learning"]:
        return "Machine Learning Engineer"

    # 📊 DATA
    if moyenne >= 13 and python == "Oui" and interested_domain == "Data Science":
        return "Data Scientist"

    if interested_domain == "Database Management" and projects >= 2:
        return "Database Administrator"

    # 🌐 WEB
    if interested_domain == "Web development":
        if projects >= 4:
            return "Full Stack Developer"
        if projects >= 2:
            return "Frontend Developer"
        return "Junior Web Developer"

    # 📱 MOBILE
    if interested_domain == "Mobile App Development":
        if projects >= 3:
            return "Mobile App Developer"
        return "Junior Mobile Developer"

    # 🔐 CYBER
    if interested_domain in ["Cybersecurity", "Network Security"]:
        if moyenne >= 14:
            return "Cybersecurity Engineer"
        return "Security Analyst"

    # ☁ CLOUD
    if interested_domain == "Cloud Computing+":
        if moyenne >= 13:
            return "Cloud Engineer"
        return "Cloud Technician"

    # 🤖 ROBOTIQUE
    if interested_domain == "Robotique":
        if python == "Oui" and moyenne >= 14:
            return "Robotics Engineer"

    # 🎮 GAME
    if interested_domain == "Game Development":
        if projects >= 3:
            return "Game Developer"
        return "Junior Game Developer"

    # 🖥 GRAPHICS
    if interested_domain == "Computer Graphics":
        return "Graphic Programmer"

    # ⚙ SOFTWARE
    if java == "Oui" and python == "Oui":
        if moyenne >= 14:
            return "Software Engineer"
        return "Software Developer"

    # 🔥 fallback intelligent
    if moyenne >= 12:
        return "IT Specialist"

    return None

# =========================================================
# 🎓 UNIVERSITES ULTRA RICHES
# =========================================================
universites = {

    "AI Engineer": [
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Machine Learning Enginee":[
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Data Scientis": [
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Database Administrator": [
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Full Stack Developer": [
    ("École Polytechnique", "https://polytechnique.cm/"),

    ],

    "Mobile App Develope": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Junior Mobile Developer": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Cybersecurity Engineer": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Security Analys": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Cloud Enginee": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Cloud Technician": [
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Robotics Engineer": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Game Developer": [
    ("IAI Cameroun" ,"https://cameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Junior Game Developer": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Graphic Programme": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Software Engineer": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "IT Specialist": [
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Software Developer": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],
    "Graphics Programmer": [
    ("IAI Cameroun" ,"https://iaicameroun.com/"),
    ("École Polytechnique", "https://polytechnique.cm/"),
    ],


}

# =========================================================
# 🚀 PREDICTION
# =========================================================
if submit_TI:

    career = None

    domain_encoded = domain_mapping[interested_domain]

    user_data = pd.DataFrame({
        "Interested Domain": [domain_encoded],
        "Projects": [projects],
        "Python": [1 if python == "Oui" else 0],
        "Java": [1 if java == "Oui" else 0],
        "moyenne": [moyenne]
    })

    user_data = user_data[modele.feature_names_in_]

    # 🔥 règles d'abord
    career_rule = apply_ti_rules(moyenne, projects, java, python, interested_domain)

    if career_rule:
        career = career_rule
    else:
        pred = modele.predict(user_data)
        try:
            career = le["Future Career"].inverse_transform(pred)[0]
        except:
            career = str(pred[0])

    # --------- RESULTAT ---------
    st.success(f"💻 Métier prédit : **{career}**")
    st.balloons()

    # --------- UNIVERSITES ---------
    if career in universites:
        st.markdown("### 🎓 Universités recommandées")

        for nom, lien in universites[career]:
            st.markdown(f"**{nom}**")
            st.link_button("📎 Accéder à la formation", lien)
    else:
        st.warning("Aucune université spécifique trouvée, explore des plateformes généralistes.")

# --------- RETOUR ---------
if st.button("⬅️ Retour accueil"):
    st.switch_page("app.py")