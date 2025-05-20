import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from pathlib import Path
from utils.logger import logger
from utils.decorators import log_execution_time, retry, validate_input
from utils.exceptions import DataCollectionError, StorageError
from config import config
import re  # 정규식 모듈 추가

class DataCollector:
    def __init__(self):
        self.llm = ChatOpenAI(
            model_name=config.openai.model_name,
            temperature=config.openai.temperature,
            max_tokens=config.openai.max_tokens
        )
        self.logger = logging.getLogger(__name__)
        
        # 데이터 저장 디렉토리 생성
        self.data_dirs = {
            'papers': 'data/papers',
            'news': 'data/news',
            'patents': 'data/patents',
            'investments': 'data/investments',
            'analysis': 'data/analysis'
        }
        self._create_directories()
        
        # 프롬프트 로드
        self.prompts = self._load_prompts()

    def _create_directories(self):
        """데이터 저장을 위한 디렉토리 생성"""
        for dir_path in self.data_dirs.values():
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                self.logger.info(f"Created directory: {dir_path}")

    @log_execution_time
    def _load_prompts(self) -> Dict[str, str]:
        """프롬프트 파일들을 로드"""
        prompt_files = [
            'research_prompt.txt',
            'summary_prompt.txt',
            'prediction_prompt.txt',
            'risk_prompt.txt',
            'report_prompt.txt'
        ]
        prompts = {}
        for file in prompt_files:
            try:
                file_path = config.paths.prompts_dir / file
                with open(file_path, 'r', encoding='utf-8') as f:
                    prompts[file] = f.read()
                logger.info(f"Loaded prompt: {file}")
            except Exception as e:
                logger.error(f"Error loading prompt {file}: {e}")
                raise DataCollectionError(f"Failed to load prompt {file}: {e}")
        return prompts

    @log_execution_time
    @validate_input
    @retry(max_attempts=3)
    def collect_research_data(self, query: str) -> Dict[str, Any]:
        """연구 데이터 수집 및 분석"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # 영어로 된 주제가 더 정확한 데이터를 얻을 수 있음
            english_query = self._translate_query_if_needed(query)
            
            # 모든 데이터를 한 번에 수집 (실패 확률 감소)
            complete_data = self._collect_complete_data(english_query)
            
            if complete_data:
                self.logger.info("Successfully collected complete data in a single API call")
                papers = complete_data.get("papers", [])
                news = complete_data.get("news", [])
                patents = complete_data.get("patents", [])
                investments = complete_data.get("investments", [])
                tech_categories = complete_data.get("tech_categories", [])
            else:
                # 실패한 경우 개별 수집 시도 (백업 방법)
                self.logger.warning("Complete data collection failed, trying individual collection")
                papers = self._collect_papers(english_query)
                news = self._collect_news(english_query)
                patents = self._collect_patents(english_query)
                investments = self._collect_investments(english_query)
                tech_categories = []
            
            # 데이터 수집 결과 수집
            research_data = {
                "query": query,
                "english_query": english_query,
                "timestamp": timestamp,
                "papers": papers,
                "news": news,
                "patents": patents,
                "investments": investments,
                "tech_categories": tech_categories
            }
            
            # 수집된 데이터 저장
            self._save_research_data(research_data, query, timestamp)
            
            # 데이터 품질 메트릭 계산
            quality_metrics = self._calculate_quality_metrics(research_data)
            research_data["quality_metrics"] = quality_metrics
            
            return research_data
            
        except Exception as e:
            logger.error(f"Error in research data collection: {e}")
            raise DataCollectionError(f"Failed to collect research data: {e}")
    
    def _translate_query_if_needed(self, query: str) -> str:
        """한글 쿼리를 영어로 변환 (필요한 경우)"""
        # 간단한 규칙 기반 번역 (실제 프로덕션에서는 번역 API 사용 권장)
        translations = {
            "인공지능 기반 자율 에이전트 기술": "AI-based Autonomous Agent Technology",
            "자율 에이전트": "Autonomous Agents",
            "인공지능": "Artificial Intelligence",
            "기계학습": "Machine Learning",
            "딥러닝": "Deep Learning",
            "강화학습": "Reinforcement Learning"
        }
        
        # 한글 포함 여부 확인
        contains_korean = any(ord(char) > 127 for char in query)
        
        if contains_korean:
            # 정확한 번역이 있는지 확인
            if query in translations:
                return translations[query]
            
            # 부분 일치 확인
            for kr, en in translations.items():
                if kr in query:
                    return en
            
            # 직접 번역 요청 (기본적인 구현)
            try:
                prompt = ChatPromptTemplate.from_template(
                    "Translate the following Korean text to English, keeping technical terms accurate:\n\n{text}"
                )
                response = self.llm.invoke(prompt.format(text=query))
                translated = response.content.strip()
                
                # 번역 결과가 있고 모두 ASCII 문자인지 확인
                if translated and all(ord(char) < 128 for char in translated):
                    return translated
            except Exception as e:
                self.logger.warning(f"Translation failed: {e}")
        
        # 번역이 불필요하거나 실패한 경우 원본 반환
        return query

    @retry(max_attempts=3)
    def _collect_complete_data(self, query: str) -> Dict[str, Any]:
        """모든 데이터를 한 번에 수집 (효율성 및 일관성 향상)"""
        try:
            prompt = ChatPromptTemplate.from_template(self.prompts['research_prompt.txt'])
            response = self.llm.invoke(prompt.format(query=query))
            
            # 응답 텍스트에서 JSON 부분 추출 (개선된 메서드 사용)
            json_text = self._extract_json_improved(response.content)
            
            if json_text:
                try:
                    data = json.loads(json_text)
                    
                    # JSON 구조 유효성 검사
                    required_fields = ["papers", "news", "patents", "investments"]
                    if isinstance(data, dict) and all(field in data for field in required_fields):
                        return data
                    else:
                        self.logger.warning("Incomplete JSON structure received")
                        return {}
                except json.JSONDecodeError as e:
                    self.logger.error(f"JSON decode error: {e}")
                    return {}
            else:
                self.logger.warning("No valid JSON found in complete response")
                return {}
        except Exception as e:
            self.logger.error(f"Error collecting complete data: {e}")
            return {}

    @retry(max_attempts=3)
    def _collect_papers(self, query: str) -> List[Dict[str, Any]]:
        """학술 논문 데이터 수집"""
        try:
            # 더 명확한 지시로 프롬프트 업데이트
            papers_prompt = f"""Generate research paper data about {query}.
            Return ONLY a JSON array of paper objects with these fields: title, authors, publication_date, key_findings, impact_score, citations, methodology, future_implications.
            Example: [{{ "title": "Paper Title", "authors": ["Author1"], ... }}]
            Do NOT include any explanations or markdown, ONLY the JSON array."""
            
            response = self.llm.invoke(papers_prompt)
            
            # 응답 텍스트에서 JSON 부분 추출 (개선된 메서드 사용)
            json_text = self._extract_json_improved(response.content)
            
            if json_text:
                try:
                    data = json.loads(json_text)
                    # 응답이 배열인지 확인
                    if isinstance(data, list):
                        return data
                    # 응답이 객체이고 papers 필드를 포함하는지 확인
                    elif isinstance(data, dict) and "papers" in data and isinstance(data["papers"], list):
                        return data["papers"]
                    else:
                        self.logger.warning("Unexpected papers data structure")
                        return []
                except json.JSONDecodeError as e:
                    self.logger.error(f"Papers JSON decode error: {e}")
                    return []
            else:
                self.logger.warning("No valid JSON found in papers response")
                return []
        except Exception as e:
            self.logger.error(f"Error collecting papers: {e}")
            return []
    
    def _collect_news(self, query: str) -> List[Dict[str, Any]]:
        """뉴스 데이터 수집"""
        try:
            # 더 명확한 지시로 프롬프트 업데이트
            news_prompt = f"""Generate recent news data about {query}.
            Return ONLY a JSON array of news objects with these fields: title, source, date, key_points, market_impact, companies_mentioned.
            Example: [{{ "title": "News Title", "source": "Source", ... }}]
            Do NOT include any explanations or markdown, ONLY the JSON array."""
            
            response = self.llm.invoke(news_prompt)
            
            # 응답 텍스트에서 JSON 부분 추출 (개선된 메서드 사용)
            json_text = self._extract_json_improved(response.content)
            
            if json_text:
                try:
                    data = json.loads(json_text)
                    # 응답이 배열인지 확인
                    if isinstance(data, list):
                        return data
                    # 응답이 객체이고 news 필드를 포함하는지 확인
                    elif isinstance(data, dict) and "news" in data and isinstance(data["news"], list):
                        return data["news"]
                    else:
                        self.logger.warning("Unexpected news data structure")
                        return []
                except json.JSONDecodeError as e:
                    self.logger.error(f"News JSON decode error: {e}")
                    return []
            else:
                self.logger.warning("No valid JSON found in news response")
                return []
        except Exception as e:
            self.logger.error(f"Error collecting news: {e}")
            return []
    
    def _collect_patents(self, query: str) -> List[Dict[str, Any]]:
        """특허 데이터 수집"""
        try:
            # 더 명확한 지시로 프롬프트 업데이트
            patents_prompt = f"""Generate patent data about {query}.
            Return ONLY a JSON array of patent objects with these fields: title, inventors, filing_date, company, key_innovations, potential_applications.
            Example: [{{ "title": "Patent Title", "inventors": ["Inventor1"], ... }}]
            Do NOT include any explanations or markdown, ONLY the JSON array."""
            
            response = self.llm.invoke(patents_prompt)
            
            # 응답 텍스트에서 JSON 부분 추출 (개선된 메서드 사용)
            json_text = self._extract_json_improved(response.content)
            
            if json_text:
                try:
                    data = json.loads(json_text)
                    # 응답이 배열인지 확인
                    if isinstance(data, list):
                        return data
                    # 응답이 객체이고 patents 필드를 포함하는지 확인
                    elif isinstance(data, dict) and "patents" in data and isinstance(data["patents"], list):
                        return data["patents"]
                    else:
                        self.logger.warning("Unexpected patents data structure")
                        return []
                except json.JSONDecodeError as e:
                    self.logger.error(f"Patents JSON decode error: {e}")
                    return []
            else:
                self.logger.warning("No valid JSON found in patents response")
                return []
        except Exception as e:
            self.logger.error(f"Error collecting patents: {e}")
            return []
    
    def _collect_investments(self, query: str) -> List[Dict[str, Any]]:
        """투자 데이터 수집"""
        try:
            # 더 명확한 지시로 프롬프트 업데이트
            investments_prompt = f"""Generate investment data related to {query}.
            Return ONLY a JSON array of investment objects with these fields: company, funding_amount, date, investors, technology_focus, market_potential.
            Example: [{{ "company": "Company Name", "funding_amount": "Amount", ... }}]
            Do NOT include any explanations or markdown, ONLY the JSON array."""
            
            response = self.llm.invoke(investments_prompt)
            
            # 응답 텍스트에서 JSON 부분 추출 (개선된 메서드 사용)
            json_text = self._extract_json_improved(response.content)
            
            if json_text:
                try:
                    data = json.loads(json_text)
                    # 응답이 배열인지 확인
                    if isinstance(data, list):
                        return data
                    # 응답이 객체이고 investments 필드를 포함하는지 확인
                    elif isinstance(data, dict) and "investments" in data and isinstance(data["investments"], list):
                        return data["investments"]
                    else:
                        self.logger.warning("Unexpected investments data structure")
                        return []
                except json.JSONDecodeError as e:
                    self.logger.error(f"Investments JSON decode error: {e}")
                    return []
            else:
                self.logger.warning("No valid JSON found in investments response")
                return []
        except Exception as e:
            self.logger.error(f"Error collecting investments: {e}")
            return []
    
    def _extract_json_improved(self, text: str) -> Optional[str]:
        """응답 텍스트에서 JSON 부분 추출 (향상된 버전)"""
        try:
            # 1. 코드 블록 내부의 JSON 찾기 (가장 신뢰할 수 있는 방법)
            code_block_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
            code_blocks = re.findall(code_block_pattern, text)
            
            # 코드 블록 내에서 유효한 JSON 찾기
            for block in code_blocks:
                try:
                    # 유효성 검사를 위한 간단한 로드 시도
                    json.loads(block.strip())
                    return block.strip()
                except:
                    continue
            
            # 2. 중괄호로 완전히a 감싸진 JSON 객체 찾기
            json_pattern = r'(\{[\s\S]*\})'
            json_matches = re.findall(json_pattern, text)
            
            for match in json_matches:
                try:
                    # 유효성 검사를 위한 간단한 로드 시도
                    json.loads(match)
                    return match
                except:
                    continue
            
            # 3. 대괄호로 완전히 감싸진 JSON 배열 찾기
            array_pattern = r'(\[[\s\S]*\])'
            array_matches = re.findall(array_pattern, text)
            
            for match in array_matches:
                try:
                    # 유효성 검사를 위한 간단한 로드 시도
                    json.loads(match)
                    return match
                except:
                    continue
            
            # 4. 마지막 시도: 가장 바깥쪽 중괄호만 추출
            outer_json_match = re.search(r'\{(?:[^{}]|(?:\{(?:[^{}]|(?:\{[^{}]*\}))*\}))*\}', text)
            if outer_json_match:
                try:
                    json_str = outer_json_match.group(0)
                    # 유효성 검사
                    json.loads(json_str)
                    return json_str
                except:
                    pass
            
            # 5. 마지막 시도: 가장 바깥쪽 대괄호만 추출
            outer_array_match = re.search(r'\[(?:[^\[\]]|(?:\[(?:[^\[\]]|(?:\[[^\[\]]*\]))*\]))*\]', text)
            if outer_array_match:
                try:
                    array_str = outer_array_match.group(0)
                    # 유효성 검사
                    json.loads(array_str)
                    return array_str
                except:
                    pass
                    
            # JSON을 찾지 못함
            return None
            
        except Exception as e:
            self.logger.error(f"Error extracting JSON: {e}")
            return None

    def _calculate_quality_metrics(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """수집된 데이터의 품질 메트릭 계산"""
        metrics = {
            "research_coverage": {},
            "analysis_completeness": {}
        }
        
        # 연구 범위 메트릭
        papers_count = len(data.get("papers", []))
        news_count = len(data.get("news", []))
        patents_count = len(data.get("patents", []))
        investments_count = len(data.get("investments", []))
        
        # 최소 항목 수
        min_count = 3
        data_freshness = "high" if (papers_count >= min_count and news_count >= min_count) else "medium" if (papers_count + news_count >= min_count) else "low"
        
        # 모든 회사 및 기관 수집
        companies = set()
        
        # 뉴스에서 언급된 회사
        for news in data.get("news", []):
            companies_mentioned = news.get("companies_mentioned", [])
            if isinstance(companies_mentioned, list):
                companies.update(companies_mentioned)
        
        # 특허에서 언급된 회사
        for patent in data.get("patents", []):
            company = patent.get("company", "")
            if company:
                companies.add(company)
        
        # 투자 데이터에서 언급된 회사
        for investment in data.get("investments", []):
            company = investment.get("company", "")
            if company:
                companies.add(company)
            
            investors = investment.get("investors", [])
            if isinstance(investors, list):
                companies.update(investors)
        
        # 소스 다양성 계산
        source_diversity = {}
        
        # 논문 출처
        papers_sources = {}
        for paper in data.get("papers", []):
            authors = paper.get("authors", [])
            if isinstance(authors, list) and authors:
                source = authors[0]  # 첫 번째 저자 기준
                papers_sources[source] = papers_sources.get(source, 0) + 1
        
        # 뉴스 출처
        news_sources = {}
        for news in data.get("news", []):
            source = news.get("source", "unknown")
            if source:
                news_sources[source] = news_sources.get(source, 0) + 1
        
        # 출처 다양성 종합
        if papers_sources or news_sources:
            source_diversity = {**papers_sources, **news_sources}
        else:
            source_diversity = {"unknown": 1}
        
        # 연구 범위 종합
        metrics["research_coverage"] = {
            "total_papers": papers_count,
            "total_news": news_count,
            "total_patents": patents_count,
            "total_investments": investments_count,
            "total_companies": len(companies),
            "data_freshness": data_freshness,
            "source_diversity": source_diversity
        }
        
        # 분석 완성도 메트릭
        tech_categories_count = len(data.get("tech_categories", []))
        
        # 트렌드 예측 및 리스크 요소는 다음 단계에서 생성되므로 0으로 설정
        metrics["analysis_completeness"] = {
            "tech_categories": tech_categories_count,
            "trend_predictions": 0,  # 다음 단계에서 생성됨
            "risk_factors": 0        # 다음 단계에서 생성됨
        }
        
        return metrics

    def _save_research_data(self, data: Dict[str, Any], query: str, timestamp: str) -> None:
        """수집된 데이터 저장"""
        try:
            filename = f"{query.replace(' ', '_')}_{timestamp}.json"
            save_path = config.paths.data_dir / filename
            
            with open(save_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Saved research data to {save_path}")
        except Exception as e:
            logger.error(f"Error saving research data: {e}")
            raise StorageError(f"Failed to save research data: {e}")
