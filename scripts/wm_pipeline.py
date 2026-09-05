"""Standard-library pipeline for collecting and publishing Physical AI papers."""

from __future__ import annotations

import copy
import datetime as dt
import html
import json
import os
import re
import ssl
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "sources.json"
APPROVED_PATH = ROOT / "data" / "approved" / "papers.json"
QUEUE_PATH = ROOT / "data" / "review_queue.json"
REJECTED_PATH = ROOT / "data" / "rejected.json"
INBOX_PATH = ROOT / "data" / "inbox.json"
REPORT_PATH = ROOT / "data" / "last_ingest_report.json"
PAPER_DATA_PATH = ROOT / "paper-data.js"
README_PATH = ROOT / "README.md"
DAILY_DIR = ROOT / "data" / "daily"

README_STATS_START = "<!-- AUTO-GENERATED:STATS:START -->"
README_STATS_END = "<!-- AUTO-GENERATED:STATS:END -->"

ATOM = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
REQUIRED_FIELDS = ("id", "title", "authors", "source", "publication", "taxonomy", "review", "provenance")
ALLOWED_PUBLICATION_STATUS = {"preprint", "submitted", "accepted", "published", "technical_report"}
ALLOWED_REVIEW_STATUS = {"pending", "approved", "rejected"}


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0)


def isoformat(value: dt.datetime | None = None) -> str:
    value = value or utc_now()
    if value.tzinfo is None:
        value = value.replace(tzinfo=dt.timezone.utc)
    return value.astimezone(dt.timezone.utc).isoformat().replace("+00:00", "Z")


def parse_datetime(value: Any) -> dt.datetime | None:
    if value in (None, ""):
        return None
    if isinstance(value, (int, float)):
        return dt.datetime.fromtimestamp(value / 1000, tz=dt.timezone.utc)
    text = str(value).strip().replace("Z", "+00:00")
    try:
        parsed = dt.datetime.fromisoformat(text)
    except ValueError:
        try:
            parsed = dt.datetime.strptime(text, "%a, %d %b %Y %H:%M:%S %z")
        except ValueError:
            return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=dt.timezone.utc)
    return parsed.astimezone(dt.timezone.utc)


def normalize_space(value: Any) -> str:
    return re.sub(r"\s+", " ", html.unescape(str(value or ""))).strip()


def normalize_title(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", value)


def ascii_name(value: str) -> str:
    return " ".join(re.findall(r"[A-Za-z]+", value)).casefold()


def read_json(path: Path, default: Any = None) -> Any:
    if not path.exists():
        if default is not None:
            return copy.deepcopy(default)
        raise FileNotFoundError(path)
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text, encoding="utf-8")
    temp.replace(path)


def load_config(path: Path = CONFIG_PATH) -> dict[str, Any]:
    return read_json(path)


def request_bytes(url: str, config: dict[str, Any], *, data: bytes | None = None, headers: dict[str, str] | None = None) -> bytes:
    http = config.get("http", {})
    request_headers = {
        "User-Agent": http.get("user_agent", "world-model-mapping/1.0"),
        "Accept": "application/json, application/atom+xml, application/xml, text/html;q=0.8",
    }
    request_headers.update(headers or {})
    request = urllib.request.Request(url, data=data, headers=request_headers)
    attempts = int(http.get("retry_attempts", 3))
    timeout = int(http.get("timeout_seconds", 30))
    context = ssl.create_default_context()
    if not ssl.get_default_verify_paths().cafile:
        try:
            from pip._vendor import certifi  # type: ignore[import-not-found]

            context = ssl.create_default_context(cafile=certifi.where())
        except ImportError:
            pass
    last_error: Exception | None = None
    for attempt in range(attempts):
        try:
            with urllib.request.urlopen(request, timeout=timeout, context=context) as response:
                return response.read()
        except urllib.error.HTTPError as exc:
            last_error = exc
            if exc.code not in (429, 500, 502, 503, 504):
                break
            if attempt + 1 < attempts:
                retry_after = exc.headers.get("Retry-After", "")
                delay = int(retry_after) if retry_after.isdigit() else 3 * (attempt + 1)
                time.sleep(min(delay, 30))
        except (urllib.error.URLError, TimeoutError) as exc:
            last_error = exc
            if attempt + 1 < attempts:
                time.sleep(2**attempt)
    raise RuntimeError(f"request failed after {attempts} attempts: {url}: {last_error}")


def _text(parent: ET.Element, path: str, namespaces: dict[str, str] | None = None) -> str:
    element = parent.find(path, namespaces or {})
    return normalize_space(element.text if element is not None else "")


