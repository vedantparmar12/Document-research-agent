# Document Research Agent

A sophisticated RAG-based research tool that helps developers discover, analyze, and compare developer tools and companies. The agent leverages web scraping, AI analysis, and structured data extraction to provide comprehensive insights about technology solutions.

## 🚀 Features

- **Intelligent Research**: AI-powered search and analysis of developer tools and companies
- **Web Scraping**: Automated extraction of structured data from websites using FireCrawl
- **Comprehensive Analysis**: Detailed comparisons and recommendations based on multiple criteria
- **Real-time Data**: Fresh information scraped from official websites and documentation
- **Structured Output**: Clean, organized results with company profiles and analysis
- **Extensible Architecture**: Modular design for easy customization and extension

## 🏗️ Architecture

The system follows a modular architecture with the following components:

```
src/
├── agents/           # AI agents for research and analysis
│   ├── research_agent.py    # Company/tool discovery and data extraction
│   └── analysis_agent.py    # Results analysis and recommendations
├── models/           # Data models and schemas
│   ├── company.py           # Company/tool data structure
│   └── research_result.py   # Research result container
├── tools/            # Utility tools
│   ├── web_scraper.py       # FireCrawl integration for web scraping
│   └── company_analyzer.py  # Company data analysis utilities
├── utils/            # Utility functions
│   ├── logger.py            # Logging configuration
│   └── config.py            # Configuration management
└── workflow.py       # Main workflow orchestrator
```

## 📋 Prerequisites

Before running the application, ensure you have:

- Python 3.12 or higher
- OpenAI API key
- FireCrawl API key

## 🔧 Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd document-research-agent
```

2. **Create a virtual environment:**
```bash
python -m venv .venv

# On Windows:
.venv\Scripts\activate

# On macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables:**

Create a `.env` file in the project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
FIRECRAWL_API_KEY=your_firecrawl_api_key_here

# Optional configurations
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.1
MAX_SEARCH_RESULTS=10
LOG_LEVEL=INFO
```

## 🎯 Usage

### Basic Usage

```bash
python main.py
```

The application will start an interactive session where you can enter queries about developer tools and companies:

```
Developer Tools Research Agent

🔍 Developer Tools Query: NoSQL databases

📊 Results for: NoSQL databases
============================================================

1. 🏢 MongoDB
   🌐 Website: https://www.mongodb.com
   💰 Pricing: freemium
   📖 Open Source: True
   🛠️  Tech Stack: C++, JavaScript, Python
   💻 Language Support: Python, JavaScript, Java, C#
   🔌 API: ✅ Available
   🔗 Integrations: AWS, Azure, Docker, Kubernetes
   📝 Description: NoSQL database for modern applications

2. 🏢 Redis
   🌐 Website: https://redis.io
   💰 Pricing: open_source
   📖 Open Source: True
   ...
```

### Programmatic Usage

```python
from src.workflow import Workflow
from src.utils.config import Config

# Initialize workflow
config = Config.from_env()
workflow = Workflow(config)

# Research companies
result = workflow.run("machine learning frameworks", max_results=5)

# Print results
print(f"Found {result.total_results} companies")
for company in result.companies:
    print(f"- {company.name}: {company.description}")

print(f"\nAnalysis: {result.analysis}")
```

### Advanced Features

**1. Company Comparison:**
```python
comparison = workflow.compare_companies(
    result.companies, 
    criteria=["pricing_model", "is_open_source", "api_available"]
)
print(comparison)
```

**2. Personalized Recommendations:**
```python
recommendations = workflow.get_recommendations(
    result.companies,
    user_requirements="Need a free, open-source solution with Python support"
)
print(recommendations)
```

**3. Category-specific Search:**
```python
result = workflow.search_by_category("CI/CD", max_results=8)
```

**4. Health Check:**
```python
health = workflow.health_check()
print(f"System status: {health['status']}")
```

## 🔧 Configuration

The application can be configured through environment variables:

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | Required | OpenAI API key for LLM operations |
| `FIRECRAWL_API_KEY` | Required | FireCrawl API key for web scraping |
| `LLM_MODEL` | `gpt-4o-mini` | OpenAI model to use |
| `LLM_TEMPERATURE` | `0.1` | Temperature for LLM responses |
| `MAX_TOKENS` | `2000` | Maximum tokens for LLM responses |
| `MAX_SEARCH_RESULTS` | `10` | Maximum number of search results |
| `MAX_SCRAPING_CONCURRENT` | `5` | Maximum concurrent scraping operations |
| `SCRAPING_TIMEOUT` | `30` | Scraping timeout in seconds |
| `LOG_LEVEL` | `INFO` | Logging level |

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/ -v
```

