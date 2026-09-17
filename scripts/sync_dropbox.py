"""Dropbox inbox 폴더를 읽어 사이트 데이터에 반영합니다.

폴더 구조 (Dropbox):
  /InnoBD_Website/inbox/       <- 여기에 메모(.md .txt)나 사진(.jpg .png)을 넣습니다
  /InnoBD_Website/processed/   <- 처리된 파일은 월별 폴더로 이동

파일 이름 규칙 (선택):
  member_<id>.jpg    -> public/images/members/<id>.jpg 로 저장되고 해당 멤버 photo 필드가 갱신됩니다
  news_<anything>.jpg -> public/images/news/ 로 저장
  그 외 텍스트 파일    -> 내용을 Claude가 읽고 news / member / publication / research 로 분류

필요한 환경변수: DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN, ANTHROPIC_API_KEY
"""
import json
import os
from datetime import date

import requests

from ingest import ingest_text
from lib import PUBLIC, load_json, log_change, save_json

INBOX = os.environ.get("DROPBOX_INBOX", "/InnoBD_Website/inbox")
PROCESSED = os.environ.get("DROPBOX_PROCESSED", "/InnoBD_Website/processed")
TEXT_EXT = {".md", ".txt", ".markdown"}
IMG_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def access_token():
    r = requests.post(
        "https://api.dropboxapi.com/oauth2/token",
        data={
            "grant_type": "refresh_token",
            "refresh_token": os.environ["DROPBOX_REFRESH_TOKEN"],
            "client_id": os.environ["DROPBOX_APP_KEY"],
            "client_secret": os.environ["DROPBOX_APP_SECRET"],
        },
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["access_token"]


class Dropbox:
    def __init__(self):
        self.h = {"Authorization": f"Bearer {access_token()}"}

    def list_files(self, path):
        r = requests.post("https://api.dropboxapi.com/2/files/list_folder", headers=self.h, json={"path": path}, timeout=30)
        if r.status_code == 409:  # 폴더 없음
            return []
        r.raise_for_status()
        return [e for e in r.json()["entries"] if e[".tag"] == "file"]

    def download(self, path) -> bytes:
        r = requests.post(
            "https://content.dropboxapi.com/2/files/download",
            headers={**self.h, "Dropbox-API-Arg": json.dumps({"path": path})},
            timeout=120,
        )
        r.raise_for_status()
        return r.content

    def move(self, src, dst):
        requests.post(
            "https://api.dropboxapi.com/2/files/move_v2",
            headers=self.h,
            json={"from_path": src, "to_path": dst, "autorename": True},
            timeout=30,
        ).raise_for_status()


def handle_image(name, data):
    stem, ext = os.path.splitext(name.lower())
    if stem.startswith("member_"):
        member_id = stem[len("member_"):]
        out = PUBLIC / "images" / "members" / f"{member_id}{ext}"
        out.write_bytes(data)
        members = load_json("members")
        hit = False
        for m in members:
            if m["id"] == member_id:
                m["photo"] = f"/images/members/{member_id}{ext}"
                hit = True
        save_json("members", members)
        log_change(f"Photo: {member_id}" + ("" if hit else " (member id not found, file saved only)"))
    else:
        out = PUBLIC / "images" / "news" / name
        out.write_bytes(data)
        log_change(f"Image saved: /images/news/{name}")


def main():
    dbx = Dropbox()
    files = dbx.list_files(INBOX)
    if not files:
        print("inbox empty")
        return
    month_dir = f"{PROCESSED}/{date.today():%Y-%m}"
    for f in files:
        name = f["name"]
        ext = os.path.splitext(name.lower())[1]
        print(f"processing {name}")
        try:
            data = dbx.download(f["path_lower"])
            if ext in IMG_EXT:
                handle_image(name, data)
            elif ext in TEXT_EXT:
                ingest_text(data.decode("utf-8", errors="replace"), source=f"dropbox:{name}")
            else:
                print("  unsupported type, leaving in inbox")
                continue
            dbx.move(f["path_lower"], f"{month_dir}/{name}")
        except Exception as e:
            print(f"  failed: {e}")


if __name__ == "__main__":
    main()
