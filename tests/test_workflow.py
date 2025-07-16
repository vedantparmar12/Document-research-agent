import pytest
from unittest.mock import Mock, patch
from src.workflow import Workflow
from src.models.company import Company
from src.models.research_result import ResearchResult
from src.utils.config import Config


class TestWorkflow:
    """Test cases for the Workflow class."""

    def test_workflow_initialization(self):
        """Test that workflow initializes with proper configuration."""
        # Mock the config to avoid requiring actual API keys
        with patch('src.utils.config.Config.from_env') as mock_config:
            mock_config.return_value = Mock(validate_keys=Mock(return_value=[]))
            
            with patch('src.agents.research_agent.ResearchAgent'):
                with patch('src.agents.analysis_agent.AnalysisAgent'):
                    workflow = Workflow()
                    assert workflow is not None

    def test_health_check_structure(self):
        """Test that health check returns proper structure."""
        with patch('src.utils.config.Config.from_env') as mock_config:
            mock_config.return_value = Mock(validate_keys=Mock(return_value=[]))
            
            with patch('src.agents.research_agent.ResearchAgent'):
                with patch('src.agents.analysis_agent.AnalysisAgent'):
                    workflow = Workflow()
                    
                    # Mock the health check components
                    with patch.object(workflow, 'research_agent') as mock_research:
                        mock_research.llm.invoke.return_value = Mock()
                        mock_research.web_scraper.firecrawl_app = Mock()
                        
                        health = workflow.health_check()
                        
                        assert 'status' in health
                        assert 'components' in health
                        assert 'timestamp' in health

    def test_run_with_empty_query(self):
        """Test workflow behavior with empty query."""
        with patch('src.utils.config.Config.from_env') as mock_config:
            mock_config.return_value = Mock(validate_keys=Mock(return_value=[]))
            
            with patch('src.agents.research_agent.ResearchAgent') as mock_research_agent:
                with patch('src.agents.analysis_agent.AnalysisAgent') as mock_analysis_agent:
                    # Mock the research agent to return empty results
                    mock_research_instance = Mock()
                    mock_research_instance.search_companies.return_value = []
                    mock_research_agent.return_value = mock_research_instance
                    
                    mock_analysis_instance = Mock()
                    mock_analysis_agent.return_value = mock_analysis_instance
                    
                    workflow = Workflow()
                    result = workflow.run("")
                    
                    assert isinstance(result, ResearchResult)
                    assert result.total_results == 0

    def test_run_with_valid_query(self):
        """Test workflow with a valid query."""
        with patch('src.utils.config.Config.from_env') as mock_config:
            mock_config.return_value = Mock(validate_keys=Mock(return_value=[]))
            
            with patch('src.agents.research_agent.ResearchAgent') as mock_research_agent:
                with patch('src.agents.analysis_agent.AnalysisAgent') as mock_analysis_agent:
                    # Mock company data
                    mock_company = Company(
                        name="Test Company",
                        website="https://test.com",
                        description="Test description",
                        pricing_model="free",
                        is_open_source=True
                    )
                    
                    # Mock the research agent
                    mock_research_instance = Mock()
                    mock_research_instance.search_companies.return_value = [mock_company]
                    mock_research_agent.return_value = mock_research_instance
                    
                    # Mock the analysis agent
                    mock_analysis_instance = Mock()
                    mock_analysis_instance.analyze_companies.return_value = "Test analysis"
                    mock_analysis_agent.return_value = mock_analysis_instance
                    
                    workflow = Workflow()
                    result = workflow.run("test query")
                    
                    assert isinstance(result, ResearchResult)
                    assert result.total_results == 1
                    assert result.companies[0].name == "Test Company"
                    assert result.analysis == "Test analysis"

    def test_config_validation_error(self):
        """Test that workflow raises error when API keys are missing."""
        with patch('src.utils.config.Config.from_env') as mock_config:
            mock_config.return_value = Mock(validate_keys=Mock(return_value=['OPENAI_API_KEY']))
            
            with pytest.raises(ValueError) as excinfo:
                Workflow()
            
            assert "Missing required API keys" in str(excinfo.value)


if __name__ == "__main__":
    pytest.main([__file__])
