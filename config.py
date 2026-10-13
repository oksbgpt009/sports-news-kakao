# 카테고리별 검색어와 필터 조건
# - queries: 네이버 뉴스 검색어 (결과를 합쳐서 중복 제거)
# - title_any: 제목에 이 중 하나는 반드시 포함 (관련 주체. 지나가듯 언급된 기사 제외용)
# - topic_any: 제목+요약에 이 중 하나는 반드시 포함 (종목 확인용)

TEAM = ["OK저축은행", "OK 저축은행", "OK저축銀", "오케이저축은행", "읏맨"]

CATEGORIES = [
    {
        "name": "🏐 배구",
        "queries": ["OK저축은행 배구", "읏맨 배구"],
        "title_any": TEAM,
        "topic_any": ["배구", "V리그", "V-리그", "KOVO", "컵대회"],
    },
    {
        "name": "🏉 럭비",
        "queries": ["OK저축은행 럭비", "읏맨 럭비"],
        "title_any": TEAM,
        "topic_any": ["럭비"],
    },
    {
        "name": "⛳ 골프",
        "queries": ["OK배정장학재단", "김우정 골프", "이태희 골프"],
        "title_any": ["배정장학", "김우정", "이태희"],
        "topic_any": ["골프", "KLPGA", "KPGA", "LPGA", "투어", "라운드", "버디", "우승"],
    },
]

ARTICLES_PER_CATEGORY = 3
