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
* **Lenguaje:** Python 3.9
* **Frontend:** Streamlit
* **Orquestación de IA:** LangChain
* **Modelo de Lenguaje (LLM):** Google Gemini (vía langchain-google-genai)
* **Embeddings:** HuggingFace (sentence-transformers)
* **Base de Datos Vectorial:** ChromaDB
* **Infraestructura (Cloud):** Oracle Cloud Infrastructure (OCI) con Linux

---

## 🚀 Instrucciones para Ejecutar el Proyecto

### Ejecución Local (Tu PC)

1. **Clona este repositorio:**
   git clone [https://github.com/ovelaztiqui/proyecto_alura_ovelaztiqui.git](https://github.com/ovelaztiqui/proyecto_alura_ovelaztiqui.git)
   cd proyecto_alura_ovelaztiqui

2. **Instala las dependencias:**
   pip install -r requirements.txt

3. **Crea un archivo .env en la raíz del proyecto y agrega tu API Key de Google:**
   GOOGLE_API_KEY=tu_clave_secreta_aqui

4. **Ejecuta la aplicación:**
   python -m streamlit run app.py

---

### Ejecución en Servidor Linux (OCI)
El proyecto incluye un parche automático en app.py que intercambia la versión del sistema de sqlite3 por pysqlite3-binary para garantizar la compatibilidad de ChromaDB en entornos Linux antiguos. Se recomienda usar nohup para mantener la ejecución en segundo plano:

nohup python3 -m streamlit run app.py &

---

## 💬 Ejemplos de Interacción

**Pregunta del usuario:**
> "¿Me das las opciones de envío por favor?"

**Respuesta del Agente:**
> "¡Hola! Con gusto te comparto las opciones de envío que tenemos disponibles en O Market:
> 1. **Envío Estándar:** Tiene un costo de $5 USD. El tiempo estimado de entrega es de 3 a 5 días hábiles.
> 2. **Envío Exprés:** Tiene un costo de $15 USD. El tiempo estimado de entrega es de 24 a 48 horas hábiles.
> 
> Además, ofrecemos **Envío Gratuito** (estándar) para todas las compras que superen los $100 USD.
> 
> *Fuente: Documentación general de O Market*"

---

## ☁️ Evidencia del Deploy en OCI
La aplicación se encuentra desplegada y funcionando de manera ininterrumpida en una instancia de Oracle Cloud Infrastructure (OCI). 
* **Enlace Público:** [http://137.131.176.198:8501](http://137.131.176.198:8501)
* **Nota:** Puedes revisar la carpeta evidencias/ de este repositorio para ver capturas de pantalla de los logs del backend y videos del funcionamiento.