# Gmail RAG System

Chat with your own inbox. This project fetches emails from Gmail, turns them into searchable vector embeddings, and lets you ask questions in plain English through a conversational interface. Answers are grounded in your actual emails using Retrieval-Augmented Generation (RAG).

> Example questions: "What did the recruiter say about the interview date?", "Summarize my emails from last week about the hackathon", "Find the invoice from my cloud provider."

---

## Features

- **Secure Gmail access** via OAuth 2.0 (no password sharing)
- **Incremental email fetching**, so only new emails are pulled on later runs
- **Chunking and embeddings** using Hugging Face SentenceTransformer models
- **Local vector storage** with ChromaDB for fast semantic search
- **LLM-powered answers** through a Gemini or OpenAI interface
- **Conversation memory**, so follow-up questions work naturally
- **Gradio web UI** for a simple chat experience

---

## How It Works

```
Gmail (OAuth 2.0)
      |
      v
Fetch emails (IMAP / Gmail API, incremental)
      |
      v
Clean + chunk email text
      |
      v
Embed chunks (SentenceTransformer, Hugging Face)
      |
      v
Store in ChromaDB (vector database)
      |
      v
User question --> retrieve top-k relevant chunks
      |
      v
LLM (Gemini / OpenAI) answers using retrieved context
      |
      v
Gradio chat interface
```

1. **Ingest:** Authenticate with Google and fetch emails.
2. **Index:** Split emails into chunks, embed them, and store them in ChromaDB.
3. **Retrieve:** For each question, find the most semantically similar chunks.
4. **Generate:** Pass the question, the retrieved context, and the conversation history to the LLM.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Auth | Gmail OAuth 2.0 |
| Embeddings | Hugging Face SentenceTransformers |
| Vector DB | ChromaDB |
| LLM | Gemini / OpenAI |
| UI | Gradio |
| Language | Python |

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://www.github.com/ParmeshLata/Gmail-RAG-System.git
cd Gmail-RAG-System
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Set up Gmail OAuth

1. Go to the [Google Cloud Console](https://console.cloud.google.com/) and create a project.
2. Enable the **Gmail API**.
3. Create **OAuth client credentials** (Desktop app) and download the JSON file.
4. Save it in the project folder as `credentials.json`.
5. On first run, a browser window opens so you can grant read-only access to your mailbox.

### 4. Configure API keys

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_key_here
# or
OPENAI_API_KEY=your_openai_key_here
```

### 5. Run the app

```bash
python app.py
```

Open the local URL that Gradio prints in the terminal (usually `http://127.0.0.1:7860`).

---

## Usage

1. Click to sync or index your emails (the first run may take a few minutes).
2. Ask a question in the chat box.
3. Ask follow-ups. The system remembers the conversation.

---

## Project Structure

```
Gmail-RAG-System/
|-- app.py                # Gradio UI entry point
|-- requirements.txt
|-- .env                  # API keys (never commit this)
|-- credentials.json      # Google OAuth client file (never commit this)
`-- ...                   # Fetching, chunking, embedding, and retrieval modules
```

---

## Privacy and Security

- Your emails are processed and stored **locally** in ChromaDB.
- Only the retrieved snippets relevant to your question are sent to the LLM provider.
- Use read-only Gmail scopes.
- Add `.env`, `credentials.json`, `token.json`, and the ChromaDB folder to `.gitignore`.

---

## Challenges Solved

- **Tool-call reliability:** Made LLM tool calling more dependable with Gemini.
- **Incremental sync:** Avoided re-fetching and re-embedding emails already indexed.
- **Conversation history:** Managed chat context so follow-up questions stay accurate.
- **Dependency conflicts:** Resolved environment and package version issues for a clean setup.

---

## Future Improvements

- Metadata filters (sender, date range, label)
- Attachment parsing (PDF, DOCX)
- Hybrid search (keyword + semantic)
- Evaluation of retrieval quality (hit rate, answer faithfulness)

---

## Author

**Parmesh Lata**
[LinkedIn](https://www.linkedin.com/in/parmesh-lata/) | [GitHub](https://www.github.com/ParmeshLata) | [Portfolio](https://www.huggingface.co/spaces/parmeshlata)

---

## License

Add your preferred license here (e.g., MIT).
