from langchain_text_splitters import RecursiveCharacterTextSplitter
from utils import *
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

class PDFIndexer():
    def __init__(self, persist_directory="./chroma_db", collection_name='rag-q_a'):
        self.db = Chroma(embedding_function=OpenAIEmbeddings(), persist_directory=persist_directory, collection_name=collection_name)
        print("ChromaDB initialized")
        
    def text_to_docs(self, text: str, chunk_size=500, chunk_overlap=50):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap
        )
        docs = splitter.create_documents([text])
        return docs

    def is_already_indexed(self, pdf_link):
        all_docs_meta = self.db.get()['metadatas']
        pdf_indexed = []
        for item in all_docs_meta:
            pdf_indexed.append(item['pdf_url'])
        if pdf_link in pdf_indexed:
            return True
        else:
            return False
        
    def index_to_db(self, text, pdf_link):
        if self.is_already_indexed(pdf_link):
            print("Already indexed")
            pass
        else:
            docs = self.text_to_docs(text)
            docs = add_meta(docs, {'pdf_url': pdf_link})
            self.db.add_documents(docs)
            print("Not present: Indexed")
        
    def get_retriever(self, pdf_link, top_k=10):
        return self.db.as_retriever(search_kwargs={'k': 10,'filter': {'pdf_url':pdf_link}})