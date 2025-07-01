import logging
from maat_mcp.config import Config
from mcp.server.fastmcp import FastMCP
from maat_mcp.services.service_implementation import (
    find_restaurants,
    find_random_restaurant,
    find_stores_in_complex
)

# 컨피그 세팅
Config.load()

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# MCP 서버 생성
mcp = FastMCP(
    name="Place Agent",
    instructions="""
1. If a complex_id is provided, use the find_stores_in_complex MCP tool to search for stores within the complex.
   - Handle the user request exclusively using this MCP tool and respond based solely on its results.
   - Do not use any regional names or coordinate values from the user's location context; the response must be strictly based on the results retrieved using complex_id.

2. If no complex_id is provided, make an appropriate judgment and use either the find_restaurants or recommend_random_restaurant MCP tool to search for restaurants.
   - Do not use these MCP tools if the user request does not express hunger or explicitly ask for restaurant recommendations.
""",
)

# 프롬프트 등록
@mcp.prompt("맛집 검색")
async def search_restaurants_prompt(query: str):
    """맛집을 검색합니다.
    
    Args:
        query (str): 검색어 (예: '맛집', '한식 맛집', '강남 맛집', '내 주변 맛집')
        context (str, optional): 이전 대화 내용
    
    Returns:
        Dict[str, Any]: 검색된 맛집 정보
    """
    return "현재 위치 기반으로 맛집 정보를 제공합니다."

# 도구 등록
@mcp.tool(description="search restaurants", name="find_restaurants")
async def find_restaurants_tool(query: str, context: str = ""):
    """현재 위치 기반으로 맛집 리스트를 검색합니다.
    
    Args:
        query (str): 검색어 (예: '맛집', '한식 맛집', '강남 맛집', '내 주변 맛집')
        context (str, optional): 이전 대화 내용
    
    Returns:
        Dict[str, Any]: 검색된 맛집 정보
    """
    return await find_restaurants(query, context)

@mcp.tool(description="Recommends random restaurants based on the user’s current location.",name="recommend_random_restaurant")
async def recommend_random_restaurant_tool(category: str = None):
    """현재 위치 기반으로 랜덤하게 하나의 맛집을 추천합니다.
    
    Args:
        category (str, optional): 음식 종류 (예: '한식', '중식', '일식', '양식')
    
    Returns:
        Dict[str, Any]: 추천된 맛집 정보
    """
    return await find_random_restaurant(category)

@mcp.tool(
        description="Finds and recommends stores located within a specified complex or mall, based on the user's current location.", 
        name="find_stores_in_complex",
        annotations={
            "title": "Find Stores in Complex",
            "readOnlyHint": True,
            "openWorldHint": False
        }
)
async def find_stores_in_complex_tool(complex_id: int):
    """복합 쇼핑몰 내의 매장을 검색합니다.
    
    Args:
        complex_id (int): 복합몰 ID
    
    Returns:
        Dict[str, Any]: 매장 정보
    """
    # 여기에 복합 쇼핑몰 내 매장 검색 로직을 추가하세요.
    return await find_stores_in_complex(complex_id)

if __name__ == "__main__":
    try:
        mcp.run(transport="sse")
    except Exception as e:
        logging.error(f"서버 실행 중 에러 발생: {str(e)}")
        raise