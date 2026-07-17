import os
import ssl
import warnings

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

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def buscar_en_base_de_datos():
    print("1. Cargando el modelo matemático multilingüe...")
    # Usamos el modelo experto en español
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    print("2. Conectando a la base de datos ChromaDB...")
    carpeta_db = "./base_de_datos_chroma"
    vectorstore = Chroma(persist_directory=carpeta_db, embedding_function=embeddings)
    
    pregunta = "¿Cuántos días de vacaciones tengo?"
    print(f"3. Buscando fragmentos relevantes para la pregunta: '{pregunta}'...\n")
    
    resultados = vectorstore.similarity_search(pregunta, k=2)
    
    print("=== FRAGMENTOS ENCONTRADOS ===")
    for i, doc in enumerate(resultados):
        print(f"\n[Resultado {i+1}]")
        print(f"Fuente: {doc.metadata['source']}")
        print(f"Contenido: {doc.page_content}")
    print("==============================")

if __name__ == "__main__":
    buscar_en_base_de_datos()