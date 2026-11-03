#!/usr/bin/env python3
"""네이버 블로그 글을 가져와 트립닷컴 앱에 붙여넣기 좋은 형태로 저장한다.

사용법:
  python naver2trip.py BLOG_ID              # 최근 글 목록 (RSS) 보기
  python naver2trip.py BLOG_ID --all        # 목록의 모든 글 변환
  python naver2trip.py BLOG_ID --post LOGNO # 특정 글 하나만 변환
  python naver2trip.py --html 파일.html     # 저장해 둔 HTML로 변환 (테스트용)

결과: out/<글번호>/title.txt, body.txt, images/01.jpg ...
이미 변환한 글은 건너뛴다 (out/.done). 올리기는 직접 한다.
"""
import argparse
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

UA = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15"}
OUT = Path("out")
TITLE_MAX = 40  # 앱 제목 칸이 짧아서 자른다. 필요하면 조절.


def fetch(url, binary=False):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    return data if binary else data.decode("utf-8", errors="replace")


def list_posts(blog_id):
    """RSS에서 (logNo, 제목, 링크) 목록을 가져온다."""
    root = ET.fromstring(fetch(f"https://rss.blog.naver.com/{blog_id}.xml"))
    posts = []
    for item in root.iter("item"):
        link = (item.findtext("link") or "").strip()
        m = re.search(r"/(\d{6,})", link)
        if m:
            posts.append((m.group(1), (item.findtext("title") or "").strip(), link))
    return posts


class PostParser(HTMLParser):
    """스마트에디터(se-main-container) 본문에서 텍스트와 이미지 URL을 뽑는다."""

    BLOCK = {"p", "div", "br", "li", "h1", "h2", "h3", "h4"}

    def __init__(self):
        super().__init__()
        self.depth = 0  # se-main-container 안에 있는지
        self.title = ""
        self._in_title = 0
        self.lines = [""]
        self.images = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        cls = a.get("class", "") or ""
        if self.depth:
            if tag == "div":
                self.depth += 1
            if tag == "img":
                src = a.get("data-lazy-src") or a.get("src") or ""
                # 스티커·이모티콘·아이콘 제외
                if src.startswith("http") and "storep-phinf" not in src and "ssl.pstatic.net/static" not in src:
                    self.images.append(src.split("?")[0] + "?type=w966")
                    self.lines.append("[사진]")
                    self.lines.append("")
            elif tag in self.BLOCK:
                self.lines.append("")
        elif tag == "div" and "se-main-container" in cls:
            self.depth = 1
        if "se-title-text" in cls:
            self._in_title = 1

    def handle_endtag(self, tag):
        if self.depth and tag == "div":
            self.depth -= 1
        if self._in_title and tag in ("div", "span", "p"):
            pass

    def handle_data(self, data):
        if self._in_title and not self.title.strip():
            self.title += data
        if self.depth and data.strip():
            self.lines[-1] += data.strip()
            self.lines[-1] += " "


def clean_body(lines):
    text = "\n".join(l.rstrip() for l in lines)
    text = text.replace("​", "")
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def convert(html, fallback_title, dest):
    p = PostParser()
    p.feed(html)
    title = (p.title.strip() or fallback_title or "제목 없음")
    title = re.sub(r"\s+", " ", title)[:TITLE_MAX]
    body = clean_body(p.lines)
    if not body and not p.images:
        raise ValueError("본문을 찾지 못했습니다 (비공개 글이거나 구버전 에디터일 수 있음)")
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "title.txt").write_text(title + "\n", encoding="utf-8")
    (dest / "body.txt").write_text(body + "\n", encoding="utf-8")
    return title, body, p.images


def download_images(urls, dest):
    img_dir = dest / "images"
    img_dir.mkdir(exist_ok=True)
    for i, u in enumerate(urls, 1):
        try:
            (img_dir / f"{i:02d}.jpg").write_bytes(fetch(u, binary=True))
        except Exception as e:  # 한 장 실패해도 계속
            print(f"  ! 이미지 {i} 실패: {e}", file=sys.stderr)


def process(blog_id, log_no, title_hint):
    done_file = OUT / ".done"
    done = set(done_file.read_text().split()) if done_file.exists() else set()
    if log_no in done:
        print(f"- {log_no} 이미 변환됨, 건너뜀")
        return
    url = f"https://blog.naver.com/PostView.naver?blogId={blog_id}&logNo={log_no}&redirect=Dlog&widgetTypeCall=true"
    dest = OUT / log_no
    title, body, imgs = convert(fetch(url), title_hint, dest)
    download_images(imgs, dest)
    OUT.mkdir(exist_ok=True)
    with done_file.open("a") as f:
        f.write(log_no + "\n")
    print(f"✓ {log_no} '{title}' (본문 {len(body)}자, 사진 {len(imgs)}장) -> {dest}/")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("blog_id", nargs="?")
    ap.add_argument("--all", action="store_true")
    ap.add_argument("--post")
    ap.add_argument("--html", help="저장한 HTML 파일로 변환 (오프라인 테스트)")
    a = ap.parse_args()

    if a.html:
        t, b, imgs = convert(Path(a.html).read_text(encoding="utf-8"), "", OUT / "local")
        print(f"제목: {t}\n본문 {len(b)}자, 사진 {len(imgs)}장 -> {OUT/'local'}/")
        return
    if not a.blog_id:
        ap.error("BLOG_ID가 필요합니다")
    if a.post:
        process(a.blog_id, a.post, "")
        return
    posts = list_posts(a.blog_id)
    if a.all:
        for no, title, _ in posts:
            try:
                process(a.blog_id, no, title)
            except Exception as e:
                print(f"! {no} 실패: {e}", file=sys.stderr)
    else:
        for no, title, _ in posts:
            print(f"{no}  {title}")
        print("\n변환하려면 --post 글번호 또는 --all")


if __name__ == "__main__":
    main()
