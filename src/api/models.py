from pydantic import BaseModel, Field

class PropertyDataIngestion(BaseModel):
    """Configuration for importing property datasets into the search engine."""
    
    file_location: str = Field(
        ..., 
        description="The local or remote filesystem path to the property CSV."
    )


class PropertyDiscoveryQuery(BaseModel):
    """Schema for processing natural language real estate search requests."""
    
    user_prompt: str = Field(
        ..., 
        min_length=3,
        description="The descriptive search criteria provided by the user (e.g., 'Modern 2-bed in downtown')."
    )
    
    max_results: int = Field(
        default=5, 
        ge=1, 
        le=20, 
        description="The upper limit of relevant property matches to return."
    )


class CallRequest(BaseModel):
    """Request model for initiating a Twilio phone call."""

    from_number: str = Field(..., alias="from", description="Phone number to call from")
    to_number: str = Field(..., alias="to", description="Phone number to call to")
    voice_agent_url: str = Field(..., description="URL of the voice agent to connect to")

    class Config:
        populate_by_name = True