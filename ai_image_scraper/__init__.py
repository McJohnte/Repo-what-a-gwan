"""ai_image_scraper — an end-to-end scraper for AI-generated images.

The package exposes a small, source-pluggable pipeline:

    search a source  ->  download images  ->  persist images + metadata

See ``ai_image_scraper.cli`` for the command-line entry point and
``ai_image_scraper.sources`` for the available image sources.
"""

from ai_image_scraper.models import ImageRecord
from ai_image_scraper.config import ScraperConfig
from ai_image_scraper.pipeline import ScrapePipeline

__all__ = ["ImageRecord", "ScraperConfig", "ScrapePipeline"]
__version__ = "1.0.0"
