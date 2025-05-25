# AskPdf

AskPdf is a full-stack application that enables users to upload PDFs and interact with their contents using AI-powered chat. The backend is built with **FastAPI**, uses **PostgreSQL** for metadata, and stores uploaded files locally. The frontend is a **React** SPA. **LlamaIndex** and **LangChain** power the PDF Q&A features.

---

## 📁 Project Structure

```
AskPdf/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/
│   │   │   │   ├── upload.py
│   │   │   │   └── query.py
│   │   │   └── __init__.py
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   └── vector.py
│   │   ├── db/
│   │   │   ├── database.py
│   │   │   ├── models.py
│   │   │   └── crud.py
│   │   ├── services/
│   │   │   └── document_processor.py
│   │   ├── main.py
│   │   └── schemas.py
│   ├── uploaded_documents/      # Locally stored PDFs
│   ├── faiss_vector_store/      # Vector store for embeddings
│   ├── .env
│   ├── requirements.txt
│   └── README.md
├── client/
│   ├── public/
│   ├── src/
│   │   ├── component/
│   │   │   ├── ChatInterface.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   └── Navbar.jsx
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
├── .gitignore
└── README.md
```

---

## ⚙️ Tech Stack

### Backend

- **FastAPI** – API framework
- **PostgreSQL** – Metadata storage
- **Local file storage** – PDF storage
- **FAISS** – Vector store for embeddings
- **LlamaIndex** – Document indexing and query support
- **LangChain** – LLM orchestration

### Frontend

- **React** – SPA for user interaction
- **Vite** – Fast dev/build tool

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- PostgreSQL (local or remote)

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Set up environment variables (example)
export DATABASE_URL=postgresql://user:password@localhost:5432/askpdf
uvicorn app.main:app --reload
```

### 2. Frontend Setup

```bash
cd client
npm install
npm run dev
```

---

## 📦 Features

- Upload PDF files
- Chat with PDF contents using LLMs
- Vector store and context retrieval with LlamaIndex & FAISS
- Persistent metadata with PostgreSQL
- Responsive UI using React

---

## 📄 License

This project is licensed under the MIT License.

---

## ✍️ Author

[Satyam Kumar](https://github.com/satyamkr203)

