"""
The Factory Blueprints (Core Data Models)
These models define the exact structure of all data flowing through our factory.
"""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


# --- The Categories: Enums (The Sorting System) ---
class DocumentType(str, Enum):
    """What Kind of Files Can We Handle?"""

    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MD = "md"
    HTML = "html"
    JSON = "json"
    CSV = "csv"
    URL = "url"


class TaskType(str, Enum):
    """What Jobs Can Our Robots Do?"""

    QA_GENERATION = "qa_generation"
    CLASSIFICATION = "classification"
    SUMMARIZATION = "summarization"
    NER = "named_entity_recognition"
    RED_TEAMING = "red_teaming"
    INSTRUCTION_RESPONSE = "instruction_response"


# --- The Foundation: BaseEntity (The Master Template) ---
class BaseEntity(BaseModel):
    """The master blueprint that gives every item a tracking ID and timestamp."""

    id: UUID = Field(default_factory=uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


# --- The Document Family (Our Input Data) ---
class Document(BaseEntity):
    """The Original Source (e.g., A textbook)."""

    title: str
    content: str
    source: str
    doc_type: DocumentType
    word_count: int
    char_count: Optional[int] = None


class TextChunk(BaseEntity):
    """The Bite-Sized Pieces cut up for the AI to read."""

    document_id: UUID
    content: str
    start_index: int
    end_index: int
    chunk_index: int
    token_count: int


# --- The Task Family (Our Work Instructions) ---
class TaskTemplate(BaseEntity):
    """The Recipe Card for the AI."""

    name: str
    task_type: TaskType
    description: str
    prompt_template: str
    parameters: dict


class TaskResult(BaseEntity):
    """The Finished Product from the AI."""

    task_id: UUID
    input_chunk_id: UUID
    output: str
    confidence: float
    quality_scores: dict
    processing_time: float


# --- The Training Family (Our Final Products) ---
class TrainingExample(BaseEntity):
    """One Perfect Learning Item."""

    input_text: str
    output_text: str
    task_type: TaskType
    source_document_id: UUID
    quality_scores: dict


class Dataset(BaseEntity):
    """A Complete Collection of Training Examples."""

    name: str
    description: str
    examples: List[TrainingExample]
    total_examples: int
    train_split: float = 0.8
    validation_split: float = 0.1
    test_split: float = 0.1


# --- The Quality Family (Our Inspectors) ---
class QualityReport(BaseEntity):
    """The Report Card."""

    target_id: UUID
    overall_score: float
    passed: bool
    metric_scores: dict
    issues: List[str]
    warnings: List[str]
