# app.py
import os
import logging
from datetime import datetime
from typing import Dict, Any
from dotenv import load_dotenv

from agents.research_agent import ResearchAgent
from agents.summary_agent import SummaryAgent
from agents.prediction_agent import PredictionAgent
from agents.risk_agent import RiskAnalysisAgent
from agents.report_agent import ReportAgent

# .env 파일 로드
load_dotenv()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

class TrendAnalysisPipeline:
    def __init__(self):
        self.research_agent = ResearchAgent()
        self.summary_agent = SummaryAgent()
        self.prediction_agent = PredictionAgent()
        self.risk_agent = RiskAnalysisAgent()
        self.report_agent = ReportAgent()
        
    def run(self, topic: str) -> Dict[str, Any]:
        """전체 분석 파이프라인 실행"""
        try:
            logging.info(f"Starting analysis pipeline for topic: {topic}")
            
            # 1. 연구 데이터 수집 및 분석
            logging.info("Step 1: Collecting research data...")
            research_state = self.research_agent(topic)
            
            # 2. 핵심 기술 요약
            logging.info("Step 2: Generating technology summary...")
            summary_state = self.summary_agent(research_state)
            
            # 3. 트렌드 예측
            logging.info("Step 3: Predicting future trends...")
            prediction_state = self.prediction_agent(summary_state)
            
            # 4. 리스크 분석
            logging.info("Step 4: Analyzing risks and responses...")
            risk_state = self.risk_agent(prediction_state)
            
            # 5. 최종 보고서 생성
            logging.info("Step 5: Generating final comprehensive report...")
            final_report = self.report_agent(risk_state)
            
            logging.info(f"Analysis pipeline completed successfully. Report saved to: {final_report.get('report_pdf_path', 'Unknown')}")
            
            return final_report
            
        except Exception as e:
            logging.error(f"Error in analysis pipeline: {e}")
            raise

def main():
    # 분석할 주제 설정
    topic = "인공지능 기반 자율 에이전트 기술"
    
    # 파이프라인 실행
    pipeline = TrendAnalysisPipeline()
    
    try:
        result = pipeline.run(topic)
        logging.info(f"Analysis completed successfully. Generated report: {result.get('report_pdf_path')}")
        
        # 보고서 경로 출력
        md_path = result.get("report_md_path")
        pdf_path = result.get("report_pdf_path")
        
        if md_path:
            print(f"\n마크다운 보고서: {md_path}")
        if pdf_path:
            print(f"PDF 보고서: {pdf_path}")
        
    except Exception as e:
        logging.error(f"Error in main execution: {e}")
        raise

if __name__ == "__main__":
    main()