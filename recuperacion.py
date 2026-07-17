import os
import ssl
import warnings

# --- SÚPER PARCHE ANTIBLOQUEO CORPORATIVO ---
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
# ---------------------------------------------

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def recuperar_contexto(pregunta):
    """
    Toma una pregunta, busca en la base de datos vectorial
    y ensambla un bloque de texto con los mejores fragmentos.
    """
    # 1. Cargamos el modelo matemático (en español)
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    # 2. Conectamos a la base de datos
    carpeta_db = "./base_de_datos_chroma"
    vectorstore = Chroma(persist_directory=carpeta_db, embedding_function=embeddings)
    
    # 3. Búsqueda Semántica (traemos los 3 mejores fragmentos)
    resultados = vectorstore.similarity_search(pregunta, k=3)
    
    # 4. ENSAMBLAJE DEL CONTEXTO (El punto 5 de tu tarjeta)
    # Aquí unimos los fragmentos en un formato claro para que el LLM lo pueda leer después
    contexto_ensamblado = ""
    for doc in resultados:
        fuente = doc.metadata.get('source', 'Documento desconocido')
        contenido = doc.page_content
        contexto_ensamblado += f"Fuente: {fuente}\nContenido: {contenido}\n\n"
        
    return contexto_ensamblado

# --- PRUEBA DEL MÓDULO ---
if __name__ == "__main__":
    pregunta_prueba = "¿De cuánto es el límite para gastos de alimentación?"
    print(f"Pregunta del usuario: '{pregunta_prueba}'\n")
    
    # Llamamos a nuestra nueva función
    contexto_listo = recuperar_contexto(pregunta_prueba)
    
    print("=== CONTEXTO ENSAMBLADO PARA EL CHATBOT ===")
    print(contexto_listo)
    print("===========================================")