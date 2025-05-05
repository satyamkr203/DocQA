import logging
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from services.document_service import DocumentService
from services.qa_service import QAService
from database.models import init_db
from database.session import engine

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

app = FastAPI(title="PDF Q&A Backend")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
document_service = DocumentService()
qa_service = QAService()

# Initialize database
init_db(engine)

class QuestionRequest(BaseModel):
    document_id: str
    question: str

class Answer(BaseModel):
    content: str
    document_id: str
    timestamp: datetime

@app.post("/api/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename.endswith('.pdf'):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    try:
        logger.info(f"Uploading file: {file.filename}")
        document = await document_service.save_document(file)
        logger.info(f"Document uploaded successfully: {document.id}")
        return document
    except Exception as e:
        logger.error(f"Error occurred during file upload: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

@app.post("/api/question", response_model=Answer)
async def ask_question(request: QuestionRequest):
    try:
        logger.info(f"Received question for document {request.document_id}: {request.question}")
        answer = await qa_service.get_answer(request.document_id, request.question)
        logger.info(f"Answer found for document {request.document_id}")
        return Answer(
            content=answer,
            document_id=request.document_id,
            timestamp=datetime.now()
        )
    except Exception as e:
        logger.error(f"Error occurred while processing question for document {request.document_id}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting the FastAPI server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)
