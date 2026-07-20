import streamlit as st
from chatbot import generar_respuesta

# Configuración de la página
st.set_page_config(
    page_title="O Market - Asistente IA",
    page_icon="🤖",
    layout="centered"
)

# ---------------------------------------------------------
# ELEMENTO 1: Indicación clara de que se habla con una IA
# ---------------------------------------------------------
st.title("🤖 Asistente Virtual - O Market")
st.caption("⚡ Agente de Inteligencia Artificial para atención a clientes. Respuestas basadas únicamente en documentación oficial.")

st.info("💡 **Aviso:** Estás interactuando con un asistente automatizado. Si necesitas atención humana, escribe a soporte@omarket.com", icon="ℹ️")

st.divider()

# ---------------------------------------------------------
# ELEMENTO 2: Historial de conversación (st.session_state)
# ---------------------------------------------------------
if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# Mostrar el historial guardado en la sesión
for i, msg in enumerate(st.session_state.mensajes):
    with st.chat_message(msg["rol"]):
        st.write(msg["contenido"])
        
        # ELEMENTO 3: Visualización de fuentes (si existen)
        if "fuentes" in msg and msg["fuentes"]:
            with st.expander("📚 Ver fuentes consultadas"):
                st.write(msg["fuentes"])

        # ELEMENTO 4: Botones de retroalimentación (solo para respuestas de la IA)
        if msg["rol"] == "assistant":
            col1, col2, _ = st.columns([1, 1, 8])
            with col1:
                if st.button("👍", key=f"up_{i}"):
                    st.toast("¡Gracias por tu retroalimentación positiva!", icon="✅")
            with col2:
                if st.button("👎", key=f"down_{i}"):
                    st.toast("Gracias. Usaremos esto para mejorar la base de conocimiento.", icon="📝")

# Entrada de texto para el cliente
pregunta_usuario = st.chat_input("Escribe tu consulta sobre envíos, devoluciones, pagos...")

if pregunta_usuario:
    # 1. Mostrar y guardar el mensaje del usuario
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta_usuario})
    with st.chat_message("user"):
        st.write(pregunta_usuario)

    # 2. Generar la respuesta con el chatbot
    with st.chat_message("assistant"):
        with st.spinner("Consultando políticas de O Market..."):
            try:
                respuesta_bruta = generar_respuesta(pregunta_usuario)
                
                # Separar la respuesta de la cita de fuentes si es posible
                if "Fuentes:" in respuesta_bruta:
                    partes = respuesta_bruta.split("Fuentes:")
                    texto_respuesta = partes[0].strip()
                    fuentes_texto = partes[1].strip()
                else:
                    texto_respuesta = respuesta_bruta
                    fuentes_texto = "Documentación general de O Market"

                st.write(texto_respuesta)
                
                # Mostrar fuentes en un desplegable
                with st.expander("📚 Ver fuentes consultadas"):
                    st.write(fuentes_texto)

                # Guardar respuesta en el historial
                st.session_state.mensajes.append({
                    "rol": "assistant",
                    "contenido": texto_respuesta,
                    "fuentes": fuentes_texto
                })
                
                # Forzar recarga ligera para habilitar los botones de feedback
                st.rerun()

            except Exception as e:
                st.error(f"⚠️ Detalle exacto del error: {e}")