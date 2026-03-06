# 🧠 Evidence Collection & Intelligence System

An **AI-powered Evidence Collection and Intelligence Platform** designed to store, analyze, and retrieve investigative evidence using **semantic search and Retrieval-Augmented Generation (RAG)**.

Traditional systems rely on keyword search, which often fails to capture the **true context of evidence documents**. This system uses **vector embeddings and LLM-based reasoning** to enable investigators to ask natural language questions and retrieve the most relevant evidence.

---

# 🚀 Key Features

🔍 **Semantic Evidence Search**
Search evidence using natural language queries instead of exact keywords.

🧠 **Retrieval-Augmented Generation (RAG)**
Combines document retrieval with a Large Language Model to generate contextual answers.

📂 **Secure Evidence Storage**
Evidence files are stored using **object storage architecture** ensuring scalability and durability.

📊 **Vector Embeddings**
Documents are transformed into high-dimensional embeddings for similarity search.

💬 **Investigator Chat Interface**
Investigators can interact with the system using conversational queries.

📁 **Multi-format Evidence Support**

* PDF documents
* Text files
* Images
* Video metadata

---

# 🏗 System Architecture

```
                   ┌─────────────────────────┐
                   │  Investigator Interface │
                   │  (Chat / Search UI)     │
                   └─────────────┬───────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │   FastAPI API   │
                        │  Backend Server │
                        └────────┬────────┘
                                 │
         ┌───────────────────────┼────────────────────────┐
         ▼                       ▼                        ▼
 ┌───────────────┐     ┌──────────────────┐      ┌─────────────────┐
 │ Object Storage│     │ Embedding Model  │      │ Vector Database │
 │ Evidence Files│     │ SentenceTransformer │   │ Semantic Search │
 └───────────────┘     └──────────────────┘      └─────────────────┘
                                 │
                                 ▼
                         ┌──────────────┐
                         │  LLM Engine  │
                         │  (RAG Model) │
                         └──────────────┘
                                 │
                                 ▼
                        AI Generated Insights
```

---

# 🧠 RAG Pipeline

The system follows a **Retrieval Augmented Generation workflow**:

### 1️⃣ Evidence Ingestion

Evidence files are uploaded and stored in **object storage**.

### 2️⃣ Text Extraction

Content is extracted from documents such as PDFs or text files.

### 3️⃣ Embedding Generation

The extracted text is converted into **vector embeddings** using transformer models.

### 4️⃣ Vector Storage

Embeddings are stored inside a **vector database** to enable similarity search.

### 5️⃣ Query Processing

When an investigator asks a question:

1. Query is converted into an embedding
2. Similar evidence documents are retrieved
3. Relevant context is sent to the LLM
4. LLM generates the final answer

---

# 🛠 Tech Stack

### Backend

* Python
* FastAPI

### AI / Machine Learning

* Sentence Transformers
* Retrieval-Augmented Generation (RAG)
* Cosine Similarity Search

### Storage

* Object Storage (Evidence files)
* Vector Database (Embeddings)

### Frontend

* HTML
* Bootstrap
* JavaScript

### DevOps

* Git & GitHub
* Docker (optional)
* Cloud deployment ready

---

# 📂 Project Structure

```
evidence-collection-system
│
├── main.py
├── embedding_pipeline.py
├── rag_engine.py
├── retrieval_system.py
│
├── static/
│   ├── index.html
│   ├── css
│   └── js
│
├── uploads/
├── chroma/
│
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation & Setup

### Clone Repository

```
git clone https://github.com/vivek07thate/evidence-collection-system.git
```

### Navigate to Project

```
cd evidence-collection-system
```

### Create Virtual Environment

```
python -m venv venv
```

### Activate Environment

Windows:

```
venv\Scripts\activate
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Run Application

```
uvicorn main:app --reload
```

Application will start at:

```
http://127.0.0.1:8000
```

---

# 💡 Example Query

Investigators can ask questions like:

```
"What evidence mentions financial fraud?"
"Show documents related to suspect X."
"Find reports connected to cybercrime activities."
```

The system retrieves the **most relevant evidence and generates contextual insights**.

---

# 🔒 Security Considerations

* Evidence stored in **secure object storage**
* Metadata managed separately
* Scalable distributed storage architecture
* Controlled investigator access

---

# 🎯 Use Cases

* Law enforcement investigations
* Digital forensic analysis
* Intelligence agencies
* Legal case evidence management
* Cybercrime investigation

---

# 📈 Future Enhancements

* Multi-modal embeddings (image + text + video)
* Real-time evidence indexing
* Advanced access control (RBAC)
* Automated case intelligence summaries

---

# 👨‍💻 Author

**Vivekanand Thate**

AI / Backend Developer
Specializing in **AI Systems, Semantic Search, and RAG Architectures**

GitHub
https://github.com/vivek07thate

---

⭐ If you found this project useful, consider starring the repository!
