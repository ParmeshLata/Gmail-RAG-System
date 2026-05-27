from sentence_transformers import SentenceTransformer
import chromadb

model=SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def making_embeddings(chunks):
    if not chunks:
        print("No chinks to embed")
        return
    
    client=chromadb.PersistentClient(path="./data/chroma_db")

    collection=client.get_or_create_collection(name="gmail_rag")

    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]
    ids = [c["chunk_id"] for c in chunks]
    print(f"Embedding {len(chunks)} chunks.")

    embeddings=model.encode(texts).tolist()

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=metadatas
    )

    print("Embeddings stored successfully in chromaDB!")