
import streamlit as st
import unicodedata
import random
from fuzzywuzzy import fuzz
import os
from PIL import Image

st.set_page_config(page_title="🌟 Proyecto AXIA: Habla con Deneh", layout="wide")

st.markdown("""
    <style>
    html, body, .stApp {
        background: linear-gradient(to bottom, #e6f0ff, #ffffff);
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }
    h1, h2, h3, .stTextInput label {
        color: #002244;
    }
    .mensaje-final {
        font-size: 2rem;
        font-weight: bold;
        text-align: center;
        color: #004080;
        background-color: #dff0ff;
        border-radius: 10px;
        padding: 1rem;
        margin-top: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

if "brillo" not in st.session_state:
    st.session_state.brillo = 1
if "mensajes" not in st.session_state:
    st.session_state.mensajes = 0
if "musica_activa" not in st.session_state:
    st.session_state.musica_activa = False
if "musica_mostrada" not in st.session_state:
    st.session_state.musica_mostrada = False

def mensaje_negativo(texto):
    palabras_malas = ["tonta", "fea", "te odio", "no vales", "maldita", "asco", "te detesto", "eres mala"]
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != "Mn")
    return any(p in texto for p in palabras_malas)

claves = {
    "ayuda": ["ayude", "ayudamos", "ayudarte"],
    "felicidad": ["feliz", "contenta", "alegre", "ya estas feliz"],
    "estado": ["como estas", "que tal", "estas bien"],
    "sombra": ["sombra", "la sombra"],
    "cariño": ["te queremos", "te amo", "os queremos", "me gustas"],
    "brillo": ["ya brillas", "brillando", "recuperaste tu luz"]
}

respuestas_deneh = {
    "ayuda": lambda: "¡Sí! Gracias por ayudarme a brillar ⭐" if st.session_state.brillo >= 4 else "¡Gracias por ayudarme, lo valoro mucho!",
    "felicidad": lambda: "¡Estoy feliz gracias a vosotros! ✨",
    "estado": lambda: [
        "Me siento triste... pero vuestras palabras ayudan 🌑",
        "Voy mejorando, gracias a vosotros 🌘",
        "Casi recuperada 🌟",
        "¡Brillo casi al máximo! 💫",
        "¡Estoy totalmente brillante! ✨"
    ][st.session_state.brillo - 1],
    "sombra": lambda: "La sombra aún existe, pero se hace pequeña con vuestra luz.",
    "cariño": lambda: "Gracias por vuestro cariño 💖",
    "brillo": lambda: "¡Sí! He vuelto a brillar con vuestra ayuda ✨" if st.session_state.brillo == 5 else "Todavía falta un poco para brillar por completo."
}

st.markdown("<h1 style='text-align:center;'>🌟 Proyecto AXIA: Habla con Deneh</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Envía un mensaje y observa cómo Deneh recupera su luz poco a poco...</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    if st.session_state.musica_activa:
        st.markdown("""
        <audio autoplay loop id="musica" style="display:none">
            <source src="axia_cancion.mp3" type="audio/mp3">
        </audio>
        """, unsafe_allow_html=True)

    if not st.session_state.musica_mostrada:
        if st.button("🔊 Activar música"):
            st.session_state.musica_activa = True
            st.session_state.musica_mostrada = True
        else:
            st.session_state.musica_activa = False
    else:
        if st.button("🔈 Silenciar música"):
            st.session_state.musica_activa = False
            st.session_state.musica_mostrada = False

    mensaje = st.text_input("Tu mensaje para Deneh")
    if st.button("Hablar con Deneh"):
        if mensaje.strip():
            if mensaje_negativo(mensaje):
                st.warning("Tus palabras me entristecen... 💔")
            else:
                clave = max(claves, key=lambda k: max(fuzz.partial_ratio(m, mensaje) for m in claves[k]))
                respuesta = respuestas_deneh[clave]() if clave in respuestas_deneh else "Gracias por tu mensaje 💫"
                st.success(respuesta)
                st.session_state.mensajes += 1
                st.session_state.brillo += 1
                if st.session_state.brillo > 5:
                    st.session_state.brillo = 1
        else:
            st.info("Escribe algo para hablar con Deneh.")

    st.markdown("### ✨ Estado de Deneh")
    st.progress(st.session_state.brillo / 5)
    st.text(f"Nivel de brillo: {st.session_state.brillo} / 5")
    st.text(f"Mensajes enviados: {st.session_state.mensajes}")

    if st.session_state.brillo == 5:
        st.markdown("<div class='mensaje-final'>🎉 ¡Gracias a vosotros, Deneh ha vuelto a brillar! 🌟</div>", unsafe_allow_html=True)

with col2:
    brillo = st.session_state.brillo
    ruta = f"imagenes_deneh/deneh_{brillo}.png"
    if os.path.exists(ruta):
        st.image(Image.open(ruta), use_container_width=True, caption="Deneh ahora")
    else:
        st.warning(f"No se encontró {ruta}")
