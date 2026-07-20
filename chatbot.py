from dotenv import load_dotenv
import os
import ssl
import warnings

# --- PARCHE ANTIBLOQUEO CORPORATIVO ---
warnings.filterwarnings("ignore")
try:
    import httpx
    original_init = httpx.Client.__init__
    def patched_init(self, *args, **kwargs):
        kwargs['verify'] = False
        original_init(self, *args, **kwargs)
    httpx.Client.__init__ = patched_init
except ImportError:
    pass

os.environ["HF_HUB_DISABLE_SSL_VERIFICATION"] = "1"
ssl._create_default_https_context = ssl._create_unverified_context
# ----------------------------------------

from recuperacion import recuperar_contexto
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Cargar las variables de entorno desde el archivo .env
load_dotenv()


def generar_respuesta(pregunta):
    print("1. Buscando fragmentos en la base de datos local...")
    contexto_recuperado = recuperar_contexto(pregunta)
    
    print("2. Enviando contexto al 'cerebro' de Gemini...")
    # Usamos el modelo exacto que acepta tu llave
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

    plantilla = """
    Eres un asistente corporativo experto. Tu tarea es responder a la pregunta del colaborador basándote ÚNICAMENTE en la información proporcionada en el siguiente 'Contexto'.

    REGLAS DE ORO:
    1. Si la respuesta a la pregunta no está en el 'Contexto', no inventes información. Debes responder EXACTAMENTE con esta frase: "No encontré esta información en los documentos disponibles. Por favor, ponte en contacto con el área responsable correspondiente (RH, Finanzas, Legal, etc.)."
    2. Si encuentras la respuesta, redáctala de forma clara y amable.
    3. Siempre debes citar la fuente al final de tu respuesta (indicando el nombre del archivo de donde sacaste la información).

    Contexto:
    {contexto}

    Pregunta del colaborador: {pregunta}
    
    Respuesta final:
    """
    
    prompt = PromptTemplate(
        input_variables=["contexto", "pregunta"],
        template=plantilla
    )

    # Conectamos las piezas y agregamos el filtro para limpiar el texto de salida
    cadena = prompt | llm | StrOutputParser()
    
    # Invocamos la generación de la respuesta
    resultado = cadena.invoke({"contexto": contexto_recuperado, "pregunta": pregunta})
    
    return resultado

if __name__ == "__main__":
    pregunta_usuario = "¿Cuántos días de vacaciones tengo y cuánto dinero me dan por día para alimentación en un viaje?"
    print(f"\nUsuario: {pregunta_usuario}\n")
    
    respuesta = generar_respuesta(pregunta_usuario)
    
    print("\n=== RESPUESTA FINAL DEL BOT ===")
    print(respuesta)
    print("===============================\n")