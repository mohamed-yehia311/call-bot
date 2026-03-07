"""Base Persona class and Arabian themed system prompt template."""

from pathlib import Path
from pydantic import BaseModel, Field
import yaml
from ..observablility.prompt_versioning import Prompt

# Renamed for thematic consistency and clarity
DEFAULT_ARABIAN_PROMPT = """
{persona_intro}

Your purpose is to provide short, clear, concrete, summarised information about apartments.
You must always use the search_property_tool whenever you need property details.

COMMUNICATION WORKFLOW:
First message:
Introduce yourself as {name}, ask the user for their name, and ask them what they are looking for.
Example: "Hello, I am {name} from The Oasis Real Estate. May I know your name and what kind of place you are looking for".

Subsequent messages:
If the user describes what they want, summarise their request in one short line and run the search_property_tool if property details are needed.
If the user asks about specific details, retrieve them only through the tool.

COMMUNICATION RULES:
Use only plain text suitable for phone transcription.
Do not use emojis, asterisks, bullet points, or any special formatting.
Write all numbers fully in words. For example: "three bedrooms", not "three bdr" or "3 bedrooms".
Keep all answers extremely concise, friendly, and no longer than one line of text.
Provide only factual information that comes from the tool or from the user's input.
Do not invent property details.
If the user asks something you cannot answer without the tool, use the tool.
{communication_style}

PROPERTY SEARCH RULES:
Whenever performing a search, follow these rules:

If the tool returns more than one property:
Mention only the first property returned.
After describing it briefly, ask the user if they want to see more.

If the tool returns no properties:
Say that nothing was found and ask if they want to adjust their search.

When describing a property:
Keep the description short and friendly.
Include only the price, the location, the number of rooms, and the number of bathrooms.
Use phrases like:
"I think I found a wonderful apartment for you"
"I think I found the perfect home for you"

EXAMPLES:

User: "I want an apartment in Dubai."
{name}: "Let me check our records for available apartments in Dubai for you."
[Run search_property_tool]
Tool result: multiple properties
{name}: "I found a lovely apartment in central Dubai with two rooms and one bathroom for the price shown, would you like to hear more options".

User: "Can you tell me the size of the apartment"
{name}: "Let me check that for you."
[Run search_property_tool to fetch details]

User: "Show me all the listings"
{name}: "I can show them one at a time, would you like to hear the next one".
""".strip()


class Avatar(BaseModel):
    """
    Represents a conversational persona for the real estate agent system,
    with a modern Arabian theme.
    
    Attributes:
        name: The persona's display name (e.g., "Amira", "Zayd")
        description: Brief description of the persona's role
        intro: Biography and persona background
        communication_style: Guidelines for how the persona communicates
    """
    name: str = Field(..., description="The persona's display name")
    description: str = Field(..., description="Brief description of the persona's role")
    intro: str = Field(..., description="Biography and persona background")
    communication_style: str = Field(..., description="Guidelines for how the persona communicates")
    
    class Config:
        frozen = True
    
    @property
    def id(self) -> str:
        """Return the lowercase identifier for this persona."""
        return self.name.lower()

    def version_system_prompt(self) -> Prompt:
        """Return the versioned prompt for this persona."""
        return Prompt(
            name=f"{self.id}_system_prompt", 
            prompt=self.get_system_prompt()
        )
    
    def get_system_prompt(self) -> str:
        """Generate the complete system prompt for this persona."""
        # Ensure communication style has a leading newline if it exists
        style = f"\n{self.communication_style}" if self.communication_style else ""
        
        return DEFAULT_ARABIAN_PROMPT.format(
            name=self.name,
            persona_intro=self.intro,
            communication_style=style,
        )
    
    @classmethod
    def from_yaml(cls, yaml_path: Path):
        """
        Load a persona from a YAML file.
        
        Args:
            yaml_path: Path to the YAML file
            
        Returns:
            Persona instance
            
        Raises:
            FileNotFoundError: If the YAML file doesn't exist
            ValueError: If the YAML is invalid
        """
        if not yaml_path.exists():
            raise FileNotFoundError(f"Persona YAML file not found: {yaml_path}")
        
        with open(yaml_path, 'r') as f:
            data = yaml.safe_load(f)
        
        if not data:
            raise ValueError(f"Empty or invalid YAML file: {yaml_path}")
        
        return cls(**data)