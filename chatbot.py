import os
import ssl
import warnings
from dotenv import load_dotenv

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

# Cargar la API Key oculta desde el archivo .env
load_dotenv()

def generar_respuesta(pregunta):
    print("1. Buscando información en los documentos de O Market...")
    contexto_recuperado = recuperar_contexto(pregunta)
    
    print("2. Generando respuesta con Gemini...")
    llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", temperature=0)

    plantilla = """
    Eres el asistente virtual oficial de O Market. Tu tarea es responder a las preguntas de los clientes basándote ÚNICAMENTE en la información proporcionada en el siguiente 'Contexto'.

    REGLAS DE ORO:
    1. Si la respuesta no está en el 'Contexto', responde EXACTAMENTE: "No encontré esta información en nuestros documentos oficiales. Por favor, contacta a soporte escribiendo a soporte@omarket.com."
    2. Responde de forma cordial, clara y profesional en nombre de O Market.
    3. Cita la fuente al final de tu respuesta indicando el archivo o política de donde obtuviste la información.

    Contexto:
    {contexto}

    Pregunta del cliente: {pregunta}
    
    Respuesta final:
    """
    
    prompt = PromptTemplate(
        input_variables=["contexto", "pregunta"],
        template=plantilla
    )

    cadena = prompt | llm | StrOutputParser()
    resultado = cadena.invoke({"contexto": contexto_recuperado, "pregunta": pregunta})
    
    return resultado

if __name__ == "__main__":
    # Pregunta de prueba sobre la tienda
    pregunta_usuario = "¿Cuánto cuesta el envío exprés y cuántos días tengo para solicitar una devolución?"
    print(f"\nCliente: {pregunta_usuario}\n")
    
    respuesta = generar_respuesta(pregunta_usuario)
    
    print("\n=== RESPUESTA DE O MARKET ===")
    print(respuesta)
    print("=============================\n")