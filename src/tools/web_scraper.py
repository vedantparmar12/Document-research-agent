import os
import asyncio
from typing import List, Optional, Dict, Any
from firecrawl import FirecrawlApp
from langchain.tools import BaseTool
from pydantic import Field
import logging

logger = logging.getLogger(__name__)


class WebScraperTool(BaseTool):
    """Tool for web scraping using FireCrawl API."""
    
    name: str = "web_scraper"
    description: str = "Scrapes web pages to extract information about companies and developer tools"
    
    firecrawl_app: FirecrawlApp = Field(default=None)
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        api_key = os.getenv("FIRECRAWL_API_KEY")
        if not api_key:
            raise ValueError("FIRECRAWL_API_KEY environment variable is required")
        self.firecrawl_app = FirecrawlApp(api_key=api_key)
    
    def _run(self, url: str, **kwargs) -> Dict[str, Any]:
        """Scrape a single URL and return structured data."""
        try:
            # Scrape the URL
            scrape_result = self.firecrawl_app.scrape_url(
                url=url,
                params={
                    'formats': ['markdown', 'extract'],
                    'extract': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'company_name': {'type': 'string'},
                                'description': {'type': 'string'},
                                'pricing_model': {'type': 'string'},
                                'is_open_source': {'type': 'boolean'},
                                'tech_stack': {'type': 'array', 'items': {'type': 'string'}},
                                'language_support': {'type': 'array', 'items': {'type': 'string'}},
                                'api_available': {'type': 'boolean'},
                                'integrations': {'type': 'array', 'items': {'type': 'string'}},
                                'github_url': {'type': 'string'},
                                'documentation_url': {'type': 'string'}
                            }
                        }
                    }
                }
            )
            
            if scrape_result.get('success'):
                return {
                    'success': True,
                    'url': url,
                    'markdown': scrape_result.get('markdown', ''),
                    'extracted_data': scrape_result.get('extract', {}),
                    'metadata': scrape_result.get('metadata', {})
                }
            else:
                logger.error(f"Failed to scrape {url}: {scrape_result.get('error', 'Unknown error')}")
                return {
                    'success': False,
                    'url': url,
                    'error': scrape_result.get('error', 'Unknown error')
                }
                
        except Exception as e:
            logger.error(f"Exception while scraping {url}: {str(e)}")
            return {
                'success': False,
                'url': url,
                'error': str(e)
            }
    
    async def _arun(self, url: str, **kwargs) -> Dict[str, Any]:
        """Async version of _run."""
        return await asyncio.get_event_loop().run_in_executor(
            None, self._run, url
        )
    
    def search_and_scrape(self, query: str, max_results: int = 10) -> List[Dict[str, Any]]:
        """Search for URLs related to a query and scrape them."""
        try:
            # Use FireCrawl's search functionality
            search_result = self.firecrawl_app.search(
                query=query,
                params={
                    'limit': max_results,
                    'search_depth': 'basic',
                    'include_domains': [
                        'github.com',
                        'docs.mongodb.com',
                        'www.postgresql.org',
                        'redis.io',
                        'cassandra.apache.org',
                        'www.docker.com',
                        'kubernetes.io',
                        'aws.amazon.com',
                        'cloud.google.com',
                        'azure.microsoft.com'
                    ]
                }
            )
            
            if not search_result.get('success'):
                logger.error(f"Search failed for query '{query}': {search_result.get('error', 'Unknown error')}")
                return []
            
            results = []
            for result in search_result.get('data', []):
                url = result.get('url', '')
                if url:
                    scraped_data = self._run(url)
                    results.append(scraped_data)
            
            return results
            
        except Exception as e:
            logger.error(f"Exception during search and scrape for query '{query}': {str(e)}")
            return []
    
    def scrape_github_repo(self, repo_url: str) -> Dict[str, Any]:
        """Specifically scrape GitHub repository for developer tool information."""
        try:
            scrape_result = self.firecrawl_app.scrape_url(
                url=repo_url,
                params={
                    'formats': ['markdown', 'extract'],
                    'extract': {
                        'schema': {
                            'type': 'object',
                            'properties': {
                                'repository_name': {'type': 'string'},
                                'description': {'type': 'string'},
                                'language': {'type': 'string'},
                                'languages': {'type': 'array', 'items': {'type': 'string'}},
                                'stars': {'type': 'integer'},
                                'forks': {'type': 'integer'},
                                'license': {'type': 'string'},
                                'topics': {'type': 'array', 'items': {'type': 'string'}},
                                'website': {'type': 'string'},
                                'documentation': {'type': 'string'}
                            }
                        }
                    }
                }
            )
            
            if scrape_result.get('success'):
                return {
                    'success': True,
                    'url': repo_url,
                    'extracted_data': scrape_result.get('extract', {}),
                    'markdown': scrape_result.get('markdown', ''),
                    'metadata': scrape_result.get('metadata', {})
                }
            else:
                return {
                    'success': False,
                    'url': repo_url,
                    'error': scrape_result.get('error', 'Unknown error')
                }
                
        except Exception as e:
            logger.error(f"Exception while scraping GitHub repo {repo_url}: {str(e)}")
            return {
                'success': False,
                'url': repo_url,
                'error': str(e)
            }
