import streamlit as st
import base64
import os

# --------- CONFIG ---------
st.set_page_config(page_title="Orientation Carrière", layout="wide")

# --------- IMAGE FOND ---------
def get_base64(file):
    with open(file, "rb") as f:
        return base64.b64encode(f.read()).decode()

img_path = "IMG-20260412-WA0034.jpg"

if os.path.exists(img_path):
    img_base64 = get_base64(img_path)

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{img_base64}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    h1 {{
        color: white !important;
        text-align: center;
        font-weight: bold;
    }}

    /* 🔥 CONTENEUR EN BAS */
    .bottom-cards {{
        position: fixed;
        bottom: 20px;
        left: 0;
        width: 100%;
        padding: 20px;
    }}

    /* Cartes */
    .card {{
        position:absolute;
        text-align: center;
    }}

    .card img {{
        width: 100%;
        border-radius: 12px;
    }}

    .stButton>button {{
        background-color: #444;
        color: white;
        border-radius: 10px;
        width: 100%;
    }}

    </style>
    """, unsafe_allow_html=True)

# --------- TITRE ---------
st.markdown("<h1>🎓 DECOUVRE TON FUTURE METIER</h1>", unsafe_allow_html=True)
st.markdown("<h1>🎓 Choisis ta série</h1>", unsafe_allow_html=True)

# --------- CONTENEUR BAS ---------
st.markdown('<div class="bottom-cards">', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)

# Terminal C
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("IMG-20260412-WA0051.jpg")
    if st.button("Choisir C", key="c"):
        st.switch_page("pages/TleC.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Terminal D
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("IMG-20260412-WA0052.jpg")
    if st.button("Choisir D", key="d"):
        st.switch_page("pages/TleD.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Terminal A
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("IMG-20260412-WA0050.jpg")
    if st.button("Choisir A", key="a"):
        st.switch_page("pages/TleA.py")
    st.markdown('</div>', unsafe_allow_html=True)

# Terminal TI
with col4:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.image("IMG-20260412-WA0049.jpg")
    if st.button("Choisir TI", key="ti"):
        st.switch_page("pages/TleTI.py")
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)