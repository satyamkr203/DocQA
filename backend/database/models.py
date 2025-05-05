from sqlalchemy import Column, String, DateTime, Integer, create_engine
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Auto-incrementing Integer ID
    name = Column(String, nullable=False)
    path = Column(String, nullable=False)
    upload_date = Column(DateTime, default=datetime.utcnow)  # Automatically sets current time if no value is provided
    size = Column(Integer)

def init_db(engine):
    """Creates the database tables if they don't exist."""
    Base.metadata.create_all(bind=engine)

# Example usage:
# engine = create_engine('postgresql://postgres:password@localhost:5432/yourdb')
# init_db(engine)
