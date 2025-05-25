# Uvicorn is the ASGI server used to run the FastAPI application
import uvicorn

# FastAPI framework imports
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

# Load environment variables from a .env file
from dotenv import load_dotenv

# LangChain modules for building chains and handling I/O
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

# Custom Retriever class that loads and calls AstraDB vector retriever
from retriever.retrieval import Retriever

# Utility class for loading LLM and embeddings
from utils.model_loader import ModelLoader

# Dictionary containing prompt templates
from prompt_library.prompt import PROMPT_TEMPLATES


# Create the FastAPI application instance
app = FastAPI()

# Mount static files like CSS/JS to the `/static` route from the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up Jinja2 template rendering from the 'templates' directory
templates = Jinja2Templates(directory="templates")

# Enable Cross-Origin Resource Sharing (CORS) for all domains and methods
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins (you can restrict this in production)
    allow_credentials=True,
    allow_methods=["*"],           # Allow all HTTP methods
    allow_headers=["*"],           # Allow all headers
)

# Load environment variables from .env file into the environment
load_dotenv()

# Instantiate the retriever and model loader (shared across requests)
retriever_obj = Retriever()
model_loader = ModelLoader()

# Function to handle the LLM chain logic
def invoke_chain(query: str):
    # Load the retriever object (wraps the AstraDB vector store)
    retriever = retriever_obj.load_retriever()

    # Load the prompt template from the dictionary of templates
    prompt = ChatPromptTemplate.from_template(PROMPT_TEMPLATES["product_bot"])

    # Load the LLM (e.g., OpenAI or other) via the model loader
    llm = model_loader.load_llm()

    # Build the chain:
    # 1. Use retriever to inject context
    # 2. Pass context + user question to the prompt
    # 3. Feed prompt to LLM
    # 4. Parse LLM output to string
    chain = (
        {"context": retriever, "question": RunnablePassthrough()}  # Pass question as-is
        | prompt
        | llm
        | StrOutputParser()   # Parse output into a clean string
    )

    # Invoke the chain with the user's query and get the result
    output = chain.invoke(query)

    return output

# GET endpoint to render the chat HTML page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the chat interface HTML page using Jinja2.
    """
    return templates.TemplateResponse("chat.html", {"request": request})

# POST endpoint to handle chat form submissions
@app.post("/get", response_class=HTMLResponse)
async def chat(msg: str = Form(...)):  # `msg` is the user input from the form
    result = invoke_chain(msg)         # Get the response from the chain
    print(f"Response: {result}")       # Log the result to the console (for debugging)
    return result                      # Return the LLM response to the frontend


#Use this commad to run the app on webpage
"""uvicorn main:app --reload --port 8001"""

#My project was up and runing fine