import chromadb
from sentence_transformers import SentenceTransformer

embd_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def retrieve_context(user_prompt):

    user_message_embedding = embd_model.encode(
        user_prompt
    ).tolist()

    client = chromadb.PersistentClient(
        path="./data/chroma_db"
    )

    collection = client.get_or_create_collection(
        name="gmail_rag"
    )

    if collection.count() == 0:
        return "No emails indexed yet."

    results = collection.query(
        query_embeddings=[user_message_embedding],
        n_results=5
    )

    return results