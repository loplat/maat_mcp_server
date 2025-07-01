import logging
from typing import Dict, Any
from maat_mcp.api.stores_in_complex_api import StoreInComplexApi

logger = logging.getLogger(__name__)

async def get_stores_in_complex(complex_id: int) -> Dict[str, Any]:
    """복합 쇼핑몰 내의 매장을 검색합니다.
    
    Args:
        complex_id (int): 쇼핑몰 ID
        
    Returns:
        Dict[str, Any]: 매장 정보
        
    Raises:
        Exception: API 호출 실패 시
    """
    try:
        response = await StoreInComplexApi.find_stores_in_complex(complex_id)
        
        # 응답이 필요한 필드를 포함하는지 확인
        if not response or "stores" not in response:
            raise Exception("매장 정보가 올바르지 않습니다.")
            
        return response
    except Exception as e:
        logger.error(f"복합 쇼핑몰 매장 검색 중 에러 발생: {str(e)}")
        raise
