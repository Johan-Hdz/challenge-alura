import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_classic.chains.retrieval import create_retrieval_chain
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from openai import APIError, AuthenticationError, RateLimitError
import streamlit as st

BASE_DIR = Path(__file__).parent
CHAT_MODEL = "gpt-4o-mini"
EMBEDDING_MODEL = "text-embedding-3-small"

# Configuración inicial de la página de Streamlit
st.set_page_config(page_title="Agente de Políticas - Alura", page_icon="🤖")

st.title("💬 Asistente Virtual de Políticas")
st.write("Pregúntame sobre las políticas de la empresa basadas en los documentos PDF.")


def obtener_rutas_pdf() -> list[Path]:
    return sorted(BASE_DIR.glob("*.pdf"))


def cargar_documentos(rutas_pdf: list[Path]) -> list:
    documentos = []
    for ruta_pdf in rutas_pdf:
        loader = PyPDFLoader(str(ruta_pdf))
        documentos.extend(loader.load())
    return documentos


def crear_retriever(documentos: list):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
    )
    chunks = splitter.split_documents(documentos)

    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)
    vectorstore = FAISS.from_documents(chunks, embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 4})


def crear_cadena_politicas(retriever):
    prompt = ChatPromptTemplate.from_template(
        """
        Responde solo con base en el contexto.
        Si la respuesta no aparece en los documentos, di claramente que no esta en las politicas.

        Contexto:
        {context}

        Pregunta:
        {input}
        """.strip()
    )

    llm = ChatOpenAI(model=CHAT_MODEL, temperature=0)
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, question_answer_chain)


# Función cacheada para inicializar el agente una sola vez y optimizar el rendimiento
@st.cache_resource
def inicializar_agente():
    load_dotenv()

    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Falta la variable OPENAI_API_KEY en el archivo .env")

    rutas_pdf = obtener_rutas_pdf()
    if not rutas_pdf:
        raise FileNotFoundError("No se encontraron archivos PDF en la carpeta del proyecto")

    documentos = cargar_documentos(rutas_pdf)
    retriever = crear_retriever(documentos)
    chain = crear_cadena_politicas(retriever)
    return chain


# Inicializar el historial de chat en la sesión
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- REEMPLAZA ESTA PARTE ---
# Cargar el agente manejando posibles errores de API o archivos
try:
    with st.spinner("Cargando documentos y configurando el agente de políticas... por favor espera."):
        chain = inicializar_agente()
except Exception as exc:
    st.error(f"Error al inicializar el agente: {exc}")
    st.stop()
# ----------------------------

# Mostrar mensajes anteriores en la interfaz gráfica
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capturar la entrada del usuario en el chat inferior de Streamlit
if prompt := st.chat_input("Escribe tu pregunta sobre las políticas..."):
    # Guardar y mostrar mensaje del usuario
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generar la respuesta del asistente
    with st.chat_message("assistant"):
        with st.spinner("Buscando en las políticas..."):
            try:
                respuesta = chain.invoke({"input": prompt})
                texto_respuesta = respuesta["answer"]
            except RateLimitError:
                texto_respuesta = "Error al consultar el agente: cuota o límite de solicitudes agotado en la API de OpenAI."
            except (APIError, AuthenticationError, ValueError) as exc:
                texto_respuesta = f"Error al consultar el agente: {exc}"

            st.markdown(texto_respuesta)

    # Guardar la respuesta en el historial de la sesión
    st.session_state.messages.append({"role": "assistant", "content": texto_respuesta})