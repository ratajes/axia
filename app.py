
import streamlit as st
import unicodedata
import random
from fuzzywuzzy import fuzz
import os
from PIL import Image

st.set_page_config(page_title="🌟 Proyecto AXIA: Habla con Deneh", layout="wide")

# Fondo adaptado
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom, #f0f8ff, #e6f0ff);
        background-attachment: fixed;
        font-family: 'Arial', sans-serif;
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

# Estado inicial
if 'brillo' not in st.session_state:
    st.session_state.brillo = 1
if 'mensajes' not in st.session_state:
    st.session_state.mensajes = 0
if 'musica_activa' not in st.session_state:
    st.session_state.musica_activa = True

# Insertar música al inicio
if st.session_state.musica_activa:
    st.markdown("""
    <audio autoplay loop id="musica" style="display:none">
        <source src="https://meninos-axia.hf.space/file/axia_cancion.mp3" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

# Botón para silenciar/activar
if st.button("🔈 Silenciar música" if st.session_state.musica_activa else "🔊 Activar música"):
    st.session_state.musica_activa = not st.session_state.musica_activa

# Lista palabras negativas
palabras_negativas = [
    "tonta", "fea", "no te quiero", "me das miedo", "no vales", "eres mala", "te odio", "no sirves", "fuera"
]

def mensaje_negativo(texto):
    texto = unicodedata.normalize('NFD', texto.lower())
    texto = ''.join(c for c in texto if unicodedata.category(c) != 'Mn')
    return any(palabra in texto for palabra in palabras_negativas)

def normalizar_texto(texto):
    texto = texto.lower()
    texto = unicodedata.normalize('NFD', texto)
    return ''.join(c for c in texto if unicodedata.category(c) != 'Mn')

claves = {
    "ayuda": ["ayude", "ayudamos", "ayudarte", "yude", "ayudé", "te yude"],
    "felicidad": ["feliz", "felis", "contenta", "alegre", "estas felis", "ya estas feliz"],
    "tristeza": ["triste", "sigue triste", "apagada"],
    "estado": ["como estas", "como te sientes", "que tal", "estas bien", "como stas"],
    "cariño": ["te queremos", "os queremos", "te kiero", "os kiero", "te amo", "me gustas", "queremos cuidarte", "t kiero muxo"],
    "sombra": ["sombra", "la sombra", "ganamos a la sombra"],
    "brillo": ["ya brillas", "ya brillaste", "estas brillando", "volviste a brillar",
               "recuperaste tu luz", "tienes luz", "estas mejor", "brillas ya", "ya estas bien"]
}

def detectar_intencion_fuzzy(mensaje):
    mensaje = normalizar_texto(mensaje)
    mejor_match = ("", 0)
    for clave, variantes in claves.items():
        for variante in variantes:
            puntuacion = fuzz.partial_ratio(variante, mensaje)
            if puntuacion > mejor_match[1]:
                mejor_match = (clave, puntuacion)
    return mejor_match[0]

respuestas_deneh = {
    "ayuda": lambda: "¡Sí! Gracias a vosotras y vosotros estoy recuperando mi luz. Sois verdaderos héroes del buen trato ⭐"
        if st.session_state.brillo >= 4 else
        "Me estáis ayudando muchísimo, aunque aún me falta un poco para brillar del todo.",
    "felicidad": lambda: "¡Estoy más feliz que nunca! Me hicisteis volver a brillar con vuestra empatía ✨"
        if st.session_state.brillo == 5 else
        "Gracias a vuestras palabras y acciones me siento cada vez mejor. ¡Seguid brillando!",
    "tristeza": lambda: "Aún queda un poquito de sombra en mí, pero vuestra luz me reconforta.",
    "estado": lambda: [
        "Me siento un poco apagada... pero vuestras palabras me reconfortan 🌑",
        "Voy recuperando mi brillo poco a poco, gracias a vosotras y vosotros 🌙",
        "Estoy casi completamente luminosa. ¡Gracias por estar ahí! 🌟",
        "¡Estoy feliz y brillante! Vuestro buen trato lo ha hecho posible 💫",
        "¡Mi luz está más viva que nunca! ¡Gracias por iluminarme! ✨"
    ][st.session_state.brillo - 1],
    "brillo": lambda: "¡Sí! ¡Gracias a vosotras y vosotros he vuelto a brillar con fuerza! 🌟"
        if st.session_state.brillo == 5 else
        "Todavía me falta un poco, pero gracias a vuestras acciones estoy mucho mejor 💫",
    "cariño": lambda: "Yo también os quiero. ¡Gracias por cuidar de mí con vuestra luz interior 💖!",
    "sombra": lambda: "La sombra aún existe, pero cada gesto de buen trato que hacéis la hace más pequeña."
}

st.markdown("<h1 style='text-align: center;'>🌟 Proyecto AXIA: Habla con Deneh</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Envía un mensaje y observa cómo Deneh recupera su luz poco a poco...</p>", unsafe_allow_html=True)

col1, col2 = st.columns([2, 1])

with col1:
    mensaje = st.text_input("Tu mensaje para Deneh")
    if st.button("Hablar con Deneh"):
        if mensaje.strip():
            if mensaje_negativo(mensaje):
                st.warning("Tus palabras me hacen daño... pero aún confío en la luz que hay en ti 💔")
            else:
                intencion = detectar_intencion_fuzzy(mensaje)
                respuesta = respuestas_deneh[intencion]() if intencion in respuestas_deneh else random.choice([
                    "Gracias por escribirme, aunque no entienda todo, vuestra luz me llega igual.",
                    "¡Sois parte de mi recuperación! Seguid brillando.",
                    "Vuestras palabras me ayudan a curarme. ¡No dejéis de cuidaros y cuidar!",
                    "Aunque esté muy lejos, siento vuestra luz como un abrazo estelar."
                ])
                st.success(f"💬 {respuesta}")
                st.session_state.mensajes += 1
                st.session_state.brillo += 1
                if st.session_state.brillo > 5:
                    st.session_state.brillo = 1
        else:
            st.warning("Por favor escribe un mensaje para hablar con Deneh.")

    st.markdown("---")
    st.subheader("✨ Estado de Deneh")
    st.progress(st.session_state.brillo / 5)
    st.text(f"Nivel de brillo: {st.session_state.brillo} / 5")
    st.text(f"Mensajes enviados: {st.session_state.mensajes}")

    if st.session_state.brillo == 5:
        st.markdown("<div class='mensaje-final'>🎉 ¡Gracias a vosotros, Deneh ha vuelto a brillar! 🌟</div>", unsafe_allow_html=True)

with col2:
    brillo = st.session_state.brillo
    img_path = f"imagenes_deneh/deneh_{brillo}.png"
    if os.path.exists(img_path):
        st.image(Image.open(img_path), caption="Deneh ahora", use_container_width=True)
    else:
        st.warning(f"No se encontró la imagen: {img_path}")
