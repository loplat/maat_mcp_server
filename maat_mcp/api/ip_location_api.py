import logging
import os
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from maat_mcp.api.http_client import HttpClient
from maat_mcp.config import Config

logger = logging.getLogger(__name__)

DATABASE_URL = f"mysql+aiomysql://{Config.DB_USER}:{Config.DB_PASSWORD}@{Config.DB_HOST}:{Config.DB_PORT}/{Config.DB_NAME}"

# 비동기 엔진 생성
try:
    engine = create_async_engine(DATABASE_URL)
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
except Exception as e:
    logger.error(f"데이터베이스 엔진 생성 실패: {str(e)}")
    engine = None
    async_session = None

class IpLocationApi:
    """IP 기반 위치 정보를 조회하는 클라이언트"""
    
    @staticmethod
    async def get_location_info(client_ip: Optional[str] = None) -> Dict[str, Any]:
        """IP 기반으로 위치 정보를 조회합니다.
        
        Args:
            client_ip (str, optional): 클라이언트 IP 주소
            
        Returns:
            Dict[str, Any]: 위치 정보
            
        Raises:
            Exception: API 호출 실패 시
        """
        try:
            # IP 주소가 없는 경우 현재 IP 사용
            if not client_ip:
                client_ip = (await HttpClient.get(Config.get_iplocation_base_url()))

            print("client_ip ", client_ip)
            
            # 데이터베이스에서 IP 검색
            async with async_session() as session:
                query = text(f"""
                    SELECT lat, lng, addr_name 
                    FROM {Config.DB_IP_TABLE}
                    WHERE ip = :ip
                """)
                result = await session.execute(query, {"ip": client_ip})
                row = result.fetchone()
                
                if row:
                    return {
                        "latitude": float(row.lat),
                        "longitude": float(row.lng),
                        "city": row.addr_name,
                        "country": 'South Korea'
                    }
            
            # DB에서 찾지 못한 경우 기본 위치 정보 반환
            return {
                "latitude": 37.5665,  # 서울시 기본 위도
                "longitude": 126.9780,  # 서울시 기본 경도
                "city": "Seoul",
                "country": "South Korea"
            }
            
        except Exception as e:
            logger.error(f"IP 위치 정보 조회 중 에러 발생: {str(e)}")
            raise