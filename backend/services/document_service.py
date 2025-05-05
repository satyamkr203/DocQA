import os
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from database.session import get_db
from database.models import Document
import logging

class DocumentService:
    UPLOAD_DIR = "uploads"

    def __init__(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    async def save_document(self, file: UploadFile) -> Document:
        try:
            # Validate file type (PDF)
            if not file.filename.endswith(".pdf"):
                raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

            # Generate unique ID for the document
            doc_id = str(uuid.uuid4())
            
            # Create file path
            file_path = os.path.join(self.UPLOAD_DIR, f"{doc_id}.pdf")
            
            # Save file to disk
            content = await file.read()
            with open(file_path, "wb") as f:
                f.write(content)

            # Save document metadata to database
            db = next(get_db())
            document = Document(
                id=doc_id,
                name=file.filename,
                path=file_path,
                size=len(content)
            )
            
            db.add(document)
            db.commit()
            db.refresh(document)

            self.logger.info(f"Document uploaded successfully with ID: {doc_id}")
            return document

        except Exception as e:
            self.logger.error(f"Error occurred while saving document: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="An error occurred while saving the document.")
