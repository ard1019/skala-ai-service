# analysis/visualization.py
import logging
from typing import Dict, Any, List
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import plotly.graph_objects as go
from wordcloud import WordCloud
from pathlib import Path
import matplotlib.font_manager as fm
from utils.logger import logger
from utils.exceptions import VisualizationError
from config import config

class Visualizer:
    def __init__(self) -> None:
        self._setup_visualization_env()
        
    def _setup_visualization_env(self) -> None:
        """시각화 환경 설정"""
        try:
            # 한글 폰트 설정
            font_paths = [
                'C:/Windows/Fonts/malgun.ttf',  # Windows
                '/usr/share/fonts/truetype/nanum/NanumGothic.ttf',  # Linux
                '/System/Library/Fonts/AppleGothic.ttf'  # MacOS
            ]
            
            font_set = False
            for font_path in font_paths:
                if Path(font_path).exists():
                    fm.fontManager.addfont(font_path)
                    plt.rc('font', family=Path(font_path).stem)
                    font_set = True
                    break
                
            if not font_set:
                self.logger.warning("No suitable Korean font found. Using default font.")
            
            # 시각화 스타일 설정
            plt.style.use('seaborn')
            sns.set_palette("husl")
            
            # 출력 디렉토리 생성
            config.paths.figures_dir.mkdir(parents=True, exist_ok=True)
            
        except Exception as e:
            logger.error(f"Error setting up visualization environment: {e}")
            raise VisualizationError(f"Failed to setup visualization environment: {e}")

    def create_trend_visualizations(self, trend_data: Dict[str, Any]) -> Dict[str, str]:
        """트렌드 시각화 생성"""
        try:
            visualizations = {}
            
            # 시계열 트렌드 그래프
            timeline_path = self._create_timeline_plot(trend_data)
            visualizations["timeline"] = str(timeline_path)
            
            # 키워드 워드클라우드
            wordcloud_path = self._create_wordcloud(trend_data)
            visualizations["wordcloud"] = str(wordcloud_path)
            
            # 기술 성숙도 레이더 차트
            radar_path = self._create_radar_chart(trend_data)
            visualizations["radar"] = str(radar_path)

            return visualizations

        except Exception as e:
            logger.error(f"Error in trend visualization: {e}")
            raise VisualizationError(f"Failed to create trend visualizations: {e}")

    def create_network_visualizations(self, network_data: Dict[str, Any]) -> Dict[str, str]:
        """네트워크 시각화 생성"""
        try:
            visualizations = {}
            
            # 협력 네트워크 그래프
            network_path = self._create_network_graph(network_data)
            visualizations["network"] = network_path
            
            # 커뮤니티 분포 차트
            community_path = self._create_community_chart(network_data)
            visualizations["community"] = community_path

            return visualizations

        except Exception as e:
            logger.error(f"Error in network visualization: {e}")
            return {}

    def _create_timeline_plot(self, data: Dict[str, Any]) -> Path:
        """시계열 트렌드 그래프 생성"""
        try:
            fig, ax = plt.subplots(figsize=(12, 6))
            
            years = list(data.get("yearly_counts", {}).keys())
            counts = list(data.get("yearly_counts", {}).values())
            
            ax.plot(years, counts, marker='o')
            ax.set_xlabel('연도')
            ax.set_ylabel('건수')
            ax.set_title('기술 트렌드 타임라인')
            
            filepath = config.paths.figures_dir / "timeline_trend.png"
            plt.savefig(filepath, dpi=300, bbox_inches='tight')
            plt.close()
            
            return filepath

        except Exception as e:
            logger.error(f"Error creating timeline plot: {e}")
            raise VisualizationError(f"Failed to create timeline plot: {e}")

    def _create_wordcloud(self, data: Dict[str, Any]) -> Path:
        """워드클라우드 생성"""
        try:
            # 키워드 빈도수 데이터 준비
            word_freq = {
                item["keyword"]: item["frequency"] 
                for item in data.get("keywords", [])
            }
            
            # 워드클라우드 생성
            wordcloud = WordCloud(
                width=800, 
                height=400,
                background_color='white'
            ).generate_from_frequencies(word_freq)
            
            # 이미지 저장
            filepath = config.paths.figures_dir / "keyword_cloud.png"
            wordcloud.to_file(filepath)
            
            return filepath

        except Exception as e:
            logger.error(f"Error in wordcloud creation: {e}")
            raise VisualizationError(f"Failed to create wordcloud: {e}")

    def _create_radar_chart(self, data: Dict[str, Any]) -> Path:
        """기술 성숙도 레이더 차트 생성"""
        try:
            # 레이더 차트 데이터 준비
            categories = ['Research', 'Patents', 'Market', 'Investment', 'Implementation']
            values = [
                data.get("research_score", 0),
                data.get("patent_score", 0),
                data.get("market_score", 0),
                data.get("investment_score", 0),
                data.get("implementation_score", 0)
            ]
            
            # Plotly를 사용한 레이더 차트 생성
            fig = go.Figure(data=go.Scatterpolar(
                r=values,
                theta=categories,
                fill='toself'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 1]
                    )),
                showlegend=False
            )
            
            # 차트 저장
            filepath = config.paths.figures_dir / "maturity_radar.html"
            fig.write_html(filepath)
            
            return filepath

        except Exception as e:
            logger.error(f"Error in radar chart creation: {e}")
            raise VisualizationError(f"Failed to create radar chart: {e}")

    def _create_network_graph(self, network_data: Dict[str, Any]) -> str:
        """네트워크 그래프 시각화 생성"""
        try:
            G = network_data.get("graph", nx.Graph())
            
            # 그래프 레이아웃 계산
            pos = nx.spring_layout(G)
            
            # 노드 크기 계산 (중심성 기반)
            node_size = [
                v * 3000 for v in network_data.get("centrality", {}).values()
            ]
            
            # 그래프 그리기
            plt.figure(figsize=(12, 8))
            nx.draw_networkx(
                G,
                pos=pos,
                node_size=node_size,
                node_color='lightblue',
                edge_color='gray',
                with_labels=True,
                font_size=8
            )
            
            # 그래프 저장
            filepath = f"{config.paths.figures_dir}/collaboration_network.png"
            plt.savefig(filepath)
            plt.close()
            
            return filepath

        except Exception as e:
            logger.error(f"Error in network graph creation: {e}")
            return ""

    def _create_community_chart(self, network_data: Dict[str, Any]) -> str:
        """커뮤니티 분포 차트 생성"""
        try:
            communities = network_data.get("communities", {})
            
            # 커뮤니티 크기 계산
            community_sizes = {}
            for node, community_id in communities.items():
                if community_id not in community_sizes:
                    community_sizes[community_id] = 0
                community_sizes[community_id] += 1
            
            # 막대 그래프 생성
            plt.figure(figsize=(10, 6))
            plt.bar(
                range(len(community_sizes)),
                list(community_sizes.values())
            )
            plt.xlabel('Community ID')
            plt.ylabel('Number of Nodes')
            plt.title('Community Size Distribution')
            
            # 차트 저장
            filepath = f"{config.paths.figures_dir}/community_distribution.png"
            plt.savefig(filepath)
            plt.close()
            
            return filepath

        except Exception as e:
            logger.error(f"Error in community chart creation: {e}")
            return ""