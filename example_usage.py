#!/usr/bin/env python3
"""
Example usage script for the Document Research Agent

This script demonstrates various ways to use the research agent programmatically.
"""

from dotenv import load_dotenv
from src.workflow import Workflow
from src.utils.config import Config
from src.utils.logger import setup_logger

load_dotenv()

# Set up logging
logger = setup_logger("example_usage")

def main():
    """Main function demonstrating various usage patterns."""
    
    # Initialize the workflow
    config = Config.from_env()
    workflow = Workflow(config)
    
    # Perform health check
    print("🔍 Performing health check...")
    health = workflow.health_check()
    print(f"System status: {health['status']}")
    
    if health['status'] != 'healthy':
        print("⚠️  System is not healthy. Check your configuration.")
        return
    
    # Example 1: Basic research
    print("\n" + "="*60)
    print("📊 Example 1: Basic Research")
    print("="*60)
    
    query = "Python web frameworks"
    result = workflow.run(query, max_results=5)
    
    print(f"Query: {result.query}")
    print(f"Found {result.total_results} results in {result.search_time:.2f} seconds")
    
    for i, company in enumerate(result.companies, 1):
        print(f"\n{i}. {company.name}")
        print(f"   Website: {company.website}")
        print(f"   Pricing: {company.pricing_model}")
        print(f"   Open Source: {company.is_open_source}")
        if company.description:
            print(f"   Description: {company.description[:100]}...")
    
    print(f"\n📋 Analysis:")
    print(result.analysis)
    
    # Example 2: Company comparison
    print("\n" + "="*60)
    print("📊 Example 2: Company Comparison")
    print("="*60)
    
    if len(result.companies) > 1:
        comparison = workflow.compare_companies(
            result.companies, 
            criteria=["pricing_model", "is_open_source", "api_available"]
        )
        print(comparison)
    
    # Example 3: Personalized recommendations
    print("\n" + "="*60)
    print("📊 Example 3: Personalized Recommendations")
    print("="*60)
    
    recommendations = workflow.get_recommendations(
        result.companies,
        user_requirements="I need a free, open-source solution with good documentation and active community support"
    )
    print(recommendations)
    
    # Example 4: Category-specific search
    print("\n" + "="*60)
    print("📊 Example 4: Category-specific Search")
    print("="*60)
    
    category_result = workflow.search_by_category("CI/CD", max_results=3)
    print(f"Found {category_result.total_results} CI/CD tools:")
    
    for company in category_result.companies:
        print(f"- {company.name}: {company.description}")
    
    # Example 5: Research specific company
    print("\n" + "="*60)
    print("📊 Example 5: Research Specific Company")
    print("="*60)
    
    company_details = workflow.research_company("Docker", "https://www.docker.com")
    if company_details:
        print(f"Company: {company_details.name}")
        print(f"Website: {company_details.website}")
        print(f"Description: {company_details.description}")
        print(f"Tech Stack: {', '.join(company_details.tech_stack)}")
        print(f"Language Support: {', '.join(company_details.language_support)}")
    
    print("\n🎉 All examples completed successfully!")

def demonstrate_error_handling():
    """Demonstrate error handling and edge cases."""
    
    print("\n" + "="*60)
    print("🚨 Error Handling Examples")
    print("="*60)
    
    try:
        # This will fail if API keys are not set
        config = Config.from_env()
        workflow = Workflow(config)
        
        # Test with empty query
        result = workflow.run("")
        print(f"Empty query result: {result.total_results} results")
        
        # Test with very specific query that might not return results
        result = workflow.run("extremely specific non-existent developer tool xyz123")
        print(f"Specific query result: {result.total_results} results")
        
    except ValueError as e:
        print(f"Configuration error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    print("🚀 Document Research Agent - Example Usage")
    print("="*60)
    
    try:
        main()
        demonstrate_error_handling()
    except KeyboardInterrupt:
        print("\n👋 Interrupted by user")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"❌ Error: {e}")
