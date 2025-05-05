# AskPdf

AskPdf is a full-stack application that enables users to upload PDFs and interact with their contents using AI-powered chat. It uses **FastAPI** for the backend, **PostgreSQL** for metadata storage, and **local storage** for file uploads. The frontend is built with **React**, and **LlamaIndex** and **LangChain** are used for AI-powered PDF Q\&A.

---

## 📁 Project Structure

```
AskPdf/
├── backend/
│   ├── database/
│   │   ├── models.py
│   │   └── session.py
│   ├── services/
│   │   ├── document_service.py
│   │   └── qa_service.py
│   ├── uploads/                # Locally stored PDFs
│   ├── main.py                 # FastAPI app
│   └── pdf_qa.db               # Local SQLite (if used during dev)
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

* **FastAPI** – for serving API endpoints
* **PostgreSQL** – used for storing metadata
* **Local file storage** – for PDF storage
* **LlamaIndex** – document indexing and query support
* **LangChain** – prompt engineering and LLM orchestration

### Frontend

* **React** – SPA for interacting with the backend
* **Vite** – fast dev build tool

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10+
* Node.js 18+
* PostgreSQL running locally or remotely

### 1. Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Set up environment variables (example)
export DATABASE_URL=postgresql://user:password@localhost:5432/askpdf
uvicorn main:app --reload
```

### 2. Frontend Setup

```bash
cd client
npm install
npm run dev
```

---

## 📦 Features

* Upload PDF files
* Chat with PDF contents using LLMs
* Vector store and context retrieval with LlamaIndex
* Persistent metadata with PostgreSQL
* Responsive UI using React

---

## 📄 License

This project is licensed under the MIT License.

---

## ✍️ Author

[Satyam Kumar](https://github.com/satyamkr203)
