import os
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from sqlalchemy.orm import Session
import logging

load_dotenv()

# Initialize components
from database.models import init_db
from database.session import engine, get_db
from services.document_service import DocumentService
from services.qa_service import QAService

init_db(engine)
app = FastAPI(title="PDF Q&A")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://doc-qa-azure.vercel.app",
        "http://localhost:5173",
    ], # frontend url and the localhost url 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=600,
)

document_service = DocumentService()
qa_service = QAService(api_key=os.getenv("TOGETHER_API_KEY"))

class QuestionRequest(BaseModel):
    document_id: int
    question: str
# check the routes connection 
@app.options("/api/upload")
async def upload_options():
    return {"message": "OK"}

@app.options("/api/question")
async def question_options():
    return {"message": "OK"}

@app.post("/api/upload")
async def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        doc = await document_service.save_document(file, db)
        return {
            "id": doc.id,
            "name": doc.name,
            "size": doc.size,
            "upload_date": doc.upload_date
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        logging.error(f"Upload failed: {str(e)}")
        raise HTTPException(500, "Upload failed")

@app.post("/api/question")
async def ask_question(request: QuestionRequest, db: Session = Depends(get_db)):
    try:
        answer = await qa_service.get_answer(request.document_id, request.question, db)
        return {"answer": answer}
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        logging.error(f"QA failed: {str(e)}")
        raise HTTPException(500, "Processing failed")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)