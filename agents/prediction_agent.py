from langchain.prompts import ChatPromptTemplate
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from utils.decorators import log_execution_time, retry
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class PredictionAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("prediction_prompt.txt")

    @log_execution_time
    @retry(max_attempts=3)
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """기술 트렌드 예측 수행"""
        try:
            self._validate_state(state, ["research_data", "tech_summary"])
            
            research_data = state["research_data"]
            tech_summary = state["tech_summary"]
            
            # 예측 생성
            chain = self.prompt | self.llm
            response = chain.invoke({
                "research_data": research_data,
                "tech_summary": tech_summary,
                "tech_roadmap": research_data.get("tech_roadmap", {})
            })
            
            # 상태 업데이트
            state.update({
                "trend_prediction": response.content,
                "prediction_timestamp": state.get("timestamp")
            })
            
            return state
            
        except Exception as e:
            self.logger.error(f"Error in PredictionAgent: {e}")
            raise

    def analyze_growth_trends(self, research_data: Dict[str, Any], 
                            tech_summary: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """성장 트렌드 분석"""
        trends = {
            "high_growth": [],
            "moderate_growth": [],
            "stable": [],
            "declining": []
        }
        
        try:
            for trend in research_data.get("research_trends", []):
                growth_category = self._categorize_growth(
                    trend.get("adoption_trend", ""),
                    trend.get("maturity", "")
                )
                if growth_category:
                    trends[growth_category].append({
                        "trend_name": trend["trend_name"],
                        "description": trend["description"],
                        "maturity": trend["maturity"]
                    })
        except Exception as e:
            logger.error(f"Error in growth trends analysis: {e}")
        
        return trends

    def _categorize_growth(self, adoption_trend: str, maturity: str) -> str:
        """성장 카테고리 분류"""
        if adoption_trend == "상승" and maturity in ["신흥", "성장"]:
            return "high_growth"
        elif adoption_trend == "상승" and maturity in ["성숙", "확립"]:
            return "moderate_growth"
        elif adoption_trend == "안정":
            return "stable"
        elif adoption_trend == "하락":
            return "declining"
        return ""

    def validate_prediction(self, prediction: Dict[str, Any]) -> bool:
        """예측 결과 검증"""
        try:
            required_sections = ["tech_roadmap", "application_areas", "factors"]
            if not all(section in prediction for section in required_sections):
                logger.error("Missing required sections in prediction")
                return False

            if not prediction["tech_roadmap"]:
                logger.error("No technology roadmap found")
                return False

            return True
        except Exception as e:
            logger.error(f"Error in prediction validation: {e}")
            return False