import streamlit as st
import pandas as pd
import joblib
from PIL import Image
import os

# --------- PAGE CONFIG ---------
st.set_page_config(page_title="Orientation Carrière", layout="centered")

# --------- CSS GLOBAL (Fond noir + style université) ---------
st.markdown("""
<style>
body, .stApp { background-color: black !important; color: white !important; }
h1, h2, h3, h4, h5, h6, label, p, span, div { color: white !important; }
.stButton>button { background-color: #444444; color: white !important; font-weight: bold; border-radius: 8px; padding: 8px 16px; }
.stExpanderHeader { color: white !important; }
.univ-name { font-weight: bold; font-size: 16px; color: white; }
.univ-meta { font-size: 13px; color: #d0d0d0; }
.univ-desc { font-size: 13px; color: #bdbdbd; margin-bottom: 12px; }
</style>
""", unsafe_allow_html=True)

# --------- IMAGE D'ACCUEIL (optionnel) ---------
if os.path.exists("notebook_2312_cover_6sn8YXk.jpg"):
    try:
        st.image(Image.open("notebook_2312_cover_6sn8YXk.jpg"), width=500)
    except:
        pass

st.title("🎓 Découvre Ton Futur Métier")
st.write("Sélectionne ta classe, remplis le formulaire et obtiens des suggestions d'universités au Cameroun et à l'international adaptées au métier prédit.")

# --------- Choix de la classe ---------
classe = st.selectbox("🎓 Quelle est votre classe ?", ["", "Terminal A,C&D", "Terminal TI"])
if classe == "":
    st.info("Veuillez d’abord sélectionner une classe.")

