from abc import ABC, abstractmethod
from typing import Dict, Any
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from utils.logger import logger
from utils.exceptions import PromptError
from config import config

class BaseAgent(ABC):
    """기본 에이전트 클래스"""
    def __init__(self, prompt_file: str) -> None:
        self.llm = ChatOpenAI(
            model_name=config.openai.model_name,
            temperature=config.openai.temperature,
            max_tokens=config.openai.max_tokens
        )
        self.logger = logger
        self.prompt = self._load_prompt(prompt_file)

    def _load_prompt(self, prompt_file: str) -> ChatPromptTemplate:
        """프롬프트 템플릿 로드"""
        try:
            prompt_path = config.paths.prompts_dir / prompt_file
            with open(prompt_path, 'r', encoding='utf-8') as f:
                template = f.read()
            return ChatPromptTemplate.from_template(template)
        except Exception as e:
            self.logger.error(f"Error loading prompt {prompt_file}: {e}")
            raise PromptError(f"Failed to load prompt {prompt_file}: {e}")

    def _create_chain(self) -> LLMChain:
        """LLM 체인 생성"""
        return LLMChain(llm=self.llm, prompt=self.prompt)

    @abstractmethod
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """에이전트 실행"""
        pass

    def _validate_state(self, state: Dict[str, Any], required_keys: list) -> None:
        """상태 데이터 검증"""
        missing_keys = [key for key in required_keys if key not in state]
        if missing_keys:
            raise ValueError(f"Missing required keys in state: {missing_keys}")
