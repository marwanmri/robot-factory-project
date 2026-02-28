"""
Step 4: The Document Highway System
This module contains the UnifiedLoader, our traffic controller.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, List, Optional, Union

from ..core.exceptions import TrainingDataBotError
from ..models import Document, DocumentType

# We try to import our specialist trucks (Step 5!)
try:
    from .base_loader import BaseLoader
    from .document_loader import DocumentLoader
    from .pdf_loader import PDFLoader
    from .web_loader import WebLoader
except ImportError:
    BaseLoader = object
    PDFLoader = Any
    WebLoader = Any
    DocumentLoader = Any


class DocumentLoadError(TrainingDataBotError):
    """Raised when a document fails to load."""

    pass


class UnifiedLoader(BaseLoader):
    """
    The Smart Traffic Controller.
    Automatically routes documents to the correct specialist.
    """

    def __init__(self) -> None:
        self.logger = logging.getLogger("training_data_bot")

        # Initialize all our specialized vehicles
        try:
            self.document_loader = DocumentLoader()  # Text
            self.pdf_loader = PDFLoader()  # PDF
            self.web_loader = WebLoader()  # Internet
        except TypeError:
            self.logger.warning("Specialists not yet built!")
            self.document_loader = None
            self.pdf_loader = None
            self.web_loader = None

        # List of all formats we can handle
        self.supported_formats: List[DocumentType] = list(DocumentType)

    def _get_document_type(self, source: Union[str, Path]) -> Optional[DocumentType]:
        """The Detective Work: Figures out the file type."""
        source_str = str(source)
        if source_str.startswith(("http://", "https://")):
            return DocumentType.URL

        source_path = Path(source)
        if not source_path.exists():
            self.logger.error(f"File not found: {source_path}")
            return None

        suffix = source_path.suffix.lower().strip(".")
        try:
            return DocumentType(suffix)
        except ValueError:
            self.logger.warning(f"Unsupported format: {suffix}")
            return None

    async def load_single(self, source: Union[str, Path], **kwargs: Any) -> Document:
        """Routes a single document to the right specialist."""
        doc_type = self._get_document_type(source)

        if not doc_type:
            raise DocumentLoadError(f"Invalid type: {source}")

        # Choose the right loader
        loader = None
        if doc_type == DocumentType.PDF:
            loader = self.pdf_loader
        elif doc_type == DocumentType.URL:
            loader = self.web_loader
        elif doc_type in [
            DocumentType.TXT,
            DocumentType.MD,
            DocumentType.HTML,
            DocumentType.CSV,
            DocumentType.DOCX,
        ]:
            loader = self.document_loader

        if not loader:
            raise DocumentLoadError(f"Specialist for {doc_type} is missing.")

        try:
            return await loader.load_single(source, **kwargs)
        except Exception as e:
            self.logger.error(f"Failed to load {source}: {e}")
            raise DocumentLoadError(f"Failed to load: {source}") from e

    async def load_directory(
        self, directory: Union[str, Path], recursive: bool = True, max_workers: int = 4
    ) -> List[Document]:
        """Multi-Document Loading: The Convoy System."""
        dir_path = Path(directory)

        # Step 1: Scout the Territory
        sources = []
        patterns = ["*.pdf", "*.txt", "*.md", "*.html", "*.docx", "*.json", "*.csv"]
        for pattern in patterns:
            if recursive:
                sources.extend(dir_path.rglob(pattern))
            else:
                sources.extend(dir_path.glob(pattern))

        # Step 2: Deploy Multiple Trucks (Parallel Loading)
        semaphore = asyncio.Semaphore(max_workers)

        async def load_with_semaphore(src: Path) -> Optional[Document]:
            async with semaphore:
                try:
                    return await self.load_single(src)
                except Exception as e:
                    self.logger.error(f"Skipping {src}: {e}")
                    return None

        tasks = [load_with_semaphore(src) for src in sources]
        results = await asyncio.gather(*tasks)

        # Step 3: Quality Control
        documents = [res for res in results if res is not None]
        return documents
