from pydantic import BaseModel, Field
from typing import List, Optional


class Company(BaseModel):
    """Data model for a company/developer tool."""
    
    name: str = Field(..., description="Name of the company or tool")
    website: Optional[str] = Field(None, description="Official website URL")
    description: Optional[str] = Field(None, description="Brief description of the company/tool")
    pricing_model: Optional[str] = Field(None, description="Pricing model (free, paid, freemium, etc.)")
    is_open_source: bool = Field(False, description="Whether the tool is open source")
    tech_stack: List[str] = Field(default_factory=list, description="Technologies used")
    language_support: List[str] = Field(default_factory=list, description="Programming languages supported")
    api_available: Optional[bool] = Field(None, description="Whether API is available")
    integration_capabilities: List[str] = Field(default_factory=list, description="Available integrations")
    category: Optional[str] = Field(None, description="Category of the tool")
    github_url: Optional[str] = Field(None, description="GitHub repository URL")
    documentation_url: Optional[str] = Field(None, description="Documentation URL")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "MongoDB",
                "website": "https://mongodb.com",
                "description": "NoSQL database for modern applications",
                "pricing_model": "freemium",
                "is_open_source": True,
                "tech_stack": ["C++", "JavaScript", "Python"],
                "language_support": ["Python", "JavaScript", "Java", "C#"],
                "api_available": True,
                "integration_capabilities": ["AWS", "Azure", "Docker"],
                "category": "Database",
                "github_url": "https://github.com/mongodb/mongo",
                "documentation_url": "https://docs.mongodb.com"
            }
        }
