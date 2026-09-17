"""변경 요약을 Slack 웹훅으로 보냅니다. 변경이 없으면 조용히 끝납니다."""
import os

import requests

from lib import SUMMARY_FILE

SITE_URL = os.environ.get("SITE_URL", "https://innobdlab.github.io")


def main():
    if not SUMMARY_FILE.exists() or not SUMMARY_FILE.read_text(encoding="utf-8").strip():
        print("no changes to report")
        return
    lines = [l for l in SUMMARY_FILE.read_text(encoding="utf-8").splitlines() if l.strip()]
    text = "*InnoBD Lab 웹사이트 업데이트*\n" + "\n".join(f"• {l}" for l in lines) + f"\n{SITE_URL}"
    url = os.environ.get("SLACK_WEBHOOK_URL")
    if not url:
        print(text)
        return
    requests.post(url, json={"text": text}, timeout=30).raise_for_status()
    print("slack notified")


if __name__ == "__main__":
    main()
