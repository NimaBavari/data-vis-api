import uuid

from sqlalchemy import Column, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AssessmentBatch(Base):
    __tablename__ = "assessment_batches"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    contents = Column(JSONB)


class Stat(Base):
    """Basis for creating, saving, and sharing visualizations."""

    __tablename__ = "stats"

    ID = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    dataview = Column(JSONB)
    batch_id = Column(UUID(as_uuid=True), ForeignKey("assessment_batches.id"))
