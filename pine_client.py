from dotenv import load_dotenv
import os
from pinecone import Pinecone as pine
import time

load_dotenv()

class PineConeDB:
    def __init__(self):
        # creating a client for pinecone
        self.pc = pine(api_key=os.getenv("PINECONE_API"))
        
        # name of the index will be the same
        self.index_name = "rag-pipeline"
        
        # create an index here if it doesn't exist
        if not self.pc.has_index(self.index_name):
            self.pc.create_index_for_model(
                name=self.index_name,
                
                cloud='aws',
                
                region='us-east-1',
                
                # embedded index keeping in mind text only data and to reduce complexity
                embed={
                    "model":"llama-text-embed-v2",
                    "field_map":{"text": "chunk_text"}
                }
            )

        self.index = self.pc.Index(self.index_name)
        self.namespace = "ns1"
        
    # inserting data -> upsert
    def upsert_data(self, records: list[dict]):        
        self.index.upsert_records(namespace=self.namespace, records=records)
        
        print("Uploading records......")
        time.sleep(15) # to allow upsert to take shape
        print("Uploaded")

    def search_index(self, query: str):
        results = self.index.search(
            namespace=self.namespace,
            query={
                "top_k": 5,
                "inputs": {
                    "text": query
                }
            }
        )
        
        return results
    
    def delete_index(self):
        self.pc.delete_index(self.index_name)