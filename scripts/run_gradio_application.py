from src.Agent.fastrtcagent import FastRTCAgent
from src.Agent.tools.property_search import lookup_listings_tool
from src.infrastructure.superlinked.service import get_property_search_service

property_search_service = get_property_search_service()
property_search_service.ingest_properties("./data/properties.csv")

agent = FastRTCAgent(
    tools=[lookup_listings_tool],
)

agent.stream.ui.launch()