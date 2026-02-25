"""
Training Data Curation Bot
Enterprise-grade training data curation bot for LLM fine-tuning using Decodo + Python automation.
"""

__version__ = "0.1.0"
__author__ = "Training Data Bot Team"
__email__ = "team@company.com"
__description__ = "Enterprise-grade training data curation bot for LLM fine-tuning"


# Core imports for easy access
# Main bot class
from .bot import TrainingDataBot
from .core.config import settings
from .core.exceptions import TrainingDataBotError
from .core.logging import get_logger
from .decodo import DecodoClient  # The internet scraper
from .evaluation import QualityEvaluator  # The quality checker
from .preprocessing import TextPreprocessor  # The text cleaner
from .sources import (
    DocumentLoader,  # Worker who reads text files
    PDFLoader,  # Worker who reads PDF files WebLoader , # Worker who reads websites
    UnifiedLoader,  # Boss who decides which worker to use
)
from .storage import DatasetExporter  # The packager
from .tasks import (
    ClassificationGenerator,  # Worker who sorts things into categories
    QAGenerator,  # Worker who makes questions and answers
    SummarizationGenerator,  # Worker who makes short summaries
    TaskTemplate,  # The instruction sheets for workers
)

__all__ = [
    # Core
    "TrainingDataBot",
    "settings",
    "get_logger",
    "TrainingDataBotError",
    # Sources
    "PDFLoader",
    "WebLoader",
    "DocumentLoader",
    "UnifiedLoader",
    # Tasks
    "QAGenerator",
    "ClassificationGenerator",
    "SummarizationGenerator",
    "TaskTemplate",
    # Services
    "DecodoClient",
    "TextPreprocessor",
    "QualityEvaluator",
    "DatasetExporter",
]
