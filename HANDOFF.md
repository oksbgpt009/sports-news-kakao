# 스포츠단 뉴스 카톡 알림: 집 PC 이어서 작업하기

> 집 PC의 Claude Code에서 이 폴더를 열고 **"HANDOFF.md 읽고 이어서 진행해줘"** 라고 하면 됩니다.
> 작성일: 2026-10-12 (회사 PC에서 작업한 내용 정리)

## 0. 한눈에 보기 (집에서 남은 일)

| # | 할 일 | 상태 |
|---|---|---|
| 1 | 코드 수정 (대상 필터, 0건 미전송, 07:30 cron 등) | ✅ 완료 |
| 2 | GitHub Private 저장소 생성 (`oksbgpt009/sports-news-kakao`) | ✅ 완료 |
| 3 | `git push -u origin main` (4-④) | ⬜ 집에서 |
| 4 | `news.py` 수집 방식을 네이버 검색 페이지 파싱으로 교체 (4-②, 5장 코드) + 워크플로 NAVER env 정리 | ⬜ 집에서 |
| 5 | 카카오 개발자 앱 등록 → `python get_token.py` 로 refresh token 발급 (4-③) | ⬜ 집에서 |
| 6 | GitHub Secrets 등록 (`KAKAO_REST_API_KEY`, `KAKAO_REFRESH_TOKEN`, `GH_PAT`, 필요시 `KAKAO_CLIENT_SECRET`) | ⬜ 집에서 |
| 7 | Actions 에서 수동 실행 → 카톡 수신 확인, 해외 서버에서 네이버 접속되는지 확인 (6장) | ⬜ 집에서 |
| 8 | claude.ai 「배구단 뉴스 카톡 알림」 루틴 삭제 (이미 비활성) | ⬜ 아무 때나 |

---

## 1. 목표 (확정된 요구사항)

매일 **07:30(KST)** 에 **전일 07:00 ~ 당일 07:00** 사이에 나온 기사를 종목별로 모아 **내 카카오톡(나에게 보내기)** 으로 보낸다.

| 종목 | 받을 기사 | 비고 |
|---|---|---|
| 🏐 배구 | **OK저축은행 읏맨 배구단** 관련 기사만 | OK저축은행이 지나가듯 언급되는 기사 제외 (예: 전 OK저축은행 감독 김세진의 타팀 기사, OK금융그룹 경영 기사) |
| 🏉 럭비 | **OK저축은행 읏맨 럭비단** 관련 기사만 | |
| ⛳ 골프 | **OK배정장학재단, 김우정 프로, 이태희 프로** 관련 기사만 | OK저축은행 골프는 대상 아님. 동명이인(정치부 이태희 기자 등) 제외 |

- 메시지는 **종목별 1통**, 한 통에 기사 **최대 3개(제목 + 링크)**
- 해당 기간에 기사가 **없는 종목은 보내지 않는다** ("기사 없음" 메시지도 보내지 않음). 세 종목 모두 없으면 그날은 아무것도 안 보냄
- **PC가 꺼져 있어도** 돌아야 함 → **GitHub Actions** 로 결정 (회사 PC는 자동 잠김·절전 변경 불가)
- **API 키는 코드/파일에 넣지 않고 GitHub Secrets 에만** 저장
- 카톡 수신 계정: **집에서 `get_token.py` 를 실행할 때 로그인한 카카오 계정으로 받게 됨** (claude.ai 루틴과 달리 계정을 자유롭게 정할 수 있음 ← GitHub로 옮기는 이유 중 하나)

---

## 2. 지금까지 경과

1. 처음엔 **네이버 검색 API**(openapi.naver.com) + GitHub Actions 로 코드를 만들었음 (이 폴더의 `*.py`)
2. 그런데 **네이버 검색 API는 2026-07-30부터 신규 신청이 막힘** (NAVER API HUB 로 이관, 약관상 결과 가공·재정렬 제한도 생김) → 키 발급 못 함
3. 대안으로 **claude.ai 루틴**(Claude Code 원격 예약 작업 + PlayMCP 카카오 "나에게 보내기")으로 구현해서 테스트까지 성공
   - 네이버 **검색 결과 페이지(search.naver.com)** 를 직접 받아 파싱하는 방식으로 수집 → 키 없이 동작 확인
