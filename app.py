import gradio as gr
from fuzzywuzzy import fuzz

def responder(mensaje):
    respuestas = {
        "hola": "¡Hola! Soy Deneh, la estrella del buen trato. ¿Quieres ayudarme a brillar?",
        "cómo estás": "¡Estoy muy ilusionada de hablar contigo! 😊",
        "qué es axia": "AXIA es una alianza para luchar contra la sombra y defender el buen trato.",
        "adiós": "¡Hasta pronto! Gracias por compartir tu luz conmigo 🌟",
    }

    mensaje = mensaje.lower()
    mejor_respuesta = "No entendí bien... ¿puedes decirlo de otra forma?"

    mayor_similitud = 0
    for clave, respuesta in respuestas.items():
        similitud = fuzz.partial_ratio(mensaje, clave)
        if similitud > mayor_similitud and similitud > 70:
            mayor_similitud = similitud
            mejor_respuesta = respuesta

    return mejor_respuesta

iface = gr.Interface(fn=responder, inputs="text", outputs="text", title="Deneh: a estrela do bo trato")
iface.launch()
