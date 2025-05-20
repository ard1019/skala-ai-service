import time
import functools
from typing import Any, Callable
from utils.logger import logger

def log_execution_time(func: Callable) -> Callable:
    """함수 실행 시간 로깅 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            logger.debug(f"{func.__name__} executed in {execution_time:.2f} seconds")
            return result
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {e}")
            raise
    return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable:
    """재시도 데코레이터"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    if attempts == max_attempts:
                        logger.error(f"Failed after {max_attempts} attempts: {e}")
                        raise
                    logger.warning(f"Attempt {attempts} failed, retrying in {delay} seconds")
                    time.sleep(delay)
            return None
        return wrapper
    return decorator

def validate_input(func: Callable) -> Callable:
    """입력 검증 데코레이터"""
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Validation error in {func.__name__}: {e}")
            raise ValidationError(str(e))
    return wrapper
