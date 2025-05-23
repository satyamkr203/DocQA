from sqlalchemy import Column, String, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)  
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)  
    size = Column(Integer)

def init_db(engine):
    """Creates the database tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
