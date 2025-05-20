# analysis/trend_analysis.py
import logging
from typing import List, Dict, Any
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression

class TrendAnalyzer:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def analyze_technology_trends(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """기술 트렌드 분석"""
        try:
            # 각 데이터 소스별 트렌드 분석
            paper_trends = self._analyze_paper_trends(data.get("papers", []))
            patent_trends = self._analyze_patent_trends(data.get("patents", []))
            investment_trends = self._analyze_investment_trends(data.get("investments", []))

            # 통합 트렌드 분석
            return {
                "research_trends": paper_trends,
                "innovation_trends": patent_trends,
                "market_trends": investment_trends,
                "integrated_analysis": self._integrate_trends(paper_trends, patent_trends, investment_trends)
            }

        except Exception as e:
            self.logger.error(f"Error in technology trend analysis: {e}")
            return {}

    def _analyze_paper_trends(self, papers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """연구 논문 트렌드 분석"""
        try:
            # 시간별 논문 수 및 인용 수 분석
            timeline = self._create_timeline(papers, "publication_date")
            citation_impact = self._analyze_citations(papers)

            return {
                "publication_timeline": timeline,
                "citation_impact": citation_impact,
                "key_research_areas": self._identify_research_areas(papers)
            }

        except Exception as e:
            self.logger.error(f"Error in paper trend analysis: {e}")
            return {}

    def _analyze_patent_trends(self, patents: List[Dict[str, Any]]) -> Dict[str, Any]:
        """특허 트렌드 분석"""
        try:
            # 시간별 특허 출원 수 분석
            timeline = self._create_timeline(patents, "filing_date")
            
            return {
                "patent_timeline": timeline,
                "technology_categories": self._categorize_patents(patents),
                "top_inventors": self._identify_top_inventors(patents)
            }

        except Exception as e:
            self.logger.error(f"Error in patent trend analysis: {e}")
            return {}

    def _analyze_investment_trends(self, investments: List[Dict[str, Any]]) -> Dict[str, Any]:
        """투자 트렌드 분석"""
        try:
            # 시간별 투자 금액 분석
            timeline = self._create_timeline(investments, "date")
            
            return {
                "investment_timeline": timeline,
                "funding_distribution": self._analyze_funding_distribution(investments),
                "investor_analysis": self._analyze_investor_patterns(investments)
            }

        except Exception as e:
            self.logger.error(f"Error in investment trend analysis: {e}")
            return {}

    def _create_timeline(self, items: List[Dict[str, Any]], date_field: str) -> Dict[str, Any]:
        """시간별 트렌드 타임라인 생성"""
        try:
            timeline = {}
            for item in items:
                date = datetime.strptime(item[date_field], "%Y-%m-%d")
                year = date.year
                if year not in timeline:
                    timeline[year] = 0
                timeline[year] += 1

            # 성장률 계산
            years = sorted(timeline.keys())
            if len(years) >= 2:
                growth_rate = (timeline[years[-1]] - timeline[years[0]]) / timeline[years[0]] * 100
            else:
                growth_rate = 0

            return {
                "yearly_counts": timeline,
                "growth_rate": growth_rate
            }

        except Exception as e:
            self.logger.error(f"Error in timeline creation: {e}")
            return {}

    def _integrate_trends(self, paper_trends: Dict[str, Any], 
                        patent_trends: Dict[str, Any], 
                        investment_trends: Dict[str, Any]) -> Dict[str, Any]:
        """통합 트렌드 분석"""
        try:
            return {
                "overall_growth_rate": self._calculate_overall_growth(
                    paper_trends.get("publication_timeline", {}).get("growth_rate", 0),
                    patent_trends.get("patent_timeline", {}).get("growth_rate", 0),
                    investment_trends.get("investment_timeline", {}).get("growth_rate", 0)
                ),
                "technology_maturity": self._assess_technology_maturity(
                    paper_trends, patent_trends, investment_trends
                ),
                "market_readiness": self._assess_market_readiness(
                    paper_trends, patent_trends, investment_trends
                )
            }

        except Exception as e:
            self.logger.error(f"Error in trend integration: {e}")
            return {}

    def _calculate_overall_growth(self, paper_growth: float, 
                                patent_growth: float, 
                                investment_growth: float) -> float:
        """전체 성장률 계산"""
        weights = [0.3, 0.3, 0.4]  # 논문, 특허, 투자 가중치
        return np.average([paper_growth, patent_growth, investment_growth], weights=weights)