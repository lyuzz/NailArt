from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.types import JSON
from sqlalchemy.sql import func

from app.db.base import Base


class Asset(Base):
    __tablename__ = "assets"

    id = Column(String, primary_key=True, index=True)
    owner_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    type = Column(String, nullable=False)
    preview_url = Column(String, nullable=False)
    nails_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())


class Job(Base):
    __tablename__ = "jobs"

    id = Column(String, primary_key=True, index=True)
    kind = Column(String, nullable=False)
    status = Column(String, nullable=False)
    progress = Column(Integer, default=0)
    input_json = Column(JSON, nullable=False)
    output_json = Column(JSON, nullable=True)
    error_code = Column(String, nullable=True)
    error_message = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
