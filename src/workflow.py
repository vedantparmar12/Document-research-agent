import time
import logging
from typing import List, Optional

from src.models.research_result import ResearchResult
from src.models.company import Company
from src.agents.research_agent import ResearchAgent
from src.agents.analysis_agent import AnalysisAgent
from src.utils.logger import setup_logger
from src.utils.config import Config

logger = setup_logger(__name__)


class Workflow:
    """Main workflow orchestrator for the document research agent."""
    
    def __init__(self, config: Optional[Config] = None):
        """Initialize the workflow with configuration."""
        
        self.config = config or Config.from_env()
        
        # Validate configuration
        missing_keys = self.config.validate_keys()
        if missing_keys:
            raise ValueError(f"Missing required API keys: {', '.join(missing_keys)}")
        
        # Initialize agents
        self.research_agent = ResearchAgent()
        self.analysis_agent = AnalysisAgent()
        
        logger.info("Workflow initialized successfully")
    
    def run(self, query: str, max_results: int = 10) -> ResearchResult:
        """Run the complete research workflow for a given query."""
        
        start_time = time.time()
        
        logger.info(f"Starting research workflow for query: '{query}'")
        
        try:
            # Step 1: Research companies/tools
            logger.info("Step 1: Researching companies and tools...")
            companies = self.research_agent.search_companies(query, max_results)
            
            if not companies:
                logger.warning("No companies found for the query")
                return ResearchResult(
                    query=query,
                    companies=[],
                    analysis="No companies or tools found for the given query. Please try a different search term.",
                    total_results=0,
                    search_time=time.time() - start_time
                )
            
            logger.info(f"Found {len(companies)} companies")
            
            # Step 2: Analyze results
            logger.info("Step 2: Analyzing research results...")
            analysis = self.analysis_agent.analyze_companies(companies, query)
            
            # Step 3: Create final result
            result = ResearchResult(
                query=query,
                companies=companies,
                analysis=analysis,
                total_results=len(companies),
                search_time=time.time() - start_time
            )
            
            logger.info(f"Research workflow completed in {result.search_time:.2f} seconds")
            return result
            
        except Exception as e:
            logger.error(f"Error in research workflow: {str(e)}")
            return ResearchResult(
                query=query,
                companies=[],
                analysis=f"Research failed due to an error: {str(e)}",
                total_results=0,
                search_time=time.time() - start_time
            )
    
    def research_company(self, company_name: str, website: str = None) -> Optional[Company]:
        """Research detailed information about a specific company."""
        
        logger.info(f"Researching specific company: {company_name}")
        
        try:
            return self.research_agent.get_company_details(company_name, website)
        except Exception as e:
            logger.error(f"Error researching company {company_name}: {str(e)}")
            return None
    
    def compare_companies(self, companies: List[Company], criteria: List[str] = None) -> str:
        """Compare multiple companies based on given criteria."""
        
        logger.info(f"Comparing {len(companies)} companies")
        
        try:
            return self.analysis_agent.compare_companies(companies, criteria)
        except Exception as e:
            logger.error(f"Error comparing companies: {str(e)}")
            return "Comparison failed due to an error."
    
    def get_recommendations(self, companies: List[Company], user_requirements: str = None) -> str:
        """Get personalized recommendations based on user requirements."""
        
        logger.info("Generating personalized recommendations")
        
        try:
            return self.analysis_agent.generate_recommendations(companies, user_requirements)
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return "Recommendations failed due to an error."
    
    def search_by_category(self, category: str, max_results: int = 10) -> ResearchResult:
        """Search for companies/tools in a specific category."""
        
        query = f"{category} tools and companies"
        return self.run(query, max_results)
    
    def health_check(self) -> dict:
        """Perform a health check of the system."""
        
        logger.info("Performing health check")
        
        health_status = {
            "status": "healthy",
            "components": {},
            "timestamp": time.time()
        }
        
        # Check OpenAI API
        try:
            self.research_agent.llm.invoke([{"role": "user", "content": "test"}])
            health_status["components"]["openai"] = "healthy"
        except Exception as e:
            health_status["components"]["openai"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"
        
        # Check FireCrawl API
        try:
            # This is a simple check - in practice you might want to test with a real URL
            self.research_agent.web_scraper.firecrawl_app
            health_status["components"]["firecrawl"] = "healthy"
        except Exception as e:
            health_status["components"]["firecrawl"] = f"unhealthy: {str(e)}"
            health_status["status"] = "degraded"
        
        # Check configuration
        missing_keys = self.config.validate_keys()
        if missing_keys:
            health_status["components"]["config"] = f"missing keys: {', '.join(missing_keys)}"
            health_status["status"] = "unhealthy"
        else:
            health_status["components"]["config"] = "healthy"
        
        logger.info(f"Health check completed: {health_status['status']}")
        return health_status
