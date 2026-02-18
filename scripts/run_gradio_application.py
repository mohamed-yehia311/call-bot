from ..src.Agent.fastrtcagent import FastRTCAgent
from ..src.Agent.tools.property_search import get_search_service
from ..src.infrastructure.superlinked.service import get_property_search_service

property_search_service = get_property_search_service()
property_search_service.ingest_properties("./data/properties.csv")

agent = FastRTCAgent(
    tools=[get_search_service],
)

agent.stream.ui.launch()