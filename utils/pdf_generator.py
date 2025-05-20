"""
PDF 생성 모듈
WeasyPrint를 사용하여 마크다운 형식의 보고서를 PDF로 변환합니다.
"""
import os
import logging
import markdown
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
from weasyprint import HTML, CSS
from config import config
from utils.logger import logger

class PDFGenerator:
    def __init__(self):
        """PDF 생성기 초기화"""
        self.logger = logger
        
        # CSS 스타일 정의
        self.css_template = """
        @font-face {
            font-family: 'NanumGothic';
            src: url('%s/NanumGothic.otf') format('opentype');
            font-weight: normal;
            font-style: normal;
        }
        
        @font-face {
            font-family: 'NanumGothic';
            src: url('%s/NanumGothicBold.otf') format('opentype');
            font-weight: bold;
            font-style: normal;
        }
        
        body {
            font-family: 'NanumGothic', sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            margin: 2cm;
        }
        
        h1 {
            font-size: 20pt;
            font-weight: bold;
            color: #000080;
            text-align: center;
            margin-top: 1cm;
            margin-bottom: 0.5cm;
        }
        
        h2 {
            font-size: 16pt;
            color: #000080;
            border-bottom: 1px solid #000080;
            margin-top: 0.8cm;
            margin-bottom: 0.3cm;
        }
        
        h3 {
            font-size: 14pt;
            color: #404040;
            margin-top: 0.6cm;
            margin-bottom: 0.2cm;
        }
        
        h4 {
            font-size: 12pt;
            color: #404040;
            margin-top: 0.4cm;
            margin-bottom: 0.1cm;
        }
        
        p {
            margin-bottom: 0.3cm;
        }
        
        ul, ol {
            margin-bottom: 0.3cm;
        }
        
        table {
            width: 100%%;
            border-collapse: collapse;
            margin-bottom: 0.5cm;
        }
        
        th {
            background-color: #f0f0f0;
            border: 1px solid #d0d0d0;
            padding: 8px;
            text-align: center;
            font-weight: bold;
        }
        
        td {
            border: 1px solid #d0d0d0;
            padding: 8px;
        }
        
        /* 목차 스타일 */
        .toc {
            margin-top: 1cm;
            margin-bottom: 1cm;
        }
        
        .toc h2 {
            text-align: center;
        }
        
        .toc ul {
            list-style-type: none;
        }
        
        .toc a {
            text-decoration: none;
            color: #000;
        }
        
        /* 첫 페이지(표지) 스타일 */
        .cover {
            text-align: center;
            margin-top: 5cm;
        }
        
        .cover h1 {
            font-size: 24pt;
        }
        
        .cover .subtitle {
            font-size: 16pt;
            margin-top: 1cm;
            margin-bottom: 3cm;
        }
        
        .cover .info {
            margin-top: 3cm;
            text-align: right;
            margin-right: 2cm;
        }
        
        /* 페이지 나누기 */
        .page-break {
            page-break-after: always;
        }
        
        /* 각주 */
        .footnote {
            font-size: 9pt;
            color: #606060;
        }
        """
        
    def generate_pdf(self, markdown_content: str, output_path: Optional[str] = None, metadata: Dict[str, Any] = None) -> str:
        """
        마크다운 형식의 보고서를 PDF로 변환
        
        Args:
            markdown_content: 마크다운 형식의 문자열
            output_path: 저장할 파일 경로 (없으면 자동 생성)
            metadata: 문서 메타데이터 (제목, 작성자 등)
            
        Returns:
            생성된 PDF 파일 경로
        """
        try:
            # 출력 경로가 없으면 자동 생성
            if output_path is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                title = metadata.get('title', 'report')
                filename = f"{title.replace(' ', '_')}_{timestamp}.pdf"
                output_path = str(config.paths.reports_dir / filename)
            
            # 메타데이터 설정
            if metadata is None:
                metadata = {}
            
            title = metadata.get('title', '기술 트렌드 분석 보고서')
            author = metadata.get('author', 'AI 기술 분석 시스템')
            date = metadata.get('date', datetime.now().strftime("%Y년 %m월 %d일"))
            subtitle = metadata.get('subtitle', '')
            
            # 표지 HTML 생성
            cover_html = self._create_cover_page(title, subtitle, author, date)
            
            # 마크다운을 HTML로 변환
            html_content = markdown.markdown(markdown_content, extensions=['tables', 'toc'])
            
            # 표지와 본문 결합
            full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
    {cover_html}
    <div class="page-break"></div>
    {html_content}
