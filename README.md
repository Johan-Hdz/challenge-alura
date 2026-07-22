# challenge-alura
# 🤖 Asistente Virtual de Políticas Corporativas (RAG)

## 📌 Descripción General del Proyecto
Este proyecto consiste en un Agente Inteligente basado en **RAG (Retrieval-Augmented Generation)** diseñado para consultar y responder preguntas sobre las políticas internas de una empresa (Reembolsos, Teletrabajo y Seguridad de la Información). El agente utiliza documentos PDF oficiales como fuente de conocimiento para garantizar respuestas precisas, evitando alucinaciones y negándose a responder temas fuera del alcance documental. Cuenta con una interfaz web interactiva desarrollada para facilitar la experiencia del usuario.

---

## 🏗️ Arquitectura de la Solución
La solución implementa un flujo RAG clásico utilizando LangChain y OpenAI:
1. **Carga y Fragmentación (*Loading & Splitting*):** Los archivos PDF institucionales son leídos y divididos en fragmentos (*chunks*) optimizados mediante un divisor basado en caracteres (`RecursiveCharacterTextSplitter`).
2. **Embeddings y Vector Store:** Los fragmentos se convierten en vectores utilizando modelos de OpenAI y se almacenan temporalmente en memoria mediante **FAISS** para permitir búsquedas semánticas rápidas.
3. **Recuperación y Generación (*Retrieval & LLM*):** Al recibir una pregunta, el sistema busca los fragmentos más relevantes y los inyecta como contexto en un prompt estricto, el cual es procesado por el modelo de lenguaje de OpenAI para redactar la respuesta final.
4. **Interfaz de Usuario:** La aplicación está montada sobre **Streamlit**, ofreciendo una interfaz de chat reactiva con historial de sesión.

---

## 🛠️ Tecnologías y Herramientas Utilizadas
* **Lenguaje:** Python 3.10+
* **Framework de IA:** LangChain (`langchain-openai`, `langchain-community`, etc.)
* **Modelos de IA:** OpenAI GPT-4o-mini (Generación) y `text-embedding-3-small` (Embeddings)
* **Base de Datos Vectorial:** FAISS
* **Procesamiento de PDF:** PyPDF
* **Interfaz Gráfica:** Streamlit
* **Control de Versiones y Despliegue:** Git, GitHub y Streamlit Cloud

---

## 🚀 Instrucciones para Ejecutar el Proyecto Localmente

Si deseas clonar y ejecutar este proyecto en tu entorno local, sigue estos pasos:

1. **Clonar el repositorio:**
   ```bash
   git clone [https://github.com/Johan-Hdz/challenge-alura.git](https://github.com/Johan-Hdz/challenge-alura.git)
   cd challenge-alura

2. **Crear y activar un entorno virtual:**

   * En **Windows (PowerShell)**:
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```

   * En **Mac / Linux**:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
3. **Instalar las dependencias:**
     ```bash
     pip install -r requirements.txt
4. **Configurar las credenciales:**
   Crea un archivo denominado .env en la raíz del proyecto y añade tu API Key de OpenAI:
   ```Windows
   OPENAI_API_KEY="tu-clave-real-de-openai"
5. Ejecutar la aplicación:
   ```Bash
   streamlit run agente_politicas.py



## 💡 Ejemplos de Preguntas que el Agente Puede Responder
* ¿Cuál es el límite de dinero cubierto por noche para hoteles en categoría estándar?
* ¿Qué requisitos necesito para solicitar la modalidad de teletrabajo?
* ¿Se permite enviar información confidencial a correos externos como Gmail?
* ¿Cuáles son las reglas para el reembolso de transporte terrestre (Uber/Cabify)?

---

## 💬 Ejemplos de Respuestas Generadas por el Agente

* **Pregunta:** ¿Qué requisitos necesito para solicitar teletrabajo?
  **Respuesta del Agente:**
  > Para solicitar teletrabajo, necesitas cumplir con los siguientes requisitos:
  > 1. Desempeñar funciones que puedan realizarse eficazmente fuera de la oficina.
  > 2. Haber completado el período de prueba de 6 meses.
  > 3. Contar con la aprobación formal de tu gerente directo.

* **Pregunta:** ¿En qué año fue la Segunda Guerra Mundial?
  **Respuesta del Agente:**
  > No está en las políticas.
