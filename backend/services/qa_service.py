from database.models import Document
import os
import logging
from tenacity import retry, stop_after_attempt, wait_exponential
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    StorageContext,
    load_index_from_storage,
    set_global_service_context
)
from llama_index.llms import TogetherLLM
from llama_index.embeddings import HuggingFaceEmbedding
from llama_index.readers import PDFReader
from sqlalchemy.orm import Session
from typing import Optional
import warnings

os.environ["TOKENIZERS_PARALLELISM"] = "false"
warnings.filterwarnings("ignore", category=UserWarning)


class QAService:
    def __init__(self, api_key: str):
        self.logger = logging.getLogger(__name__)
        self._initialize_services(api_key)
        os.makedirs("storage", exist_ok=True)

    def _initialize_services(self, api_key: str):
        """Initialize all NLP services with optimized settings"""
        try:
            self.llm = TogetherLLM(
                api_key=api_key,
                model="meta-llama/Llama-3-70b-chat-hf",
                temperature=0.2,
                max_tokens=768,
                top_p=0.9,
                request_timeout=45
            )

            self.embed_model = HuggingFaceEmbedding(
                model_name="BAAI/bge-small-en-v1.5"
            )

            self.service_context = ServiceContext.from_defaults(
                llm=self.llm,
                embed_model=self.embed_model,
                chunk_size=512,
                chunk_overlap=128,
                num_output=1
            )

            set_global_service_context(self.service_context)

        except Exception as e:
            self.logger.error(f"Service initialization failed: {str(e)}")
            raise

    def _get_index(self, doc_path: str, doc_id: int) -> Optional[VectorStoreIndex]:
        """Get or create index with error handling"""
        storage_path = f"storage/doc_{doc_id}"

        try:
            # Try loading the existing index
            if os.path.exists(storage_path):
                self.logger.info(f"Loading existing index for doc {doc_id}")
                try:
                    return load_index_from_storage(
                        StorageContext.from_defaults(persist_dir=storage_path),
                        service_context=self.service_context
                    )
                except Exception as load_err:
                    self.logger.warning(f"Failed to load index from storage. Rebuilding index... Error: {str(load_err)}")

            # If not found or failed to load, create a new index
            self.logger.info(f"Creating new index from {doc_path}")
            documents = PDFReader().load_data(file=doc_path)

            if not documents:
                raise ValueError("Failed to parse the PDF. No content found.")

            index = VectorStoreIndex.from_documents(
                documents,
                service_context=self.service_context,
                show_progress=True
            )
            index.storage_context.persist(persist_dir=storage_path)
            return index

        except Exception as e:
            self.logger.error(f"Index operation failed: {str(e)}")
            return None

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        reraise=True
    )
    async def get_answer(self, doc_id: int, question: str, db: Session) -> str:
        """Get answer with retry logic and proper resource management"""
        try:
            # Validate document exists
            doc = db.query(Document).filter(Document.id == doc_id).first()
            if not doc or not os.path.exists(doc.path):
                raise ValueError(f"Document {doc_id} not found or path invalid: {doc.path}")

            # Ensure the global context is always current
            set_global_service_context(self.service_context)

            # Load or create the index
            index = self._get_index(doc.path, doc_id)
            if not index:
                raise ValueError("Failed to process document index")

            # Setup query engine
            query_engine = index.as_query_engine(
                similarity_top_k=2,
                response_mode="tree_summarize",
                streaming=False,
                verbose=True
            )

            # Perform the query
            response = query_engine.query(question)
            return str(response).strip()

        except Exception as e:
            self.logger.error(f"QA processing failed: {str(e)}")
            if "rate limit" in str(e).lower():
                raise ValueError("Server busy. Please wait and try again.")
            elif "timeout" in str(e).lower():
                raise ValueError("Processing took too long. Try a simpler question.")
            raise ValueError(f"Could not process your question: {str(e)}")
