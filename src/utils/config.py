import os
from pydantic import BaseModel, Field
from typing import Optional, List


class Config(BaseModel):
    """Configuration settings for the research agent."""
    
    # API Keys
    openai_api_key: str = Field(..., description="OpenAI API key")
    firecrawl_api_key: str = Field(..., description="FireCrawl API key")
    
    # LLM Settings
    llm_model: str = Field(default="gpt-4o-mini", description="LLM model to use")
    llm_temperature: float = Field(default=0.1, description="LLM temperature")
    max_tokens: int = Field(default=2000, description="Maximum tokens for LLM responses")
    
    # Research Settings
    max_search_results: int = Field(default=10, description="Maximum number of search results")
    max_scraping_concurrent: int = Field(default=5, description="Maximum concurrent scraping operations")
    
    # Scraping Settings
    scraping_timeout: int = Field(default=30, description="Scraping timeout in seconds")
    include_domains: List[str] = Field(
        default_factory=lambda: [
            "github.com",
            "docs.mongodb.com",
            "www.postgresql.org",
            "redis.io",
            "cassandra.apache.org",
            "www.docker.com",
            "kubernetes.io",
            "aws.amazon.com",
            "cloud.google.com",
            "azure.microsoft.com",
            "www.elastic.co",
            "www.splunk.com",
            "grafana.com",
            "prometheus.io"
        ],
        description="Domains to include in search results"
    )
    
    # Logging Settings
    log_level: str = Field(default="INFO", description="Logging level")
    log_file: str = Field(default="research_agent.log", description="Log file name")
    
    @classmethod
    def from_env(cls) -> 'Config':
        """Create configuration from environment variables."""
        return cls(
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            firecrawl_api_key=os.getenv("FIRECRAWL_API_KEY", ""),
            llm_model=os.getenv("LLM_MODEL", "gpt-4o-mini"),
            llm_temperature=float(os.getenv("LLM_TEMPERATURE", "0.1")),
            max_tokens=int(os.getenv("MAX_TOKENS", "2000")),
            max_search_results=int(os.getenv("MAX_SEARCH_RESULTS", "10")),
            max_scraping_concurrent=int(os.getenv("MAX_SCRAPING_CONCURRENT", "5")),
            scraping_timeout=int(os.getenv("SCRAPING_TIMEOUT", "30")),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_file=os.getenv("LOG_FILE", "research_agent.log")
        )
    
    def validate_keys(self) -> List[str]:
        """Validate that required API keys are present."""
        missing_keys = []
        
        if not self.openai_api_key:
            missing_keys.append("OPENAI_API_KEY")
        
        if not self.firecrawl_api_key:
            missing_keys.append("FIRECRAWL_API_KEY")
        
        return missing_keys
