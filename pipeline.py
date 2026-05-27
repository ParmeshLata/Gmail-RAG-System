from gmail.fetch_emails import fetch_all_emails
from rag.chunking import create_email_chunks
from rag.embeddings import making_embeddings
from credentials import save_credentials

def save_and_run(email, password):
    cred_result=save_credentials(email, password)
    run_pipeline()
    return f"{cred_result}"

def run_pipeline():

    print("=== Starting Gmail RAG Pipeline ===")

    print("\n[1/3] Fetching new emails...")
    new_emails = fetch_all_emails()

    if not new_emails:
        print("No new emails — skipping chunking and embedding.")
        print("=== Pipeline complete (nothing new) ===")
        return

    print("\n[2/3] Chunking new emails...")
    chunks = create_email_chunks(new_emails)
    print(f"Created {len(chunks)} chunks")

    print("\n[3/3] Creating embeddings...")
    making_embeddings(chunks)

    print("=== Pipeline complete ===")
    return f"Pipeline complete! Processed {len(chunks)} chunks."