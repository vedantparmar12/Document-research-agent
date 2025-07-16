import os
import logging
from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

from src.models.company import Company

logger = logging.getLogger(__name__)


class AnalysisAgent:
    """Agent responsible for analyzing research results and providing recommendations."""
    
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0.3,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
    
    def analyze_companies(self, companies: List[Company], query: str) -> str:
        """Analyze a list of companies and generate insights and recommendations."""
        
        if not companies:
            return "No companies found for the given query."
        
        # Create a summary of the companies
        companies_summary = self._create_companies_summary(companies)
        
        # Generate analysis using LLM
        prompt = f"""
        Based on the following research results for the query: "{query}"
        
        {companies_summary}
        
        Please provide a comprehensive analysis including:
        
        1. **Key Findings**: What are the main patterns and trends?
        2. **Recommendations**: Which tools/companies would you recommend and why?
        3. **Comparison**: How do these options compare in terms of:
           - Pricing models
           - Open source vs proprietary
           - Technical capabilities
           - Integration options
        4. **Use Cases**: What scenarios would each option be best suited for?
        5. **Considerations**: What factors should developers consider when choosing?
        
        Keep the analysis practical and actionable for developers.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert technical analyst specializing in developer tools and technology recommendations."),
                HumanMessage(content=prompt)
            ])
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating analysis: {str(e)}")
            return "Analysis failed due to an error."
    
    def _create_companies_summary(self, companies: List[Company]) -> str:
        """Create a structured summary of companies for analysis."""
        
        summary_lines = []
        
        for i, company in enumerate(companies, 1):
            summary_lines.append(f"\n{i}. **{company.name}**")
            summary_lines.append(f"   - Website: {company.website or 'N/A'}")
            summary_lines.append(f"   - Description: {company.description or 'N/A'}")
            summary_lines.append(f"   - Pricing: {company.pricing_model or 'N/A'}")
            summary_lines.append(f"   - Open Source: {'Yes' if company.is_open_source else 'No'}")
            
            if company.tech_stack:
                summary_lines.append(f"   - Tech Stack: {', '.join(company.tech_stack[:5])}")
            
            if company.language_support:
                summary_lines.append(f"   - Language Support: {', '.join(company.language_support[:5])}")
            
            if company.api_available is not None:
                summary_lines.append(f"   - API Available: {'Yes' if company.api_available else 'No'}")
            
            if company.integration_capabilities:
                summary_lines.append(f"   - Integrations: {', '.join(company.integration_capabilities[:5])}")
            
            if company.category:
                summary_lines.append(f"   - Category: {company.category}")
        
        return "\n".join(summary_lines)
    
    def compare_companies(self, companies: List[Company], criteria: List[str] = None) -> str:
        """Compare companies based on specific criteria."""
        
        if not companies:
            return "No companies to compare."
        
        if criteria is None:
            criteria = ["pricing_model", "is_open_source", "api_available", "tech_stack"]
        
        comparison_data = []
        for company in companies:
            company_data = {
                "name": company.name,
                "pricing_model": company.pricing_model,
                "is_open_source": company.is_open_source,
                "api_available": company.api_available,
                "tech_stack": company.tech_stack,
                "language_support": company.language_support,
                "integration_capabilities": company.integration_capabilities
            }
            comparison_data.append(company_data)
        
        # Create comparison prompt
        prompt = f"""
        Compare these companies/tools based on the following criteria: {', '.join(criteria)}
        
        Companies to compare:
        {self._format_comparison_data(comparison_data)}
        
        Provide a detailed comparison highlighting:
        1. Strengths and weaknesses of each option
        2. Best use cases for each
        3. Key differentiators
        4. Recommendations based on different scenarios
        
        Format as a clear, structured comparison.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert technical analyst specializing in technology comparisons."),
                HumanMessage(content=prompt)
            ])
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating comparison: {str(e)}")
            return "Comparison failed due to an error."
    
    def _format_comparison_data(self, comparison_data: List[Dict[str, Any]]) -> str:
        """Format comparison data for LLM analysis."""
        
        formatted_lines = []
        
        for data in comparison_data:
            formatted_lines.append(f"\n**{data['name']}:**")
            formatted_lines.append(f"- Pricing: {data['pricing_model']}")
            formatted_lines.append(f"- Open Source: {'Yes' if data['is_open_source'] else 'No'}")
            formatted_lines.append(f"- API Available: {data['api_available']}")
            formatted_lines.append(f"- Tech Stack: {', '.join(data['tech_stack'][:3]) if data['tech_stack'] else 'N/A'}")
            formatted_lines.append(f"- Language Support: {', '.join(data['language_support'][:3]) if data['language_support'] else 'N/A'}")
            formatted_lines.append(f"- Integrations: {', '.join(data['integration_capabilities'][:3]) if data['integration_capabilities'] else 'N/A'}")
        
        return "\n".join(formatted_lines)
    
    def generate_recommendations(self, companies: List[Company], user_requirements: str = None) -> str:
        """Generate specific recommendations based on user requirements."""
        
        if not companies:
            return "No companies available for recommendations."
        
        requirements_text = f"User requirements: {user_requirements}" if user_requirements else "No specific requirements provided."
        
        prompt = f"""
        Based on the following companies and user requirements, provide specific recommendations:
        
        {requirements_text}
        
        Available options:
        {self._create_companies_summary(companies)}
        
        Please provide:
        1. Top 3 recommendations with reasoning
        2. Pros and cons of each recommended option
        3. Implementation considerations
        4. Budget considerations
        5. Scalability factors
        
        Tailor recommendations to the user's specific needs.
        """
        
        try:
            response = self.llm.invoke([
                SystemMessage(content="You are an expert technical consultant providing personalized technology recommendations."),
                HumanMessage(content=prompt)
            ])
            
            return response.content
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            return "Recommendations failed due to an error."
