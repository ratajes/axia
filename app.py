
import streamlit as st
from PIL import Image
import difflib
from transformers import pipeline

# Cargar fondo estelar
page_bg_img = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('imagenes_deneh/fondo_estelar.jpg');
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}
[data-testid="stHeader"], [data-testid="stToolbar"] {
    background-color: rgba(0,0,0,0);
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Inicializar estado de sesión
if "brillo" not in st.session_state:
    st.session_state.brillo = 1
    st.session_state.mensajes = set()
    st.session_state.musica_activa = False
    st.session_state.finalizado = False

# Cargar clasificador de sentimiento
@st.cache_resource
def cargar_modelo():
    return pipeline("sentiment-analysis")

modelo_sentimiento = cargar_modelo()

# Título
st.markdown("<h1 style='text-align: center; color: white;'>🌟 Habla con Deneh 🌟</h1>", unsafe_allow_html=True)

# Columna para música y reinicio
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🔊 Activar música"):
        st.session_state.musica_activa = True
    if st.session_state.musica_activa:
        st.markdown("""
        <audio autoplay loop controls style='display:none'>
          <source src="axia_cancion.mp3" type="audio/mpeg">
        </audio>
        """, unsafe_allow_html=True)
    if st.session_state.finalizado:
        if st.button("🔁 Reiniciar"):
            st.session_state.brillo = 1
            st.session_state.mensajes = set()
            st.session_state.finalizado = False

# Entrada de usuario
user_input = st.text_input("Escribe un mensaje para Deneh", "", key="input_mensaje", on_change=lambda: None)

# Evaluación del mensaje
if user_input:
    if user_input in st.session_state.mensajes:
        st.warning("⚠️ Ya has enviado este mensaje.")
    else:
        resultado = modelo_sentimiento(user_input)[0]
        if resultado['label'] == 'NEGATIVE':
            st.warning("😔 Ese mensaje no ayuda a Deneh a brillar.")
        else:
            st.session_state.mensajes.add(user_input)
            if st.session_state.brillo < 5:
                st.session_state.brillo += 1

# Mostrar imagen correspondiente
img_path = f"imagenes_deneh/deneh_{st.session_state.brillo}.png"
try:
    img = Image.open(img_path)
    st.image(img, use_column_width=True)
except:
    st.error("No se pudo cargar la imagen.")

# Mostrar barra de progreso
st.progress(st.session_state.brillo / 5)

# Mensaje final
if st.session_state.brillo == 5:
    st.markdown("""
    <h2 style='color: yellow; text-align: center;'>🌟 Gracias a vosotras y vosotros, ¡Deneh ha vuelto a brillar! 🌟</h2>
    """, unsafe_allow_html=True)
    st.session_state.finalizado = True
