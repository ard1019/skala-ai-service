# analysis/network_analysis.py
import logging
from typing import List, Dict, Any
import networkx as nx
import community
from utils.logger import logger
from utils.exceptions import ValidationError

class NetworkAnalyzer:
    def __init__(self) -> None:
        self.logger = logger

    def analyze_collaboration_network(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """협력 네트워크 분석"""
        try:
            # 논문 저자 네트워크 생성
            author_network = self._create_author_network(data.get("papers", []))
            
            # 특허 발명자 네트워크 생성
            inventor_network = self._create_inventor_network(data.get("patents", []))
            
            # 기업 협력 네트워크 생성
            company_network = self._create_company_network(data.get("investments", []))

            return {
                "author_network": self._analyze_network(author_network),
                "inventor_network": self._analyze_network(inventor_network),
                "company_network": self._analyze_network(company_network),
                "integrated_analysis": self._integrate_network_analysis(
                    author_network, inventor_network, company_network
                )
            }

        except Exception as e:
            logger.error(f"Error in collaboration network analysis: {e}")
            raise

    def _create_author_network(self, papers: List[Dict[str, Any]]) -> nx.Graph:
        """논문 저자 네트워크 생성"""
        try:
            G = nx.Graph()
            for paper in papers:
                authors = paper.get("authors", [])
                for i in range(len(authors)):
                    for j in range(i + 1, len(authors)):
                        if not G.has_edge(authors[i], authors[j]):
                            G.add_edge(authors[i], authors[j], weight=1)
                        else:
                            G[authors[i]][authors[j]]["weight"] += 1
            return G

        except Exception as e:
            logger.error(f"Error in author network creation: {e}")
            raise

    def _create_inventor_network(self, patents: List[Dict[str, Any]]) -> nx.Graph:
        """특허 발명자 네트워크 생성"""
        try:
            G = nx.Graph()
            for patent in patents:
                inventors = patent.get("inventors", [])
                # 발명자 간 연결 생성
                for i in range(len(inventors)):
                    for j in range(i + 1, len(inventors)):
                        if not G.has_edge(inventors[i], inventors[j]):
                            G.add_edge(inventors[i], inventors[j], weight=1)
                        else:
                            G[inventors[i]][inventors[j]]["weight"] += 1
            return G

        except Exception as e:
            logger.error(f"Error in inventor network creation: {e}")
            return nx.Graph()

    def _create_company_network(self, investments: List[Dict[str, Any]]) -> nx.Graph:
        """기업 협력 네트워크 생성"""
        try:
            G = nx.Graph()
            for investment in investments:
                company = investment.get("company")
                investors = investment.get("investors", [])
                # 기업-투자자 간 연결 생성
                for investor in investors:
                    if not G.has_edge(company, investor):
                        G.add_edge(company, investor, weight=1)
                    else:
                        G[company][investor]["weight"] += 1
            return G

        except Exception as e:
            logger.error(f"Error in company network creation: {e}")
            return nx.Graph()

    def _analyze_network(self, G: nx.Graph) -> Dict[str, Any]:
        """네트워크 분석 수행"""
        if G.number_of_nodes() == 0:
            return {}

        try:
            # 중심성 분석
            degree_centrality = nx.degree_centrality(G)
            betweenness_centrality = nx.betweenness_centrality(G)
            
            # 커뮤니티 탐지
            communities = community.best_partition(G)
            
            # 핵심 노드 식별
            top_nodes = sorted(
                degree_centrality.items(), 
                key=lambda x: x[1], 
                reverse=True
            )[:10]

            return {
                "network_stats": {
                    "num_nodes": G.number_of_nodes(),
                    "num_edges": G.number_of_edges(),
                    "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
                    "density": nx.density(G)
                },
                "centrality": {
                    "degree": degree_centrality,
                    "betweenness": betweenness_centrality
                },
                "communities": communities,
                "top_nodes": top_nodes
            }

        except Exception as e:
            logger.error(f"Error in network analysis: {e}")
            raise

    def _integrate_network_analysis(self, 
                                  author_network: nx.Graph, 
                                  inventor_network: nx.Graph,
                                  company_network: nx.Graph) -> Dict[str, Any]:
        """네트워크 분석 결과 통합"""
        try:
            return {
                "collaboration_patterns": {
                    "research": self._analyze_collaboration_patterns(author_network),
                    "innovation": self._analyze_collaboration_patterns(inventor_network),
                    "business": self._analyze_collaboration_patterns(company_network)
                },
                "key_players": {
                    "research": self._identify_key_players(author_network),
                    "innovation": self._identify_key_players(inventor_network),
                    "business": self._identify_key_players(company_network)
                }
            }

        except Exception as e:
            logger.error(f"Error in network analysis integration: {e}")
            return {}