# Importing necessary libraries and modules
import os
from langchain_astradb import AstraDBVectorStore  # Importing the AstraDB vector store class
from typing import List  # For typing hinting the return type of functions
from langchain_core.documents import Document  # Importing the Document class for LangChain
from config.config_loader import load_config  # Custom config loader to load configurations
from utils.model_loader import ModelLoader  # Custom model loader to load embeddings or other models
from dotenv import load_dotenv  # To load environment variables from a .env file

class Retriever:
    """
    This class handles the initialization of the AstraDB vector store and retrieval of relevant documents 
    from it based on a user query.
    """
    
    def __init__(self):
        # Initialize the model loader, load configurations, and environment variables
        self.model_loader = ModelLoader()  # Load the model loader object
        self.config = load_config()  # Load configuration from the config_loader
        self._load_env_variables()  # Call the function to load environment variables
        self.vstore = None  # Placeholder for AstraDB vector store (will be initialized later)
        self.retriever = None  # Placeholder for the retriever object
        """Initializing the instance variables to None. This is called as placeholder variables.
        These variables are initialized with None value, but their actual values will be set later in the code."""
    
    def _load_env_variables(self):
        """
        Load and validate environment variables.
        The required variables should be in the .env file for proper functioning.
        """
        load_dotenv()  # Load environment variables from the .env file
        
        required_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]
        # List of environment variables that are required for the pipeline
        
        # Check if any required environment variables are missing
        missing_vars = [var for var in required_vars if os.getenv(var) is None]
        
        if missing_vars:  # If any required variables are missing
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        # Raise an error if any of the required variables are missing
        
        # Assign values from environment variables to the class attributes
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")
    
    def load_retriever(self):
        """
        This method initializes the vector store and the retriever.
        - The vector store (vstore) is responsible for storing the embeddings of the documents.
        - The retriever will use the vector store to fetch relevant documents based on a query.
        """
        if not self.vstore:  # If the vector store is not already initialized
            collection_name = self.config["astra_db"]["collection_name"]  # Load the collection name from the config
            
            # Initialize the AstraDB vector store with necessary parameters (embedding model, collection name, etc.)
            self.vstore = AstraDBVectorStore(
                embedding=self.model_loader.load_embeddings(),  # Load the embeddings from the ModelLoader
                collection_name=collection_name,  # Set the collection name
                api_endpoint=self.db_api_endpoint,  # AstraDB API endpoint from the environment variables
                token=self.db_application_token,  # Authentication token for AstraDB
                namespace=self.db_keyspace,  # Keyspace from environment variables
            )
        
        if not self.retriever:  # If the retriever is not already initialized
            # Get the value of 'top_k' from the config to define how many documents to return in search results (default is 3)
            top_k = self.config["retriever"]["top_k"] if "retriever" in self.config else 3
            
            # Create the retriever from the vector store, specifying the number of documents to retrieve
            retriever = self.vstore.as_retriever(search_kwargs={"k": top_k})
            print("Retriever loaded successfully.")  # Print a confirmation message
            
            return retriever  # Return the retriever object
    
    def call_retriever(self, query: str) -> List[Document]:
        """
        This method uses the retriever to fetch documents that are relevant to the user query.
        It invokes the retriever and returns the results.
        """
        retriever = self.load_retriever()  # Load the retriever (will initialize the vector store if needed)
        
        # Use the retriever to invoke a search with the user query
        output = retriever.invoke(query)
        
        return output  # Return the list of retrieved documents as output
    
if __name__ == '__main__':
    # This block of code is executed if the script is run directly (not imported as a module)
    retriever_obj = Retriever()  # Create an instance of the Retriever class
    user_query = "Can you suggest good budget laptops?"  # Sample query from the user
    
    # Call the retriever with the user's query and get the results
    results = retriever_obj.call_retriever(user_query)
    
    # Print the results (i.e., relevant documents) along with their metadata
    for idx, doc in enumerate(results, 1):  # Enumerate over the results and print them
        print(f"Result {idx}: {doc.page_content}\nMetadata: {doc.metadata}\n")