## 📊 Data Models

### Company Model

```python
class Company(BaseModel):
    name: str
    website: Optional[str]
    description: Optional[str]
    pricing_model: Optional[str]  # free, paid, freemium, open_source
    is_open_source: bool
    tech_stack: List[str]
    language_support: List[str]
    api_available: Optional[bool]
    integration_capabilities: List[str]
    category: Optional[str]
    github_url: Optional[str]
    documentation_url: Optional[str]
```

### Research Result Model

```python
class ResearchResult(BaseModel):
    query: str
    companies: List[Company]
    analysis: Optional[str]
    total_results: int
    search_time: Optional[float]
```

## 🔍 How It Works

1. **Query Processing**: The system receives a user query about developer tools or companies

2. **Web Research**: 
   - Uses FireCrawl to search and scrape relevant websites
   - Targets specific domains (GitHub, official documentation, etc.)
   - Extracts structured data using predefined schemas

3. **AI Enhancement**: 
   - LLM fills in missing information
   - Generates additional companies if scraping results are insufficient
   - Ensures data quality and consistency

4. **Analysis & Recommendations**:
   - Analyzes patterns and trends in the data
   - Generates comparative insights
   - Provides actionable recommendations

5. **Result Presentation**: 
   - Structures data into user-friendly format
   - Provides both detailed company profiles and summary analysis

## 🛠️ Development

### Adding New Data Sources

1. **Extend the web scraper** in `src/tools/web_scraper.py`:
```python
def scrape_new_source(self, url: str) -> Dict[str, Any]:
    # Custom scraping logic
    pass
```

2. **Update the include_domains** in `src/utils/config.py`:
```python
include_domains: List[str] = [
    "github.com",
    "your-new-domain.com",
    # ... other domains
]
```

### Adding New Analysis Types

1. **Extend the analysis agent** in `src/agents/analysis_agent.py`:
```python
def custom_analysis(self, companies: List[Company]) -> str:
    # Custom analysis logic
    pass
```

2. **Update the workflow** in `src/workflow.py` to include new analysis types.

## 📝 API Documentation

### Workflow Class

#### `run(query: str, max_results: int = 10) -> ResearchResult`
Executes the complete research workflow.

#### `research_company(company_name: str, website: str = None) -> Optional[Company]`
Researches detailed information about a specific company.

#### `compare_companies(companies: List[Company], criteria: List[str] = None) -> str`
Compares companies based on specified criteria.

#### `get_recommendations(companies: List[Company], user_requirements: str = None) -> str`
Generates personalized recommendations.

#### `health_check() -> dict`
Performs system health check.

## 🚨 Troubleshooting

### Common Issues

1. **Missing API Keys**:
   ```
   ValueError: Missing required API keys: OPENAI_API_KEY, FIRECRAWL_API_KEY
   ```
   - Solution: Set the required environment variables in your `.env` file

2. **Import Errors**:
   ```
   ModuleNotFoundError: No module named 'src'
   ```
   - Solution: Ensure you're running from the project root directory

3. **Rate Limiting**:
   - If you encounter rate limits, reduce `MAX_SCRAPING_CONCURRENT` in your configuration

4. **Network Timeouts**:
   - Increase `SCRAPING_TIMEOUT` if you experience frequent timeouts

## 📈 Performance Considerations

- **Caching**: Consider implementing caching for frequently searched companies
- **Batch Processing**: For large queries, consider processing in batches
- **Rate Limiting**: Respect API rate limits for both OpenAI and FireCrawl
- **Concurrent Scraping**: Adjust `MAX_SCRAPING_CONCURRENT` based on your system capabilities

## 🔮 Future Enhancements

- [ ] Add support for more data sources (Crunchbase, ProductHunt, etc.)
- [ ] Implement result caching and persistence
- [ ] Add export functionality (CSV, JSON, PDF reports)
- [ ] Create web interface for easier interaction
- [ ] Add support for custom analysis templates
- [ ] Implement real-time monitoring and alerting
- [ ] Add support for bulk queries and batch processing

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **OpenAI** for providing powerful language models
- **FireCrawl** for excellent web scraping capabilities
- **LangChain** for the agent framework
- **Pydantic** for data validation

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ for the developer community**