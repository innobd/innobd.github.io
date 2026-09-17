"""Slack 채널의 명령 메시지를 읽어 사이트 데이터에 반영합니다.

사용법 (Slack #website 채널에서):
  !news 구현서 학생이 KOGO 2026에서 우수 포스터상을 받았습니다
  !member 박하현 석사과정 신규 합류
  !pub 10.1016/j.jconrel.2026.01.001
  !research 광천공 요약을 "..." 로 수정

처리된 메시지에는 봇이 ✅ 반응을 남깁니다.
필요한 환경변수: SLACK_BOT_TOKEN (chat:write, channels:history, reactions:write), SLACK_CHANNEL_ID, ANTHROPIC_API_KEY
"""
import json
import os
from pathlib import Path

import requests

from ingest import ingest_text

STATE = Path(__file__).with_name("state.json")
PREFIXES = ("!news", "!member", "!pub", "!research", "!site")


def api(method, **params):
    r = requests.post(
        f"https://slack.com/api/{method}",
        headers={"Authorization": f"Bearer {os.environ['SLACK_BOT_TOKEN']}"},
        json=params,
        timeout=30,
    )
    r.raise_for_status()
    body = r.json()
    if not body.get("ok"):
        raise RuntimeError(f"{method}: {body.get('error')}")
    return body


def main():
    channel = os.environ["SLACK_CHANNEL_ID"]
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    oldest = state.get("last_ts", "0")

    res = api("conversations.history", channel=channel, oldest=oldest, inclusive=False, limit=100)
    messages = sorted(res.get("messages", []), key=lambda m: float(m["ts"]))
    if not messages:
        print("no new slack messages")
        return

    for m in messages:
        text = (m.get("text") or "").strip()
        if m.get("bot_id") or not text.lower().startswith(PREFIXES):
            continue
        cmd, _, body = text.partition(" ")
        print(f"processing slack {m['ts']}: {text[:60]}")
        try:
            line = ingest_text(f"[{cmd[1:]}] {body}", source="slack")
            api("reactions.add", channel=channel, timestamp=m["ts"], name="white_check_mark" if line else "grey_question")
        except Exception as e:
            print(f"  failed: {e}")
            api("chat.postMessage", channel=channel, thread_ts=m["ts"], text=f"처리 실패: {e}")

    state["last_ts"] = messages[-1]["ts"]
    STATE.write_text(json.dumps(state))


if __name__ == "__main__":
    main()