def _base_record(*, record_id: str, title: str, authors: list[str], abstract: str, source: dict[str, Any], publication: dict[str, Any], source_name: str, discovered_at: str | None = None) -> dict[str, Any]:
    return {
        "id": record_id,
        "title": normalize_space(title),
        "title_zh": "",
        "authors": [normalize_space(author) for author in authors if normalize_space(author)],
        "affiliations": [],
        "abstract": normalize_space(abstract),
        "summary_zh": "",
        "contribution_zh": "",
        "source": source,
        "publication": publication,
        "taxonomy": {"route_id": "latent_wm", "topics": [], "relevance_score": 0.0, "relevance_reasons": []},
        "team_node_ids": [],
        "review": {"status": "pending", "notes": ""},
        "provenance": {
            "discovered_at": discovered_at or isoformat(),
            "source_name": source_name,
            "evidence_urls": [source["url"]],
        },
    }


def parse_arxiv_feed(payload: bytes, source_name: str, discovered_at: str | None = None) -> list[dict[str, Any]]:
    root = ET.fromstring(payload)
    records: list[dict[str, Any]] = []
    for entry in root.findall("a:entry", ATOM):
        abs_url = _text(entry, "a:id", ATOM)
        raw_id = abs_url.rstrip("/").split("/")[-1]
        external_id = re.sub(r"v\d+$", "", raw_id)
        title = _text(entry, "a:title", ATOM)
        abstract = _text(entry, "a:summary", ATOM)
        authors = [_text(author, "a:name", ATOM) for author in entry.findall("a:author", ATOM)]
        published = _text(entry, "a:published", ATOM)
        updated = _text(entry, "a:updated", ATOM) or published
        pdf_url = f"https://arxiv.org/pdf/{external_id}"
        for link in entry.findall("a:link", ATOM):
            if link.attrib.get("title") == "pdf" or link.attrib.get("type") == "application/pdf":
                pdf_url = link.attrib.get("href", pdf_url).replace("http://", "https://")
        categories = [item.attrib.get("term", "") for item in entry.findall("a:category", ATOM)]
        comment = _text(entry, "arxiv:comment", ATOM)
        venue = "arXiv"
        status = "preprint"
        venue_match = re.search(r"(?:accepted (?:at|to)|published (?:at|in))\s+([^.;]+)", comment, flags=re.I)
        if venue_match:
            venue = normalize_space(venue_match.group(1))
            status = "accepted"
        record = _base_record(
            record_id=f"arxiv:{external_id}",
            title=title,
            authors=authors,
            abstract=abstract,
            source={
                "kind": "arxiv",
                "external_id": external_id,
                "url": f"https://arxiv.org/abs/{external_id}",
                "pdf_url": pdf_url,
            },
            publication={
                "status": status,
                "venue": venue,
                "venue_id": venue if venue != "arXiv" else "arXiv",
                "published_at": published,
                "updated_at": updated,
            },
            source_name=source_name,
            discovered_at=discovered_at,
        )
        record["taxonomy"]["topics"] = [value for value in categories if value]
        if comment:
            record["provenance"]["source_comment"] = comment
        records.append(record)
    return records


