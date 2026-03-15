"""
Script to ingest properties data into Qdrant Cloud using PropertySearchService.
"""

import sys
from pathlib import Path

from loguru import logger
from src.infrastructure.superlinked.service import (
    get_property_search_service,
)

# Configure logger to output to stdout for better visibility in logs
logger.remove()
logger.add(sys.stdout, format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <level>{message}</level>")

def get_data_path() -> Path:
    """Resolves the path to the properties CSV file."""
    # Assuming the script is run from inside the 'scripts' folder, 
    # and data is in the project root.
    project_root = Path(__file__).resolve().parent.parent
    return project_root / "data" / "properties.csv"

def ingest_data(service, file_path: Path) -> None:
    """Handles the ingestion logic for a single file."""
    if not file_path.exists():
        raise FileNotFoundError(f"Properties file not found at: {file_path}")
    
    logger.info(f"Starting ingestion from: {file_path}")
    
    # Ingest properties
    service.ingest_properties(str(file_path))
    
    logger.success("Property ingestion completed successfully!")

def main():
    """Main function to ingest properties into Qdrant Cloud."""
    logger.info("Initializing PropertySearchService...")
    
    try:
        # Get the property search service instance
        service = get_property_search_service()
        
        properties_data_path = get_data_path()
        ingest_data(service, properties_data_path)
        
        logger.info("Properties are now available for semantic search.")
        
    except FileNotFoundError as e:
        logger.error(e)
        sys.exit(1)
    except Exception as e:
        logger.exception(f"An unexpected error occurred during ingestion: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()