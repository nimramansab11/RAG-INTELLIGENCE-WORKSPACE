# Groq + ChromaDB RAG

This is the corrected version using **Groq**, not xAI Grok.

## Components

```text
Embeddings -> SentenceTransformers (local/free)
Vector DB  -> ChromaDB (local/free)
LLM        -> Groq API (Free tier available, rate limited)
```

## Architecture

```text
Documents
   |
   v
Extract text
   |
   v
Chunk text
   |
   v
SentenceTransformers
(local embeddings)
   |
   v
ChromaDB


Question
   |
   v
SentenceTransformers
(local query embedding)
   |
   v
ChromaDB similarity search
   |
   v
Top-K relevant chunks
   |
   v
Groq API
   |
   v
LLM answer
```

## 1. Get a Groq API key

Create/login to your GroqCloud account:

https://console.groq.com

Create an API key from the API Keys section.

The Groq Free tier can be used without upgrading to Developer tier, but
it has model-specific rate limits.

## 2. Create `.env`

Copy:

```text
.env.example
```

to:

```text
.env
```

Then:

```env
GROQ_API_KEY=gsk_your_real_key
GROQ_MODEL=llama-3.3-70b-versatile

EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

There is no xAI key and no embedding API key.

## 3. Install

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 4. Add documents

Put PDF, TXT, or Markdown files into:

```text
data/
```

## 5. Build ChromaDB

```bash
python ingest.py --reset
```

This step does NOT call Groq.

It runs:

```text
documents
   ->
local SentenceTransformer
   ->
vectors
   ->
ChromaDB
```

## 6. Ask questions

```bash
python cli.py
```

Question processing:

```text
question
   ->
local embedding
   ->
ChromaDB search
   ->
top document chunks
   ->
Groq
   ->
answer
```

## 7. FastAPI

Start:

```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
```

Query:

```text
POST http://localhost:8000/rag/query
```

JSON:

```json
{
  "question": "What is an embedding?",
  "top_k": 5
}
```

You can restrict retrieval to one exact filename:

```json
{
  "question": "What is the refund policy?",
  "top_k": 5,
  "source": "policy.pdf"
}
```

## Environment variables

```env
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHROMA_PATH=./chroma_db
CHROMA_COLLECTION=knowledge_base
TOP_K=5
CHUNK_SIZE=1200
CHUNK_OVERLAP=200
EMBEDDING_BATCH_SIZE=64
```

## Cost behavior

```text
Document embedding:     local/free
Query embedding:        local/free
ChromaDB:               local/free
Groq LLM:               Free tier subject to rate limits
```

## Important embedding rule

Always use the same embedding model for document ingestion and query
embedding.

If you change:

```env
EMBEDDING_MODEL=...
```

rebuild the database:

```bash
python ingest.py --reset
```

## Default Groq model

The example defaults to:

```text
llama-3.3-70b-versatile
```

This is the model used in Groq's current Python quickstart at the time
this project was created. Model availability and Free-tier limits can
change, so you can replace `GROQ_MODEL` with another model available in
your Groq Console.