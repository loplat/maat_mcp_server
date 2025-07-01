import logging
import os
from typing import Dict, Any, Optional
from sqlalchemy import create_engine, text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from maat_mcp.api.google_maps_api import GoogleMapsApi
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

class StoreInComplexApi:
    """복합 쇼핑몰 내의 매장을 검색하는 API 클라이언트"""

    @staticmethod
    async def find_stores_in_complex(complex_id: int) -> Dict[str, Any]:
        """복합 쇼핑몰 내의 매장을 검색합니다.
        
        Args:
            complex_name (str): 쇼핑몰 이름
            
        Returns:
            Dict[str, Any]: 매장 정보
            
        Raises:
            Exception: API 호출 실패 시
        """
        print(complex_id)
        try:
            # 데이터베이스에서 매장 검색
            async with async_session() as session:
                query = text(f"""
                    SELECT * FROM {Config.DB_STORE_TABLE}
                    JOIN {Config.DB_LAYER_TABLE} ON {Config.DB_STORE_TABLE}.pid = {Config.DB_LAYER_TABLE}.id1
                    WHERE {Config.DB_LAYER_TABLE}.layers = 203 AND {Config.DB_LAYER_TABLE}.id2 = :complex_id;
                """)
                result = await session.execute(query, {"complex_id": complex_id})
                rows = result.fetchall()
                
                if rows:
                    result = {
                        "stores": []
                    }
                    for row in rows:
                        result["stores"].append({
                            "name": row.name + " " + (row.branch_name or ""),
                            "floor": row.floor
                        })
                    return result
                else:
                    return {"message": f"{complex_id}에 해당하는 매장이 없습니다."}
        
        except Exception as e:
            logger.error(f"매장 검색 중 에러 발생: {str(e)}")
            raise