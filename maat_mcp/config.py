import os
from typing import Dict, Any
from dotenv import load_dotenv

class Config:
    """환경 변수 설정을 관리하는 클래스입니다."""
    # 환경 변수 로드
    load_dotenv()

    # DB 설정 값
    DB_USER = os.getenv('DB_USER', '')
    DB_PASSWORD = os.getenv('DB_PASSWORD', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_PORT = os.getenv('DB_PORT', '')
    DB_NAME = os.getenv('DB_NAME', '')
    DB_IP_TABLE = os.getenv('DB_IP_TABLE', '')
    DB_STORE_TABLE = os.getenv('DB_STORE_TABLE', '')
    DB_LAYER_TABLE = os.getenv('DB_LAYER_TABLE', '')
    
    # API 키
    GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY", "")
    
    # 기본 설정
    DEFAULT_SEARCH_QUERY = "맛집"
    MAX_CACHE_SIZE = 1000
    REQUEST_TIMEOUT = 10
    
    # 평점 기준
    RATING_THRESHOLDS = [4.5, 4.0, 3.8]
    
    # API 기본 URL
    GOOGLE_MAPS_BASE_URL = "https://maps.googleapis.com/maps/api"
    IPLOCATION_BASE_URL = os.getenv("IPLOCATION_BASE_URL", "")

    # 검색 설정
    SEARCH_RADIUS = "1000"  # 미터 단위
    
    # HTTP 설정
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # 초
    
    # 캐시 설정
    CACHE_TTL = 3600  # 초 (1시간)

    @classmethod
    def load(cls):
        load_dotenv()
    
    @classmethod
    def get_google_maps_base_url(cls) -> str:
        """Google Maps API 기본 URL을 반환합니다."""
        return cls.GOOGLE_MAPS_BASE_URL
    
    @classmethod
    def get_iplocation_base_url(cls) -> str:
        """IPLocation API 기본 URL을 반환합니다."""
        return cls.IPLOCATION_BASE_URL
    
    @classmethod
    def get_google_api_key(cls) -> str:
        """Google Maps API 키를 반환합니다."""
        if not cls.GOOGLE_MAPS_API_KEY:
            raise ValueError("Google Maps API 키가 설정되지 않았습니다.")
        return cls.GOOGLE_MAPS_API_KEY