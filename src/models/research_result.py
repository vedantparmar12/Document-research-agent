from pydantic import BaseModel, Field
from typing import List, Optional
from .company import Company


class ResearchResult(BaseModel):
    """Data model for research results."""
    
    query: str = Field(..., description="Original query that was searched")
    companies: List[Company] = Field(default_factory=list, description="List of companies/tools found")
    analysis: Optional[str] = Field(None, description="Analysis and recommendations")
    total_results: int = Field(0, description="Total number of results found")
    search_time: Optional[float] = Field(None, description="Time taken to complete the search")
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "NoSQL databases",
                "companies": [
                    {
                        "name": "MongoDB",
                        "website": "https://mongodb.com",
                        "description": "NoSQL database for modern applications",
                        "pricing_model": "freemium",
                        "is_open_source": True
                    }
                ],
                "analysis": "MongoDB is a popular choice for modern applications...",
                "total_results": 1,
                "search_time": 2.5
            }
        }
