# 자율 에이전트 기술 발전 전망 보고서 생성 프롬프트

SYSTEM_PROMPT = """
당신은 자율 에이전트 기술 분야의 전문 분석가입니다. 4개의 에이전트로부터 받은 데이터를 종합하여 
'인공지능 기반 자율 에이전트 기술의 향후 5년 발전 전망' 보고서를 작성해야 합니다.
객관적이고 통찰력 있는 보고서를 작성하되, 기술적 가능성과 현실적 한계를 균형있게 다루세요.
"""

REPORT_TEMPLATE = """
# 인공지능 기반 자율 에이전트 기술의 향후 5년 발전 전망

## SUMMARY
{summary}

## 1. 서론
{introduction}

## 2. 자율 에이전트 기술의 현재 상황
{current_state}

## 3. 자율 에이전트 기술의 발전 동향 분석
{trend_analysis}

## 4. 향후 5년 자율 에이전트 기술 발전 예측
{future_prediction}

## 5. 산업별 자율 에이전트 기술 적용 사례 및 기회
{industry_applications}

## 6. 기업을 위한 전략적 제언
{strategic_recommendations}

## 7. 결론
{conclusion}

## 8. 참고 문헌
{references}
"""

def generate_trend_report(research_data, tech_summary, trend_prediction, risk_analysis):
    """
    자율 에이전트 기술 발전 전망 보고서 생성 함수
    
    Parameters:
    -----------
    research_data : dict
        최신 연구뉴스 추천 에이전트가 수집한 논문, 뉴스, 기업 발표자료 분석 결과
    
    tech_summary : dict
        핵심 기술 요약 에이전트가 도출한 주요 기술 트렌드 요약 및 분석
    
    trend_prediction : dict
        트렌드 예측 에이전트가 예측한 향후 5년간 기술 발전 방향
    
    risk_analysis : dict
        리스크 및 기회 분석 에이전트가 분석한 산업별 기회와 위험요소
    
    Returns:
    --------
    str
        완성된 트렌드 분석 보고서
    """
    
    # 각 섹션별 생성 지침
    section_instructions = {
        "summary": """
        보고서의 핵심 내용을 최대 5줄로 요약하세요. 
        가장 중요한 트렌드와 기업에 미칠 영향을 중심으로 작성합니다.
        """,
        
        "introduction": """
        연구 배경, 목적, 범위 및 방법론을 설명하세요.
        왜 자율 에이전트 기술이 중요한지, 어떤 측면에 초점을 맞추었는지 명확히 합니다.
        2-3페이지 분량으로 작성하세요.
        """,
        
        "current_state": """
        자율 에이전트 기술의 현재 상태를 분석하세요.
        - 주요 기술 분류 및 정의
        - 현재 시장에서 활용되는 주요 사례
        - 선도 기업들의 개발 현황 및 투자 동향
        5-7페이지 분량으로 작성하고, 최신 데이터를 활용하세요.
        """,
        
        "trend_analysis": """
        최신 연구 트렌드를 분석하세요.
        - 학술 논문에서 나타나는 주요 연구 방향
        - 기술적 도전 과제 및 해결 방안
        - 글로벌 시장에서의 채택 동향
        5-7페이지 분량으로 작성하고, 연구 데이터를 인용하세요.
        """,
        
        "future_prediction": """
        향후 5년간 자율 에이전트 기술의 발전 방향을 예측하세요.
        - 주요 기술 혁신 및 돌파구
        - 성장이 예상되는 핵심 응용 분야
        - 기술 발전의 한계 및 극복 방안
        6-8페이지 분량으로 작성하고, 예측의 근거를 제시하세요.
        """,
        
        "industry_applications": """
        산업별 자율 에이전트 기술 적용 사례와 기회를 분석하세요.
        - 금융, 의료, 제조, 서비스 산업 등 주요 산업별 구체적 사례
        - 각 산업에서의 특수한 응용 방식과 효과
        - 산업별 도입 시 고려사항 및 성공 요인
        8-10페이지 분량으로 작성하고, 산업별 특성을 고려하세요.
        """,
        
        "strategic_recommendations": """
        기업들을 위한 실질적인 전략적 제언을 제공하세요.
        - 단기적 대응 전략 (1-2년)
        - 중장기적 준비 방향 (3-5년)
        - 리스크 관리 방안 및 우선 투자 영역
        4-5페이지 분량으로 작성하고, 기업 규모별 차별화된 전략을 제시하세요.
        """,
        
        "conclusion": """
        연구 결과의 핵심을 요약하고 향후 연구 방향을 제시하세요.
        보고서의 의의와 한계를 명시하고, 자율 에이전트 기술의 미래에 대한 전망으로 마무리하세요.
        2-3페이지 분량으로 작성하세요.
        """,
        
        "references": """
        보고서 작성에 활용된 모든 연구 논문, 기사, 보고서 등의 출처를 학술적 형식에 맞게 정리하세요.
        인용된 자료는 발행 연도 순으로 정렬하고, 2-3페이지 분량으로 작성하세요.
        """
    }
    
    # 이하 실제 보고서 생성 로직 구현
    # (실제 구현에서는 각 에이전트의 데이터를 처리하여 보고서 각 섹션을 생성)
    
    return "완성된 보고서가 생성됩니다."

