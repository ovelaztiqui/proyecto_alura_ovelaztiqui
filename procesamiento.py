import os
import shutil
import warnings
import ssl

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

from langchain_community.document_loaders import DirectoryLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

# Rutas exactas de tu proyecto
carpeta_documentos = "./documentos_empresa"
carpeta_db = "./bd_vectorial"

def procesar_documentos():
    # 1. Limpieza de la base de datos vieja
    if os.path.exists(carpeta_db):
        print("Borrando la base de datos anterior...")
        shutil.rmtree(carpeta_db)

    # 2. Cargar los nuevos documentos de Word (.docx)
    print("Leyendo archivos de Word (.docx)...")
    loader = DirectoryLoader(carpeta_documentos, glob="**/*.docx", loader_cls=Docx2txtLoader)
    documentos = loader.load()
    
    if not documentos:
        print(f"❌ No se encontraron archivos .docx en la carpeta '{carpeta_documentos}'.")
        return

    # 3. Dividir los textos en fragmentos
    print(f"Dividiendo {len(documentos)} documento(s) en fragmentos...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    fragmentos = text_splitter.split_documents(documentos)

    # 4. Crear los embeddings y guardar en la base de datos
    print("Creando la nueva base de datos vectorial...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    
    Chroma.from_documents(
        documents=fragmentos, 
        embedding=embeddings, 
        persist_directory=carpeta_db
    )

    print("✅ ¡Éxito! Base de datos actualizada correctamente con los documentos de Word.")

if __name__ == "__main__":
    procesar_documentos()