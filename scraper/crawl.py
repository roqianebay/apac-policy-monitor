#!/usr/bin/env python3
"""Biweekly APAC employer-policy crawler.

Reads public RSS (agency feeds + Google News site-restricted RSS),
classifies items, merges with the baseline dashboard dataset, and
writes web/data/policies.json for the local site.
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_lib
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

try:
    import feedparser
except ImportError:
    print("Missing dependencies. Run: python -m pip install -r requirements.txt", file=sys.stderr)
    raise

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "web" / "data" / "policies.json"
LOG = ROOT / "web" / "data" / "crawl-log.json"
INTERVAL_DAYS = 14
UA = "APAC-Policy-Monitor/1.0 (local biweekly research crawler; +https://localhost)"
MAX_NEW_PER_SOURCE = 8
MAX_TOTAL = 160
RELEVANT = (
    "employ", "labour", "labor", "wage", "payroll", "visa", "permit",
    "cpf", "epf", "superannuat", "leave", "contract", "dismiss",
    "redundan", "worker", "workplace", "osha", "ohs", "immigration",
    "minimum", "pension", "insurance", "gig", "ai ", "recruit",
    "劳动", "雇佣", "劳工", "工资", "社保", "外籍", "签证", "休假",
    "職安", "最低", "雇用", "賃金", "労働", "최저", "고용",
)
SKIP_SUBSTR = (
    "cause list", "industrial tribunal", "rti disclosure", "untitled",
    "upcoming events", "new publications", "search licensed",
    "temporary downtime", "clients portal", "job fair", "job fairs",
    "before the presiding officer", "before central government",
)

sys.path.insert(0, str(ROOT))
from scraper.seed import SEED_POLICIES  # noqa: E402
from scraper.sources import (  # noqa: E402
    CRITICAL_WORDS,
    SOURCES,
    TOPIC_QUERY,
    TYPE_RULES,
    UPCOMING_WORDS,
    WATCH_WORDS,
)


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().replace(microsecond=0).isoformat()


def google_news_rss(site: str) -> str:
    q = f"when:{INTERVAL_DAYS}d {TOPIC_QUERY} site:{site}"
    return "https://news.google.com/rss/search?" + urllib.parse.urlencode(
        {"q": q, "hl": "en-US", "gl": "US", "ceid": "US:en"}
    )


def fetch_bytes(url: str, timeout: int = 25) -> bytes:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": UA,
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        },
    )
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_feed(url: str):
    try:
        raw = fetch_bytes(url)
    except Exception as exc:
        return None, str(exc)
    parsed = feedparser.parse(raw)
    if getattr(parsed, "bozo", False) and not parsed.entries:
        return None, str(getattr(parsed, "bozo_exception", "parse error"))
    return parsed, None


def classify_type(text: str) -> str:
    low = f" {text.lower()} "
    for label, keys in TYPE_RULES:
        if any(k in low for k in keys):
            return label
    return "Contracts"


def classify_status(text: str) -> str:
    low = text.lower()
    if any(w in low for w in WATCH_WORDS):
        return "watch"
    if any(w in low for w in UPCOMING_WORDS):
        return "upcoming"
    return "live"


def classify_impact(text: str, critical: bool) -> str:
    if critical:
        return "high"
    low = text.lower()
    if any(w in low for w in WATCH_WORDS):
        return "monitor"
    return "med"


def is_critical(text: str) -> bool:
    low = text.lower()
    return any(w in low for w in CRITICAL_WORDS)


def item_id(country: str, title: str, link: str) -> str:
    h = hashlib.sha1(f"{country}|{title.strip().lower()}|{link}".encode("utf-8")).hexdigest()[:12]
    return f"crawl-{country.lower()}-{h}"


def norm_title(title: str) -> str:
    t = re.sub(r"\s+", " ", title).strip().lower()
    t = re.sub(r" - .*$", "", t)
    return t[:180]


def strip_html(s: str) -> str:
    s = html_lib.unescape(re.sub(r"<[^>]+>", " ", s or ""))
    s = re.sub(r"\s+", " ", s).strip()
    return s


def is_relevant(title: str, body: str) -> bool:
    if not title or title.lower().startswith("untitled"):
        return False
    blob = f"{title} {body}".lower()
    if any(s in blob for s in SKIP_SUBSTR):
        return False
    return any(k in blob for k in RELEVANT)


def published_label(entry) -> str:
    st = entry.get("published_parsed") or entry.get("updated_parsed")
    if st:
        try:
            dt = datetime(*st[:6], tzinfo=timezone.utc)
            return dt.date().isoformat()
        except Exception:
            pass
    return "Recent"


def to_policy(entry, src: dict, fetched: str) -> dict | None:
    title = strip_html(entry.get("title") or "")
    if len(title) < 12:
        return None
    summary = strip_html(entry.get("summary") or entry.get("description") or "")
    if len(summary) > 420:
        summary = summary[:417] + "..."
    if not summary:
        summary = (
            f"Public update indexed from {src['name']}. "
            "Open the source link and verify on the official site."
        )
    if not is_relevant(title, summary):
        return None
    link = entry.get("link") or src["home"]
    blob = f"{title} {summary}"
    critical = is_critical(blob)
    return {
        "id": item_id(src["country"], title, link),
        "country": src["country"],
        "flag": src["flag"],
        "status": classify_status(blob),
        "critical": critical,
        "title": title,
        "body": summary,
        "type": classify_type(blob),
        "effective": published_label(entry),
        "impact": classify_impact(blob, critical),
        "src": link,
        "sourceName": src["name"],
        "fetchedAt": fetched,
        "origin": "crawl",
    }


def crawl_all() -> tuple[list[dict], list[dict]]:
    fetched = now_iso()
    found: list[dict] = []
    log: list[dict] = []
    for src in SOURCES:
        urls = list(src.get("rss") or [])
        urls.append(google_news_rss(src["site"]))
        source_count = 0
        errors = []
        for url in urls:
            parsed, err = parse_feed(url)
            if err:
                errors.append(err)
                continue
            for entry in parsed.entries:
                if source_count >= MAX_NEW_PER_SOURCE:
                    break
                pol = to_policy(entry, src, fetched)
                if not pol:
                    continue
                found.append(pol)
                source_count += 1
            time.sleep(0.6)
        log.append({
            "source": src["name"],
            "country": src["country"],
            "added": source_count,
            "errors": errors[:3],
        })
    return found, log


def merge(existing: list[dict], crawled: list[dict]) -> list[dict]:
    seen = set()
    out: list[dict] = []

    def key(p: dict) -> str:
        return f"{p.get('country')}|{norm_title(p.get('title', ''))}"

    for p in crawled + existing:
        k = key(p)
        if k in seen:
            continue
        seen.add(k)
        out.append(p)
        if len(out) >= MAX_TOTAL:
            break
    return out


def build_trends(policies: list[dict], new_ids: set[str]) -> list[dict]:
    recent = [p for p in policies if p.get("id") in new_ids]
    by_type: dict[str, int] = {}
    for p in recent:
        by_type[p["type"]] = by_type.get(p["type"], 0) + 1
    top = sorted(by_type.items(), key=lambda x: -x[1])[:4]
    cards = []
    icons = {
        "Wages": "⚡", "AI & Tech": "🤖", "Foreign Workers": "🌐", "Leave": "🛡️",
        "Contracts": "📄", "Social Insurance": "💳", "Workplace Safety": "🦺",
    }
    if not top:
        return [
            {"icon": "📡", "title": "Awaiting first successful crawl", "body": "Run python scraper/crawl.py while online. Baseline policies remain visible.", "alert": False},
            {"icon": "📅", "title": "Cadence: every 14 days", "body": "Use install_windows_task.ps1 or GitHub Actions biweekly-crawl.yml.", "alert": False},
            {"icon": "🔎", "title": "Always verify official text", "body": "Indexed headlines are a monitor, not legal advice.", "alert": False},
            {"icon": "🌏", "title": "14 APAC markets", "body": "China, Japan, Korea, Singapore, Hong Kong, Taiwan, Australia, New Zealand, India, and SE Asia.", "alert": False},
        ]
    for label, n in top:
        cards.append({
            "icon": icons.get(label, "📌"),
            "title": f"{label}: {n} new item(s)",
            "body": f"{n} public update(s) matched this topic in the latest {INTERVAL_DAYS}-day crawl.",
            "alert": label in ("Wages", "Foreign Workers"),
        })
    while len(cards) < 4:
        cards.append({"icon": "📌", "title": "Monitor remaining markets", "body": "Use country and topic filters. Critical alerts stay in the red bar.", "alert": False})
    return cards[:4]


def load_existing() -> list[dict]:
    if OUT.exists():
        try:
            data = json.loads(OUT.read_text(encoding="utf-8"))
            return data.get("policies") or []
        except Exception:
            pass
    seeded = []
    for p in SEED_POLICIES:
        q = dict(p)
        q.setdefault("origin", "seed")
        q.setdefault("sourceName", "Baseline")
        seeded.append(q)
    return seeded


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh", action="store_true", help="Rebuild from seed, drop previous crawl items")
    args = parser.parse_args()
    existing = [] if args.fresh else load_existing()
    if args.fresh:
        for p in SEED_POLICIES:
            q = dict(p)
            q.setdefault("origin", "seed")
            q.setdefault("sourceName", "Baseline")
            existing.append(q)
    crawled, source_log = crawl_all()
    new_ids = {p["id"] for p in crawled}
    merged = merge(existing, crawled)
    payload = {
        "generatedAt": now_iso(),
        "intervalDays": INTERVAL_DAYS,
        "newThisCycle": len(crawled),
        "policies": merged,
        "trends": build_trends(merged, new_ids),
        "crawlLog": source_log,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    LOG.write_text(
        json.dumps({"at": payload["generatedAt"], "new": len(crawled), "sources": source_log}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {OUT}")
    print(f"New/indexed this cycle: {len(crawled)}  |  total: {len(merged)}")
    failed = [s for s in source_log if s["added"] == 0 and s["errors"]]
    if failed:
        print(f"Sources with no items: {len(failed)} (see web/data/crawl-log.json)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