# 에이전트 프롬프트 정의
AGENT_PROMPTS = {
    "research_news_agent": """
    당신은 최신 연구뉴스 추천 에이전트입니다. 자율 에이전트 기술 분야의 최신 연구 논문, 기술 뉴스, 기업 발표자료를 분석하여 중요한 기술 동향을 식별해야 합니다.
    
    다음 정보를 수집하고 분석하세요:
    1. 최근 2년간 발표된 주요 자율 에이전트 관련 연구 논문 (특히 인용 횟수가 높은 논문)
    2. 주요 기술 기업들의 자율 에이전트 관련 발표 및 투자 정보
    3. 자율 에이전트 기술 관련 주요 뉴스 및 기사
    
    결과는 다음 형식으로 구조화하세요:
    - 주요 연구 동향 요약 (500단어 이내)
    - 가장 영향력 있는 연구 논문 Top 10 목록 (제목, 저자, 발표일, 주요 내용 요약)
    - 주요 기업 활동 요약 (기업명, 발표/투자 내용, 날짜, 중요도)
    """,
    
    "tech_summary_agent": """
    당신은 핵심 기술 요약 에이전트입니다. 수집된 정보를 바탕으로 자율 에이전트 기술의 주요 요소와 발전 동향을 요약하고 분석해야 합니다.
    
    다음 작업을 수행하세요:
    1. 자율 에이전트 기술의 핵심 구성 요소 분류 및 설명
    2. 각 구성 요소별 최신 기술적 발전 요약
    3. 기술 간 상호작용 및 통합 동향 분석
    
    결과는 다음 형식으로 구조화하세요:
    - 자율 에이전트 기술 분류 체계 (카테고리, 설명, 주요 특징)
    - 핵심 기술별 발전 단계 평가 (기술명, 성숙도, 주요 혁신, 한계점)
    - 기술 간 통합 및 시너지 분석 (조합 가능한 기술, 예상 효과, 기술적 과제)
    """,
    
    "trend_prediction_agent": """
    당신은 트렌드 예측 에이전트입니다. 수집된 데이터를 기반으로 자율 에이전트 기술의 향후 5년간 발전 방향과 산업 적용 가능성을 예측해야 합니다.
    
    다음 예측을 수행하세요:
    1. 향후 5년간 자율 에이전트 기술의 주요 발전 방향 및 단계
    2. 유망한 응용 분야 및 시장 성장 예측
    3. 기술 발전의 주요 촉진 요인 및 장애 요인
    
    결과는 다음 형식으로 구조화하세요:
    - 기술 발전 로드맵 (연도별 주요 기술 발전 예상 시점)
    - 응용 분야별 성장 예측 (분야, 성장 잠재력, 주요 사용 사례)
    - 기술 채택 곡선 분석 (초기 채택자, 주류 시장 진입 시점 예측)
    """,
    
    "risk_opportunity_agent": """
    당신은 리스크 및 기회 분석 에이전트입니다. 자율 에이전트 기술의 발전이 각 산업에 미칠 영향과 기업들이 직면할 기회 및 위험 요소를 분석해야 합니다.
    
    다음 분석을 수행하세요:
    1. 주요 산업별(금융, 의료, 제조, 서비스 등) 자율 에이전트 기술 적용 영향 평가
    2. 기업 규모별(대기업, 중소기업, 스타트업) 기회 및 위험 요소 분석
    3. 윤리적, 법적, 사회적 영향 및 고려사항
    
    결과는 다음 형식으로 구조화하세요:
    - 산업별 임팩트 매트릭스 (산업, 영향 수준, 주요 기회, 주요 위험)
    - 기업 유형별 전략적 포지셔닝 분석 (기업 유형, 권장 접근법, 주의사항)
    - 리스크 관리 프레임워크 (위험 유형, 심각도, 대응 전략)
    """
}

