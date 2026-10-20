import html
import os
import sys

import kakao
import news
from config import ARTICLES_PER_CATEGORY, CATEGORIES, PAGES_URL


def main():
    dry_run = "--dry-run" in sys.argv  # 카톡 전송 없이 결과만 출력
    start, end = news.time_window()
    period = f"{start:%m/%d %H:%M}~{end:%m/%d %H:%M}"

    # 전송 중간에 실패해 일부만 가는 일이 없도록 수집을 먼저 모두 끝낸다
    results = [
        (f"{c['name']} | {period}", news.collect(c, start, end))
        for c in CATEGORIES
    ]

    if dry_run:
        for header, articles in results:
            print(f"{header}: {len(articles)}건")
            for a in articles:
                print(f"  - [{a['published']:%m/%d %H:%M}] {a['title']}\n    {a['link']}")
        return

    # 기사가 없는 종목은 보내지 않음. 전부 없으면 아무것도 보내지 않고 종료
    sent = [(i, header, articles) for i, (header, articles) in enumerate(results) if articles]
    if sent:
        page = write_page(start, end, period, results)
        token = kakao.get_access_token()
        for i, header, articles in sent:
            template = kakao.build_template(
                header, articles[:ARTICLES_PER_CATEGORY], f"{PAGES_URL}{page}#c{i}", len(articles))
            kakao.send(token, template)
    write_log(period, results)


def write_page(start, end, period, results):
    """카톡 '전체 N건 보기'가 여는 기간별 기사 전체 목록. docs/ 를 GitHub Pages 로 공개."""
    name = f"{end:%Y%m%d-%H}.html"
    parts = []
    for i, (header, articles) in enumerate(results):
        parts.append(f'<h2 id="c{i}">{html.escape(header.split(" | ")[0])} <small>{len(articles)}건</small></h2>')
        if not articles:
            parts.append('<p class="none">기사 없음</p>')
        for a in articles:
            parts.append(
                f'<a href="{html.escape(a["link"])}"><span>{a["published"]:%m/%d %H:%M}</span>'
                f'{html.escape(a["title"])}</a>')
    os.makedirs("docs", exist_ok=True)
    with open(os.path.join("docs", name), "w", encoding="utf-8") as f:
        f.write(f"""<!doctype html>
<html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>스포츠단 뉴스 {period}</title>
<style>
body {{ margin: 0 auto; max-width: 640px; padding: 16px; font-family: sans-serif; background: #fff; color: #222; }}
h1 {{ font-size: 18px; }} h2 {{ font-size: 16px; margin-top: 28px; }} small {{ color: #888; font-weight: normal; }}
a {{ display: block; padding: 12px 0; border-bottom: 1px solid #eee; color: #222; text-decoration: none; line-height: 1.4; }}
span {{ display: block; font-size: 12px; color: #888; }} .none {{ color: #888; }}
</style></head><body>
<h1>스포츠단 뉴스 {period}</h1>
{chr(10).join(parts)}
</body></html>
""")
    return name


def write_log(period, results):
    """발송 이력: 실행 로그에 출력하고, GitHub Actions 실행 요약 화면에도 표로 남김."""
    lines = [f"## 발송 이력 ({period})", "", "| 종목 | 기사 시각 | 제목 |", "|---|---|---|"]
    for header, articles in results:
        name = header.split(" | ")[0]
        print(f"{header}: {len(articles)}건 수집" if articles else f"{header}: 기사 없음, 전송 안 함")
        for a in articles:
            print(f"  - [{a['published']:%m/%d %H:%M}] {a['title']}\n    {a['link']}")
            title = a["title"].replace("|", "/")
            lines.append(f"| {name} | {a['published']:%m/%d %H:%M} | [{title}]({a['link']}) |")
        if not articles:
            lines.append(f"| {name} | - | 기사 없음 (전송 안 함) |")
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a", encoding="utf-8") as f:
            f.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
