import logging
from logging.handlers import RotatingFileHandler
from typing import Optional
from config import config
import threading

class Logger:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_logger(cls, name: str = __name__) -> logging.Logger:
        """스레드 세이프 싱글톤 로거 인스턴스 반환"""
        with cls._lock:
            if cls._instance is None:
                # 로거 설정
                logger = logging.getLogger(name)
                logger.setLevel(getattr(logging, config.logging.level))

                # 포맷터 설정
                formatter = logging.Formatter(
                    fmt=config.logging.format,
                    datefmt=config.logging.date_format
                )

                # 파일 핸들러 설정
                file_handler = RotatingFileHandler(
                    filename=str(config.logging.file_path),
                    maxBytes=10*1024*1024,  # 10MB
                    backupCount=5,
                    encoding='utf-8'
                )
                file_handler.setFormatter(formatter)

                # 콘솔 핸들러 설정
                console_handler = logging.StreamHandler()
                console_handler.setFormatter(formatter)

                # 핸들러 추가
                logger.addHandler(file_handler)
                logger.addHandler(console_handler)

                cls._instance = logger

        return cls._instance

# 전역 로거 인스턴스
logger = Logger.get_logger()
