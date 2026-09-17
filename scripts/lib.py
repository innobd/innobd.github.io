"""공용 유틸: JSON 입출력, Claude 호출, 변경 요약 기록."""
import json
import os
import re
import unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "src" / "data"
PUBLIC = ROOT / "public"
SUMMARY_FILE = Path(os.environ.get("SYNC_SUMMARY_FILE", "/tmp/sync_summary.txt"))

CLAUDE_MODEL = os.environ.get("CLAUDE_MODEL", "claude-sonnet-4-6")


def load_json(name):
    p = DATA / f"{name}.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else []


def save_json(name, data):
    p = DATA / f"{name}.json"
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def slugify(text, maxlen=48):
    text = unicodedata.normalize("NFKD", text)
    text = re.sub(r"[^\w\s-]", "", text, flags=re.ASCII).strip().lower()
    text = re.sub(r"[\s_]+", "-", text)
    return text[:maxlen].strip("-") or date.today().isoformat()


def log_change(line):
    """Slack 알림용 변경 내역 한 줄 추가."""
    print("  +", line)
    SUMMARY_FILE.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_FILE.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def claude_json(system, user, max_tokens=2000):
    """Claude에게 JSON만 답하게 하고 파싱해서 돌려줍니다."""
    import anthropic

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system=system + "\n\nRespond with a single JSON object only. No markdown fences, no commentary.",
        messages=[{"role": "user", "content": user}],
    )
    text = "".join(b.text for b in msg.content if getattr(b, "type", "") == "text").strip()
    text = re.sub(r"^```(?:json)?|```$", "", text, flags=re.M).strip()
    return json.loads(text)
