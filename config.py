import os
from typing import Dict, Any
from pathlib import Path
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# 프로젝트 루트 디렉토리
ROOT_DIR = Path(__file__).parent.absolute()

class OpenAIConfig(BaseModel):
    """OpenAI 설정"""
    api_key: str = Field(default=os.getenv("OPENAI_API_KEY"))
    model_name: str = Field(default="gpt-4")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=2000)

class PathConfig(BaseModel):
    """경로 설정"""
    data_dir: Path = Field(default=ROOT_DIR / "data")
    prompts_dir: Path = Field(default=ROOT_DIR / "prompts")
    outputs_dir: Path = Field(default=ROOT_DIR / "outputs")
    figures_dir: Path = Field(default=ROOT_DIR / "outputs" / "figures")
    reports_dir: Path = Field(default=ROOT_DIR / "outputs" / "reports")
    assets_dir: Path = Field(default=ROOT_DIR / "assets")
    fonts_dir: Path = Field(default=ROOT_DIR / "assets" / "fonts")

    def __init__(self, **data):
        super().__init__(**data)
        self.data_dir = Path(str(self.data_dir)).resolve()
        self.prompts_dir = Path(str(self.prompts_dir)).resolve()
        self.outputs_dir = Path(str(self.outputs_dir)).resolve()
        self.figures_dir = Path(str(self.figures_dir)).resolve()
        self.reports_dir = Path(str(self.reports_dir)).resolve()
        self.assets_dir = Path(str(self.assets_dir)).resolve()
        self.fonts_dir = Path(str(self.fonts_dir)).resolve()

class LogConfig(BaseModel):
    """로깅 설정"""
    level: str = Field(default="INFO")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    date_format: str = Field(default="%Y-%m-%d %H:%M:%S")
    file_path: Path = Field(default=ROOT_DIR / "logs" / "app.log")

class AppConfig(BaseModel):
    """애플리케이션 설정"""
    auto_open_report: bool = Field(default=True)  # 보고서를 브라우저에서 자동으로 열지 여부
    report_length_multiplier: float = Field(default=2.0)  # 보고서 길이 배수
    enhance_references: bool = Field(default=True)  # 참고문헌 강화 여부
    include_charts: bool = Field(default=False)  # 차트 포함 여부 (향후 확장)

class Config(BaseModel):
    """전체 설정"""
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    logging: LogConfig = Field(default_factory=LogConfig)
    app: AppConfig = Field(default_factory=AppConfig)
    
    class Config:
        arbitrary_types_allowed = True

    def validate_environment(self) -> None:
        """환경 설정 검증"""
        if not self.openai.api_key:
            raise ValueError("OpenAI API key is not set in environment variables")
        
        # 필요한 디렉토리 생성
        for path in [
            self.paths.data_dir,
            self.paths.outputs_dir,
            self.paths.figures_dir,
            self.paths.reports_dir,
            self.paths.prompts_dir,
            self.paths.assets_dir,
            self.paths.fonts_dir,
            self.logging.file_path.parent
        ]:
            path.mkdir(parents=True, exist_ok=True)

# 전역 설정 객체 생성
config = Config()

# 환경 검증
try:
    config.validate_environment()
except Exception as e:
    raise RuntimeError(f"Configuration validation failed: {e}")
