"""PubMed에서 새 논문을 찾아 publications.json에 추가합니다.

기본 검색식은 PUBMED_QUERY 환경변수로 바꿀 수 있습니다.
새로 추가된 논문은 selected=false 로 들어가며, 홈에 노출할 논문은 JSON에서 selected를 true로 바꿔주세요.
"""
import os
import re

import requests

from lib import load_json, log_change, save_json, slugify

QUERY = os.environ.get(
    "PUBMED_QUERY",
    'Byun J[Author] AND (Sookmyung[Affiliation] OR "Seoul National University"[Affiliation] OR Ghent[Affiliation]) AND (nanoparticle OR mRNA OR delivery OR hydrogel OR photoporation)',
)
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def main():
    pubs = load_json("publications")
    known_doi = {p.get("doi", "").lower() for p in pubs if p.get("doi")}
    known_pmid = {p.get("pmid") for p in pubs if p.get("pmid")}

    ids = requests.get(f"{EUTILS}/esearch.fcgi", params={"db": "pubmed", "term": QUERY, "retmax": 300, "retmode": "json"}, timeout=30).json()["esearchresult"]["idlist"]
    if not ids:
        print("pubmed: no results")
        return
    summ = requests.get(f"{EUTILS}/esummary.fcgi", params={"db": "pubmed", "id": ",".join(ids), "retmode": "json"}, timeout=60).json()["result"]

    added = 0
    for pmid in ids:
        if pmid in known_pmid:
            continue
        it = summ.get(pmid, {})
        doi = next((a["value"] for a in it.get("articleids", []) if a.get("idtype") == "doi"), "")
        if doi and doi.lower() in known_doi:
            continue
        year = int(re.match(r"\d{4}", it.get("pubdate", "") or it.get("epubdate", "") or "0").group())
        entry = {
            "id": slugify(doi or it["title"]),
            "pmid": pmid,
            "title": it.get("title", "").rstrip("."),
            "authors": ", ".join(a["name"] for a in it.get("authors", [])),
            "journal": it.get("source", ""),
            "year": year,
            "volume": it.get("volume", ""),
            "pages": it.get("pages", ""),
            "doi": doi,
            "pdf": "",
            "selected": False,
        }
        pubs.append(entry)
        log_change(f"Publication (PubMed): {entry['title']} ({entry['journal']} {year})")
        added += 1

    if added:
        pubs.sort(key=lambda p: (-int(p.get("year") or 0), p.get("title", "")))
        save_json("publications", pubs)
    print(f"pubmed: {added} new")


if __name__ == "__main__":
    main()
