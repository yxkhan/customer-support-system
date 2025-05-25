import os
import pandas as pd
from dotenv import load_dotenv
from typing import List, Tuple
from langchain_core.documents import Document
from langchain_astradb import AstraDBVectorStore
from utils.model_loader import ModelLoader
from config.config_loader import load_config
import hashlib #for generating unique IDs for documents (to avoid duplicates)

class DataIngestion:
    """
    Class to handle data transformation and ingestion into AstraDB vector store.
    """

    def __init__(self):
        """
        Initialize environment variables, embedding model, and set CSV file path.
        """
        print("Initializing DataIngestion pipeline...")
        self.model_loader=ModelLoader()
        self._load_env_variables()
        """Calls the private method _load_env_variables() defined later in the class.
         Even though it appears "later" in the file, Python doesn't care — 
         it just needs to know the method exists in the class, and it will resolve it at runtime."""
        self.csv_path = self._get_csv_path()
        self.product_data = self._load_csv()
        self.config=load_config()

    def _load_env_variables(self):       #wherever you _ in the starting of the function it is a private function and we don't want to expose it to the outside world (encapsulation) in oops concept
        """
        Load and validate required environment variables. If any are missing, raise an error.
        """
        load_dotenv()
        
        required_vars = ["GOOGLE_API_KEY", "ASTRA_DB_API_ENDPOINT", "ASTRA_DB_APPLICATION_TOKEN", "ASTRA_DB_KEYSPACE"]
        
        missing_vars = [var for var in required_vars if os.getenv(var) is None]
        if missing_vars:
            raise EnvironmentError(f"Missing environment variables: {missing_vars}")
        
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.db_api_endpoint = os.getenv("ASTRA_DB_API_ENDPOINT")
        self.db_application_token = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
        self.db_keyspace = os.getenv("ASTRA_DB_KEYSPACE")

       

    def _get_csv_path(self):
        """
        Get path to the CSV file located inside 'data' folder.
        """
        current_dir = os.getcwd()   #get current working directory (It returns the absolute path of the directory where your Python script is currently running.)
        csv_path = os.path.join(current_dir, 'data', 'flipkart_product_review.csv')

        if not os.path.exists(csv_path):      #Return True/False if the path exists or not.
            raise FileNotFoundError(f"CSV file not found at: {csv_path}")

        return csv_path

    def _load_csv(self):
        """
        Load product data from CSV.
        """
        df = pd.read_csv(self.csv_path)
        expected_columns = {'product_title', 'rating', 'summary', 'review'}

        if not expected_columns.issubset(set(df.columns)):
            raise ValueError(f"CSV must contain columns: {expected_columns}")

        return df

    def transform_data(self):
        """
        Transform product data into list of LangChain Document objects.
        """
        product_list = []

        for _, row in self.product_data.iterrows():   #_ we are getting index, we don't need it
            product_entry = {
                "product_name": row['product_title'],
                "product_rating": row['rating'],
                "product_summary": row['summary'],
                "product_review": row['review']
            }
            product_list.append(product_entry)

        documents = []
        for entry in product_list:
            metadata = {
                "product_name": entry["product_name"],
                "product_rating": entry["product_rating"],
                "product_summary": entry["product_summary"]
            }
            doc_id = hashlib.md5(entry["product_review"].encode()).hexdigest() ## (To avoid duplicates)Generate a unique ID for the document using MD5 hash of the review text
            doc = Document(page_content=entry["product_review"], metadata=metadata,id=doc_id)  
            documents.append(doc)

        print(f"Transformed {len(documents)} documents.")
        return documents

    def store_in_vector_db(self, documents: List[Document]):
        """
        Store documents into AstraDB vector store. configurations
        """
        collection_name=self.config["astra_db"]["collection_name"]
        vstore = AstraDBVectorStore(
            embedding= self.model_loader.load_embeddings(),
            collection_name=collection_name,
            api_endpoint=self.db_api_endpoint,
            token=self.db_application_token,
            namespace=self.db_keyspace,
        )
        #vstore.delete_collection()   #clear everything in that collection — only use it for development/testing.

        inserted_ids = vstore.add_documents(documents)
        print(f"Successfully inserted {len(inserted_ids)} documents into AstraDB.")
        return vstore, inserted_ids

    def run_pipeline(self):
        """
        Run the full data ingestion pipeline: transform data and store into vector DB.
        """
        documents = self.transform_data()
        vstore, inserted_ids = self.store_in_vector_db(documents)

        # Optionally do a quick search
        query = "Can you tell me the low budget headphone?"
        results = vstore.similarity_search(query)

        print(f"\nSample search results for query: '{query}'")
        for res in results:
            print(f"Content: {res.page_content}\nMetadata: {res.metadata}\n")

# Run if this file is executed directly
#While running the script, it will execute the code inside this block.
if __name__ == "__main__":
    ingestion = DataIngestion()    #Loading this class
    ingestion.run_pipeline()     #running this method of this class


#We have run this code multiple times and hence the DB is updating with same data each time we run the code.
#Hence we are getting the duplicate data in the DB.

#We overcame the issue of duplicate data by using the unique ID for each document using MD5 hash of the review text.
#This way, even if the same review is added multiple times, it will be stored as a unique document in the database.