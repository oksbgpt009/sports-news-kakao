# OK AI 디자인 시스템 (Design System)

> **AI Visit / 방문동선 자동화** 에서 사용한 색상·타이포·컴포넌트 규칙을 정리한 문서.
> 새 앱을 만들 때 이 문서의 토큰과 CSS 스니펫을 그대로 가져다 쓰면 동일한 디자인이 나옵니다.
>
> 두 가지 톤을 함께 담았습니다.
> - **App 톤 (다크)** — 실제 프로그램 화면. 검정 헤더/사이드바 + 오렌지 포인트.
> - **Doc 톤 (라이트/인쇄)** — 매뉴얼·문서·리포트. 흰 배경 + 오렌지 포인트.
>
> 둘은 **같은 색·같은 폰트·같은 라운드/그림자 언어**를 공유합니다. 배경 명도만 다릅니다.

---

## 1. 디자인 원칙 (5가지)

1. **오렌지는 포인트로만.** `#FF6B00` 은 강조·주요 액션·현재 상태에만. 면적을 넓게 칠하지 않는다.
2. **면은 검정 계열 그라데이션, 텍스트는 흰색.** 앱의 헤더/사이드바/결과바는 `#333→#232323` 그라데이션.
3. **모서리는 둥글게, 그림자는 부드럽게.** 카드 12–14px, 버튼/입력 9–13px, pill/배지 999px.
4. **숫자는 표(表) 정렬.** 수치·시간·통계는 `font-variant-numeric: tabular-nums`.
5. **상태색은 의미로 고정.** 초록=정상/완료, 빨강=위험/삭제, 앰버=주의, 파랑=정보.

---

## 2. 색상 토큰 (Color Tokens)

CSS 변수로 그대로 복사해서 쓰세요. (App/Doc 공통)

```css
:root {
  /* ── 브랜드 포인트 ── */
  --accent:       #FF6B00;   /* OK 오렌지 (주 강조) */
  --accent-2:     #FF8C3A;   /* 밝은 오렌지 (보조·호버·그라데이션 끝) */
  --accent-soft:  rgba(255, 107, 0, 0.10);  /* 오렌지 배경 틴트 */

  /* ── 뉴트럴 (텍스트/배경) ── */
  --ink:       #0E1726;   /* 본문 진한 글자 (라이트 배경) */
  --ink-soft:  #4A5468;   /* 보조 글자 */
  --muted:     #8A94A6;   /* 흐린 라벨·캡션 */
  --line:      #E4E7EC;   /* 라이트 경계선 */
  --line-dark: #3A3A3A;   /* 다크 경계선 */

  /* ── 배경/면 ── */
  --bg:        #F4F5F7;   /* 라이트 페이지 배경 */
  --panel:     #FFFFFF;   /* 카드/패널 흰 면 */
  --dark:      #2C2C2C;   /* 다크 면 기준색 */

  /* ── 상태색 (의미 고정) ── */
  --green: #22C55E;   /* 정상·완료·정확 */
  --red:   #EF4444;   /* 위험·삭제·오류 */
  --amber: #F59E0B;   /* 주의·경고 */
  --blue:  #3B82F6;   /* 정보 */

  /* ── 그라데이션 ── */
  --grad-dark:   linear-gradient(135deg, #333333 0%, #232323 100%);  /* 헤더·사이드바·결과바 */
  --grad-accent: linear-gradient(135deg, #FF6B00 0%, #FF8C3A 100%);  /* 주요 버튼·현재상태 */
  --grad-panel:  linear-gradient(180deg, #FFFFFF 0%, #FBFCFE 100%);  /* 흰 카드 미세 그라데이션 */

  /* ── 그림자 ── */
  --shadow-card: 0 6px 22px rgba(15, 23, 42, 0.06);
  --shadow-soft: 0 2px 10px rgba(15, 23, 42, 0.04);
}
```

### 부가 색 (하드코딩되는 값들)

| 용도 | 값 |
|---|---|
| 오렌지 틴트 배경 (배지) | `#FFF1E3` / 글자 `#C2410C` / 테두리 `#FFD7B0` |
| 정보 박스 (tip) | 배경 `#eef4ff` / 테두리 `#cfe0ff` / 글자 `#1e3a63` |
| 경고 박스 (warn) | 배경 `#fff5f5` / 테두리 `#ffd0d0` / 글자 `#7a1f1f` |
| 성공 박스 (ok) | 배경 `#f0fdf4` / 테두리 `#bbf7d0` / 글자 `#14532d` |
| 다크 카드 면 | `linear-gradient(160deg, #3C3C3C 0%, #272727 100%)` |
| 다크 입력창 배경 | `#1f1f1f` |
| 네이버 그린 (지도/길안내) | `#03C75A` |
| 코드 글자색 | `#b4460b` (배경 `#f1f3f7`) |

