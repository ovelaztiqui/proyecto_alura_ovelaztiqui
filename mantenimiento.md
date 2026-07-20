# ⚙️ Plan de Mantenimiento Continuo - O Market AI Bot

Para garantizar que el Asistente Virtual de O Market siga siendo preciso y confiable a medida que la empresa crece, implementaremos el siguiente ciclo de mantenimiento:

### 1. Pipeline de Actualización de Documentos
* **Rutina:** Cada vez que el equipo legal o de operaciones modifique una política (ej. cambio en tarifas de envío), el nuevo documento `.docx` reemplazará al antiguo en la carpeta `documentos_empresa`.
* **Ejecución:** Se ejecutará mensualmente (o bajo demanda) el script `procesamiento.py` para limpiar la base de datos vectorial y generar los nuevos embeddings automáticamente.

### 2. Curaduría de Contenido
* Se asignará a un responsable de **Atención al Cliente** para revisar trimestralmente que los 5 documentos fundacionales (Envíos, Devoluciones, Privacidad, Términos y FAQ) sean la versión más reciente y oficial de O Market.

### 3. Monitoreo de Calidad y Feedback
* Utilizaremos los botones de interacción (👍 / 👎) integrados en la interfaz de Streamlit. 
* Si una respuesta recibe múltiples 👎, se revisará si el error fue por alucinación del modelo o por falta de información en los `.docx`.

### 4. Ciclo de Mejora
* Las consultas frecuentes de los clientes que el bot responda con "No encontré esta información..." serán recopiladas.
* Con base en estas consultas huérfanas, redactaremos nuevos documentos de políticas (por ejemplo, "Política de Garantías") para agregarlos a la base de conocimiento vectorial.

### 5. Actualización del Modelo LLM
* Revisaremos semestralmente las nuevas versiones de los modelos de Google Gemini.
* Antes de cambiar el modelo en `chatbot.py` (ej. de `gemini-1.5-flash` a una futura versión), realizaremos pruebas en un entorno de desarrollo para asegurar que no degrade la calidad de las respuestas ni el tiempo de latencia.