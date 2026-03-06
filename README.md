# evidence-collection-system

An AI-powered evidence management platform that enables investigators to securely store, retrieve, and analyze digital evidence using semantic search and Retrieval-Augmented Generation (RAG).

Instead of relying on traditional keyword search, the system understands the contextual meaning of documents using embeddings and large language models.

🚀 Features

🔎 Semantic Evidence Search
Search evidence using natural language queries instead of exact keywords.

🧠 RAG-Based Intelligence System
Combines document retrieval with an LLM to generate contextual answers.

📂 Secure Evidence Storage
Files are stored in object storage with metadata management.

📊 Vector Embeddings
Documents are converted into embeddings to enable semantic similarity search.

💬 Investigator Chat Interface
Users can ask questions like:

"What evidence mentions financial fraud?"
"Show documents related to suspect X."

📁 Multi-format Evidence Support

PDF

Images

Text documents

Video metadata

🏗 System Architecture
                ┌──────────────────────┐
                │   Investigator UI    │
                │  (Chat Interface)    │
                └──────────┬───────────┘
                           │
                           ▼
                 ┌──────────────────┐
                 │   FastAPI API    │
                 │ Backend Service  │
                 └──────────┬───────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
 ┌─────────────┐   ┌────────────────┐   ┌────────────────┐
 │ Object      │   │ Embedding      │   │ Vector Search  │
 │ Storage     │   │ Model          │   │ Engine         │
 │ (Evidence)  │   │ (Transformers) │   │ (Chroma / etc) │
 └─────────────┘   └────────────────┘   └────────────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │ Large Language  │
                   │ Model (LLM)     │
                   └─────────────────┘
                            │
                            ▼
                    Generated Intelligence
🧠 RAG Pipeline

The system uses Retrieval Augmented Generation (RAG) to answer user queries.

Step 1 — Evidence Upload

Evidence documents are uploaded and stored in object storage.

Step 2 — Text Extraction

Text is extracted from files such as PDFs or images.

Step 3 — Embedding Generation

The text is converted into vector embeddings using a transformer model.

Step 4 — Vector Storage

Embeddings are stored in a vector database.

Step 5 — Query Processing

When the investigator asks a question:

1️⃣ Query is converted into embedding
2️⃣ Similar documents are retrieved
3️⃣ Relevant context is sent to the LLM
4️⃣ LLM generates the final answer

🛠 Tech Stack
Backend

Python

FastAPI

AI / ML

Sentence Transformers

RAG Architecture

Cosine Similarity

Data Storage

Object Storage (Evidence files)

Vector Database (Embeddings)

Frontend

HTML

Bootstrap

JavaScript

Deployment

Docker / Cloud Platform

GitHub

📂 Project Structure
evidence-collection-system
│
├── app/
│   ├── main.py
│   ├── embedding.py
│   ├── retrieval.py
│   └── rag_pipeline.py
│
├── static/
│   ├── index.html
│   └── styles.css
│
├── uploads/
├── chroma/
├── requirements.txt
└── README.md
⚙️ Installation

Clone the repository:

git clone https://github.com/vivek07thate/evidence-collection-system.git

Navigate to the project:

cd evidence-collection-system

Create virtual environment:

python -m venv venv

Activate environment:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the server:

uvicorn main:app --reload
🌐 API Example

Example query request:

POST /query

Request body:

{
 "question": "What evidence mentions cyber fraud?"
}

Response:

{
 "answer": "The uploaded evidence indicates financial fraud activity in document X."
}
🔒 Security Considerations

Evidence stored in secure object storage

Metadata separated from files

Access control for investigators

No direct access to raw storage

🎯 Use Cases

Law enforcement investigations

Digital forensics analysis

Intelligence agencies

Legal evidence management

📌 Future Improvements

Multi-modal embeddings (image + text)

Video evidence analysis

Real-time evidence monitoring

Role-based access control

👨‍💻 Author

Vivekanand Thate

AI / Backend Developer
Interested in AI systems, RAG architectures, and intelligent search systems

GitHub
https://github.com/vivek07thate

⭐ If you found this project useful, consider giving it a star!
