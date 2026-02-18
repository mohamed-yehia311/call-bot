import json
from langchain.tools import tool
from loguru import logger
from ...infrastructure.superlinked.service import get_search_service

@tool
async def lookup_listings_tool(user_description: str, max_results: int = 3) -> str:
    """
    Search the real estate inventory using semantic natural language processing.
    
    Use this tool when a client describes their ideal home or specific requirements. 
    The tool interprets intent behind location, budget, and lifestyle features.
    
    Query Examples:
    - "Quiet 2-bedroom cottage with a garden in the suburbs"
    - "Luxury penthouse in Manhattan with floor-to-ceiling windows"
    - "Budget-friendly studio near the university district"
    
    Args:
        user_description: A detailed string describing desired property traits.
        max_results: The quantity of candidate properties to retrieve (default is 3).
    
    Returns:
        A JSON-formatted string of matching property data or a 'no results' notice.
    """
    try:
        # Utilizing the renamed singleton accessor
        search_engine = get_search_service()
        
        # Calling the updated async search method
        results = await search_engine.execute_search(
            text_input=user_description, 
            top_k=max_results
        )

        if not results:
            return "Discovery Complete: No listings currently match those specific requirements."
        
        # Returning serialized data for the LLM to process
        return json.dumps(results, indent=2, ensure_ascii=False)

    except Exception as error:
        logger.error(f"Listing Tool Error: {error}")
        return f"Service Error: Unable to perform search at this time. Details: {str(error)}"