4. 하지만 PlayMCP 카카오 연결은 claude.ai 계정당 1개라서 **다른 루틴(09시 아침 기사 모니터링)과 같은 카톡 계정으로 섞여서 옴** → 계정 분리 불가
5. 그래서 **GitHub Actions 로 다시 가기로 결정**. claude.ai 의 「배구단 뉴스 카톡 알림」 루틴은 **비활성화해 둠** (삭제는 claude.ai/code/routines 에서 직접)

---

## 2-1. 2026-10-12 오후 추가 작업 (회사 PC, 네이버 연동 제외 완료)

- `config.py`: 새 대상으로 교체 (`must_any` → `title_any`, 골프에서 OK저축은행 제외, `TEAM` 공통 목록)
- `news.py`: `collect()` 필터만 변경 (제목에 대상 필수, `포토]` 제외). **`search()`(네이버 연동)는 그대로 → 아래 4-② 수집 방식 교체만 남음**
- `main.py`: 기사 0건 종목 전송 생략, 전부 0건이면 토큰 발급 없이 종료
- `kakao.py`: "기사 없음" 템플릿 제거 (안 쓰게 됨)
- 워크플로 cron `30 22 * * *` (07:30 KST). NAVER 시크릿 env 는 수집 방식 확정 때 정리하려고 남겨둠
- `.gitignore`: `.playwright-mcp/`, `.new_refresh_token` 추가
- `git init` + 첫 커밋 완료 (`9a99a1c`). 작성자는 이 저장소에만 `oksbgpt009 <oksbgpt009@gmail.com>` 로 설정
- **GitHub Private 저장소 생성 완료: https://github.com/oksbgpt009/sports-news-kakao** (비어 있음, remote `origin` 등록됨)
- **push 는 아직 안 됨**: 회사 PC 터미널에서 GitHub 로그인 창을 못 띄워 실패 → 집에서 진행 (아래 4-④)
- 가짜 검색 데이터로 검증 완료: 기간 밖/제목에 대상 없음/사진기사/종목 단어 없음 → 제외, 0건 종목 미전송, 전부 0건이면 토큰 발급도 안 함, 2건↑ 리스트·1건 텍스트 템플릿

※ 아래 3·4장 표/설명 중 위 항목은 이미 반영된 상태임

## 3. 현재 폴더 상태

| 파일 | 상태 | 할 일 |
|---|---|---|
| `config.py` | 예전 요구사항(골프에 OK저축은행 포함 등) | **수정 필요** (아래 4-②) |
| `news.py` | 네이버 검색 **API** 사용 → 키 발급 불가라 못 씀 | **수집부를 검색 페이지 파싱 방식으로 교체** (아래 4-②) |
| `kakao.py` | 카카오 "나에게 보내기" (리스트 템플릿 2~3개 / 1개는 텍스트 / 0개는 "기사 없음") | 0개일 때 안 보내도록 main 쪽에서 처리 |
| `main.py` | 3종목 모두 전송, `--dry-run` 지원 | **기사 0건 종목은 건너뛰기** |
| `get_token.py` | 카카오 refresh token 최초 1회 발급 (입력값 화면에 안 보임) | 집에서 실행 |
| `.github/workflows/daily-news.yml` | cron `0 22 * * *`(=07:00 KST), NAVER 시크릿 사용, 갱신 토큰 자동 저장 | **cron 을 `30 22 * * *`(=07:30)로**, NAVER 시크릿 제거 |
| `requirements.txt` | `requests` | 그대로 |
| `.gitignore` | `__pycache__/` 만 있음 | `.playwright-mcp/`, `.new_refresh_token` 추가 |
| `CLAUDE.md` | 코딩 가이드라인 (단순하게, 필요한 것만 수정) | 그대로 |
| `DESIGN_SYSTEM.md` | 이 작업과 무관 | 그대로 |
| `.playwright-mcp/` | 브라우저 자동화 임시 파일 | 커밋하지 말 것 (삭제해도 됨) |

---

## 4. 집에서 할 일 (순서대로)

