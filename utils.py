import json
import os
import logging
from datetime import datetime

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def save_to_json(data, filepath):
    """데이터를 JSON 파일로 저장"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        logger.info(f"Data saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving data to {filepath}: {e}")
        return False

def load_from_json(filepath):
    """JSON 파일에서 데이터 로드"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        logger.info(f"Data loaded from {filepath}")
        return data
    except Exception as e:
        logger.error(f"Error loading data from {filepath}: {e}")
        return None

def save_report(report_content, filepath):
    """보고서 내용을 파일로 저장"""
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        logger.info(f"Report saved to {filepath}")
        return True
    except Exception as e:
        logger.error(f"Error saving report to {filepath}: {e}")
        return False

def extract_json_from_text(text):
    """텍스트에서 JSON 부분 추출"""
    try:
        # JSON 형식을 찾기 위한 간단한 방법
        start_idx = text.find('{')
        end_idx = text.rfind('}') + 1
        
        if start_idx >= 0 and end_idx > start_idx:
            json_str = text[start_idx:end_idx]
            return json.loads(json_str)
        else:
            logger.warning("No JSON found in text")
            return None
    except Exception as e:
        logger.error(f"Error extracting JSON from text: {e}")
        return None

def get_timestamp():
    """현재 시간 스탬프 생성"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")