def fetch_arxiv(source: dict[str, Any], config: dict[str, Any], since: dt.datetime | None) -> list[dict[str, Any]]:
    params = {
        "search_query": source["query"],
        "start": 0,
        "max_results": int(source.get("max_results", 100)),
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    records = parse_arxiv_feed(request_bytes(url, config), source.get("name", source["id"]))
    return filter_since(records, since)


def fetch_arxiv_ids(ids: list[str], config: dict[str, Any], source_name: str = "Manual inbox") -> list[dict[str, Any]]:
    if not ids:
        return []
    params = {"id_list": ",".join(ids), "max_results": len(ids)}
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    return parse_arxiv_feed(request_bytes(url, config), source_name)


def unwrap_openreview(value: Any) -> Any:
    if isinstance(value, dict) and "value" in value:
        return value["value"]
    return value


def parse_openreview_payload(payload: bytes, source: dict[str, Any], discovered_at: str | None = None) -> list[dict[str, Any]]:
    data = json.loads(payload.decode("utf-8"))
    records: list[dict[str, Any]] = []
    for note in data.get("notes", []):
        content = {key: unwrap_openreview(value) for key, value in note.get("content", {}).items()}
        title = normalize_space(content.get("title", ""))
        if not title:
            continue
        authors = content.get("authors", [])
        if isinstance(authors, str):
            authors = [authors]
        abstract = normalize_space(content.get("abstract", ""))
        note_id = str(note.get("id") or note.get("forum") or normalize_title(title)[:32])
        venue = normalize_space(content.get("venue", "") or source.get("venue_name", "OpenReview"))
        published = parse_datetime(note.get("pdate") or note.get("cdate") or note.get("tcdate")) or utc_now()
        status = "accepted" if source.get("accepted_only") else "submitted"
        if re.search(r"reject|withdrawn|desk rejected", venue, flags=re.I):
            continue
        record = _base_record(
            record_id=f"openreview:{note_id}",
            title=title,
            authors=[str(author) for author in authors],
            abstract=abstract,
            source={
                "kind": "openreview",
                "external_id": note_id,
                "url": f"https://openreview.net/forum?id={note_id}",
                "pdf_url": f"https://openreview.net/pdf?id={note_id}",
            },
            publication={
                "status": status,
                "venue": venue or source.get("venue_name", "OpenReview"),
                "venue_id": source.get("venue_id", ""),
                "published_at": isoformat(published),
                "updated_at": isoformat(parse_datetime(note.get("tmdate") or note.get("mdate")) or published),
            },
            source_name=source.get("name", source.get("id", "OpenReview")),
            discovered_at=discovered_at,
        )
        keywords = content.get("keywords", []) or content.get("subject_areas", []) or []
        record["taxonomy"]["topics"] = [normalize_space(value) for value in keywords if normalize_space(value)]
        records.append(record)
    return records


def fetch_openreview(source: dict[str, Any], config: dict[str, Any], since: dt.datetime | None) -> list[dict[str, Any]]:
    maximum = int(source.get("max_results", 1000))
    search_terms = source.get("search_terms", ["world model", "embodied", "vision-language-action", "physical ai"])
    page_size = max(1, min(1000, maximum // max(1, len(search_terms))))
    records: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for term in search_terms:
        params = {"term": term, "venueid": source["venue_id"], "limit": page_size, "sort": "tmdate:desc"}
        url = "https://api2.openreview.net/notes/search?" + urllib.parse.urlencode(params)
        payload = request_bytes(url, config)
        page = parse_openreview_payload(payload, source)
        for record in page:
            if record["id"] not in seen_ids:
                seen_ids.add(record["id"])
                records.append(record)
    return filter_since(records, since)


def filter_since(records: Iterable[dict[str, Any]], since: dt.datetime | None) -> list[dict[str, Any]]:
    if since is None:
        return list(records)
    result = []
    for record in records:
        publication = record.get("publication", {})
        changed_at = parse_datetime(publication.get("updated_at") or publication.get("published_at"))
        if changed_at and changed_at >= since:
            result.append(record)
    return result


class CitationMetaParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.meta: dict[str, list[str]] = defaultdict(list)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() != "meta":
            return
        values = {key.casefold(): value or "" for key, value in attrs}
        name = (values.get("name") or values.get("property") or "").casefold()
        if name and values.get("content"):
            self.meta[name].append(values["content"])


def fetch_manual_page(item: dict[str, Any], config: dict[str, Any]) -> dict[str, Any] | None:
    url = item["url"]
    parser = CitationMetaParser()
    parser.feed(request_bytes(url, config).decode("utf-8", errors="replace"))
    metadata = parser.meta
    title = item.get("title") or next(iter(metadata.get("citation_title", []) or metadata.get("og:title", [])), "")
    if not title:
        return None
    authors = item.get("authors") or metadata.get("citation_author", [])
    abstract = item.get("abstract") or next(iter(metadata.get("citation_abstract", []) or metadata.get("description", []) or metadata.get("og:description", [])), "")
    published = item.get("published_at") or next(iter(metadata.get("citation_publication_date", []) or metadata.get("article:published_time", [])), "")
    parsed_published = parse_datetime(published) or utc_now()
    pdf_url = item.get("pdf_url") or next(iter(metadata.get("citation_pdf_url", [])), "")
    external_id = normalize_title(title)[:40]
    return _base_record(
        record_id=f"manual:{external_id}",
        title=title,
        authors=list(authors),
        abstract=abstract,
        source={"kind": item.get("kind", "manual"), "external_id": external_id, "url": url, "pdf_url": pdf_url},
        publication={
            "status": item.get("status", "technical_report"),
            "venue": item.get("venue", "Technical report"),
            "venue_id": item.get("venue_id", ""),
            "published_at": isoformat(parsed_published),
            "updated_at": isoformat(parsed_published),
        },
        source_name="Manual inbox",
    )


def collect_inbox(config: dict[str, Any], inbox: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    unprocessed = [item for item in inbox.get("items", []) if not item.get("processed_at")]
    arxiv_items: dict[str, dict[str, Any]] = {}
    other_items: list[dict[str, Any]] = []
    for item in unprocessed:
        match = re.search(r"arxiv\.org/(?:abs|pdf)/(\d{4}\.\d{4,5})(?:v\d+)?", item.get("url", ""))
        if match:
            arxiv_items[match.group(1)] = item
        else:
            other_items.append(item)
    records = fetch_arxiv_ids(list(arxiv_items), config) if arxiv_items else []
    processed: dict[str, str] = {}
    for record in records:
        source_id = record["source"]["external_id"]
        item = arxiv_items.get(source_id)
        if item:
            processed[item["url"]] = record["id"]
    for item in other_items:
        record = fetch_manual_page(item, config)
        if record:
            records.append(record)
            processed[item["url"]] = record["id"]
    return records, processed


def classify_record(record: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    searchable = " ".join(
        [record.get("title", ""), record.get("abstract", ""), " ".join(record.get("authors", [])), " ".join(record.get("affiliations", []))]
    ).casefold()
    title = record.get("title", "").casefold()
    score = 0.0
    route_scores: dict[str, float] = defaultdict(float)
    reasons: list[str] = []
    topics = list(record.get("taxonomy", {}).get("topics", []))
    for keyword in config.get("keywords", []):
        term = keyword["term"].casefold()
        if term not in searchable:
            continue
        weight = float(keyword.get("weight", 1))
        score += weight * (1.25 if term in title else 1.0)
        reasons.append(keyword["term"])
        if keyword["term"] not in topics:
            topics.append(keyword["term"])
        for route_id in keyword.get("routes", []):
            route_scores[route_id] += weight
    for keyword in config.get("negative_keywords", []):
        if keyword["term"].casefold() in searchable:
            score -= float(keyword.get("weight", 1))
    route_id = max(route_scores, key=route_scores.get) if route_scores else "latent_wm"
    taxonomy = record.setdefault("taxonomy", {})
    taxonomy.update(
        {
            "route_id": route_id,
            "topics": topics[:12],
            "relevance_score": round(max(0.0, score), 2),
            "relevance_reasons": reasons,
        }
    )
    team_ids = []
    for team in config.get("key_teams", []):
        if any(alias.casefold() in searchable for alias in team.get("aliases", [])):
            team_ids.append(team["node_id"])
            if team["name"] not in record.setdefault("affiliations", []):
                record["affiliations"].append(team["name"])
    record["team_node_ids"] = sorted(set(team_ids))
    return record


def _extract_json_object(text: str) -> dict[str, Any]:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end < start:
        raise ValueError("LLM response did not contain a JSON object")
    return json.loads(text[start : end + 1])


def enrich_with_llm(records: list[dict[str, Any]], config: dict[str, Any]) -> list[str]:
    api_key = os.environ.get("WM_LLM_API_KEY", "").strip()
    model = os.environ.get("WM_LLM_MODEL", "").strip()
    if not api_key or not model:
        return []
    base_url = (os.environ.get("WM_LLM_BASE_URL") or "https://api.openai.com/v1").rstrip("/")
    allowed_routes = config.get("taxonomy", {})
    errors = []
    maximum = int(config.get("max_llm_enrich_per_run", 20))
    for record in records[:maximum]:
        prompt = (
            "你是 Physical AI 论文图谱编辑。根据标题和摘要输出严格 JSON，字段为 title_zh、summary_zh、"
            "contribution_zh、route_id、topics。summary_zh 不超过 90 字，contribution_zh 不超过 70 字；"
            f"route_id 只能是 {list(allowed_routes)}。\n标题：{record['title']}\n摘要：{record.get('abstract', '')[:6000]}"
        )
        body = json.dumps(
            {
                "model": model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1,
                "response_format": {"type": "json_object"},
            }
        ).encode("utf-8")
        try:
            payload = request_bytes(
                f"{base_url}/chat/completions",
                config,
                data=body,
                headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
            )
            response = json.loads(payload.decode("utf-8"))
            value = _extract_json_object(response["choices"][0]["message"]["content"])
            record["title_zh"] = normalize_space(value.get("title_zh", ""))
            record["summary_zh"] = normalize_space(value.get("summary_zh", ""))
            record["contribution_zh"] = normalize_space(value.get("contribution_zh", ""))
            if value.get("route_id") in allowed_routes:
                record["taxonomy"]["route_id"] = value["route_id"]
            if isinstance(value.get("topics"), list):
                record["taxonomy"]["topics"] = [normalize_space(item) for item in value["topics"] if normalize_space(item)][:12]
        except Exception as exc:
            errors.append(f"{record['id']}: {exc}")
    return errors


def dedupe_key(record: dict[str, Any]) -> tuple[str, str]:
    return record.get("id", ""), normalize_title(record.get("title", ""))


def collect_candidates(config: dict[str, Any], *, since_hours: int | None = None, now: dt.datetime | None = None) -> dict[str, Any]:
    now = now or utc_now()
    hours = config.get("lookback_hours", 72) if since_hours is None else since_hours
    since = now - dt.timedelta(hours=int(hours)) if int(hours) > 0 else None
    candidates: list[dict[str, Any]] = []
    source_counts: dict[str, int] = {}
    errors: list[str] = []
    for source in config.get("sources", []):
        if not source.get("enabled", True):
            continue
        try:
            if source["kind"] == "arxiv":
                found = fetch_arxiv(source, config, since)
            elif source["kind"] == "openreview":
                found = fetch_openreview(source, config, since)
            else:
                errors.append(f"{source['id']}: unsupported source kind {source['kind']}")
                continue
            source_counts[source["id"]] = len(found)
            candidates.extend(found)
        except Exception as exc:
            errors.append(f"{source['id']}: {exc}")

    inbox = read_json(INBOX_PATH, {"schema_version": 1, "items": []})
    try:
        inbox_records, processed = collect_inbox(config, inbox)
        candidates.extend(inbox_records)
        source_counts["manual-inbox"] = len(inbox_records)
    except Exception as exc:
        processed = {}
        errors.append(f"manual-inbox: {exc}")

    for record in candidates:
        classify_record(record, config)

    approved_store = read_json(APPROVED_PATH, {"schema_version": 1, "papers": []})
    queue_store = read_json(QUEUE_PATH, {"schema_version": 1, "papers": []})
    rejected_store = read_json(REJECTED_PATH, {"schema_version": 1, "papers": []})
    existing = approved_store["papers"] + queue_store["papers"] + rejected_store["papers"]
    known_ids = {record.get("id") for record in existing}
    known_titles = {normalize_title(record.get("title", "")) for record in existing}
    minimum = float(config.get("min_relevance_score", 4.0))
    accepted: list[dict[str, Any]] = []
    ignored_low_score = 0
    duplicates = 0
    run_ids: set[str] = set()
    run_titles: set[str] = set()
    for record in sorted(candidates, key=lambda item: item["publication"].get("published_at", ""), reverse=True):
        record_id, title_key = dedupe_key(record)
        if record_id in known_ids or title_key in known_titles or record_id in run_ids or title_key in run_titles:
            duplicates += 1
            continue
        if float(record["taxonomy"].get("relevance_score", 0)) < minimum:
            ignored_low_score += 1
            continue
        accepted.append(record)
        run_ids.add(record_id)
        run_titles.add(title_key)

    errors.extend(f"llm: {message}" for message in enrich_with_llm(accepted, config))
    if accepted:
        queue_store["papers"].extend(accepted)
        queue_store["papers"].sort(key=lambda item: item["publication"].get("published_at", ""), reverse=True)
        queue_store["updated_at"] = isoformat(now)
        write_json(QUEUE_PATH, queue_store)

    if processed:
        for item in inbox.get("items", []):
            if item.get("url") in processed:
                item["processed_at"] = isoformat(now)
                item["record_id"] = processed[item["url"]]
        write_json(INBOX_PATH, inbox)

    report = {
        "schema_version": 1,
        "run_at": isoformat(now),
        "since": isoformat(since) if since else None,
        "source_counts": source_counts,
        "fetched": len(candidates),
        "queued": len(accepted),
        "duplicates": duplicates,
        "ignored_low_score": ignored_low_score,
        "pending_total": len(queue_store["papers"]),
        "queued_ids": [record["id"] for record in accepted],
        "errors": errors,
    }
    write_json(REPORT_PATH, report)
    return report


def review_records(*, action: str, record_ids: list[str], reviewer: str, route_id: str | None = None, notes: str = "", now: dt.datetime | None = None) -> dict[str, Any]:
    now = now or utc_now()
    config = load_config()
    if route_id and route_id not in config.get("taxonomy", {}):
        raise ValueError(f"unknown route_id: {route_id}")
    queue = read_json(QUEUE_PATH)
    approved = read_json(APPROVED_PATH)
    rejected = read_json(REJECTED_PATH)
    requested = set(record_ids)
    matched = [record for record in queue["papers"] if record["id"] in requested]
    missing = sorted(requested - {record["id"] for record in matched})
    if missing:
        raise ValueError("not found in review queue: " + ", ".join(missing))
    destination = approved if action == "approve" else rejected
    status = "approved" if action == "approve" else "rejected"
    for record in matched:
        if route_id:
            record["taxonomy"]["route_id"] = route_id
        record["review"] = {"status": status, "reviewed_by": reviewer, "reviewed_at": isoformat(now), "notes": notes}
        destination["papers"].append(record)
    queue["papers"] = [record for record in queue["papers"] if record["id"] not in requested]
    for store in (queue, destination):
        store["updated_at"] = isoformat(now)
    write_json(QUEUE_PATH, queue)
    write_json(APPROVED_PATH if action == "approve" else REJECTED_PATH, destination)
    if action == "approve":
        export_graph_data(config=config, generated_at=now)
        build_digest(target_date=now.date(), now=now)
    return {"action": action, "processed": [record["id"] for record in matched], "pending_total": len(queue["papers"])}


def load_legacy_graph(path: Path = ROOT / "graph-data.js") -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = re.search(r"window\.GRAPH_DATA\s*=\s*(\{.*\})\s*;\s*$", text, flags=re.S)
    if not match:
        raise ValueError(f"could not parse graph data from {path}")
    return json.loads(match.group(1))


def graph_node_id(record: dict[str, Any]) -> str:
    if record.get("graph_node_id"):
        return record["graph_node_id"]
    external = record.get("source", {}).get("external_id") or record["id"]
    safe = re.sub(r"[^A-Za-z0-9_]+", "_", external).strip("_")
    return "paper_" + safe


def _person_name_index(nodes: Iterable[dict[str, Any]]) -> dict[str, str]:
    result: dict[str, str] = {}
    for node in nodes:
        if node.get("type") != "person":
            continue
        candidate = ascii_name(node.get("name", ""))
        if candidate:
            result[candidate] = node["id"]
    return result


def build_paper_graph(config: dict[str, Any], approved_records: list[dict[str, Any]], base_graph: dict[str, Any], generated_at: dt.datetime | None = None) -> dict[str, Any]:
    generated_at = generated_at or utc_now()
    base_nodes = base_graph.get("nodes", [])
    base_ids = {node["id"] for node in base_nodes}
    person_names = _person_name_index(base_nodes)
    route_names = config.get("taxonomy", {})
    nodes: list[dict[str, Any]] = []
    links: list[dict[str, Any]] = []
    link_keys = {(link.get("source"), link.get("target"), link.get("relation_type")) for link in base_graph.get("links", [])}
    for record in approved_records:
        node_id = graph_node_id(record)
        route_id = record["taxonomy"]["route_id"]
        status = record["publication"]["status"]
        node_type = "tech_report" if status == "technical_report" else "paper"
        description = record.get("summary_zh") or record.get("abstract") or record.get("title")
        node: dict[str, Any] = {
            "id": node_id,
            "name": record.get("title_zh") or record["title"],
            "type": node_type,
            "description": description[:1000],
            "group_id": route_id,
            "group_name": route_names.get(route_id, route_id),
            "tags": record["taxonomy"].get("topics", []),
            "paper_id": record["id"],
            "title_en": record["title"],
            "authors": record.get("authors", []),
            "affiliations": record.get("affiliations", []),
            "venue": record["publication"].get("venue", ""),
            "publication_status": status,
            "published_at": record["publication"].get("published_at", ""),
            "updated_at": record["publication"].get("updated_at", ""),
            "source_kind": record["source"].get("kind", ""),
            "source_url": record["source"].get("url", ""),
            "pdf_url": record["source"].get("pdf_url", ""),
            "contribution_zh": record.get("contribution_zh", ""),
            "review_status": record["review"].get("status", ""),
            "reviewed_at": record["review"].get("reviewed_at", ""),
            "relevance_score": record["taxonomy"].get("relevance_score", 0),
        }
        if node_id not in base_ids:
            node["degree"] = 0
            node["composite_weight"] = min(0.2, max(0.02, float(node["relevance_score"]) / 100))
        nodes.append(node)
        targets: list[tuple[str, str, str]] = []
        for team_id in record.get("team_node_ids", []):
            if team_id in base_ids:
                targets.append((team_id, "released_by", "团队发布"))
        for author in record.get("authors", []):
            person_id = person_names.get(ascii_name(author))
            if person_id:
                targets.append((person_id, "authored_by", "论文作者"))
        seen_targets: set[tuple[str, str]] = set()
        for target, relation_type, label in targets:
            target_key = (target, relation_type)
            key = (node_id, target, relation_type)
            if target_key in seen_targets or key in link_keys:
                continue
            seen_targets.add(target_key)
            link_keys.add(key)
            links.append({"source": node_id, "target": target, "relation_type": relation_type, "label": label, "weight": 3})
    degree_counts: dict[str, int] = defaultdict(int)
    for link in links:
        degree_counts[link["source"]] += 1
        degree_counts[link["target"]] += 1
    for node in nodes:
        if node["id"] not in base_ids:
            node["degree"] = degree_counts[node["id"]]
    return {
        "meta": {
            "schema_version": 1,
            "generated_at": isoformat(generated_at),
            "approved_papers": len(approved_records),
            "new_nodes": sum(1 for node in nodes if node["id"] not in base_ids),
        },
        "nodes": nodes,
        "links": links,
    }


def export_graph_data(*, config: dict[str, Any] | None = None, generated_at: dt.datetime | None = None) -> dict[str, Any]:
    config = config or load_config()
    approved = read_json(APPROVED_PATH)
    base_graph = load_legacy_graph()
    generated_at = generated_at or parse_datetime(approved.get("updated_at")) or utc_now()
    graph = build_paper_graph(config, approved.get("papers", []), base_graph, generated_at)
    PAPER_DATA_PATH.write_text("window.PAPER_GRAPH_DATA = " + json.dumps(graph, ensure_ascii=False, indent=2) + ";\n", encoding="utf-8")
    update_readme_stats(config=config, base_graph=base_graph, paper_graph=graph)
    return graph


def render_readme_stats(*, config: dict[str, Any], base_graph: dict[str, Any], paper_graph: dict[str, Any]) -> str:
    relation_types = {
        link.get("relation_type")
        for link in base_graph.get("links", []) + paper_graph.get("links", [])
        if link.get("relation_type")
    }
    base_nodes = len(base_graph.get("nodes", []))
    base_links = len(base_graph.get("links", []))
    new_nodes = int(paper_graph.get("meta", {}).get("new_nodes", 0))
    approved = int(paper_graph.get("meta", {}).get("approved_papers", 0))
    total_nodes = base_nodes + new_nodes
    total_links = base_links + len(paper_graph.get("links", []))
    routes = len(config.get("taxonomy", {}))
    return "\n".join(
        [
            README_STATS_START,
            "| 指标 | 当前值 |",
            "| --- | ---: |",
            f"| 实体数 | {total_nodes:,} |",
            f"| 关系数 | {total_links:,} |",
            f"| 关系类型 | {len(relation_types)} 种 |",
            f"| 技术路线 | {routes} 条 |",
            f"| 已审核论文/技术报告 | {approved} 篇 |",
            "",
            f"基础图谱包含 {base_nodes:,} 个节点和 {base_links:,} 条关系；论文更新层新增 {new_nodes:,} 个节点。以上统计由 `python scripts/pipeline.py export` 自动更新。",
            README_STATS_END,
        ]
    )


def update_readme_stats(*, config: dict[str, Any], base_graph: dict[str, Any], paper_graph: dict[str, Any]) -> None:
    if not README_PATH.exists():
        return
    text = README_PATH.read_text(encoding="utf-8")
    if README_STATS_START not in text or README_STATS_END not in text:
        return
    before, remainder = text.split(README_STATS_START, 1)
    _, after = remainder.split(README_STATS_END, 1)
    block = render_readme_stats(config=config, base_graph=base_graph, paper_graph=paper_graph)
    README_PATH.write_text(before + block + after, encoding="utf-8")


def build_digest(*, target_date: dt.date | None = None, now: dt.datetime | None = None) -> dict[str, Any]:
    now = now or utc_now()
    target_date = target_date or now.date()
    approved = read_json(APPROVED_PATH, {"papers": []})["papers"]
    queue = read_json(QUEUE_PATH, {"papers": []})["papers"]

    def on_date(record: dict[str, Any], field_path: tuple[str, str]) -> bool:
        value = record.get(field_path[0], {}).get(field_path[1])
        parsed = parse_datetime(value)
        return bool(parsed and parsed.date() == target_date)

    newly_approved = [record for record in approved if on_date(record, ("review", "reviewed_at"))]
    new_candidates = [record for record in queue if on_date(record, ("provenance", "discovered_at"))]
    payload = {
        "schema_version": 1,
        "date": target_date.isoformat(),
        "generated_at": isoformat(now),
        "approved": newly_approved,
        "candidates": new_candidates,
        "pending_total": len(queue),
    }
    DAILY_DIR.mkdir(parents=True, exist_ok=True)
    write_json(DAILY_DIR / "latest.json", payload)
    lines = [
        f"# 世界模型与 Physical AI 每日更新 · {target_date.isoformat()}",
        "",
        f"- 今日审核入图：{len(newly_approved)}",
        f"- 今日新增候选：{len(new_candidates)}",
        f"- 待审核总数：{len(queue)}",
        "",
        "## 已审核入图",
        "",
    ]
    if newly_approved:
        for record in newly_approved:
            lines.append(f"- [{record.get('title_zh') or record['title']}]({record['source']['url']}) · {record['publication'].get('venue', '')} · `{record['taxonomy']['route_id']}`")
    else:
        lines.append("- 无")
    lines.extend(["", "## 待审核候选", ""])
    if new_candidates:
        for record in new_candidates:
            lines.append(f"- `{record['id']}` [{record['title']}]({record['source']['url']}) · 相关性 {record['taxonomy']['relevance_score']}")
    else:
        lines.append("- 无")
    lines.extend(
        [
            "",
            "## 审核命令",
            "",
            "```bash",
            "python scripts/pipeline.py review --approve <paper-id> --reviewer <name>",
            "python scripts/pipeline.py review --reject <paper-id> --reviewer <name> --notes \"原因\"",
            "```",
            "",
        ]
    )
    markdown = "\n".join(lines)
    (DAILY_DIR / "latest.md").write_text(markdown, encoding="utf-8")
    (DAILY_DIR / f"{target_date.isoformat()}.md").write_text(markdown, encoding="utf-8")
    return payload


def validate_all(config: dict[str, Any] | None = None) -> tuple[list[str], list[str]]:
    config = config or load_config()
    errors: list[str] = []
    warnings: list[str] = []
    stores = {
        "approved": read_json(APPROVED_PATH, {"papers": []}),
        "pending": read_json(QUEUE_PATH, {"papers": []}),
        "rejected": read_json(REJECTED_PATH, {"papers": []}),
    }
    routes = set(config.get("taxonomy", {}))
    all_ids: set[str] = set()
    all_titles: set[str] = set()
    for expected_status, store in stores.items():
        status = "approved" if expected_status == "approved" else "pending" if expected_status == "pending" else "rejected"
        for index, record in enumerate(store.get("papers", [])):
            label = f"{expected_status}[{index}]"
            for field in REQUIRED_FIELDS:
                if field not in record:
                    errors.append(f"{label}: missing {field}")
            if not record.get("id") or ":" not in record.get("id", ""):
                errors.append(f"{label}: invalid id")
            if record.get("review", {}).get("status") != status:
                errors.append(f"{label}: review status must be {status}")
            if record.get("review", {}).get("status") not in ALLOWED_REVIEW_STATUS:
                errors.append(f"{label}: invalid review status")
            if record.get("publication", {}).get("status") not in ALLOWED_PUBLICATION_STATUS:
                errors.append(f"{label}: invalid publication status")
            route_id = record.get("taxonomy", {}).get("route_id")
            if route_id not in routes:
                errors.append(f"{label}: unknown route_id {route_id}")
            source_url = record.get("source", {}).get("url", "")
            if not source_url.startswith(("http://", "https://")):
                errors.append(f"{label}: invalid source URL")
            if not parse_datetime(record.get("publication", {}).get("published_at")):
                errors.append(f"{label}: invalid published_at")
            title_key = normalize_title(record.get("title", ""))
            if record.get("id") in all_ids:
                errors.append(f"{label}: duplicate id {record['id']}")
            if title_key and title_key in all_titles:
                errors.append(f"{label}: duplicate title {record['title']}")
            all_ids.add(record.get("id", ""))
            all_titles.add(title_key)

    base_graph = load_legacy_graph()
    base_ids = {node["id"] for node in base_graph.get("nodes", [])}
    for store in stores.values():
        for record in store.get("papers", []):
            for team_id in record.get("team_node_ids", []):
                if team_id not in base_ids:
                    errors.append(f"{record['id']}: unknown team node {team_id}")
    if PAPER_DATA_PATH.exists():
        text = PAPER_DATA_PATH.read_text(encoding="utf-8")
        match = re.search(r"window\.PAPER_GRAPH_DATA\s*=\s*(\{.*\})\s*;\s*$", text, flags=re.S)
        if not match:
            errors.append("paper-data.js: invalid JavaScript data wrapper")
        else:
            published_graph = json.loads(match.group(1))
            published_ids = base_ids | {node["id"] for node in published_graph.get("nodes", [])}
            for link in published_graph.get("links", []):
                if link.get("source") not in published_ids or link.get("target") not in published_ids:
                    errors.append(f"paper-data.js: dangling link {link}")
    else:
        warnings.append("paper-data.js has not been generated")
    return errors, warnings
