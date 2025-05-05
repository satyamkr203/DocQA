import os
import logging
from typing import Optional
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from transformers import pipeline
from database.session import get_db
from database.models import Document
from functools import lru_cache

class QAService:
    def __init__(self):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
            add_start_index=True
        )

        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-mpnet-base-v2"
        )

        self.qa_model = pipeline(
            "question-answering",
            model="deepset/roberta-base-squad2",
            device=-1  # Use 0 for CUDA, "mps" for Apple Silicon, -1 for CPU
        )

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # In-memory cache for vector store to avoid repeated computation
        self.vectorstore_cache = {}

    async def get_answer(self, document_id: str, question: str) -> str:
        try:
            db = next(get_db())
            document: Optional[Document] = db.query(Document).filter(Document.id == document_id).first()

            if not document:
                self.logger.warning(f"Document with ID '{document_id}' not found.")
                raise ValueError("Invalid document ID.")

            if not os.path.exists(document.path):
                self.logger.error(f"File not found at path: {document.path}")
                raise FileNotFoundError("Document file not found on server.")

            loader = PyMuPDFLoader(document.path)
            pages = loader.load()
            texts = self.text_splitter.split_documents(pages)

            if not texts:
                self.logger.warning("Document was loaded but contained no readable text.")
                raise ValueError("Document contains no readable text.")

            # Check if vectorstore is already cached for this document
            if document_id in self.vectorstore_cache:
                vectorstore = self.vectorstore_cache[document_id]
            else:
                vectorstore = FAISS.from_documents(texts, self.embeddings)
                self.vectorstore_cache[document_id] = vectorstore  # Cache the vector store

            similar_docs = vectorstore.similarity_search(question, k=3)
            context = " ".join([doc.page_content for doc in similar_docs])

            if not context.strip():
                self.logger.info("Similarity search found no relevant content.")
                raise ValueError("No relevant content found to answer the question.")

            result = self.qa_model({
                "context": context,
                "question": question
            })

            raw_answer = result.get('answer', '').strip()
            if not raw_answer:
                self.logger.info("QA model returned an empty answer.")
                raise ValueError("The model could not extract an answer.")

            return self._polish_answer(raw_answer, question)

        except ValueError as ve:
            self.logger.warning(f"[QAService] {ve}")
            raise ve

        except FileNotFoundError as fe:
            self.logger.error(f"[QAService] {fe}")
            raise fe

        except Exception as e:
            self.logger.exception(f"[QAService Unexpected Error] {e}")
            raise RuntimeError("Internal error occurred while processing the question.")

    def _polish_answer(self, answer: str, question: str) -> str:
        answer = ' '.join(answer.split())  # Clean extra whitespace
        question_lower = question.lower()

        if "what kind of document" in question_lower:
            if not answer.endswith('.'):
                answer += '.'
            parts = [s.strip() for s in answer.split('.') if s.strip()]
            if len(parts) >= 2:
                return f"{parts[0]}. {parts[1]}."
            elif len(parts) == 1:
                return f"This appears to be {parts[0]}."
            return answer

        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        if len(sentences) > 1:
            return '. '.join(sentences[:2]) + '.'
        return answer
