import os
import sys

import kakao
import news
from config import ARTICLES_PER_CATEGORY, CATEGORIES


def main():
    dry_run = "--dry-run" in sys.argv  # 카톡 전송 없이 결과만 출력
    start, end = news.time_window()
    period = f"{start:%m/%d %H:%M}~{end:%m/%d %H:%M}"

    # 전송 중간에 실패해 일부만 가는 일이 없도록 수집을 먼저 모두 끝낸다
    results = [
        (f"{c['name']} | {period}", news.collect(c, start, end, ARTICLES_PER_CATEGORY))
        for c in CATEGORIES
    ]

    if dry_run:
        for header, articles in results:
            print(f"{header}: {len(articles)}건")
            for a in articles:
                print(f"  - [{a['published']:%m/%d %H:%M}] {a['title']}\n    {a['link']}")
        return

    # 기사가 없는 종목은 보내지 않음. 전부 없으면 아무것도 보내지 않고 종료
    sent = [(header, articles) for header, articles in results if articles]
    if sent:
        token = kakao.get_access_token()
        for header, articles in sent:
            kakao.send(token, kakao.build_template(header, articles))
    write_log(period, results)


def write_log(period, results):
    """발송 이력: 실행 로그에 출력하고, GitHub Actions 실행 요약 화면에도 표로 남김."""
    lines = [f"## 발송 이력 ({period})", "", "| 종목 | 기사 시각 | 제목 |", "|---|---|---|"]
    for header, articles in results:
        name = header.split(" | ")[0]
        print(f"{header}: {len(articles)}건 전송" if articles else f"{header}: 기사 없음, 전송 안 함")
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
