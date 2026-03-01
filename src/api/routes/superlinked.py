from fastapi import APIRouter, HTTPException, Request, status
from loguru import logger

# Using the updated model names from our previous step
from ..models import PropertyDataIngestion, PropertyDiscoveryQuery

# Updated prefix and tags for a unique API signature
router = APIRouter(prefix="/discovery", tags=["Search Engine"])


@router.post("/ingest", status_code=status.HTTP_201_CREATED)
async def populate_vector_store(payload: PropertyDataIngestion, request: Request):
    """
    Search for properties using natural language queries.
    
    Args:
        payload: PropertyDataIngestion containing the query and result limit
        request: FastAPI request object to access app state
        
    Returns:
        List of matching properties with their details
    """
    try:
        # Accessing the service via the renamed engine instance
        engine = request.app.state.property_service
        engine.load_data(payload.file_location)
        
        return {
            "status": "success",
            "details": f"Successfully synchronized records from {payload.file_location}",
        }
        
    except FileNotFoundError:
        logger.error(f"Source file missing: {payload.file_location}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The specified data file could not be located on the server."
        )
    except Exception as err:
        logger.exception("Ingestion pipeline failure")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during data sync: {str(err)}"
        )


@router.post("/search")
async def find_relevant_properties(search_request: PropertyDiscoveryQuery, request: Request):
    """
    Retrieves property matches based on semantic similarity to the user prompt.
    """
    try:
        engine = request.app.state.property_service
        
        # Calling the renamed async method
        matches = await engine.execute_search(
            text_input=search_request.user_prompt, 
            top_k=search_request.max_results
        )
        
        return {
            "outcome": "success",
            "metadata": {
                "input_prompt": search_request.user_prompt,
                "returned_count": len(matches),
                "requested_limit": search_request.max_results
            },
            "listings": matches,
        }
        
    except Exception as err:
        logger.error(f"Search endpoint failure: {err}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="The search engine encountered an issue processing your request."
        )