"""자유 형식 메모(한국어/영어)를 사이트 데이터 항목으로 바꾸어 병합합니다.

Dropbox inbox 파일, Slack 메시지 모두 이 함수 하나를 거칩니다.
Claude가 종류를 판별하고 (news / member / publication / research)
한영 필드를 채운 뒤, 해당 JSON 파일에 추가 또는 갱신합니다.
"""
import json
from datetime import date

from lib import claude_json, load_json, log_change, save_json, slugify

SYSTEM = """You maintain the data files of a pharmacy research lab website (InnoBD Lab,
Laboratory of Innovative Biopharmaceutical Delivery, Sookmyung Women's University, PI Junho Byun).
You receive a short note written by a lab member in Korean or English and convert it into one entry.

Decide the kind and fill BOTH languages naturally (translate, do not transliterate). Write plainly.
Do not use em dashes or middle dots. Keep the original meaning; never invent facts not in the note.
If the note gives no date, use today's date provided.

Return exactly one of these shapes:

{"kind":"news","entry":{"id":"<slug>","date":"YYYY-MM-DD","type":"grant|honor|talk|paper|news",
  "text":{"en":"...","ko":"..."},"link":"<url or empty>"}}

{"kind":"member","action":"add|update|alumni","entry":{"id":"<firstname-lastname>","role":"pi|postdoc|phd|ms|undergrad|alumni",
  "name":{"en":"...","ko":"..."},"title":{"en":"...","ko":"..."},"photo":"","email":""}}

{"kind":"publication","entry":{"id":"<slug>","title":"...","authors":"Last F, Last F, ...","journal":"...",
  "year":2026,"volume":"","pages":"","doi":"","pdf":"","selected":false}}

{"kind":"research","action":"add|update","entry":{"id":"<slug>","track":"platform|method",
  "title":{"en":"...","ko":"..."},"summary":{"en":"...","ko":"..."},"keywords":[]}}

If the note is not usable, return {"kind":"skip","reason":"..."}."""


def ingest_text(note: str, source: str) -> str | None:
    """메모 하나를 처리하고 결과 요약 문자열을 반환합니다 (skip이면 None)."""
    members = load_json("members")
    context = {
        "today": date.today().isoformat(),
        "existing_member_ids": [m["id"] for m in members],
        "existing_research_ids": [r["id"] for r in load_json("research")],
    }
    result = claude_json(SYSTEM, f"Context: {json.dumps(context, ensure_ascii=False)}\n\nNote from {source}:\n{note}")
    kind = result.get("kind")
    entry = result.get("entry", {})

    if kind == "skip":
        print(f"  skip ({source}): {result.get('reason')}")
        return None

    if kind == "news":
        items = load_json("news")
        entry["id"] = entry.get("id") or slugify(f"{entry['date']}-{entry['text']['en']}")
        items = [n for n in items if n["id"] != entry["id"]] + [entry]
        save_json("news", items)
        line = f"News: {entry['text']['ko']}"

    elif kind == "member":
        action = result.get("action", "add")
        if action == "alumni":
            for m in members:
                if m["id"] == entry["id"]:
                    m["role"] = "alumni"
            line = f"Member -> alumni: {entry['id']}"
        else:
            members = [m for m in members if m["id"] != entry["id"]] + [entry]
            line = f"Member {action}: {entry['name']['ko']} ({entry['title']['ko']})"
        save_json("members", members)

    elif kind == "publication":
        pubs = load_json("publications")
        if entry.get("doi"):
            entry = _enrich_from_crossref(entry)
        entry["id"] = entry.get("id") or slugify(entry.get("doi") or entry["title"])
        pubs = [p for p in pubs if p["id"] != entry["id"]] + [entry]
        save_json("publications", pubs)
        line = f"Publication: {entry['title']} ({entry['journal']} {entry['year']})"

    elif kind == "research":
        items = load_json("research")
        items = [r for r in items if r["id"] != entry["id"]] + [entry]
        save_json("research", items)
        line = f"Research: {entry['title']['ko']}"

    else:
        print(f"  unknown kind from Claude: {kind}")
        return None

    log_change(line)
    return line


def _enrich_from_crossref(entry):
    """DOI가 있으면 Crossref에서 정확한 서지정보를 받아 채웁니다."""
    import requests

    try:
        r = requests.get(f"https://api.crossref.org/works/{entry['doi']}", timeout=20)
        r.raise_for_status()
        w = r.json()["message"]
        entry["title"] = entry.get("title") or (w.get("title") or [""])[0]
        entry["journal"] = (w.get("container-title") or [entry.get("journal", "")])[0]
        entry["year"] = (w.get("issued", {}).get("date-parts") or [[entry.get("year")]])[0][0]
        entry["volume"] = w.get("volume", entry.get("volume", ""))
        entry["pages"] = w.get("page", entry.get("pages", ""))
        if w.get("author"):
            entry["authors"] = ", ".join(
                f"{a.get('family','')} {''.join(p[0] for p in a.get('given','').split())}".strip() for a in w["author"]
            )
    except Exception as e:  # 실패해도 Claude가 채운 값으로 진행
        print(f"  crossref lookup failed: {e}")
    return entry