### ① 준비
- 이 폴더를 집 PC로 복사 (USB/클라우드 드라이브. **키는 파일에 없으므로 그대로 옮겨도 안전**). 숨김 폴더 **`.git` 도 같이** 복사할 것 (커밋·원격 저장소 설정이 들어 있음)
- 설치: Python 3.12, Git, GitHub CLI(`gh`), Claude Code
- 회사 PC는 사내 보안 프록시 때문에 Python 으로 네이버 접속이 SSL 오류가 났음 → **집에서는 정상일 것**. 그래도 `python main.py --dry-run` 으로 먼저 확인

### ② 코드 수정
**수집 방식**: claude.ai 루틴에서 검증한 방식을 그대로 옮긴다 (아래 5장 코드). 핵심:
- 검색 URL: `https://search.naver.com/search.naver?where=news&sort=1&pd=3&ds=YYYY.MM.DD&de=YYYY.MM.DD&query=검색어`
  (`sort=1` 최신순, `pd=3` + `ds/de` 날짜 범위 — 전일·당일 두 날짜를 넣고, 시각은 아래에서 분 단위로 다시 거름)
- 페이지 안의 `"templateId":"newsItem"` 블록을 JSON으로 파싱 → `title`, `content`, `titleHref`, `sourceProfile.subTexts`
- `subTexts` 중 `text == "네이버뉴스"` 인 항목의 `textHref` 가 네이버뉴스 링크 → `https://n.news.naver.com/article/{언론사}/{기사번호}` 로 정규화 (스포츠 기사는 자동으로 m.sports.naver.com 으로 리다이렉트됨, 확인 완료)
- **정확한 입력시각**: 네이버뉴스 기사 페이지 HTML 안의 `serviceDatetime":"2026-10-11 19:06:07"` 를 정규식으로 추출 (리다이렉트 따라가야 함: requests 는 기본으로 따라감)
  - 네이버뉴스 링크가 없는 기사는 검색결과의 "N분 전 / N시간 전" 으로 추정, 그보다 오래된 표기("1일 전" 등)는 부정확하므로 제외
- **필터 (제목 기준)**: 제목에 대상 단어가 있어야 하고, 제목+요약문에 종목 단어가 있어야 함. 제목에 `포토]` 가 들어간 사진기사는 제외 (한 대회에 10개씩 쏟아짐)

**config 값** (루틴에서 쓰던 최종값):
```python
TEAM = ["OK저축은행", "OK 저축은행", "OK저축銀", "오케이저축은행", "읏맨"]
CATEGORIES = [
    {"name": "🏐 배구", "queries": ["OK저축은행 배구", "읏맨 배구"],
     "title_any": TEAM, "topic_any": ["배구", "V리그", "V-리그", "KOVO", "컵대회"]},
    {"name": "🏉 럭비", "queries": ["OK저축은행 럭비", "읏맨 럭비"],
     "title_any": TEAM, "topic_any": ["럭비"]},
    {"name": "⛳ 골프", "queries": ["OK배정장학재단", "김우정 골프", "이태희 골프"],
     "title_any": ["배정장학", "김우정", "이태희"],
     "topic_any": ["골프", "KLPGA", "KPGA", "LPGA", "투어", "라운드", "버디", "우승"]},
]
ARTICLES_PER_CATEGORY = 3
```

**main.py**: 기사 0건인 종목은 전송 생략. 전부 0건이면 카카오 토큰 발급도 하지 않고 종료.

**워크플로**: cron `30 22 * * *` (UTC 22:30 = KST 07:30. GitHub 사정으로 수~수십 분 늦을 수 있음), `NAVER_CLIENT_ID/SECRET` env 제거.

> 참고: 카카오 리스트 템플릿은 200자 제한이 없어서 제목을 자르지 않아도 됨 (루틴에서 쓰던 PlayMCP 도구는 200자 제한이 있었음).

