#This file is used to define the model configurations and load the model.

import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from config.config_loader import load_config

class ModelLoader:
    """
    A utility class to load embedding models and LLM models.
    """
    def __init__(self):     #Initialized automatically and used to set up any required logic.
        load_dotenv()
        self._validate_env()
        self.config=load_config()

        """self refers to the current object being created or used. 
        It allows access to the instance’s own variables and methods.
        self.config = load_config() This means: “store the result of load_config() inside this object’s config variable”."""

    def _validate_env(self):      #This "_validate_env" means this method is only called locally, and not outside the class directly (you cant import this as module). Demonstrates encapsulation: keeping validation logic hidden inside the class.
        """
        Validate necessary environment variables.
        """
        required_vars = ["GOOGLE_API_KEY"]
        missing_vars = [var for var in required_vars if not os.getenv(var)]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")

    def load_embeddings(self):
        """
        Load and return the embedding model.
        """
        print("Loading Embedding model")
        model_name=self.config["embedding_model"]["model_name"]
        return GoogleGenerativeAIEmbeddings(model=model_name)

    def load_llm(self):
        """
        Load and return the LLM model.
        """
        print("LLM loading...")
        model_name=self.config["llm"]["model_name"]
        gemini_model=ChatGoogleGenerativeAI(model=model_name)
        
        return gemini_model  # Placeholder for future LLM loading