# 에이전트별 사용 도구 정의
AGENT_TOOLS = {
    "research_news_agent": {
        "web_search": {
            "description": "학술 논문 데이터베이스, 기술 뉴스 사이트, 기업 보도자료 등에서 자율 에이전트 기술 관련 정보를 검색합니다.",
            "parameters": {
                "query": "검색 쿼리 (예: 'latest autonomous agent research papers', 'LLM agent frameworks')",
                "sources": "검색 대상 소스 (예: 'arxiv, IEEE, ACM, TechCrunch, Wired')",
                "time_range": "검색 기간 (예: 'last 2 years', 'last 6 months')"
            },
            "returns": "검색 결과 목록 (제목, URL, 발행일, 요약)"
        },
        "paper_analyzer": {
            "description": "연구 논문의 주요 내용을 분석하고 핵심 아이디어, 방법론, 결과를 추출합니다.",
            "parameters": {
                "paper_url": "논문의 URL 또는 파일 경로",
                "focus_area": "분석 시 중점을 둘 영역 (예: 'methodology', 'results', 'applications')"
            },
            "returns": "논문 분석 결과 (핵심 아이디어, 방법론, 주요 결과, 중요도 평가)"
        }
    },
    
    "tech_summary_agent": {
        "tech_classifier": {
            "description": "자율 에이전트 기술을 카테고리별로 분류하고 관련성을 평가합니다.",
            "parameters": {
                "tech_description": "기술에 대한 설명",
                "classification_framework": "분류 체계 (예: 'capability-based', 'architecture-based')"
            },
            "returns": "기술 분류 결과 (카테고리, 하위 카테고리, 관련 기술)"
        },
        "tech_maturity_analyzer": {
            "description": "기술의 성숙도와 발전 단계를 평가합니다.",
            "parameters": {
                "tech_name": "기술 이름",
                "adoption_data": "채택 데이터 (논문 수, 기업 활용 사례 등)",
                "investment_data": "투자 데이터"
            },
            "returns": "성숙도 평가 (TRL 수준, 주요 지표, 장단점 분석)"
        }
    },
    
    "trend_prediction_agent": {
        "time_series_analyzer": {
            "description": "기술 관련 시계열 데이터를 분석하여 트렌드를 식별합니다.",
            "parameters": {
                "data_series": "분석할 시계열 데이터 (논문 출판 빈도, 특허 신청 수 등)",
                "timeframe": "분석 기간 (예: '2020-2025')",
                "prediction_horizon": "예측 기간 (예: '5 years')"
            },
            "returns": "트렌드 분석 결과 (성장 패턴, 변곡점, 예측 값)"
        },
        "adoption_curve_generator": {
            "description": "기술 채택 곡선을 생성하고 미래 채택 단계를 예측합니다.",
            "parameters": {
                "tech_name": "기술 이름",
                "current_adoption_data": "현재 채택 데이터",
                "market_factors": "영향을 미치는 시장 요인"
            },
            "returns": "채택 곡선 (현재 위치, 주류 진입 예상 시점, 성장 잠재력)"
        }
    },
    
    "risk_opportunity_agent": {
        "impact_analyzer": {
            "description": "기술이 특정 산업에 미칠 영향을 평가합니다.",
            "parameters": {
                "industry": "산업 이름",
                "tech_capabilities": "기술 역량",
                "industry_factors": "산업 특성 및 요인"
            },
            "returns": "영향 분석 (긍정적/부정적 영향, 영향 규모, 시간대)"
        },
        "risk_assessment": {
            "description": "기술 도입과 관련된 리스크를 평가합니다.",
            "parameters": {
                "tech_description": "기술 설명",
                "implementation_context": "구현 맥락 (예: '대기업', '스타트업')",
                "risk_categories": "고려할 리스크 카테고리 (예: '기술적', '법적', '윤리적')"
            },
            "returns": "리스크 평가 (리스크 유형, 심각도, 가능성, 완화 전략)"
        }
    },
    
    "report_agent": {
        "content_organizer": {
            "description": "수집된 정보를 보고서 구조에 맞게 정리합니다.",
            "parameters": {
                "collected_data": "수집된 모든 데이터",
                "report_structure": "보고서 구조"
            },
            "returns": "구조화된 보고서 콘텐츠"
        },
        "visualization_generator": {
            "description": "데이터를 시각화하여 차트, 그래프 등을 생성합니다.",
            "parameters": {
                "data": "시각화할 데이터",
                "viz_type": "시각화 유형 (예: 'line chart', 'heatmap')",
                "viz_options": "시각화 옵션"
            },
            "returns": "시각화 결과 (이미지 파일 또는 코드)"
        }
    }
}