### ③ 카카오 개발자 앱 설정 (https://developers.kakao.com)
1. **카톡을 받을 카카오 계정**으로 로그인 → 애플리케이션 추가
2. 앱 키의 **REST API 키** 확인 (채팅에 붙여넣지 말 것)
3. 카카오 로그인 **활성화**, Redirect URI 에 `https://localhost` 등록
4. 동의항목에서 **"카카오톡 메시지 전송"(talk_message)** 설정
5. 플랫폼 → Web → 사이트 도메인에 메시지 링크 도메인 등록: `https://n.news.naver.com`, `https://m.sports.naver.com`, `https://news.naver.com`
   (등록 안 된 도메인 링크는 카톡에서 안 열릴 수 있음. 네이버뉴스 판이 없는 언론사 링크는 열리지 않을 수 있으니, 필요하면 네이버뉴스 링크 있는 기사만 보내도록 결정)
6. 보안 → Client Secret 을 켰다면 그 값도 Secret 으로 등록
7. 터미널에서 `python get_token.py` 실행 → 안내대로 로그인/동의 → 출력된 **refresh token** 을 바로 GitHub Secret 에 등록하고 창 닫기

### ④ GitHub 설정
1. ~~Private 저장소 생성~~ → **완료** (`oksbgpt009/sports-news-kakao`). 폴더를 `.git` 포함해서 통째로 복사해 왔다면 집 PC 터미널에서:
   ```
   cd "<복사한 폴더>"
   git push -u origin main
   ```
   (GitHub 로그인 창이 뜨면 "Sign in with your browser"로 승인. 수집 방식 교체 등 집에서 고친 내용은 커밋 후 다시 push)
2. Settings → Secrets and variables → Actions 에 등록:
   - `KAKAO_REST_API_KEY`
   - `KAKAO_REFRESH_TOKEN`
   - `KAKAO_CLIENT_SECRET` (Client Secret 사용 시에만)
   - `GH_PAT` — refresh token 자동 갱신용. **Fine-grained PAT, 이 저장소 1개만, 권한은 Secrets: Read and write 만**
3. Actions 탭 → `daily-sports-news` → **Run workflow** 로 수동 실행해서 카톡 수신 확인

### ⑤ 확인 (성공 기준)
- [ ] 로컬 `python main.py --dry-run` 이 종목별 기사(또는 0건)를 출력, 기간 표시가 `전일 07:00~당일 07:00`
- [ ] 수동 실행 시 기사 있는 종목만 카톡 도착, 링크 클릭 시 기사 열림
- [ ] 다음날 07:30 경 자동 실행 확인
- [ ] claude.ai 루틴 삭제 (이미 비활성), 필요 없으면 claude.ai 의 PlayMCP 연결은 09시 루틴 때문에 **유지**

---

## 5. 검증된 수집 코드 (claude.ai 루틴에서 실제로 돌던 것)

> 루틴 환경용이라 `curl` 을 subprocess 로 호출함. 프로젝트에 옮길 때는 `requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)` 로 바꾸고, 기존 `news.py` 의 `time_window()` / `collect()` 구조에 맞춰 정리할 것.

