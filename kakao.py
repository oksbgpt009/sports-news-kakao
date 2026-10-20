import json
import os

import requests

TOKEN_URL = "https://kauth.kakao.com/oauth/token"
MEMO_URL = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
NEW_REFRESH_TOKEN_FILE = ".new_refresh_token"


def get_access_token():
    data = {
        "grant_type": "refresh_token",
        "client_id": os.environ["KAKAO_REST_API_KEY"],
        "refresh_token": os.environ["KAKAO_REFRESH_TOKEN"],
    }
    if os.environ.get("KAKAO_CLIENT_SECRET"):
        data["client_secret"] = os.environ["KAKAO_CLIENT_SECRET"]
    resp = requests.post(TOKEN_URL, data=data, timeout=10)
    if not resp.ok:
        raise SystemExit(f"카카오 토큰 갱신 실패: {resp.status_code} {resp.text}")
    token = resp.json()
    # 만료 1개월 이내면 새 refresh token이 내려옴 → 워크플로가 GitHub Secret에 다시 저장
    if "refresh_token" in token:
        with open(NEW_REFRESH_TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(token["refresh_token"])
    return token["access_token"]


def _link(url):
    return {"web_url": url, "mobile_web_url": url}


def build_template(header, articles, list_url, total):
    # 리스트 템플릿은 항목 2~3개만 허용 → 1개는 텍스트 템플릿 (0개는 main에서 전송 생략)
    # list_url: 이번 기간 기사 전체 목록 페이지, total: 전체 건수
    if len(articles) >= 2:
        return {
            "object_type": "list",
            "header_title": header,
            "header_link": _link(list_url),
            "buttons": [{"title": f"전체 {total}건 보기", "link": _link(list_url)}],
            "contents": [
                {
                    "title": a["title"],
                    "description": a["published"].strftime("%m/%d %H:%M"),
                    "link": _link(a["link"]),
                }
                for a in articles
            ],
        }
    a = articles[0]
    return {
        "object_type": "text",
        "text": f"{header}\n\n{a['title']}\n({a['published'].strftime('%m/%d %H:%M')})"[:200],
        "link": _link(a["link"]),
        "button_title": "기사 보기",
    }


def send(access_token, template):
    resp = requests.post(
        MEMO_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        data={"template_object": json.dumps(template, ensure_ascii=False)},
        timeout=10,
    )
    resp.raise_for_status()
