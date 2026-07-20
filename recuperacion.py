import warnings
import ssl
import os

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

from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

carpeta_db = "./bd_vectorial"

def recuperar_contexto(pregunta, k=3):
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = Chroma(persist_directory=carpeta_db, embedding_function=embeddings)
    
    # Busca los fragmentos más relevantes en los documentos de O Market
    resultados = vectorstore.similarity_search(pregunta, k=k)
    
    contexto = "\n\n".join([doc.page_content for doc in resultados])
    return contexto