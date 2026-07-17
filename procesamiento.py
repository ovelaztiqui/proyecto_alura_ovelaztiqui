import os
import ssl
import warnings
import shutil  # <-- Para limpiar duplicados

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

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def procesar_documentos():
    print("1. Iniciando extracción de contenido...")
    loader = DirectoryLoader(
        './documentos_empresa', 
        glob="**/*.txt", 
        loader_cls=TextLoader, 
        loader_kwargs={'encoding': 'utf-8'}
    )
    documentos = loader.load()
    print(f"Se encontraron y leyeron {len(documentos)} documentos completos.")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=200,
        chunk_overlap=20
    )
    fragmentos = text_splitter.split_documents(documentos)
    print(f"2. Los documentos se dividieron en {len(fragmentos)} fragmentos pequeños.")
    
    print("\n3. Convirtiendo texto a números (Embeddings Multilingües) y guardando en ChromaDB...")
    
    # MEJORA 1: Cambiamos a un modelo experto en ESPAÑOL
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    carpeta_db = "./base_de_datos_chroma"
    
    # MEJORA 2: Si la carpeta ya existe, la borramos para eliminar duplicados viejos
    if os.path.exists(carpeta_db):
        shutil.rmtree(carpeta_db)
    
    vectorstore = Chroma.from_documents(
        documents=fragmentos,
        embedding=embeddings,
        persist_directory=carpeta_db
    )
    
    print(f"\n¡Éxito total! Tu base de datos limpia y en español se creó en: {carpeta_db}")
    return vectorstore

if __name__ == "__main__":
    procesar_documentos()