# MAAT MCP Restaurant Finder

맛집 검색 및 복합몰 매장 검색 서비스를 제공하는 remote MCP(Model Context Protocol) server입니다.

## 주요 기능

- **맛집 검색**: 사용자의 위치 기반으로 주변 맛집을 검색합니다.
- **랜덤 추천**: 현재 위치 기반으로 랜덤 맛집을 추천합니다.
- **복합몰 매장 검색**: 복합몰 loplat id를 기반으로 내부 매장을 검색합니다.

## 기술 스택

- Python 3.8+
- FastMCP 0.4.1+
- Google Maps API

## 설치 방법

1. 저장소 클론
```bash
git clone https://github.com/loplat/maat_mcp_server.git
cd maat_mcp_server
```

2. 의존성 설치
```bash
pip install -r requirements.txt
```

3. 환경 변수 설정
`.env` 파일을 생성하고 다음 변수들을 설정합니다:
```
GOOGLE_MAPS_API_KEY=your_google_maps_api_key
IPLOCATION_BASE_URL=loplat_public_ip_location_base_url
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=loplat_db_host
DB_PORT=loplat_db_port
DB_NAME=loplat_db
DB_IP_TABLE=loplat_db_ip_table_name
DB_STORE_TABLE=loplat_db_store_table_name
DB_LAYER_TABLE=lloplat_db_layer_table_name
```

## 실행 방법

```bash
python main.py
```

## API 엔드포인트

### 프롬프트
- `맛집 검색`: 맛집 검색 프롬프트

### 도구
- `find_restaurants`: 맛집 검색 도구
- `recommend_random_restaurant`: 랜덤 맛집 추천 도구
- `find_stores_in_complex`: 복합몰 내 매장 검색 도구

## 프로젝트 구조

```
maat_mcp_server/
├── main.py              # 메인 애플리케이션
├── requirements.txt     # 의존성 목록
└── maat_mcp/           # 핵심 패키지
    ├── api/            # API 클라이언트
    ├── handlers/       # 비즈니스 로직
    ├── services/       # tool 구현 로직
    └── util/           # 유틸리티 함수
```

## claude_desktop_config 설정 방법
```
"restaurants_finder": {
	"command": "npx",
	"args": [
		"mcp-remote",
		"http://server-address/sse"
	],
  	"env": {
		"GOOGLE_MAPS_API_KEY": "{YOUR_GOOGLE_MAPS_API_KEY}"
		...
  	}
}
```