> **규칙:** 위 값들도 되도록 변수로 승격해서 쓰되, 톤(orange 틴트, tip/warn/ok)은 세트로 유지하세요.

---

## 3. 타이포그래피 (Typography)

### 폰트

```css
/* App 톤 — Pretendard (권장) */
@import url('https://cdn.jsdelivr.net/gh/orioncactus/pretendard/dist/web/variable/pretendardvariable-dynamic-subset.css');

font-family: "Pretendard Variable", Pretendard, -apple-system, BlinkMacSystemFont,
  "Apple SD Gothic Neo", "Segoe UI", "Malgun Gothic", "맑은 고딕", sans-serif;
```

```css
/* Doc/인쇄 톤 — 시스템 폰트 (오프라인 안정) */
font-family: "Malgun Gothic", "맑은 고딕", -apple-system, "Segoe UI", sans-serif;
```

> 온라인 앱은 **Pretendard**, 배포 문서·PDF는 **맑은 고딕**을 기본으로. 둘 다 `-webkit-font-smoothing: antialiased` 권장.

### 스케일

| 역할 | 크기 / 굵기 | 비고 |
|---|---|---|
| 본문 | 14px / 400, line-height 1.5 | App 기본 |
| 문서 본문 | 13.5px / 400, line-height 1.6 | Doc 기본 |
| 큰 통계 숫자 | 26–30px / 900 | `tabular-nums`, letter-spacing -0.02em |
| 섹션 제목 h2 | 19px / 800 | 다크 배경 + 오렌지 좌측 바 |
| 소제목 h3 | 15px / 800 | |
| 라벨/캡션 | 10–11px / 700 | `letter-spacing 0.05~0.18em`, 대문자 라벨은 `text-transform: uppercase` |
| 배지/pill | 9–12px / 800 | |

**강조 색 글자:** 브랜드명·현재값은 `.em { color: var(--accent); }`. 진한 강조는 `b/strong { color: #16202e; }`.

---

## 4. 형태 언어 (Shape · Radius · Shadow)

| 요소 | radius | 그림자 |
|---|---|---|
| 카드/패널 | 12–14px | `--shadow-card` 또는 `0 6px 18px rgba(0,0,0,.22)` (다크) |
| 버튼 | 12–13px | `0 8px 22px rgba(255,107,0,.36)` (accent) |
| 입력창 | 9px | 없음 (focus 시 `border-color: var(--accent)`) |
| pill / 배지 / 상태칩 | 999px | 없음~soft |
| 모달 | 18px | `0 24px 60px rgba(0,0,0,.4)` |
| 아이콘 뱃지(로고칸) | 11–22px | `0 4px 12px rgba(255,107,0,.28)` |
| 순번 원형(seq) | 50% 또는 7–9px | `0 3px 8px rgba(0,0,0,.3)` |

**포인트 좌측 바:** 리스트 항목·섹션 제목은 `border-left: 3~5px solid var(--accent)` 로 오렌지 액센트.

**전환(transition):** 상호작용 요소는 `transition: all .15s`. 호버는 `filter: brightness(1.05)` 또는 `transform: translateY(-1px)`.

---

## 5. 핵심 컴포넌트 (복붙용 CSS)

### 5.1 헤더 (다크 + 오렌지 경계)

```css
.header {
  height: 64px; background: var(--grad-dark); color: #fff;
  display: flex; align-items: center; justify-content: space-between; padding: 0 28px;
  box-shadow: 0 4px 18px rgba(0,0,0,0.18);
  border-bottom: 1px solid rgba(255,107,0,0.35);
}
/* 로고칸: 흰 배경 위 아이콘 */
.brand-mark { height:40px; width:40px; display:grid; place-items:center;
  background:#fff; border-radius:11px; padding:5px; box-shadow:0 4px 12px rgba(255,107,0,0.28); }
.brand-text .name .em { color: var(--accent); }   /* 브랜드명 일부만 오렌지 */
```

