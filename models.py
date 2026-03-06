from sqlalchemy import Column, Integer, String, DateTime
from postgresql_db import Base
from datetime import datetime

class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String, primary_key=True, index=True)
    file_name = Column(String, nullable=False)
    file_size = Column(String)
    object_path = Column(String)
    upload_time = Column(DateTime, default=datetime.utcnow)