import pandas as pd
from langchain_core.documents import Document    #To craete the document object

#We gonna use this class to convert the data into the required format for the langchain
# class and then we will use the langchain to convert the data into the required format for the langchain
class data_converter:
    def __init__(self):
        print("data converter class has initialized")
        self.product_data = pd.read_csv(r"C:\\Users\\Yaseen Khan\\Documents\\Data Sceince\\DL - GenAI Projects\\Customer_Support_System\\data\\flipkart_product_review.csv")
        # print(self.product_data.head())

    def data_transformation(self):
        required_columns=self.product_data.columns
        required_columns=list(required_columns[1:])
        print("Required columns are: ",required_columns)   #We are taking all the columns except 'product_id' column

        #lets iterate on the data and convert the data into the required format for the langchain
        product_list = []

        for index,row in self.product_data.iterrows():
            
            object={
                "product_name":row['product_title'],
                "product_rating":row['rating'],
                "product_summary":row["summary"],
                "product_review":row["review"]
                
            }

            product_list.append(object)  #We have to create a product_list and append the object to it
        # print("********below is my product list************")
        # print(product_list[0])
        #Now this data we are going to store in the vector database

        #We have to iterate on the product_list and create main_data and meta_data
        docs=[]
        for entry in product_list:
            #We are going to keep it as document object
            metadata={"product_name":entry["product_name"],"product_rating":entry["product_rating"],"product_summary":entry["product_summary"]} #These variables as meta_data
            doc=Document(page_content=entry["product_review"],metadata=metadata)  #product_review as page_content and metadata as meta_data
            docs.append(doc)
        #print(docs[0])   
        return docs
            

#To check the code is running or not, if it is running then we can use this class in other files as well.
if __name__ == "__main__":
    data_con=data_converter()  #to run this you have to write "python data_ingestion\data_ingest.py" in the cmd termianl
    data_con.data_transformation()  ##creating the object of the class 