from langchain.prompts import ChatPromptTemplate
import json
import logging
from datetime import datetime
from typing import Dict, Any
import os
from dotenv import load_dotenv
from utils.decorators import log_execution_time, retry
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class SummaryAgent(BaseAgent):
    def __init__(self) -> None:
        """Summary Agent 초기화"""
        super().__init__("summary_prompt.txt")
        self.logger = logging.getLogger(__name__)

    def analyze_tech_categories(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """기술 카테고리 분석"""
        categories = {}
        try:
            for trend in research_data.get("research_trends", []):
                for tech in trend.get("key_components", []):
                    if tech not in categories:
                        categories[tech] = {
                            "count": 0,
                            "related_trends": set(),
                            "maturity_scores": []
                        }
                    categories[tech]["count"] += 1
                    categories[tech]["related_trends"].add(trend["trend_name"])
                    categories[tech]["maturity_scores"].append(
                        self._convert_maturity_to_score(trend["maturity"])
                    )
        except Exception as e:
            logger.error(f"Error in tech categories analysis: {e}")
        return categories

    def _convert_maturity_to_score(self, maturity: str) -> int:
        """성숙도 문자열을 숫자 점수로 변환"""
        maturity_scores = {
            "신흥": 1,
            "성장": 2,
            "성숙": 3,
            "확립": 4
        }
        return maturity_scores.get(maturity, 0)

    def validate_summary(self, summary: Dict[str, Any]) -> bool:
        """요약 결과 검증"""
        try:
            required_sections = ["tech_categories", "tech_advancements", "integration_trends"]
            if not all(section in summary for section in required_sections):
                logger.error("Missing required sections in summary")
                return False

            if not summary["tech_categories"]:
                logger.error("No technology categories found")
                return False

            return True
        except Exception as e:
            logger.error(f"Error in summary validation: {e}")
            return False

    @log_execution_time
    @retry(max_attempts=3)
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """연구 데이터 요약 및 핵심 기술 분석"""
        try:
            self._validate_state(state, ["research_data", "topic"])
            
            research_data = state["research_data"]
            
            # 요약 생성
            chain = self.prompt | self.llm
            response = chain.invoke({
                "research_data": research_data,
                "tech_categories": research_data.get("tech_categories", {}),
                "\n    \"executive_summary\"": ""  # 빈 값으로 초기화
            })
            
            # 상태 업데이트
            state.update({
                "tech_summary": response.content,
                "summary_timestamp": state.get("timestamp")
            })
            
            return state
            
        except Exception as e:
            self.logger.error(f"Error in SummaryAgent: {e}")
            raise