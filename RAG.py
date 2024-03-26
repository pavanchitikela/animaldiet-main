
import os
from llama_index.llms.openai.base import OpenAI
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import ServiceContext
import os, streamlit as st




#Class RAG take query and return response
class RAG:
    def __init__(self):
        os.environ['OPENAI_API_KEY']=""
        self.api_key=os.environ['OPENAI_API_KEY']
        self.documents = SimpleDirectoryReader("petData").load_data()
        self.llm = OpenAI(openai_api_key=self.api_key,model="gpt-3.5-turbo", temperature=0, max_tokens=256)
        self.service_context = ServiceContext.from_defaults(llm=self.llm, chunk_size=800, chunk_overlap=20)
        self.index = VectorStoreIndex.from_documents(self.documents, service_context=self.service_context)
        self.query_engine = self.index.as_query_engine(streaming=True)
        self.response = None

    def query(self, query):
        try:
            self.response = self.query_engine.query(query)
            return self.response
        except Exception as e:
            return f"An error occurred: {e}"
        
