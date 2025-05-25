
import os
import uuid
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from database.models import Document
import logging

class DocumentService:
    UPLOAD_DIR = "uploads"

    def __init__(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    async def save_document(self, file: UploadFile, db: Session) -> Document:
        try:
            if not file.filename.endswith(".pdf"):
                raise HTTPException(400, "Only PDF files allowed")

            content = await file.read()
            temp_path = os.path.join(self.UPLOAD_DIR, f"temp_{file.filename}")
            
            with open(temp_path, "wb") as f:
                f.write(content)

            document = Document(
                name=file.filename,
                path="",
                size=len(content)
            )
            db.add(document)
            db.commit()
            db.refresh(document)

            new_path = os.path.join(self.UPLOAD_DIR, f"{document.id}.pdf")
            os.rename(temp_path, new_path)
            document.path = new_path
            db.commit()
            db.refresh(document)

            return document

        except Exception as e:
            self.logger.error(f"Error saving document: {e}", exc_info=True)
            raise HTTPException(500, "Document save failed")