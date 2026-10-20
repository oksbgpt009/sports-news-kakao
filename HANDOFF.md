# 스포츠단 뉴스 카톡 알림: 회사 PC(Windows)에서 이어서 작업하기

> 회사 PC의 Claude Code에서 이 폴더를 열고 **"HANDOFF.md 읽고 이어서 진행해줘"** 라고 하면 됩니다.
> 작성일: 2026-10-13 (집 Mac에서 작업한 내용 정리)

## 0. 한눈에 보기

**시스템은 완성되어 매일 두 번(06:30, 18:30) 자동으로 돌고 있음.** 카톡 수신 계정은 "준호" 계정 (10/14 변경 완료).

| # | 할 일 | 상태 |
|---|---|---|
| 1 | 수집 방식을 네이버 검색 페이지 파싱으로 교체 | ✅ 완료 |
| 2 | GitHub push (`oksbgpt009/sports-news-kakao`, Private) | ✅ 완료 |
| 3 | 카카오 개발자 앱 생성·설정 (앱 "스포츠단 뉴스", ID 1606829) | ✅ 완료 |
| 4 | GitHub Secrets: `KAKAO_REST_API_KEY`, `KAKAO_CLIENT_SECRET`, `KAKAO_REFRESH_TOKEN` | ✅ 완료 |
| 5 | Actions 수동 실행 → 카톡 수신 확인 (10/13, 배구 3건 도착) | ✅ 완료 |
| 6 | **카톡 받는 카카오 계정 변경** (아래 2장) | ✅ 완료 (10/14, 방법 B: "준호" 계정으로 새 앱 ID 1607278, Secret 3개 교체, 테스트 실행 #6 에서 골프 1건 수신) |
| 7 | `GH_PAT` 등록 (토큰 자동 갱신용, 아래 4장) | ⬜ 선택 |
| 8 | claude.ai 「배구단 뉴스 카톡 알림」 루틴 삭제 (이미 비활성) | ⬜ 아무 때나 |

---

## 1. 현재 동작

- **GitHub Actions** (`.github/workflows/daily-news.yml`) 가 **하루 두 번** 실행 (10/14 변경)
  - **06:30 KST** → **전일 18:00 ~ 당일 06:00** 기사
  - **18:30 KST** → **당일 06:00 ~ 18:00** 기사
  - **실행 버튼은 cron-job.org 가 누름** (10/15 변경): GitHub 자체 schedule 이 2~5시간씩 늦어서 제거함. 다시 켜면 중복 발송되니 주의
    - cron-job.org 계정의 작업 「스포츠단 뉴스 카톡 (06:30, 18:30)」: crontab `30 6,18 * * *`, 시간대 Asia/Seoul
    - POST `https://api.github.com/repos/oksbgpt009/sports-news-kakao/actions/workflows/daily-news.yml/dispatches`, body `{"ref":"main"}`
    - 헤더: `Accept: application/vnd.github+json`, `X-GitHub-Api-Version: 2022-11-28`, `Content-Type: application/json`, `Authorization: Bearer <PAT>` (`Bearer ` 빠지면 401)
    - PAT: fine-grained `cron-job-sports-news`, 이 저장소만, Actions 읽기·쓰기, **2027-10-14 만료** → 만료 전 새로 만들어 cron-job.org 헤더 교체
    - 정상 응답 204. cron-job.org 의 HISTORY 에서 실행 기록 확인 가능
    - 참고: GitHub 가 API 버전 `2022-11-28` 을 deprecated 처리(2028-03 종료 예정). 그 전에 새 버전으로 헤더 변경 필요
  - 네트워크 대응 (10/15): 요청 실패 시 3번까지 재시도. 해외 서버에서 네이버 스포츠 기사 페이지가 가끔 무응답 → 그 기사만 'N시간 전'으로 시각 추정하고 계속 진행 (전체 중단 안 함)
  - 경계 시각(06:00/18:00 정각) 기사는 양쪽 모두에 포함 (중복 발송 허용 요청)
- 기사는 네이버 뉴스 **검색 결과 페이지**에서 수집 (API 키 불필요. 네이버 검색 API는 신규 신청 막힘)
  - 10/20 변경: 검색 화면은 최신 10건만 주고 날짜 범위도 잘 안 먹어서, 화면의 '더보기' 주소(`s.search.naver.com/p/newssearch/4/api/tab/more`, `nso=so:dd,p:fromYYYYMMDDtoYYYYMMDD`)로 10건씩 끝까지 넘김 (검색어당 최대 100건)
  - 기사 시각은 네이버뉴스 기사 페이지의 입력시각(`serviceDatetime`)으로 확인
  - GitHub 해외 서버에서도 네이버 접속 정상 확인됨 (10/13)
- 대상 (`config.py`): 🏐 배구·🏉 럭비 = OK저축은행 읏맨 배구단/럭비단, ⛳ 골프 = OK배정장학재단·김우정·이태희. **제목에 대상이 있어야** 함, 사진기사(`포토]`) 제외
- 종목별 1통, 최대 3기사(제목+링크). **기사 없는 종목은 안 보냄**, 전부 없으면 그날은 아무것도 안 감
- **전체 목록 페이지** (10/20): 기간 내 기사는 전부 수집해 `docs/YYYYMMDD-HH.html` 로 저장 → 워크플로가 커밋 → GitHub Pages(`https://oksbgpt009.github.io/sports-news-kakao/`) 로 공개. 카톡 리스트 메시지의 제목·「전체 N건 보기」 버튼이 이 페이지(종목 위치 `#c0`~`#c2`)로 연결. 페이지는 발송 후 1분쯤 뒤 열림
  - 이를 위해 저장소를 **Public** 으로 전환 (무료 계정은 Private 저장소에 Pages 불가). 키·토큰은 Secrets 에만 있음
- **네이버뉴스에 없는 기사** (10/20): 언론사 원문 링크는 카카오 미등록 도메인이라 news.naver.com 첫 화면으로 빠짐 → 기사 제목으로 네이버 뉴스 검색한 결과(`search.naver.com`)로 연결
- 카톡은 **refresh token 을 발급받을 때 로그인한 카카오 계정의 "나와의 채팅"** 으로 감 → 계정 바꾸려면 토큰만 다시 발급하면 됨
- 수동 실행 시 `days` 입력으로 수집 기간을 일 단위로 늘릴 수 있음 (테스트용. 비우면 실제와 같은 12시간)
- `get_token.py` 는 키를 붙여넣지 않고 **복사 후 엔터**하면 클립보드에서 읽음 (회사 PC 터미널에서 숨김 입력 붙여넣기가 안 돼서 변경)
- 회사 PC 는 git 로그인 창을 못 띄워 push 불가 → 10/14 변경분은 GitHub 웹 "Upload files" 로 반영함

## 2. 회사에서 할 일: 카카오 계정 바꾸기 (Windows)

### ① 준비 (처음 한 번)
PowerShell 에서:
```
winget install Python.Python.3.12 Git.Git GitHub.cli
```
설치 후 **PowerShell 을 새로 열고**:
```
gh auth login            # GitHub.com → HTTPS → 브라우저 로그인, 계정 oksbgpt009
gh repo clone oksbgpt009/sports-news-kakao
cd sports-news-kakao
pip install requests
```
(이 폴더를 USB 로 옮길 필요 없음. GitHub 에서 받으면 됨. Claude Code 도 이 `sports-news-kakao` 폴더에서 열 것)

### ② 방법 선택
**방법 A (간단, 먼저 시도)**: 지금 카카오 앱(ID 1606829, "병일" 계정 소유)을 그대로 쓰고, **토큰만 새 계정으로 발급**
- REST API 키·Client Secret 은 그대로 → GitHub Secret 도 그대로 둠
- 크롬에서 **기존 카카오 계정 로그아웃** 후 진행 (안 하면 기존 계정으로 자동 로그인됨. 시크릿 창 써도 됨)
- 동의 화면 대신 오류(KOE 코드)가 나면: 그 카카오 앱은 개인 개발 앱이라 다른 계정이 못 쓰는 경우 → 앱 소유 계정으로 developers.kakao.com 에서 **앱 → 멤버** 에 새 계정을 팀원으로 초대하거나, 방법 B 로

**방법 B (확실)**: 새 카카오 계정으로 developers.kakao.com 에 앱을 새로 만들고 아래 3장 설정을 그대로 반복
- 이 경우 `KAKAO_REST_API_KEY`, `KAKAO_CLIENT_SECRET` 도 새 값으로 다시 등록:
  ```
  gh secret set KAKAO_REST_API_KEY
  gh secret set KAKAO_CLIENT_SECRET
  ```
  (실행하면 값을 물어봄. 붙여넣고 엔터. Windows 콘솔은 오른쪽 클릭 또는 Ctrl+V 로 붙여넣기)

### ③ 토큰 발급 (A·B 공통)
```
python get_token.py
```
1. `카카오 REST API 키:` → 플랫폼 키의 **REST API 키** 붙여넣고 엔터 (화면에 안 보이는 게 정상)
2. `Client Secret:` → REST API 키 상세 화면 아래 **클라이언트 시크릿 → "카카오 로그인" 줄의 코드** (비즈니스 인증 코드 아님)
3. 출력된 `https://kauth.kakao.com/...` 주소를 브라우저에서 열고 **카톡 받을 새 계정**으로 로그인·동의
4. "사이트에 연결할 수 없음(localhost)" 화면이 정상. **주소창의 `code=` 뒤 값**만 복사 (`&` 가 있으면 그 앞까지). 1회용, 몇 분 안에 사용
5. `code:` 에 붙여넣고 엔터 → **"KAKAO_REFRESH_TOKEN 을 GitHub Secret 에 등록했습니다."** 가 나오면 끝 (gh 로 자동 등록되도록 고쳐둠)

⚠️ 10/13 실수: 주소창 `code` 값을 refresh token 자리에 넣어서 실패(KOE322). 이제 자동 등록이라 복사할 일 없음.
⚠️ `KOE010 Bad client credentials` = Client Secret 이 틀림 (빈칸, 비즈니스 인증 코드 등)

### ④ 테스트
```
gh workflow run daily-sports-news -f days=8
gh run watch
```
- 새 계정 카톡 "나와의 채팅" 에 메시지가 오면 성공. 기간 안에 기사가 없으면 안 오니 `days` 를 늘려볼 것
- 결과 로그: `gh run view --log` (마지막 실행). `카카오 토큰 갱신 실패: ...` 가 보이면 그 오류 코드 참고

---

## 3. 카카오 개발자 앱 설정값 (방법 B 때 그대로 반복)

developers.kakao.com → 앱 생성(앱 이름 `스포츠단 뉴스`, 회사명 `개인`, 카테고리 아무거나, 운영정책 체크박스는 본인이 체크) 후 왼쪽 메뉴:

| 메뉴 | 설정 |
|---|---|
| 제품 설정 → 카카오 로그인 → 일반 | 사용 설정 **ON** |
| 앱 → 플랫폼 키 → REST API 키 클릭 | 카카오 로그인 리다이렉트 URI: `https://localhost` → 저장. 이 화면에 REST API 키·클라이언트 시크릿(기본 ON) 있음 |
| 제품 설정 → 카카오 로그인 → 동의항목 | 접근권한 표 **카카오톡 메시지 전송(talk_message)** → 설정 → **선택 동의**, 목적 `뉴스 알림을 나에게 보내기 위함` → 저장 |
| 앱 → 제품 링크 관리 → 웹 도메인 | `https://n.news.naver.com`, `https://m.sports.naver.com`, `https://news.naver.com`, `https://search.naver.com`, `https://oksbgpt009.github.io` (등록 안 된 도메인 링크는 첫 번째 도메인 첫 화면으로 열림) |

(카카오 콘솔 메뉴 구조가 예전 문서와 다름: Redirect URI 는 "플랫폼 키" 안, 사이트 도메인은 "제품 링크 관리" 안)

## 4. 선택: GH_PAT (토큰 자동 갱신)

카카오 refresh token 은 약 2개월 유효. 만료 1개월 전부터 갱신 토큰이 내려오면 워크플로가 `GH_PAT` 로 Secret 을 자동 교체함. 없으면 2개월쯤 뒤 `python get_token.py` 를 다시 하면 됨.
- github.com → Settings → Developer settings → Fine-grained tokens → 저장소 `sports-news-kakao` 1개만, 권한 **Secrets: Read and write** 만
- `gh secret set GH_PAT` 로 등록

## 5. 파일

| 파일 | 내용 |
|---|---|
| `config.py` | 종목별 검색어·필터 (`queries`, `title_any`, `topic_any`) |
| `news.py` | 네이버 검색 페이지 파싱, 기간 필터 (`WINDOW_DAYS` 로 테스트 시 기간 확장) |
| `kakao.py` | 토큰 갱신(실패 시 카카오 오류 내용 출력), 나에게 보내기 (2~3건 리스트, 1건 텍스트) |
| `main.py` | 수집 → 전체 목록 페이지(`docs/`) 작성 → 기사 있는 종목만 전송. `--dry-run` 이면 전송 없이 출력. **발송 이력**: 로그에 기사 제목·링크 출력 + Actions 실행 요약(Summary) 화면에 표로 기록 (90일 보관) |
| `get_token.py` | refresh token 발급 + GitHub Secret 자동 등록 |
| `.github/workflows/daily-news.yml` | 매일 07:30, 수동 실행 시 `days` 입력 |

로컬 확인: `python main.py --dry-run` (카카오 키 없이 수집 결과만 출력)

## 6. 주의사항

- 네이버 검색 페이지 구조가 바뀌면 파싱이 깨질 수 있음 (`"templateId":"newsItem"`). 며칠 연속 아무것도 안 오면 `--dry-run` 의 `페이지 N자` 와 건수 확인
- 제목 기준 필터라 제목에 "OK"만 있는 기사(예: "OK 전광인…")는 빠짐
- 중복 방지 이력 없음 (기간이 하루씩 겹치지 않아 중복 가능성 낮음)
- 키·토큰은 채팅/파일/커밋/스크린샷에 남기지 않기. 비밀번호·키 입력은 본인이 직접
- 10/13 첫 발급 refresh token 이 스크린샷에 노출됨 (이후 새로 발급해 Secret 은 교체). 그 토큰만으론 REST 키·시크릿 없이 못 쓰지만, 계정 변경 시 기존 계정은 카카오 계정 설정 → 연결된 서비스에서 "스포츠단 뉴스" 연결 끊기 권장
