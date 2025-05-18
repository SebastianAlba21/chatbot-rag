# Chatbot RAG interactivo con PDF

## Descripción

Proyecto de chatbot que responde preguntas basadas en documentos PDF usando **Retrieval-Augmented Generation (RAG)**. Combina extracción de texto, embeddings, búsqueda vectorial y generación contextual con Langchain, ChromaDB, Ollama y Streamlit.

Forma parte de la especialización en Inteligencia Artificial, integrando conceptos clave para un desarrollo ágil y modular.

---

## Estructura del proyecto

```plaintext
chatbot-rag/
├── src/
│   ├── app.py           # Código principal del chatbot
│   └── rag.py           # Lógica para procesamiento RAG
├── data/
│   ├── documento.pdf    # PDF de ejemplo para pruebas
│   └── imagen_langchain.jpeg  # Imagen relacionada con Langchain
├── .gitignore           # Archivos y carpetas excluidos del repositorio
├── pyproject.toml       # Configuración opcional del proyecto
├── .python-version      # Versión de Python utilizada (opcional)
├── README.md            # Documentación del proyecto
└── requirements.txt     # Dependencias necesarias

---

## Instalación y configuración

1. Clona el repositorio

```bash
git clone https://github.com/tu_usuario/chatbot-rag.git
cd chatbot-rag
```

# 2. Crea y activa el entorno virtual

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell
.venv\Scripts\activate
```

# 3. Instala dependencias
```bash
pip install -r requirements.txt
```

# 4. Instala paquete extra para Ollama LLM (no está en PyPI)
```bash
pip install git+https://github.com/usuario/langchain-community-llms-ollama.git
```

# 5. Configura variables de entorno en archivo .env:

LANGSMITH_API_KEY=tu_api_key_aqui
LANGSMITH_PROJECT_NAME=RAG
LANGSMITH_SESSION_NAME=SesionDePrueba

Uso
Ejecuta la aplicación:
```bash
streamlit run src/app.py
```
# Funcionalidades

- Carga de archivos PDF para crear base de conocimiento.

- Preguntas interactivas sobre el contenido del PDF.

- Visualización de fragmentos usados para la respuesta.

- Monitoreo de interacciones en Langsmith (opcional).

| Pregunta                                            | Respuesta esperada                                     |
| --------------------------------------------------- | ------------------------------------------------------ |
| ¿Qué es la inteligencia artificial?                 | Definición, historia y clasificación de la IA.         |
| ¿Cuáles son las técnicas de aprendizaje automático? | Supervisado, no supervisado y por refuerzo.            |
| ¿Qué es RAG y cómo se aplica?                       | Explicación del método Retrieval-Augmented Generation. |

# Consideraciones técnicas

- Modelo de embeddings: nomic-embed-text (Ollama, local).

- Base de datos vectorial: ChromaDB con persistencia.

- Interfaz: Streamlit (posible adaptación a Mesop).

- Monitoreo: Langsmith para trazabilidad y métricas.