# ---------------------------
# --- Base d'universités complète ---
# ---------------------------
UNIVERSITY_DB = {
    # Terminal A,C&D
    "Médecin": [
        {"Université":"Faculté de Médecine et Sciences Biomédicales - UY1","Ville":"Yaoundé","Type":"Publique","Domaine":"Médecine/Pharmacie","Lien":"https://www.uy1.cm","Logo":"university_logos/uy1.png","Description":"Référence nationale pour les études médicales. Conditions d’accès : filière scientifique + concours d’entrée."},
        {"Université":"Faculté de Médecine - Université de Douala","Ville":"Douala","Type":"Publique","Domaine":"Médecine/Pharmacie","Lien":"https://www.univ-douala.cm","Logo":"university_logos/univdouala.png","Description":"Filière S requise + moyenne > 12/20."},
        {"Université":"Université de Montréal","Ville":"Canada","Type":"Privée","Domaine":"Médecine/Pharmacie","Lien":"https://www.umontreal.ca","Logo":"university_logos/umontreal.png","Description":"Exige diplômes validés et français courant."}
    ],
    "Journaliste": [
        {"Université":"ESSTIC","Ville":"Yaoundé","Type":"Publique","Domaine":"Communication/Journalisme","Lien":"https://www.esstic.cm","Logo":"university_logos/esstic.png","Description":"Filière L recommandée."},
        {"Université":"Université de Montréal","Ville":"Canada","Type":"Privée","Domaine":"Journalisme","Lien":"https://www.umontreal.ca","Logo":"university_logos/umontreal.png","Description":"Exige portfolio + langue d’enseignement."}
    ],
    "Avocat": [
        {"Université":"Université de Yaoundé II - Droit","Ville":"Yaoundé","Type":"Publique","Domaine":"Droit","Lien":"https://www.uni-yaounde2.cm","Logo":"university_logos/uy2.png","Description":"Filière L + concours d’entrée."},
        {"Université":"Université Panthéon-Assas (Paris 2)","Ville":"France","Type":"Publique","Domaine":"Droit","Lien":"https://www.u-paris2.fr","Logo":"university_logos/assas.png","Description":"Baccalauréat L ou S + concours français."}
    ],
    "Enseignant": [
        {"Université":"Université de Yaoundé I - Faculté des Lettres","Ville":"Yaoundé","Type":"Publique","Domaine":"Enseignement","Lien":"https://www.uy1.cm","Logo":"university_logos/uy1.png","Description":"Filière L ou S + préparation pédagogique."}
    ],
    "Banquier": [
        {"Université":"Université de Douala - Économie et Gestion","Ville":"Douala","Type":"Publique","Domaine":"Finance/Banque","Lien":"https://www.univ-douala.cm","Logo":"university_logos/univdouala.png","Description":"Filière S ou Éco + bonne moyenne en maths."},
        {"Université":"HEC Paris","Ville":"France","Type":"Privée","Domaine":"Finance","Lien":"https://www.hec.edu","Logo":"university_logos/hec.png","Description":"Exige excellentes notes + concours d’entrée."}
    ],
    "Business": [
        {"Université":"Université de Yaoundé II - Faculté d’Économie et Gestion","Ville":"Yaoundé","Type":"Publique","Domaine":"Commerce/Management","Lien":"https://www.uni-yaounde2.cm","Logo":"university_logos/uy2.png","Description":"Filière S ou Éco + projets entrepreneuriaux."},
        {"Université":"INSEAD","Ville":"France/Singapour","Type":"Privée","Domaine":"Business","Lien":"https://www.insead.edu","Logo":"university_logos/insead.png","Description":"Exige excellent dossier académique et test GMAT."}
    ],
    "Écrivain": [
        {"Université":"Université de Yaoundé I - Lettres","Ville":"Yaoundé","Type":"Publique","Domaine":"Littérature","Lien":"https://www.uy1.cm","Logo":"university_logos/uy1.png","Description":"Filière L + ateliers d’écriture."},
        {"Université":"Sorbonne Université","Ville":"France","Type":"Publique","Domaine":"Littérature","Lien":"https://www.sorbonne-universite.fr","Logo":"university_logos/sorbonne.png","Description":"Filière L + langue française parfaite."}
    ],
    "Historien": [
        {"Université":"Université de Yaoundé I - Histoire","Ville":"Yaoundé","Type":"Publique","Domaine":"Histoire","Lien":"https://www.uy1.cm","Logo":"university_logos/uy1.png","Description":"Filière L + recherche historique."}
    ],
    "Politicien": [
        {"Université":"Sciences Po Paris","Ville":"France","Type":"Privée","Domaine":"Sciences Politiques","Lien":"https://www.sciencespo.fr","Logo":"university_logos/sciencespo.png","Description":"Exige dossier académique + tests d’admission."}
    ],
    "Psychologue": [
        {"Université":"Université de Yaoundé I - Psychologie","Ville":"Yaoundé","Type":"Publique","Domaine":"Psychologie","Lien":"https://www.uy1.cm","Logo":"university_logos/uy1.png","Description":"Filière S ou L + préparation à la psychologie clinique."}
    ],

    # Terminal TI (exemples)
    "IA":[
        {"Université":"Université de Yaoundé I - FSI","Ville":"Yaoundé","Type":"Publique","Domaine":"IA","Lien":"https://facsciences.uy1.cm","Logo":"university_logos/uy1.png","Description":"Filière TI ou S + projets IA."},
        {"Université":"ICT University","Ville":"Yaoundé","Type":"Privée","Domaine":"IA","Lien":"https://www.ictuniversity.edu.cm","Logo":"university_logos/ict.png","Description":"Pratique intensive en ML et IA."}
    ],
    "Data Science":[
        {"Université":"ICT University","Ville":"Yaoundé","Type":"Privée","Domaine":"Data Science","Lien":"https://www.ictuniversity.edu.cm","Logo":"university_logos/ict.png","Description":"Big Data, ML, Python."}
    ],
    "Web development":[
        {"Université":"Université de Yaoundé I - Dépt. Informatique","Ville":"Yaoundé","Type":"Publique","Domaine":"Web Dev","Lien":"https://facsciences.uy1.cm","Logo":"university_logos/uy1.png","Description":"Frontend/Backend/BD."}
    ],
    # fallback
    "Default":[
        {"Université":"Université de Yaoundé I","Ville":"Yaoundé","Type":"Publique","Domaine":"Général","Lien":"https://www.uy1.cm","Logo":"university_logos/uy1.png","Description":"Université publique de référence au Cameroun."}
    ]
}

