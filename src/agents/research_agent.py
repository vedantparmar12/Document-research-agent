import os
import logging
from typing import List, Dict, Any, Optional
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType
from langchain.schema import HumanMessage, SystemMessage

from src.models.company import Company
from src.tools.web_scraper import WebScraperTool

logger = logging.getLogger(__name__)


class ResearchAgent:
    """Agent responsible for researching companies and developer tools."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.web_scraper = WebScraperTool()
        
    def search_companies(self, query: str, max_results: int = 10) -> List[Company]:
        """Search for companies/tools based on a query."""
        
        logger.info(f"Searching for companies with query: {query}")
        
        # First, try to get structured data from web scraping
        scraped_results = self.web_scraper.search_and_scrape(query, max_results)
        
        companies = []
        
        # Process scraped results
        for result in scraped_results:
            if result.get('success'):
                company = self._process_scraped_data(result)
                if company:
                    companies.append(company)
        
        # If we don't have enough results, use LLM to generate more
        if len(companies) < max_results:
            additional_companies = self._generate_companies_with_llm(query, max_results - len(companies))
            companies.extend(additional_companies)
        
        return companies[:max_results]
    
    def _process_scraped_data(self, scraped_data: Dict[str, Any]) -> Optional[Company]:
        """Process scraped data into a Company object."""
        try:
            extracted = scraped_data.get('extracted_data', {})
            url = scraped_data.get('url', '')
            
            if not extracted.get('company_name'):
                return None
                
            return Company(
                name=extracted.get('company_name', ''),
                website=url,
                description=extracted.get('description', ''),
                pricing_model=extracted.get('pricing_model', ''),
                is_open_source=extracted.get('is_open_source', False),
                tech_stack=extracted.get('tech_stack', []),
                language_support=extracted.get('language_support', []),
                api_available=extracted.get('api_available'),
                integration_capabilities=extracted.get('integrations', []),
                github_url=extracted.get('github_url', ''),
                documentation_url=extracted.get('documentation_url', '')
            )
        except Exception as e:
            logger.error(f"Error processing scraped data: {str(e)}")
            return None
    
    def _generate_companies_with_llm(self, query: str, count: int) -> List[Company]:
        """Use LLM to generate company information when scraping is insufficient."""
        
        prompt = f"""
        You are a research assistant specializing in developer tools and companies.
        
        Generate {count} companies/tools related to: "{query}"
        
        For each company, provide:
        - name: Company/tool name
        - website: Official website URL
        - description: Brief description (2-3 sentences)
        - pricing_model: one of [free, paid, freemium, open_source]
        - is_open_source: true/false
        - tech_stack: list of technologies used (max 5)
        - language_support: programming languages supported (max 5)
        - api_available: true/false/null
        - integration_capabilities: list of integrations (max 5)
        - category: tool category
        - github_url: GitHub repository URL if available
        - documentation_url: Documentation URL if available
        
        Return only valid, real companies/tools. Be accurate and factual.
        Format as JSON array.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a knowledgeable research assistant for developer tools and companies."),
                HumanMessage(content=prompt)
            ])
            
            # Parse the response and create Company objects
            import json
            try:
                companies_data = json.loads(response.content)
                if isinstance(companies_data, list):
                    return [Company(**company_data) for company_data in companies_data]
                else:
                    return []
            except json.JSONDecodeError:
                logger.error("Failed to parse LLM response as JSON")
                return []
                
        except Exception as e:
            logger.error(f"Error generating companies with LLM: {str(e)}")
            return []
    
    def get_company_details(self, company_name: str, website: str = None) -> Optional[Company]:
        """Get detailed information about a specific company."""
        
        if website:
            # Scrape the company website
            scraped_data = self.web_scraper._run(website)
            if scraped_data.get('success'):
                return self._process_scraped_data(scraped_data)
        
        # Fallback to LLM-based research
        prompt = f"""
        Research the company/tool: {company_name}
        
        Provide detailed information in JSON format with these fields:
        - name
        - website
        - description
        - pricing_model
        - is_open_source
        - tech_stack
        - language_support
        - api_available
        - integration_capabilities
        - category
        - github_url
        - documentation_url
        
        Be accurate and factual. If information is not available, use null.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are a knowledgeable research assistant for developer tools and companies."),
                HumanMessage(content=prompt)
            ])
            
            import json
            company_data = json.loads(response.content)
            return Company(**company_data)
            
        except Exception as e:
            logger.error(f"Error getting company details: {str(e)}")
            return None
