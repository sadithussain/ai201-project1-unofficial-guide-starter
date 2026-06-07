import os
import chromadb
from chromadb.utils import embedding_functions
from ingest import clean_text, chunk_document

def build_vector_store():
    # 1. Initialize persistent ChromaDB storage path
    persist_dir = "data/vectorstore"
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    
    # 2. Define the exact local embedding model from your planning.md
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # 3. Create or fetch your RAG collection
    collection = chroma_client.get_or_create_collection(
        name="rit_professor_reviews",
        embedding_function=embedding_func
    )
    
    raw_dir = "data/raw"
    if not os.path.exists(raw_dir):
        print("Error: Raw files path doesn't exist.")
        return
        
    files = [f for f in os.listdir(raw_dir) if f.endswith(".txt")]
    
    documents = []
    metadatas = []
    ids = []
    global_id_counter = 0
    
    print("Extracting and chunking documents for vector indexing...")
    for file in files:
        with open(os.path.join(raw_dir, file), "r", encoding="utf-8") as f:
            content = f.read()
            
        cleaned = clean_text(content)
        chunks = chunk_document(cleaned, file)
        
        for chunk in chunks:
            documents.append(chunk["text"])
            metadatas.append(chunk["metadata"])
            ids.append(f"chunk_{global_id_counter}")
            global_id_counter += 1
            
    # 4. Upsert chunks into ChromaDB
    print(f"Embedding and uploading {len(documents)} vectors to ChromaDB...")
    collection.upsert(
        documents=documents,
        metadatas=metadatas,
        ids=ids
    )
    print(f"🎉 Success! Vector store initialized and saved locally at '{persist_dir}'.")

if __name__ == "__main__":
    build_vector_store()