# Fonction pour récupérer universités par métier
def suggest_universities_with_meta(career):
    return UNIVERSITY_DB.get(career, UNIVERSITY_DB["Default"])

# Fonction pour afficher universités avec style
def display_universities_list(unis):
    for uni in unis:
        cols = st.columns([1,5])
        logo_path = uni.get("Logo","")
        with cols[0]:
            if logo_path and os.path.exists(logo_path):
                st.image(Image.open(logo_path), width=72)
        with cols[1]:
            name = uni.get("Université","—")
            lien = uni.get("Lien","")
            ville = uni.get("Ville","")
            typ = uni.get("Type","")
            domaine = uni.get("Domaine","")
            desc = uni.get("Description","")
            if lien:
                st.markdown(f"<div class='univ-name'><a href='{lien}' target='_blank' style='color:inherit;text-decoration:none'>{name}</a></div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='univ-name'>{name}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='univ-meta'>{ville} — {typ} — Domaine: {domaine}</div>", unsafe_allow_html=True)
            if desc:
                st.markdown(f"<div class='univ-desc'>{desc}</div>", unsafe_allow_html=True)
        st.markdown("---")

# ---------------------------
# --- SESSION STATE pour bouton ---
# ---------------------------
if "career_acd" not in st.session_state:
    st.session_state["career_acd"] = None
if "show_unis_acd" not in st.session_state:
    st.session_state["show_unis_acd"] = False
if "career_ti" not in st.session_state:
    st.session_state["career_ti"] = None
if "show_unis_ti" not in st.session_state:
    st.session_state["show_unis_ti"] = False

# ---------------------------
# Terminal A,C&D
# ---------------------------
if classe=="Terminal A,C&D":
    st.markdown("## 📘 Formulaire - Terminal A,C&D")
    try:
        model = joblib.load("modele_metier.pkl")
        encoders = joblib.load("label_encoder.pkl")
    except Exception as e:
        st.error(f"Erreur chargement modèle/encodeur: {e}")
        st.stop()

    with st.form("form_D"):
        part_time_job = st.selectbox("🧑‍💼 Job à temps partiel ?", [0,1])
        absence_days = st.number_input("📅 Jours d'absence", 0,10)
        weekly_self_study_hours = st.number_input("📚 Heures d'étude perso / semaine",0,20)
        math = st.slider("📐 Mathématiques",0,20)
        physics = st.slider("⚛ Physique",0,20)
        chemistry = st.slider("🧪 Chimie",0,20)
        biology = st.slider("🧬 Biologie",0,20)
        english = st.slider("📖 Anglais",0,20)
        history = st.slider("📜 Histoire",0,20)
        geography = st.slider("🌍 Géographie",0,20)

        submit_D = st.form_submit_button("🔮 Prédire ma carrière")

    if submit_D:
        input_data = pd.DataFrame([{
            'part_time_job': part_time_job,
            'absence_days': absence_days,
            'weekly_self_study_hours': weekly_self_study_hours,
            'math': math,
            'history': history,
            'physics': physics,
            'chemistry': chemistry,
            'biology': biology,
            'english': english,
            'geography': geography
        }])
        try:
            prediction = model.predict(input_data)
            career = encoders['career_aspiration'].inverse_transform(prediction)[0]
        except Exception as e:
            st.error(f"Erreur prédiction : {e}")
            st.stop()

        st.session_state["career_acd"] = career
        st.session_state["show_unis_acd"] = False

        st.success(f"💼 Métier prédit : **{career}**")
        st.balloons()

        img_path = f"career_images/{career}.jpg"
        if os.path.exists(img_path):
            st.image(Image.open(img_path), caption=f"💡 {career}", use_container_width=True)

        unis_meta = suggest_universities_with_meta(career)
        domaine = unis_meta[0].get("Domaine","Général")
        st.markdown(f"**Domaine d'étude conseillé :** {domaine}")
        st.info(f"Conseil : Si tu veux devenir **{career}**, travaille particulièrement les matières liées à *{domaine}* et fais des projets/stages.")

    if st.session_state["career_acd"]:
        if st.button("📚 Voir les universités conseillées", key="btn_acd_pro"):
            st.session_state["show_unis_acd"] = True

    if st.session_state["show_unis_acd"]:
        career = st.session_state["career_acd"]
        with st.expander(f"Universités recommandées pour {career}", expanded=True):
            display_universities_list(suggest_universities_with_meta(career))

