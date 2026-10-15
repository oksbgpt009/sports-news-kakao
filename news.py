import html
import json
import os
import re
import time
from datetime import datetime, timedelta, timezone

import requests

KST = timezone(timedelta(hours=9))
SEARCH_URL = "https://search.naver.com/search.naver"
HEADERS = {"User-Agent": "Mozilla/5.0"}


def time_window(now=None):
    """하루 두 번 (KST): 06:30 실행 → 전일 18:00~당일 06:00, 18:30 실행 → 당일 06:00~18:00.
    실행 시각 직전의 06시 또는 18시를 끝으로 하는 12시간 구간."""
    now = now or datetime.now(KST)
    end = now.replace(hour=18 if now.hour >= 18 else 6, minute=0, second=0, microsecond=0)
    if now < end:  # 06시 전에 실행되면 전일 18시까지
        end -= timedelta(hours=12)
    days = os.environ.get("WINDOW_DAYS")  # 수동 테스트 때만 일 단위로 늘려 씀
    return end - (timedelta(days=int(days)) if days else timedelta(hours=12)), end


def clean(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text or "")).strip()


def fetch(url, params=None):
    # 네이버가 가끔 응답을 안 줘서(타임아웃) 전체가 실패하는 일이 있어 3번까지 재시도
    for attempt in range(3):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=20)
            resp.raise_for_status()
            return resp.text
        except requests.RequestException as e:
            if attempt == 2:
                raise
            print(f"  재시도 {attempt + 1}/2: {url} ({type(e).__name__})")
            time.sleep(5)


def age_minutes(text):
    """'5분 전' '3시간 전' → 분. 하루 이상('1일 전' 등)은 부정확하므로 None."""
    m = re.match(r"(\d+)(분|시간) 전", text or "")
    return int(m.group(1)) * {"분": 1, "시간": 60}[m.group(2)] if m else None


def search(query, start, end):
    """네이버 뉴스 검색 결과 페이지(최신순, 날짜 범위)를 받아 기사 목록을 뽑는다."""
    page = fetch(SEARCH_URL, {
        "where": "news", "sort": 1, "pd": 3, "query": query,
        "ds": f"{start:%Y.%m.%d}", "de": f"{end:%Y.%m.%d}",
    })
    print(f"  검색 '{query}': 페이지 {len(page)}자")  # 0이나 매우 작으면 접속 차단 의심
    items = []
    # 기사 하나가 {"props":{...},"templateId":"newsItem"} 형태의 JSON으로 들어 있음
    for m in re.finditer(r'"templateId":"newsItem"', page):
        s = page.rfind('{"props":', 0, m.start())
        try:
            props = json.loads(page[s:m.end()] + "}")["props"]
        except ValueError:
            continue
        link, age = props.get("titleHref"), None
        for sub in props.get("sourceProfile", {}).get("subTexts", []):
            if sub.get("text") == "네이버뉴스" and sub.get("textHref"):
                link = sub["textHref"]
            if age is None:
                age = age_minutes(sub.get("text"))
        # 네이버뉴스 링크는 n.news.naver.com 형태로 통일 (스포츠 기사는 자동 리다이렉트)
        m2 = re.search(r"naver\.com/.*article/(\d+)/(\d+)", link or "")
        if m2:
            link = f"https://n.news.naver.com/article/{m2.group(1)}/{m2.group(2)}"
        items.append({
            "title": clean(props.get("title")),
            "description": clean(props.get("content")),
            "link": link,
            "age": age,
        })
    return items


def published_at(item):
    """네이버뉴스 기사는 기사 페이지의 정확한 입력시각, 그 외는 'N시간 전'으로 추정."""
    if item["link"].startswith("https://n.news.naver.com/"):
        m = re.search(r"serviceDatetime\W+(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", fetch(item["link"]))
        if m:
            return datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").replace(tzinfo=KST)
    if item["age"] is not None:
        return datetime.now(KST) - timedelta(minutes=item["age"])
    return None


def collect(category, start, end, limit):
    articles = {}
    for query in category["queries"]:
        for item in search(query, start, end):
            title, desc = item["title"], item["description"]
            # 제목에 대상이 있어야 함 (지나가듯 언급된 기사 제외), 사진기사 제외
            if not any(k in title for k in category["title_any"]) or "포토]" in title:
                continue
            if not any(k in title + " " + desc for k in category["topic_any"]):
                continue
            # 같은 기사가 여러 검색어에 걸리므로 제목 기준 중복 제거
            if title in articles:
                continue
            published = published_at(item)
            # 경계 시각(06:00/18:00 정각) 기사는 앞뒤 두 번 모두 보냄
            if published and start <= published <= end:
                articles[title] = {
                    "title": title,
                    "description": desc,
                    "link": item["link"],  # 네이버 뉴스 링크 우선 (카카오 도메인 등록용)
                    "published": published,
                }
    return sorted(articles.values(), key=lambda a: a["published"], reverse=True)[:limit]
