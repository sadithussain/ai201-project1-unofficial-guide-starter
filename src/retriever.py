import os
import chromadb
from chromadb.utils import embedding_functions

def get_vector_collection():
    """Connects to the local persistent ChromaDB vector store."""
    persist_dir = "data/vectorstore"
    
    if not os.path.exists(persist_dir):
        raise FileNotFoundError(
            f"Vector store not found at '{persist_dir}'. Please run store.py first."
        )
        
    chroma_client = chromadb.PersistentClient(path=persist_dir)
    embedding_func = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    return chroma_client.get_collection(
        name="rit_professor_reviews",
        embedding_function=embedding_func
    )

def retrieve_context(query_text: str, n_results: int = 4) -> list:
    """Queries the vector database and returns a list of matching text chunks."""
    collection = get_vector_collection()
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    # Flatten out the list of documents returned by ChromaDB
    return results['documents'][0] if results['documents'] else []

if __name__ == "__main__":
    # Milestone 4 Verification Test Loop
    test_queries = [
        "How strict are Maria Cepeda's deadline policies?",
        "What does Jansen Orfan do for students who are struggling in his class?",
        "What are some complaints and praises of Thomas Borelli's teaching style?",
    ]
    
    print("🚀 Initializing Milestone 4 Retrieval Test...")
    
    for q in test_queries:
        print(f"\n{'='*60}\n🔍 QUERY: '{q}'\n{'='*60}")
        try:
            matched_chunks = retrieve_context(q, n_results=4)
            for idx, chunk in enumerate(matched_chunks):
                print(f"\n[Matched Chunk {idx + 1}]")
                print(chunk)
                print("-" * 40)
        except Exception as e:
            print(f"Extraction failed: {e}")