</body>
</html>
            """
            
            # CSS 생성 (폰트 경로 설정)
            font_dir = str(config.paths.fonts_dir).replace('\\', '/')
            css = self.css_template % (font_dir, font_dir)
            
            # HTML을 PDF로 변환
            HTML(string=full_html).write_pdf(
                output_path,
                stylesheets=[CSS(string=css)]
            )
            
            self.logger.info(f"PDF 생성 완료: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"PDF 생성 오류: {e}")
            raise
    
    def _create_cover_page(self, title: str, subtitle: str, author: str, date: str) -> str:
        """표지 페이지 HTML 생성"""
        logo_html = ""
        
        # 로고 이미지 추가 (있는 경우)
        logo_path = config.paths.assets_dir / 'logo.png'
        if os.path.exists(logo_path):
            logo_html = f'<div class="logo"><img src="{logo_path}" width="200"></div>'
        
        # 부제목 HTML
        subtitle_html = f'<div class="subtitle">{subtitle}</div>' if subtitle else ''
        
        # 표지 HTML
        cover_html = f"""
        <div class="cover">
            {logo_html}
            <h1>{title}</h1>
            {subtitle_html}
            <div class="info">
                <p>작성일: {date}</p>
                <p>작성자: {author}</p>
            </div>
        </div>
        """
        
        return cover_html

    def markdown_to_pdf(self, markdown_path: str, output_path: Optional[str] = None) -> str:
        """
        마크다운 파일을 PDF로 변환
        
        Args:
            markdown_path: 마크다운 파일 경로
            output_path: 저장할 PDF 파일 경로 (없으면 자동 생성)
            
        Returns:
            생성된 PDF 파일 경로
        """
        try:
            # 마크다운 파일 읽기
            with open(markdown_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
            
            # 출력 경로가 없으면 자동 생성
            if output_path is None:
                output_path = markdown_path.replace('.md', '.pdf')
            
            # 메타데이터 추출 (가능한 경우)
            metadata = {}
            lines = markdown_content.strip().split('\n')
            if lines and lines[0].startswith('# '):
                metadata['title'] = lines[0][2:].strip()
            
            # PDF 생성
            return self.generate_pdf(markdown_content, output_path, metadata)
            
        except Exception as e:
            self.logger.error(f"마크다운 PDF 변환 오류: {e}")
            raise

    def generate_html(self, markdown_content: str, output_path: str, metadata: Dict[str, Any] = None) -> str:
        """
        마크다운 형식의 보고서를 HTML로 변환
        
        Args:
            markdown_content: 마크다운 형식의 문자열
            output_path: 저장할 파일 경로
            metadata: 문서 메타데이터 (제목, 작성자 등)
            
        Returns:
            생성된 HTML 파일 경로
        """
        try:
            # 메타데이터 설정
            if metadata is None:
                metadata = {}
            
            title = metadata.get('title', '기술 트렌드 분석 보고서')
            author = metadata.get('author', 'AI 기술 분석 시스템')
            date = metadata.get('date', datetime.now().strftime("%Y년 %m월 %d일"))
            subtitle = metadata.get('subtitle', '')
            
            # 표지 HTML 생성
            cover_html = self._create_cover_page(title, subtitle, author, date)
            
            # 마크다운을 HTML로 변환
            content_html = markdown.markdown(markdown_content, extensions=['tables', 'toc'])
            
            # CSS 스타일
            css = self.css_template % ("", "")  # 폰트 경로는 HTML에서 불필요
            
            # HTML 문서 완성
            full_html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>
        {css}
    </style>
</head>
<body>
    {cover_html}
    <div class="page-break"></div>
    {content_html}
</body>
</html>
            """
            
            # HTML 파일 저장
            with open(output_path, 'w', encoding='utf-8') as html_file:
                html_file.write(full_html)
            
            self.logger.info(f"HTML 생성 완료: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"HTML 생성 오류: {e}")
            raise
