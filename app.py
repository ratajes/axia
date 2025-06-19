
import streamlit as st
from fuzzywuzzy import fuzz

# Inicialización de estados
if "brillo" not in st.session_state:
    st.session_state.brillo = 1
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []
if "musica_activa" not in st.session_state:
    st.session_state.musica_activa = False
if "ultimo_mensaje" not in st.session_state:
    st.session_state.ultimo_mensaje = ""
if "fin_activado" not in st.session_state:
    st.session_state.fin_activado = False

# Fondos
fondo_normal = """
<style>
body {
    background-image: url('https://raw.githubusercontent.com/meninos/Deneh_bot/main/imagenes_deneh/fondo_espacial.jpg');
    background-size: cover;
}
</style>
"""

fondo_estelar = """
<style>
body {
    background-image: url('https://raw.githubusercontent.com/meninos/Deneh_bot/main/imagenes_deneh/fondo_estelar.jpg');
    background-size: cover;
}
</style>
"""

# Censura y NPL simple
mensajes_negativos = ["no me gustas", "eres fea", "me caes mal", "nadie te quiere", "no sirves", "no vales"]
def mensaje_valido(mensaje):
    for neg in mensajes_negativos:
        if fuzz.ratio(mensaje.lower(), neg) > 80:
            return False
    return True

# Fondo dinámico
st.markdown(fondo_estelar if st.session_state.fin_activado else fondo_normal, unsafe_allow_html=True)

# Título
st.markdown("<h1 style='text-align:center; color:white;'>🌟 Proyecto AXIA: Deneh 🌟</h1>", unsafe_allow_html=True)

# Música galáctica
if st.button("🔊 Activar música"):
    st.session_state.musica_activa = True

if st.session_state.musica_activa:
    st.markdown("""
        <audio autoplay loop style='display:none'>
        <source src='https://raw.githubusercontent.com/meninos/Deneh_bot/main/axia_cancion.mp3' type='audio/mpeg'>
        </audio>
    """, unsafe_allow_html=True)

# Imágenes y barra
img_path = f"https://raw.githubusercontent.com/meninos/Deneh_bot/main/imagenes_deneh/brillo_{st.session_state.brillo}.png"
st.image(img_path, use_column_width=True)

# Panel de mensajes y formulario
with st.form("formulario"):
    mensaje = st.text_input("Escribe un mensaje para Deneh", key="input")
    enviado = st.form_submit_button("Enviar")

if enviado and mensaje.strip() != "" and mensaje != st.session_state.ultimo_mensaje:
    st.session_state.ultimo_mensaje = mensaje
    st.session_state.mensajes.append(mensaje)

    if mensaje_valido(mensaje):
        if st.session_state.brillo < 5:
            st.session_state.brillo += 1
        if st.session_state.brillo == 5:
            st.session_state.fin_activado = True

# Mensaje final grande
if st.session_state.fin_activado:
    st.markdown("<h2 style='color:lightgreen; text-align:center;'>💫 Gracias a vosotras y vosotros, Deneh ha vuelto a brillar 💫</h2>", unsafe_allow_html=True)
    if st.button("🔄 Reiniciar experiencia"):
        st.session_state.brillo = 1
        st.session_state.mensajes = []
        st.session_state.ultimo_mensaje = ""
        st.session_state.fin_activado = False

# Mostrar historial si no está en brillo 5
if not st.session_state.fin_activado:
    st.markdown("### Mensajes enviados:")
    for msg in st.session_state.mensajes:
        st.markdown(f"- {msg}")
