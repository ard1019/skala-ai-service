from langchain.prompts import ChatPromptTemplate
import json
import logging
from datetime import datetime
from typing import Dict, Any, List
from utils.decorators import log_execution_time, retry
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class RiskAnalysisAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("risk_prompt.txt")

    @log_execution_time
    @retry(max_attempts=3)
    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """기술 리스크 분석 수행"""
        try:
            self._validate_state(state, ["research_data", "trend_prediction"])
            
            research_data = state["research_data"]
            trend_prediction = state["trend_prediction"]
            
            # 리스크 분석 수행
            chain = self.prompt | self.llm
            response = chain.invoke({
                "research_data": research_data,
                "trend_prediction": trend_prediction
            })
            
            # 상태 업데이트
            state.update({
                "risk_analysis": response.content,
                "risk_timestamp": state.get("timestamp")
            })
            
            return state
            
        except Exception as e:
            self.logger.error(f"Error in RiskAnalysisAgent: {e}")
            raise

    def analyze_industry_risks(self, research_data: Dict[str, Any], 
                             trend_prediction: Dict[str, Any]) -> Dict[str, List[Dict]]:
        """산업별 리스크 분석"""
        industry_risks = {}
        try:
            for industry in ["금융", "의료", "제조", "서비스"]:
                risks = self._identify_industry_risks(
                    industry, research_data, trend_prediction
                )
                industry_risks[industry] = risks
        except Exception as e:
            logger.error(f"Error in industry risks analysis: {e}")
        return industry_risks

    def _identify_industry_risks(self, industry: str, research_data: Dict[str, Any], 
                               trend_prediction: Dict[str, Any]) -> List[Dict]:
        """산업별 리스크 식별"""
        risks = []
        try:
            # 트렌드 예측에서 산업 관련 리스크 추출
            for trend in trend_prediction.get("prediction_data", {}).get("tech_roadmap", []):
                if industry.lower() in trend.get("description", "").lower():
                    risks.append({
                        "risk_type": "technical",
                        "description": trend.get("description", ""),
                        "severity": "high" if "critical" in trend.get("description", "").lower() else "medium",
                        "timeline": trend.get("year", "")
                    })
        except Exception as e:
            logger.error(f"Error identifying risks for {industry}: {e}")
        return risks

    def analyze_ethical_concerns(self, research_data: Dict[str, Any]) -> List[Dict]:
        """윤리적 고려사항 분석"""
        ethical_concerns = []
        try:
            # 연구 데이터에서 윤리적 이슈 추출
            for trend in research_data.get("research_trends", []):
                if any(keyword in trend.get("description", "").lower() 
                      for keyword in ["윤리", "프라이버시", "편향", "차별"]):
                    ethical_concerns.append({
                        "issue": trend["trend_name"],
                        "description": trend["description"],
                        "severity": "high" if "심각" in trend["description"] else "medium"
                    })
        except Exception as e:
            logger.error(f"Error in ethical concerns analysis: {e}")
        return ethical_concerns

    def validate_risk_analysis(self, risk_analysis: Dict[str, Any]) -> bool:
        """리스크 분석 결과 검증"""
        try:
            required_sections = ["industry_impact", "company_strategies", "ethical_considerations"]
            if not all(section in risk_analysis for section in required_sections):
                logger.error("Missing required sections in risk analysis")
                return False

            if not risk_analysis["industry_impact"]:
                logger.error("No industry impact analysis found")
                return False

            return True
        except Exception as e:
            logger.error(f"Error in risk analysis validation: {e}")
            return False