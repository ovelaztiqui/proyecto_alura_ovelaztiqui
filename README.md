# 🤖 Asistente Virtual IA - O Market

¡Bienvenido al repositorio del Asistente Virtual de O Market! Este proyecto es un agente de Inteligencia Artificial diseñado para atención al cliente, capaz de responder preguntas precisas basándose en la documentación oficial de la empresa (Políticas de envío, devoluciones, etc.).

Este proyecto fue desarrollado como parte del Challenge de Alura.

---

## 📖 Descripción General del Proyecto
El agente utiliza el enfoque **RAG (Retrieval-Augmented Generation)**. En lugar de inventar respuestas, el bot busca primero en una base de datos vectorial que contiene los documentos de la empresa y luego utiliza un modelo de lenguaje (LLM) para formular una respuesta clara, amigable y fundamentada únicamente en la información real proporcionada.

---

## 🏗️ Arquitectura de la Solución
La aplicación sigue un flujo de procesamiento de lenguaje natural (NLP) estructurado:
1. **Carga y Procesamiento:** Se leen los documentos oficiales (PDF/Word/TXT) y se dividen en fragmentos de texto (chunks).
2. **Embeddings e Indexación:** Los textos se convierten en vectores usando modelos de HuggingFace y se almacenan localmente en ChromaDB.
3. **Recuperación (Retrieval):** Cuando un usuario hace una pregunta, el sistema busca los fragmentos de texto más relevantes en la base de datos.
4. **Generación:** El contexto recuperado se envía a Google Gemini junto con un "Prompt" estructurado para generar la respuesta final.
5. **Interfaz de Usuario:** Todo esto es presentado a través de una interfaz web intuitiva construida con Streamlit.

---

## 🛠️ Tecnologías y Herramientas Utilizadas
*   **Lenguaje:** Python 3.9
*   **Frontend:** Streamlit
*   **Orquestación de IA:** LangChain
*   **Modelo de Lenguaje (LLM):** Google Gemini (vía `langchain-google-genai`)
*   **Embeddings:** HuggingFace (`sentence-transformers`)
*   **Base de Datos Vectorial:** ChromaDB
*   **Infraestructura (Cloud):** Oracle Cloud Infrastructure (OCI) con Linux

---

## 🚀 Instrucciones para Ejecutar el Proyecto

### Ejecución Local (Tu PC)
1. Clona este repositorio:
   ```bash
   git clone [https://github.com/ovelaztiqui/proyecto_alura_ovelaztiqui.git](https://github.com/ovelaztiqui/proyecto_alura_ovelaztiqui.git)
   cd proyecto_alura_ovelaztiqui