### 5.2 주요 버튼 (Primary / Light)

```css
.btn { border:none; padding:12px 22px; font-size:13px; font-weight:800; cursor:pointer;
  border-radius:12px; transition:all .15s; font-family:inherit; }
.btn.accent { background: var(--grad-accent); color:#fff; box-shadow:0 6px 18px rgba(255,107,0,0.4); }
.btn.accent:hover { filter: brightness(1.05); }
.btn.light  { background:#fff; color: var(--ink); }
.btn.light:hover { background:#f1f3f6; }
/* 강조 펄스(선택) */
.pulse { animation: pulse 2.2s infinite; }
@keyframes pulse { 0%,100%{box-shadow:0 6px 18px rgba(255,107,0,.4);} 50%{box-shadow:0 6px 26px rgba(255,107,0,.7);} }
```

### 5.3 Pill / 배지 / 상태칩

```css
/* 헤더 pill */
.pill { background: rgba(255,255,255,0.08); color:#fff; border:1px solid var(--line-dark);
  padding:8px 16px; border-radius:999px; font-size:12px; font-weight:700;
  display:inline-flex; align-items:center; gap:8px; cursor:pointer; transition:all .15s; }
.pill.accent { background: var(--grad-accent); border-color:transparent; box-shadow:0 4px 14px rgba(255,107,0,0.4); }
.pill .dot { width:7px; height:7px; border-radius:50%; background:var(--green); box-shadow:0 0 0 3px rgba(34,197,94,0.2); }

/* 오렌지 틴트 배지 (개수·태그) */
.tag { display:inline-block; background:#FFF1E3; color:#C2410C; border:1px solid #FFD7B0;
  font-size:11.5px; font-weight:800; padding:1px 8px; border-radius:999px; }
```

### 5.4 데이터 카드 (다크 · 통계)

```css
.data-card { background: linear-gradient(160deg,#3C3C3C 0%,#272727 100%);
  border:1px solid var(--line-dark); border-radius:14px; padding:16px 18px;
  position:relative; overflow:hidden; box-shadow:0 6px 18px rgba(0,0,0,0.22); }
/* 우상단 오렌지 광원 */
.data-card::before { content:""; position:absolute; right:-30px; top:-30px; width:120px; height:120px;
  background: radial-gradient(circle, rgba(255,107,0,0.45) 0%, transparent 70%); opacity:0.55; }
.data-card .big { font-size:30px; font-weight:900; color:#fff; font-variant-numeric:tabular-nums; }
.data-card .big.accent { background: var(--grad-accent); -webkit-background-clip:text; background-clip:text; color:transparent; }
```

### 5.5 입력창 (다크 폼)

```css
input, select { background:#1f1f1f; color:#fff; border:1px solid var(--line-dark);
  border-radius:9px; padding:9px 11px; font-size:13px; font-family:inherit; }
input:focus, select:focus { outline:none; border-color: var(--accent); }
input[type=checkbox] { accent-color: var(--accent); }
```

### 5.6 선택 버튼 (토글 / on 상태)

```css
.mode-btn { width:100%; padding:12px 14px; border-radius:12px; border:1px solid var(--line-dark);
  background: linear-gradient(160deg, rgba(255,255,255,0.04), rgba(255,255,255,0.01));
  color:#C5C5C5; font-weight:600; cursor:pointer; transition:all .15s; font-family:inherit; }
.mode-btn.on { border-color: var(--accent); color:#fff;
  background: linear-gradient(135deg, rgba(255,107,0,0.18), rgba(255,107,0,0.04));
  box-shadow: 0 4px 14px rgba(255,107,0,0.18); }
```

### 5.7 모달 · 토스트

```css
.modal-backdrop { position:fixed; inset:0; background:rgba(0,0,0,0.6); z-index:200;
  display:none; align-items:center; justify-content:center; }
.modal-backdrop.show { display:flex; }
.modal { background:#fff; border-radius:18px; padding:24px; max-width:480px; width:calc(100% - 32px);
  box-shadow:0 24px 60px rgba(0,0,0,0.4); }

.toast { position:fixed; bottom:90px; left:50%; transform:translateX(-50%);
  background:#1f1f1f; color:#fff; border:1px solid var(--line-dark);
  padding:12px 22px; border-radius:999px; font-size:12px; font-weight:700;
  box-shadow:0 12px 30px rgba(0,0,0,0.35); z-index:300; }
```