```python
import html, json, re, subprocess, urllib.parse
from datetime import datetime, timedelta, timezone
TEAM = ["OK저축은행", "OK 저축은행", "OK저축銀", "오케이저축은행", "읏맨"]
TOPICS = [
    ("배구", ["OK저축은행 배구", "읏맨 배구"], TEAM, ["배구", "V리그", "V-리그", "KOVO", "컵대회"]),
    ("럭비", ["OK저축은행 럭비", "읏맨 럭비"], TEAM, ["럭비"]),
    ("골프", ["OK배정장학재단", "김우정 골프", "이태희 골프"], ["배정장학", "김우정", "이태희"], ["골프", "KLPGA", "KPGA", "LPGA", "투어", "라운드", "버디", "우승"]),
]
KST = timezone(timedelta(hours=9))
NOW = datetime.now(KST).replace(tzinfo=None)
END = NOW.replace(hour=7, minute=0, second=0, microsecond=0)  # 당일 07:00
if NOW < END: END -= timedelta(days=1)
START = END - timedelta(days=1)  # 전일 07:00
def fetch(url): return subprocess.run(["curl","-s","-L","-m","20","-A","Mozilla/5.0",url],capture_output=True,text=True).stdout
def clean(t): return html.unescape(re.sub(r"</?mark>","",t or ""))
def age_min(t):  # "5분 전" "3시간 전" → 분 (하루 이상은 부정확하므로 제외)
    m = re.match(r"(\d+)(분|시간)", t or "")
    return int(m.group(1)) * {"분":1,"시간":60}[m.group(2)] if m else None
def published(link, age):  # 네이버뉴스는 기사 페이지의 정확한 입력시각, 그 외는 "N시간 전"으로 추정
    if link.startswith("https://n.news.naver.com/"):
        m = re.search(r"serviceDatetime\W+(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d)", fetch(link))
        if m: return datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
    return NOW - timedelta(minutes=age) if age is not None else None
out = {"기간": f"{START:%m/%d %H:%M}~{END:%m/%d %H:%M}"}
for label, queries, must_title, topic in TOPICS:
    found, seen, sizes = [], set(), []
    for q in queries:
        page = fetch("https://search.naver.com/search.naver?" + urllib.parse.urlencode(
            {"where":"news","sort":1,"pd":3,"ds":f"{START:%Y.%m.%d}","de":f"{END:%Y.%m.%d}","query":q}))
        sizes.append(len(page))
        for m in re.finditer(r'"templateId":"newsItem"', page):
            s = page.rfind('{"props":', 0, m.start())
            try: p = json.loads(page[s:m.end()] + "}")["props"]
            except ValueError: continue
            title, content, link, age = clean(p.get("title")), clean(p.get("content")), p.get("titleHref"), None
            for sub in p.get("sourceProfile",{}).get("subTexts",[]):
                if sub.get("text") == "네이버뉴스" and sub.get("textHref"): link = sub["textHref"]
                age = age if age is not None else age_min(sub.get("text"))
            m2 = re.search(r"naver\.com/.*article/(\d+)/(\d+)", link or "")
            if m2: link = f"https://n.news.naver.com/article/{m2.group(1)}/{m2.group(2)}"
            if not any(k in title for k in must_title) or "포토]" in title: continue
            if not any(k in title + content for k in topic): continue
            if link in seen or title in seen: continue
            seen.update([link, title])
            pub = published(link, age)
            if pub and START <= pub < END:
                found.append({"title":title, "link":link, "time":f"{pub:%m/%d %H:%M}", "_pub":pub})
    found.sort(key=lambda a: a.pop("_pub"), reverse=True)
    out[label] = {"html_len": min(sizes), "articles": found[:5]}
print(json.dumps(out, ensure_ascii=False, indent=1))
```

**검증 결과 (2026-10-12, 회사 PC)**
- 10/04 07:00~10/05 07:00 가정 → 배구 2건(10/04 11:06, 10:59)만 정확히 남고 구간 밖 기사 제외
- 최근 1주 기준 → 배구는 전지훈련 등 배구단 기사만 남고 김세진 감독/IBK/OK금융 기사 제외, 골프는 "OK저축은행 김우정, 하이트진로 챔피언십" 포착, 정치부 이태희 기자 기사 제외, 럭비는 비시즌이라 0건
- 10/11 07:00~10/12 07:00 실제 루틴 실행 → 세 종목 0건 (수동 확인 결과도 동일, 정상)

---

## 6. 주의사항 / 미해결

- **GitHub Actions 서버(해외)에서 search.naver.com 접속이 되는지 아직 미확인.** claude.ai 클라우드 환경에서는 정상이었음. 첫 수동 실행 때 로그의 페이지 크기(html_len)가 0이거나 매우 작으면 접속 차단 → 그때 대안 검토 (NAVER API HUB 키 발급, 또는 Google 뉴스 RSS)
- 네이버 검색 페이지 구조가 바뀌면 파싱이 깨질 수 있음 (`"templateId":"newsItem"` 부분). 0건이 며칠 계속되면 의심
- 제목 기준 필터라 제목에 "OK"만 있는 기사(예: "OK 전광인…")는 빠짐. 필요하면 조건 보완
- 이력(중복 방지) 기능은 없음. 기간이 하루씩 겹치지 않아 중복 가능성은 낮음
- 카카오 refresh token 은 약 2개월 유효, 만료 1개월 전부터 새 토큰이 내려오면 워크플로가 `GH_PAT` 로 Secret 을 자동 갱신함
- 보안 원칙: 키·토큰은 채팅/파일/커밋에 남기지 않기. 비밀번호 입력은 본인이 직접
