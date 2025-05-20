class TrendAnalysisError(Exception):
    """기본 에러 클래스"""
    pass

class DataCollectionError(TrendAnalysisError):
    """데이터 수집 관련 에러"""
    pass

class PromptError(TrendAnalysisError):
    """프롬프트 관련 에러"""
    pass

class APIError(TrendAnalysisError):
    """API 호출 관련 에러"""
    pass

class ValidationError(TrendAnalysisError):
    """데이터 검증 관련 에러"""
    pass

class VisualizationError(TrendAnalysisError):
    """시각화 관련 에러"""
    pass

class StorageError(TrendAnalysisError):
    """저장소 관련 에러"""
    pass
