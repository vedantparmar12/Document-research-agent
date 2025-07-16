from typing import List, Dict, Any
from langchain.tools import BaseTool
from src.models.company import Company


class CompanyAnalyzer(BaseTool):
    """Tool to analyze company data and provide recommendations."""

    name: str = "company_analyzer"
    description: str = "Analyzes company data and generates recommendations"

    def analyze(self, companies: List[Company]) -> Dict[str, Any]:
        """Analyze a list of companies and return insights and recommendations."""
        
        analysis = []
        for company in companies:
            if company.is_open_source:
                analysis.append(f"{company.name} is open source. This can offer flexibility and community support.")
            else:
                analysis.append(f"{company.name} is not open source. Consider open source alternatives for community-driven improvements.")
            
            if company.pricing_model == "freemium":
                analysis.append(f"{company.name} offers a freemium model. You can start for free and upgrade as needed.")
            elif company.pricing_model == "paid":
                analysis.append(f"{company.name} requires a subscription. Consider costs against your budget.")
                
            if "AWS" in company.integration_capabilities:
                analysis.append(f"{company.name} integrates with AWS, providing scalable cloud solutions.")

            if company.tech_stack:
                analysis.append(f"{company.name} uses technologies like {', '.join(company.tech_stack[:3])}.")

        return {
            "analysis": analysis,
            "total_companies": len(companies)
        }
