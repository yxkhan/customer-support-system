from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os
import pandas as pd
from data_ingestion.data_transform import data_converter  #We have created this class in data_transform.py file
from langchain_google_genai import GoogleGenerativeAIEmbeddings

#Setup the environment variables
load_dotenv()

#Reading the environment variable
GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT=os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE=os.getenv("ASTRA_DB_KEYSPACE")
#Setting the environment variable
os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY
os.environ["ASTRA_DB_API_ENDPOINT"]=ASTRA_DB_API_ENDPOINT
os.environ["ASTRA_DB_APPLICATION_TOKEN"]=ASTRA_DB_APPLICATION_TOKEN
os.environ["ASTRA_DB_KEYSPACE"]=ASTRA_DB_KEYSPACE

#We gonna ingest the data to VDB
class ingest_data:
    def __init__(self):
        print("data ingestion class has initialized")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        self.data_converter=data_converter()   #Calling the data_converter class to convert the data into the required format for the langchain

    def data_ingestion(self,status):     #Status is to check whether we have stored data or not
        vstore=AstraDBVectorStore(
            embedding=self.embeddings,
            collection_name="chatbotecomm",
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )
        storage=status  #This status is required when we run the code second time, the same data should not be stored again in the database
        
        if storage==None:
            #We have to convert the data into the required format for the langchain
            docs=self.data_converter.data_transformation()  #Calling the data_transformation method of data_converter class to convert the data into the required format for the langchain
            #Our docs we store the documents object of our data
            inserted_ids=vstore.add_documents(docs)  #This method is used to add the documents to the vector data
            print=(inserted_ids)

        else:
            return vstore      #simple return the vstore if the data is already stored in the database
        
        return vstore, inserted_ids  #(first time storing)return the vstore and inserted_ids if the data is not stored in the database


if __name__ == "__main__":      #To run this file as a standalone script we use this block
    data_ingest=ingest_data()  #create the object of the class
    vstore,inserted_ids=data_ingest.data_ingestion(None)  #call the data_ingestion method of the class to ingest the data into the vector database
    #We are passing None for to store the data for the first time
    # print(f"\nInserted {len(inserted_ids)} documents.")

    #Perform the similarity search
    results=vstore.similarity_search("can you tell me the low budget headphone")
    for res in results:
        print(f"{res.page_content} {res.metadata}")