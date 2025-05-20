import pytest
from pathlib import Path
from config import Config, OpenAIConfig, PathConfig, LogConfig

def test_config_initialization():
    """설정 초기화 테스트"""
    config = Config()
    assert isinstance(config.openai, OpenAIConfig)
    assert isinstance(config.paths, PathConfig)
    assert isinstance(config.logging, LogConfig)

def test_path_creation():
    """경로 생성 테스트"""
    config = Config()
    config.validate_environment()
    
    assert config.paths.data_dir.exists()
    assert config.paths.outputs_dir.exists()
    assert config.paths.figures_dir.exists()
    assert config.paths.reports_dir.exists()
    assert config.paths.prompts_dir.exists()

def test_openai_config_validation():
    """OpenAI 설정 검증 테스트"""
    config = Config()
    with pytest.raises(ValueError):
        config.openai.api_key = None
        config.validate_environment()
