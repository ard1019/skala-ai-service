# agents/research_agent.py (업데이트)
from langchain.agents import AgentExecutor
from langchain.prompts import ChatPromptTemplate
import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, List
from dotenv import load_dotenv
from utils.decorators import log_execution_time, retry
from data.data_collector import DataCollector
from analysis.text_analysis import TextAnalyzer
from analysis.trend_analysis import TrendAnalyzer
from analysis.network_analysis import NetworkAnalyzer
from .base_agent import BaseAgent

logger = logging.getLogger(__name__)

class ResearchAgent(BaseAgent):
    def __init__(self) -> None:
        super().__init__("research_prompt.txt")
        self.data_collector = DataCollector()
        self.text_analyzer = TextAnalyzer()
        self.trend_analyzer = TrendAnalyzer()
        self.network_analyzer = NetworkAnalyzer()
        
    @log_execution_time
    @retry(max_attempts=3)
    def __call__(self, topic: str) -> Dict[str, Any]:
        """주어진 주제에 대한 연구 분석 수행"""
        try:
            self.logger.info(f"Processing research for topic: {topic}")
            
            # 데이터 수집
            research_data = self.data_collector.collect_research_data(topic)
            
            # 데이터 품질 메트릭 계산
            quality_metrics = self._calculate_quality_metrics(research_data)
            self.logger.info(f"Data quality metrics: {quality_metrics}")
            
            # 상태 반환
            state = {
                "topic": topic,
                "research_data": research_data,
                "quality_metrics": quality_metrics,
                "timestamp": research_data.get("timestamp")
            }
            
            self.logger.info(f"Research analysis completed for topic: {topic}")
            return state
            
        except Exception as e:
            self.logger.error(f"Error in research analysis: {e}")
            raise

    def _calculate_quality_metrics(self, research_data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 품질 메트릭 계산"""
        try:
            return {
                "research_coverage": {
                    "total_papers": len(research_data.get("papers", [])),
                    "total_companies": len(research_data.get("investments", [])),
                    "data_freshness": self._calculate_data_freshness(research_data),
                    "source_diversity": self._calculate_source_diversity(research_data)
                },
                "analysis_completeness": {
                    "tech_categories": len(research_data.get("tech_categories", [])),
                    "trend_predictions": len(research_data.get("trend_predictions", [])),
                    "risk_factors": len(research_data.get("risk_factors", []))
                }
            }
        except Exception as e:
            self.logger.error(f"Error calculating quality metrics: {e}")
            raise

    def _calculate_data_freshness(self, research_data: Dict[str, Any]) -> str:
        """데이터 최신성 검사"""
        try:
            latest_date = max(
                paper.get("published_date", "2000-01-01") 
                for paper in research_data.get("papers", [])
            )
            days_old = (datetime.now() - datetime.strptime(latest_date, "%Y-%m-%d")).days
            return "high" if days_old <= 180 else "medium" if days_old <= 365 else "low"
        except Exception:
            return "unknown"

    def _calculate_source_diversity(self, research_data: Dict[str, Any]) -> Dict[str, int]:
        """데이터 소스 다양성 계산"""
        sources = {}
        try:
            # 논문 소스 분석
            for item in research_data.get("papers", []):
                source = item.get("source", "unknown")
                sources[source] = sources.get(source, 0) + 1
                
            # 뉴스 소스 분석
            for item in research_data.get("news_data", []):
                source = item.get("source", "unknown")
                sources[source] = sources.get(source, 0) + 1
                
            # 특허 소스 분석
            for item in research_data.get("patent_data", []):
                source = item.get("patent_office", "unknown")
                sources[source] = sources.get(source, 0) + 1
                
        except Exception as e:
            logger.error(f"Error in source diversity analysis: {e}")
            
        return sources

    def analyze_data_quality(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """데이터 품질 분석"""
        quality_metrics = {
            "research_coverage": {
                "total_papers": len(data.get("research_data", {}).get("research_trends", [])),
                "total_companies": len(data.get("research_data", {}).get("company_activities", [])),
                "data_freshness": self._check_data_freshness(data),
                "source_diversity": self._analyze_source_diversity(data)
            },
            "analysis_completeness": {
                "tech_categories": len(data.get("tech_summary", {}).get("tech_categories", [])),
                "trend_predictions": len(data.get("trend_prediction", {}).get("tech_roadmap", [])),
                "risk_factors": len(data.get("risk_analysis", {}).get("industry_impact", []))
            }
        }
        return quality_metrics
    
    def _check_data_freshness(self, data: Dict[str, Any]) -> str:
        """데이터 최신성 검사"""
        try:
            latest_date = max(
                paper.get("published_date", "2000-01-01") 
                for paper in data.get("research_data", {}).get("research_trends", [])
            )
            days_old = (datetime.now() - datetime.strptime(latest_date, "%Y-%m-%d")).days
            return "high" if days_old <= 180 else "medium" if days_old <= 365 else "low"
        except Exception:
            return "unknown"
    
    def _analyze_source_diversity(self, data: Dict[str, Any]) -> Dict[str, int]:
        """데이터 소스 다양성 분석"""
        sources = {}
        try:
            # 논문 소스 분석
            for item in data.get("research_data", {}).get("research_trends", []):
                source = item.get("source", "unknown")
                sources[source] = sources.get(source, 0) + 1
                
            # 뉴스 소스 분석
            for item in data.get("research_data", {}).get("news_data", []):
                source = item.get("source", "unknown")
                sources[source] = sources.get(source, 0) + 1
                
            # 특허 소스 분석
            for item in data.get("research_data", {}).get("patent_data", []):
                source = item.get("patent_office", "unknown")
                sources[source] = sources.get(source, 0) + 1
                
        except Exception as e:
            logger.error(f"Error in source diversity analysis: {e}")
            
        return sources

    def validate_results(self, research_data: Dict[str, Any]) -> bool:
        """분석 결과 검증"""
        try:
            # 필수 데이터 존재 여부 확인
            required_keys = ["collected_data", "quality_metrics", "text_analysis", "trend_analysis"]
            if not all(key in research_data for key in required_keys):
                logger.error("Missing required data sections")
                return False
            
            # 데이터 품질 검증
            quality_metrics = research_data["quality_metrics"]
            if quality_metrics["research_coverage"]["total_papers"] < 5:
                logger.warning("Insufficient research paper coverage")
                return False
            
            if quality_metrics["research_coverage"]["data_freshness"] == "low":
                logger.warning("Data freshness is too low")
                return False
            
            # 소스 다양성 검증
            sources = research_data.get("metadata", {}).get("data_sources", [])
            if len(sources) < 3:  # 최소 3개 이상의 서로 다른 소스가 필요
                logger.warning("Insufficient source diversity")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error in result validation: {e}")
            return False