import os
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ظبطنا المسارات عشان تشتغل Local جوه فولدر data
docs_folder = "data/real_docs"
output_dir = "data/faiss_index_real"

if not os.path.exists(docs_folder):
    os.makedirs(docs_folder)
    print(f"NOTICE: Created '{docs_folder}'. Please put the PDF inside and run again.")
else:
    print(f"Loading PDFs from '{docs_folder}'...")
    loader = PyPDFDirectoryLoader(docs_folder)
    docs = loader.load()

    if docs:
        print("Splitting into chunks...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = text_splitter.split_documents(docs)
        
        print("Generating embeddings...")
        embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
        
        print("Building FAISS index...")
        vector_store = FAISS.from_documents(chunks, embeddings)
        
        vector_store.save_local(output_dir)
        print(f"SUCCESS: FAISS index saved to '{output_dir}'.")
    else:
        print("No PDFs found in the folder.")