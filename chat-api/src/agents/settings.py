"""
Agents 패키지 설정
Pydantic Settings를 사용한 환경변수 관리
"""
from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class AgentSettings(BaseSettings):
    """에이전트 관련 설정"""
    
    # OpenAI 설정
    openai_api_key: str
    openai_model: str = "gpt-4o-mini"
    openai_temperature: float = 0.7
    openai_max_tokens: Optional[int] = None
    
    # 에이전트 설정
    agent_timeout: int = 60
    agent_max_retries: int = 3
    
    # 로깅 설정
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings():
    return AgentSettings()