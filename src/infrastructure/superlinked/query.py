from superlinked import framework as sl

from ...config import settings
from ...infrastructure.superlinked.constants import NEIGHBORHOODS
from ...infrastructure.superlinked.index import (
    description_space,
    price_space,
    property_index,
    property_schema,
    size_space,
)

# Initialize LLM configuration for natural language processing
llm_query_config = sl.GeminiClientConfig(
    api_key=settings.gemini.api_key, 
    model=settings.gemini.model
)

# Define the property search logic with dynamic parameters
property_search_query = (
    sl.Query(
        property_index,
        weights={
            description_space: sl.Param("weight_desc"),
            size_space: sl.Param("weight_size"),
            price_space: sl.Param("weight_price"),
        },
    )
    .find(property_schema)
    .with_natural_query(sl.Param("user_input"), llm_query_config)
    .similar(
        description_space,
        sl.Param(
            "semantic_search_term",
            description="The descriptive text used for vector similarity mapping.",
        ),
    )
    .filter(property_schema.location == sl.Param("area_filter", options=NEIGHBORHOODS))
    .filter(property_schema.rooms >= sl.Param("min_room_count"))
    .filter(property_schema.baths >= sl.Param("min_bathroom_count"))
    .filter(property_schema.sqft >= sl.Param("min_square_footage"))
    .filter(property_schema.price <= sl.Param("max_budget"))
    .limit(sl.Param("result_limit"))
    .select_all()
)