### 5.8 정보 박스 (tip / warn / ok) — 문서·안내용

```css
.tip  { background:#eef4ff; border:1px solid #cfe0ff; border-radius:10px; padding:10px 14px; color:#1e3a63; }
.warn { background:#fff5f5; border:1px solid #ffd0d0; border-radius:10px; padding:10px 14px; color:#7a1f1f; }
.ok   { background:#f0fdf4; border:1px solid #bbf7d0; border-radius:10px; padding:10px 14px; color:#14532d; }
```

---

## 6. 레이아웃 (App 톤)

```css
.app { display:grid; grid-template-columns:320px 1fr; height:calc(100vh - 64px); }
.sidebar { background: var(--grad-dark); color:#D4D4D4; }   /* 좌측 다크 사이드바 320px */
.main { position:relative; overflow:hidden; }              /* 우측 컨텐츠/지도 영역 */
```

- **헤더 64px 고정** → 아래 `320px 사이드바 + 나머지 컨텐츠` 2단.
- 스크롤바도 톤 맞춤: `::-webkit-scrollbar-thumb { background:#4a4a4a; border-radius:10px; }`
- **반응형(≤768px):** 1단 전환, 상단 탭(`.mobile-tabs`)으로 목록/지도 스위치. (앱을 웹으로 확장할 때만)

### 문서(Doc) 톤 페이지

```css
@page { size: A4; margin: 14mm; }
.page { width:210mm; min-height:297mm; margin:0 auto 8mm; background:#fff;
  padding:18mm 16mm; box-shadow:0 2px 12px rgba(0,0,0,.08); }
h2 { background: var(--grad-dark); color:#fff; border-radius:10px;
  border-left:5px solid var(--accent); padding:9px 14px; }
h2 .n { color: var(--accent-2); margin-right:8px; }   /* 섹션 번호 오렌지 */
@media print { body{background:#fff;} .page{margin:0; box-shadow:none;} .page + .page{page-break-before:always;} }
```

---

## 7. 상태색 사용 규칙

| 색 | 변수 | 쓰는 곳 | 안 쓰는 곳 |
|---|---|---|---|
| 오렌지 | `--accent` | 주요 버튼, 현재 선택, 브랜드 강조, 좌측 액센트 바 | 본문 대량 텍스트, 넓은 배경 |
| 초록 | `--green` | 정상 상태 dot, 완료, "정확" 배지, 식사 행 | 삭제/경고 |
| 빨강 | `--red` | 삭제 버튼, 오류 메시지, 위험 우선순위 | 일반 강조 |
| 앰버 | `--amber` | 주의·프로토타입 배너 | 정상 상태 |
| 파랑 | `--blue` | 정보 링크·tip 계열 | 액션 버튼(오렌지 사용) |

> 우선순위/등급 뱃지처럼 여러 색을 나열할 때: **1순위=오렌지, 위험=빨강, 보통=muted, 낮음=`--accent-2`** 순으로.

---

## 8. 새 앱에 적용하는 법 (체크리스트)

1. `:root` 토큰 블록(2장)을 새 프로젝트 CSS 맨 위에 복사.
2. 폰트 import + `font-family` 지정 (App=Pretendard / Doc=맑은 고딕).
3. 헤더는 `--grad-dark` + 오렌지 하단 경계(5.1), 로고는 흰 칸에.
4. 주요 액션 1개만 `.btn.accent`(오렌지), 나머지는 `.btn.light`.
5. 통계/수치는 다크 `.data-card` + `tabular-nums`.
6. 상태는 7장 규칙대로 색 고정.
7. 라운드/그림자는 4장 표 값 사용 — **임의값 쓰지 말 것.**
8. 오렌지 면적이 넓어졌다 싶으면 줄인다 (원칙 1).

---

## 9. 자산 (Assets)

| 파일 | 용도 |
|---|---|
| `ok-icon.png` | 브랜드 아이콘 (헤더 로고칸·표지·favicon 공용). 흰 배경 칸 위에 얹어 사용. |
| `theme-color` | `#FF6B00` (모바일 브라우저 상단바) |

---

*이 문서는 AI Visit v0.3.0의 `public/index.html` 및 배포 매뉴얼 HTML에서 실제 사용된 값을 추출해 정리한 것입니다. 값을 바꾸면 이 문서도 함께 갱신하세요.*
