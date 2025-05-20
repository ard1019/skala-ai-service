# 미래 기술 트렌드 분석: 인공지능 기반 자율 에이전트 기술의 향후 5년 발전 전망

AI 기반 자율 에이전트 기술의 현황을 분석하고 향후 5년간의 발전 방향을 예측하는 종합 보고서 생성 시스템입니다.

## 개요

- **목표**: 인공지능 기반 자율 에이전트 기술의 최신 동향을 분석하고, 향후 5년간의 기술 발전 방향을 예측하여 기업들에게 전략적 인사이트 제공
- **방법론**: 연구 논문 분석, 산업 동향 조사, 기술 트렌드 예측, 리스크 평가
- **도구**: LangChain, OpenAI API, Python, WeasyPrint(PDF 생성)

## 주요 기능

- **연구 데이터 분석**: 최신 자율 에이전트 기술 연구 논문, 특허, 뉴스 종합 분석
- **기업 동향 파악**: 주요 기업들의 자율 에이전트 관련 투자 및 개발 방향 통합 분석
- **산업 영향 평가**: 산업별 자율 에이전트 기술 적용 사례 및 영향력 평가
- **미래 전망 제시**: 향후 5년간 자율 에이전트 기술 발전 예측 모델 제시
- **통합 보고서 생성**: PDF, HTML, 마크다운 형식의 상세 보고서 자동 생성

## 🛠 기술 스택

| 영역 | 기술 |
|-------------|--------------------------------------|
| 프레임워크 | LangChain, Python |
| AI 모델 | GPT-4o via OpenAI API |
| 데이터 분석 | Pandas, NumPy, Matplotlib |
| 시각화 | Plotly |
| 보고서 생성 | WeasyPrint, Markdown |

## 에이전트 구조

시스템은 다음과 같은 특화된 AI 에이전트로 구성되어 있습니다:

- **연구 에이전트**: 최신 연구 논문, 기술 뉴스, 특허, 기업 발표자료 분석
- **요약 에이전트**: 수집된 정보를 바탕으로 주요 기술 트렌드 요약
- **예측 에이전트**: 기존 트렌드의 발전 방향 및 산업 적용 가능성 예측
- **리스크 분석 에이전트**: 트렌드에 따른 산업별 기회와 위험 분석
- **보고서 작성 에이전트**: 최종 보고서 작성 및 PDF/HTML 생성

## 분석 파이프라인

프로젝트는 다음 단계로 진행됩니다:

1. **데이터 수집**: 자율 에이전트 관련 연구 논문, 뉴스, 특허, 기업 투자 정보 수집
2. **데이터 분석**: 텍스트 분석, 트렌드 분석, 기업 활동 분석
3. **인사이트 도출**: 기술 발전 예측, 산업 영향 분석, 기회 및 위험 평가, 전략 제안
4. **보고서 생성**: 정의된 구조에 따라 최종 분석 보고서 작성 및 PDF/HTML 생성

## 디렉토리 구조
skala-ai-service/
├── agents/ # 에이전트 구현 코드
│ ├── base_agent.py # 기본 에이전트 클래스
│ ├── research_agent.py # 연구 분석 에이전트
│ ├── summary_agent.py # 핵심 기술 요약 에이전트
│ ├── prediction_agent.py # 트렌드 예측 에이전트
│ ├── risk_agent.py # 리스크 분석 에이전트
│ └── report_agent.py # 보고서 작성 에이전트
│
├── data/ # 수집 및 분석 데이터
│ ├── papers/ # 연구 논문 데이터
│ ├── news/ # 기술 뉴스 데이터
│ ├── patents/ # 특허 데이터
│ └── investments/ # 투자 동향 데이터
│
├── prompts/ # 에이전트 프롬프트
│ ├── research_prompt.txt # 연구 분석 프롬프트
│ ├── summary_prompt.txt # 요약 프롬프트
│ ├── prediction_prompt.txt # 예측 프롬프트
│ ├── risk_prompt.txt # 리스크 분석 프롬프트
│ └── report_prompt.txt # 보고서 생성 프롬프트
│
├── assets/ # 정적 자산
│ └── fonts/ # 폰트 파일(한글 지원)
│
├── utils/ # 유틸리티 클래스 및 함수
│ ├── logger.py # 로깅 유틸리티
│ ├── decorators.py # 데코레이터 함수
│ ├── exceptions.py # 커스텀 예외 클래스
│ └── pdf_generator.py # PDF/HTML 생성기
│
├── outputs/ # 생성된 보고서
│ ├── figures/ # 차트 및 그래프
│ └── reports/ # 최종 보고서(MD/PDF/HTML)
│
├── app.py # 메인 애플리케이션
├── config.py # 설정 파일
├── requirements.txt # 의존성 패키지 목록
└── README.md # 프로젝트 설명서


## 설치 및 실행

### 요구사항

- Python 3.10 이상
- OpenAI API 키
- WeasyPrint 관련 시스템 의존성(Windows의 경우 GTK3)

### 설치

```bash
# 저장소 클론
git clone https://github.com/ard1019/skala-ai-service.git
cd skala-ai-service

# 의존성 설치
pip install -r requirements.txt

# 환경 설정
cp .env.example .env
# .env 파일에 OpenAI API 키 입력
```

### 실행

```bash
python app.py
```

## 결과물

- **마크다운 보고서**: 상세한 기술 트렌드 분석 보고서(markdown)
- **PDF 문서**: 한글 폰트가 적용된 고품질 보고서(인쇄 및 공유용)
- **HTML 문서**: 웹 브라우저에서 볼 수 있는 인터랙티브 보고서

## 기여자

- 전성현: 프로젝트 설계, 데이터 분석, 에이전트 개발, 보고서 작성