# ---------------------------
# Terminal TI
# ---------------------------
elif classe=="Terminal TI":
    st.markdown("## 💻 Formulaire - Terminal TI")
    try:
        model = joblib.load("modele.pkl")
        le = joblib.load("label.pkl")
    except Exception as e:
        st.error(f"Erreur chargement modèle/label: {e}")
        st.stop()

    with st.form("form_TI"):
        moyenne = st.number_input("📊 Moyenne Générale",0.0,20.0,step=0.1)
        interested_domain = st.selectbox("💡 Domaine d'intérêt",[
            'IA','Web development','Data Science','Cybersecurity','Cloud Computing+','Robotique',
            'Software Development','Machine Learning','Database Management','Computer Graphics',
            'Sofware Engineering','Mobile App Development','Network Security','Game Development',
            'Bioinformatics','Natural Language Processing','Biomedical Computing','Geographic Information System'
        ])
        projects = st.number_input("🛠️ Projets réalisés",0,10)
        java = st.selectbox("☕ Java ?",["Oui","Non"])
        python = st.selectbox("🐍 Python ?",["Oui","Non"])

        submit_TI = st.form_submit_button("🔮 Prédire carrière informatique")

    if submit_TI:
        user_data = pd.DataFrame({
            'moyenne':[moyenne],
            'Projects':[projects],
            'Java':[1 if java=="Oui" else 0],
            'python':[1 if python=="Oui" else 0],
            'Interested Domain':[interested_domain]
        })
        user_data = pd.get_dummies(user_data, columns=['Interested Domain'])
        for col in model.feature_names_in_:
            if col not in user_data.columns:
                user_data[col]=0
        user_data = user_data[model.feature_names_in_]

        try:
            pred = model.predict(user_data)
            career = le['Future Career'].inverse_transform(pred)[0]
        except Exception as e:
            st.error(f"Erreur prédiction : {e}")
            st.stop()

        st.session_state["career_ti"] = career
        st.session_state["show_unis_ti"] = False

        st.success(f"💻 Métier technologique prédit : **{career}**")
        st.balloons()

        img_path = f"career_images_ti/{career}.jpg"
        if os.path.exists(img_path):
            st.image(Image.open(img_path), caption=f"💡 {career}", use_container_width=True)

        unis_meta = suggest_universities_with_meta(career)
        domaine = unis_meta[0].get("Domaine","Général")
        st.markdown(f"**Domaine d'étude conseillé :** {domaine}")
        st.info(f"Conseil : Pour devenir **{career}**, focalise-toi sur des projets concrets en *{domaine}* (GitHub, mini-projets, stages).")

    if st.session_state["career_ti"]:
        if st.button("📚 Voir les universités conseillées", key="btn_ti_pro"):
            st.session_state["show_unis_ti"] = True

    if st.session_state["show_unis_ti"]:
        career = st.session_state["career_ti"]
        with st.expander(f"Universités recommandées pour {career}", expanded=True):
            display_universities_list(suggest_universities_with_meta(career))






