from __future__ import annotations

import json
import math
import os
import re
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence
from urllib.parse import quote

import feedparser
import requests
import yaml

OPENALEX_BASE = "https://api.openalex.org"
SEMANTIC_SCHOLAR_BASE = "https://api.semanticscholar.org/graph/v1"
ARXIV_QUERY_URL = "http://export.arxiv.org/api/query"
CROSSREF_BASE = "https://api.crossref.org"
UNPAYWALL_BASE = "https://api.unpaywall.org/v2"


@dataclass
class PaperRecord:
    paper_uid: str
    title: str
    abstract: str
    authors: list[str]
    year: Optional[int]
    publication_date: Optional[str]
    venue: Optional[str]
    publisher: Optional[str]
    doi: Optional[str]
    arxiv_id: Optional[str]
    source_primary: str
    sources_seen: list[str]
    source_ids: dict[str, str]
    landing_page_url: Optional[str]
    pdf_url: Optional[str]
    open_access: Optional[bool]
    oa_status: Optional[str]
    citation_count: Optional[int]
    retracted_or_updated: bool
    queries_matched: list[str]
    keywords_hit: list[str]
    verification_state: str
    rank_score: float
    notes: list[str] = field(default_factory=list)


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle) or {}


def ensure_dirs(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "_", value.strip().lower())
    return value.strip("_")[:80] or "item"


def normalize_whitespace(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def strip_html(text: Optional[str]) -> str:
    if not text:
        return ""
    return re.sub(r"<[^>]+>", " ", text)


def normalize_title_key(title: str) -> str:
    title = normalize_whitespace(title).lower()
    title = re.sub(r"[^a-z0-9 ]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def normalize_doi(doi: Optional[str]) -> Optional[str]:
    if not doi:
        return None
    normalized = doi.strip()
    normalized = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"^doi:\s*", "", normalized, flags=re.IGNORECASE)
    normalized = normalized.strip()
    return normalized or None


def normalize_openalex_id(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    normalized = value.strip().rstrip("/")
    if normalized.startswith("https://openalex.org/"):
        normalized = normalized.rsplit("/", 1)[-1]
    return normalized or None


def parse_year_from_date(value: Optional[str]) -> Optional[int]:
    if not value:
        return None
    match = re.match(r"^(\d{4})", value)
    if not match:
        return None
    try:
        return int(match.group(1))
    except ValueError:
        return None


def request_with_retry(
    session: requests.Session,
    method: str,
    url: str,
    *,
    params: Optional[dict[str, Any]] = None,
    headers: Optional[dict[str, str]] = None,
    timeout: int = 30,
    retries: int = 4,
    backoff: float = 1.5,
) -> requests.Response:
    last_exc: Optional[Exception] = None
    for attempt in range(retries):
        try:
            response = session.request(
                method,
                url,
                params=params,
                headers=headers,
                timeout=timeout,
            )
            if response.status_code in {429, 500, 502, 503, 504}:
                time.sleep(backoff ** attempt)
                continue
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            last_exc = exc
            time.sleep(backoff ** attempt)
    raise RuntimeError(f"Request failed after retries: {url}") from last_exc


def save_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)


def save_text(path: Path, payload: str) -> None:
    path.write_text(payload, encoding="utf-8")


def save_jsonl(path: Path, records: Iterable[PaperRecord]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), ensure_ascii=False) + "\n")


def save_error_marker(path: Path, message: str) -> None:
    save_text(path, message.strip() + "\n")


def build_session(contact_email: Optional[str]) -> requests.Session:
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": f"adversarial-patch-research/0.1 ({contact_email or 'no-contact-email'})",
        }
    )
    return session


def rebuild_openalex_abstract(inverted_index: Optional[dict[str, list[int]]]) -> str:
    if not inverted_index:
        return ""
    positions: dict[int, str] = {}
    for word, indexes in inverted_index.items():
        for index in indexes:
            positions[index] = word
    if not positions:
        return ""
    ordered = [positions[index] for index in sorted(positions)]
    return normalize_whitespace(" ".join(ordered))


def openalex_params(api_key: Optional[str], contact_email: Optional[str]) -> dict[str, str]:
    params: dict[str, str] = {}
    if api_key:
        params["api_key"] = api_key
    if contact_email:
        params["mailto"] = contact_email
    return params


def get_openalex_results(
    session: requests.Session,
    query: str,
    limit: int,
    api_key: Optional[str],
    contact_email: Optional[str],
) -> list[dict[str, Any]]:
    params = openalex_params(api_key, contact_email)
    params.update({"search": query, "per-page": max(1, min(limit, 200))})
    response = request_with_retry(session, "GET", f"{OPENALEX_BASE}/works", params=params)
    return response.json().get("results", [])


def get_semantic_scholar_results(
    session: requests.Session,
    query: str,
    limit: int,
    min_year: Optional[int],
    api_key: Optional[str],
) -> list[dict[str, Any]]:
    headers = {"x-api-key": api_key} if api_key else None
    fields = ",".join(
        [
            "paperId",
            "title",
            "abstract",
            "year",
            "publicationDate",
            "citationCount",
            "venue",
            "url",
            "authors",
            "externalIds",
            "openAccessPdf",
        ]
    )
    params: dict[str, Any] = {
        "query": query,
        "limit": max(1, min(limit, 100)),
        "offset": 0,
        "fields": fields,
    }
    if min_year:
        params["year"] = f"{min_year}-"
    response = request_with_retry(
        session,
        "GET",
        f"{SEMANTIC_SCHOLAR_BASE}/paper/search",
        params=params,
        headers=headers,
    )
    return response.json().get("data", [])


def get_arxiv_results(
    session: requests.Session,
    query: str,
    limit: int,
    min_year: Optional[int],
) -> tuple[str, list[dict[str, Any]]]:
    params = {
        "search_query": f'all:"{query}"',
        "start": 0,
        "max_results": limit,
    }
    response = request_with_retry(session, "GET", ARXIV_QUERY_URL, params=params, timeout=45)
    feed = feedparser.parse(response.text)
    entries: list[dict[str, Any]] = []
    for entry in feed.entries:
        year = parse_year_from_date(entry.get("published"))
        if min_year and year and year < min_year:
            continue
        entries.append(entry)
    return response.text, entries


def get_crossref_record(
    session: requests.Session,
    doi: str,
    contact_email: Optional[str],
) -> Optional[dict[str, Any]]:
    params = {"mailto": contact_email} if contact_email else None
    url = f"{CROSSREF_BASE}/works/{quote(doi, safe='')}"
    try:
        response = request_with_retry(session, "GET", url, params=params, timeout=20)
    except Exception:
        return None
    payload = response.json()
    return payload.get("message")


def get_unpaywall_record(
    session: requests.Session,
    doi: str,
    contact_email: Optional[str],
) -> Optional[dict[str, Any]]:
    if not contact_email:
        return None
    url = f"{UNPAYWALL_BASE}/{quote(doi, safe='')}"
    try:
        response = request_with_retry(
            session,
            "GET",
            url,
            params={"email": contact_email},
            timeout=20,
        )
    except Exception:
        return None
    return response.json()


def get_openalex_work_by_id(
    session: requests.Session,
    work_id: str,
    api_key: Optional[str],
    contact_email: Optional[str],
) -> dict[str, Any]:
    normalized = normalize_openalex_id(work_id)
    if not normalized:
        raise ValueError("OpenAlex work id is required")
    params = openalex_params(api_key, contact_email)
    response = request_with_retry(session, "GET", f"{OPENALEX_BASE}/works/{normalized}", params=params)
    return response.json()


def get_openalex_works_by_ids(
    session: requests.Session,
    work_ids: Sequence[str],
    api_key: Optional[str],
    contact_email: Optional[str],
) -> list[dict[str, Any]]:
    normalized_ids = [normalize_openalex_id(work_id) for work_id in work_ids]
    normalized_ids = [work_id for work_id in normalized_ids if work_id]
    if not normalized_ids:
        return []
    items: list[dict[str, Any]] = []
    for index in range(0, len(normalized_ids), 25):
        chunk = normalized_ids[index : index + 25]
        params = openalex_params(api_key, contact_email)
        params.update(
            {
                "filter": f"openalex:{'|'.join(chunk)}",
                "per-page": len(chunk),
            }
        )
        response = request_with_retry(session, "GET", f"{OPENALEX_BASE}/works", params=params)
        items.extend(response.json().get("results", []))
    return items


def get_openalex_citing_works(
    session: requests.Session,
    work_id: str,
    limit: int,
    api_key: Optional[str],
    contact_email: Optional[str],
    cited_by_api_url: Optional[str] = None,
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    page = 1
    base_url = cited_by_api_url or f"{OPENALEX_BASE}/works"
    while len(results) < limit:
        params = openalex_params(api_key, contact_email)
        params.update({"per-page": min(limit - len(results), 200), "page": page})
        if not cited_by_api_url:
            params["filter"] = f"cites:{normalize_openalex_id(work_id)}"
        response = request_with_retry(session, "GET", base_url, params=params)
        batch = response.json().get("results", [])
        if not batch:
            break
        results.extend(batch)
        if len(batch) < params["per-page"]:
            break
        page += 1
    return results[:limit]


def resolve_seed_to_openalex_work(
    session: requests.Session,
    seed_slug: str,
    seed: dict[str, Any],
    api_key: Optional[str],
    contact_email: Optional[str],
) -> Optional[dict[str, Any]]:
    openalex_id = seed.get("openalex_id")
    if openalex_id:
        return get_openalex_work_by_id(session, str(openalex_id), api_key, contact_email)

    doi = normalize_doi(seed.get("doi"))
    if doi:
        params = openalex_params(api_key, contact_email)
        params.update({"filter": f"doi:https://doi.org/{doi}", "per-page": 1})
        response = request_with_retry(session, "GET", f"{OPENALEX_BASE}/works", params=params)
        results = response.json().get("results", [])
        if results:
            return results[0]

    search_terms = [seed.get("arxiv_id"), seed.get("title"), seed.get("label"), seed_slug]
    normalized_title = normalize_title_key(seed.get("title") or seed.get("label") or seed_slug)
    for term in search_terms:
        if not term:
            continue
        params = openalex_params(api_key, contact_email)
        params.update({"search": str(term), "per-page": 5})
        response = request_with_retry(session, "GET", f"{OPENALEX_BASE}/works", params=params)
        for item in response.json().get("results", []):
            title_match = normalize_title_key(item.get("display_name", "")) == normalized_title
            if doi and normalize_doi(item.get("doi")) == doi:
                return item
            if seed.get("arxiv_id") and seed.get("arxiv_id") in json.dumps(item):
                return item
            if normalized_title and title_match:
                return item
    return None


def parse_openalex_work(item: dict[str, Any], query: str) -> PaperRecord:
    doi = normalize_doi(item.get("doi"))
    primary_location = item.get("primary_location") or {}
    location_source = primary_location.get("source") or {}
    venue = location_source.get("display_name")
    publisher = location_source.get("host_organization_name")
    return PaperRecord(
        paper_uid=f"openalex:{item.get('id', '')}",
        title=normalize_whitespace(item.get("display_name")),
        abstract=rebuild_openalex_abstract(item.get("abstract_inverted_index")),
        authors=[
            author.get("author", {}).get("display_name")
            for author in item.get("authorships", [])
            if author.get("author", {}).get("display_name")
        ],
        year=item.get("publication_year"),
        publication_date=item.get("publication_date"),
        venue=venue,
        publisher=publisher,
        doi=doi,
        arxiv_id=item.get("ids", {}).get("arxiv"),
        source_primary="openalex",
        sources_seen=["openalex"],
        source_ids={"openalex": str(item.get("id", ""))},
        landing_page_url=primary_location.get("landing_page_url") or item.get("id"),
        pdf_url=primary_location.get("pdf_url"),
        open_access=(item.get("open_access") or {}).get("is_oa"),
        oa_status=(item.get("open_access") or {}).get("oa_status"),
        citation_count=item.get("cited_by_count"),
        retracted_or_updated=False,
        queries_matched=[query],
        keywords_hit=[],
        verification_state="candidate",
        rank_score=0.0,
        notes=[],
    )


def parse_semantic_scholar_paper(item: dict[str, Any], query: str) -> PaperRecord:
    external_ids = item.get("externalIds") or {}
    pdf_url = None
    if isinstance(item.get("openAccessPdf"), dict):
        pdf_url = item.get("openAccessPdf", {}).get("url")
    return PaperRecord(
        paper_uid=f"semanticscholar:{item.get('paperId', '')}",
        title=normalize_whitespace(item.get("title")),
        abstract=normalize_whitespace(item.get("abstract")),
        authors=[author.get("name") for author in item.get("authors", []) if author.get("name")],
        year=item.get("year"),
        publication_date=item.get("publicationDate"),
        venue=item.get("venue"),
        publisher=None,
        doi=normalize_doi(external_ids.get("DOI")),
        arxiv_id=external_ids.get("ArXiv"),
        source_primary="semanticscholar",
        sources_seen=["semanticscholar"],
        source_ids={"semanticscholar": str(item.get("paperId", ""))},
        landing_page_url=item.get("url"),
        pdf_url=pdf_url,
        open_access=bool(pdf_url) if pdf_url is not None else None,
        oa_status=None,
        citation_count=item.get("citationCount"),
        retracted_or_updated=False,
        queries_matched=[query],
        keywords_hit=[],
        verification_state="candidate",
        rank_score=0.0,
        notes=[],
    )


def parse_arxiv_entry(entry: dict[str, Any], query: str) -> PaperRecord:
    entry_id = entry.get("id", "")
    arxiv_id_match = re.search(r"/abs/([^/]+)$", entry_id)
    arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None
    pdf_url = None
    for link in entry.get("links", []):
        if link.get("type") == "application/pdf":
            pdf_url = link.get("href")
            break
    return PaperRecord(
        paper_uid=f"arxiv:{arxiv_id or entry_id}",
        title=normalize_whitespace(entry.get("title")),
        abstract=normalize_whitespace(strip_html(entry.get("summary"))),
        authors=[author.get("name") for author in entry.get("authors", []) if author.get("name")],
        year=parse_year_from_date(entry.get("published")),
        publication_date=entry.get("published"),
        venue="arXiv",
        publisher="arXiv",
        doi=normalize_doi(getattr(entry, "arxiv_doi", None)),
        arxiv_id=arxiv_id,
        source_primary="arxiv",
        sources_seen=["arxiv"],
        source_ids={"arxiv": entry_id},
        landing_page_url=entry_id or None,
        pdf_url=pdf_url,
        open_access=True,
        oa_status="preprint",
        citation_count=None,
        retracted_or_updated=False,
        queries_matched=[query],
        keywords_hit=[],
        verification_state="candidate",
        rank_score=0.0,
        notes=[],
    )


def add_note(record: PaperRecord, note: str) -> None:
    if note not in record.notes:
        record.notes.append(note)


def merge_papers(existing: PaperRecord, incoming: PaperRecord) -> PaperRecord:
    existing.sources_seen = sorted(set(existing.sources_seen + incoming.sources_seen))
    existing.queries_matched = sorted(set(existing.queries_matched + incoming.queries_matched))
    existing.keywords_hit = sorted(set(existing.keywords_hit + incoming.keywords_hit))
    existing.notes = sorted(set(existing.notes + incoming.notes))
    for source_name, source_id in incoming.source_ids.items():
        existing.source_ids.setdefault(source_name, source_id)
    if not existing.title and incoming.title:
        existing.title = incoming.title
    if not existing.abstract and incoming.abstract:
        existing.abstract = incoming.abstract
    if not existing.year and incoming.year:
        existing.year = incoming.year
    if not existing.publication_date and incoming.publication_date:
        existing.publication_date = incoming.publication_date
    if not existing.venue and incoming.venue:
        existing.venue = incoming.venue
    if not existing.publisher and incoming.publisher:
        existing.publisher = incoming.publisher
    if not existing.doi and incoming.doi:
        existing.doi = incoming.doi
    if not existing.arxiv_id and incoming.arxiv_id:
        existing.arxiv_id = incoming.arxiv_id
    if not existing.landing_page_url and incoming.landing_page_url:
        existing.landing_page_url = incoming.landing_page_url
    if not existing.pdf_url and incoming.pdf_url:
        existing.pdf_url = incoming.pdf_url
    if existing.open_access is None and incoming.open_access is not None:
        existing.open_access = incoming.open_access
    if not existing.oa_status and incoming.oa_status:
        existing.oa_status = incoming.oa_status
    if existing.citation_count is None and incoming.citation_count is not None:
        existing.citation_count = incoming.citation_count
    existing.retracted_or_updated = existing.retracted_or_updated or incoming.retracted_or_updated
    existing.authors = sorted({author for author in existing.authors + incoming.authors if author})
    return existing


def dedupe_papers(records: Sequence[PaperRecord]) -> list[PaperRecord]:
    deduped: list[PaperRecord] = []
    doi_index: dict[str, int] = {}
    arxiv_index: dict[str, int] = {}
    title_year_index: dict[str, int] = {}

    for record in records:
        doi = normalize_doi(record.doi)
        arxiv_id = (record.arxiv_id or "").lower() or None
        title_year = f"{normalize_title_key(record.title)}|{record.year or 'unknown'}"

        match_index = None
        if doi and doi in doi_index:
            match_index = doi_index[doi]
        elif arxiv_id and arxiv_id in arxiv_index:
            match_index = arxiv_index[arxiv_id]
        elif title_year in title_year_index:
            match_index = title_year_index[title_year]

        if match_index is None:
            deduped.append(record)
            match_index = len(deduped) - 1
        else:
            deduped[match_index] = merge_papers(deduped[match_index], record)

        merged = deduped[match_index]
        if merged.doi:
            doi_index[normalize_doi(merged.doi)] = match_index
        if merged.arxiv_id:
            arxiv_index[merged.arxiv_id.lower()] = match_index
        title_year_index[f"{normalize_title_key(merged.title)}|{merged.year or 'unknown'}"] = match_index

    for record in deduped:
        if record.doi:
            record.paper_uid = f"doi:{normalize_doi(record.doi)}"
        elif record.arxiv_id:
            record.paper_uid = f"arxiv:{record.arxiv_id.lower()}"
        elif record.source_primary and record.source_ids.get(record.source_primary):
            record.paper_uid = f"{record.source_primary}:{record.source_ids[record.source_primary]}"
        else:
            record.paper_uid = f"title:{normalize_title_key(record.title)}"
    return deduped


def extract_crossref_publication_date(message: dict[str, Any]) -> Optional[str]:
    for key in ("published-print", "published-online", "issued", "created"):
        parts = message.get(key, {}).get("date-parts", [])
        if not parts or not parts[0]:
            continue
        values = [str(value).zfill(2) for value in parts[0]]
        while len(values) < 3:
            values.append("01")
        return "-".join(values[:3])
    return None


def has_crossref_update_flag(message: dict[str, Any]) -> bool:
    relation = message.get("relation") or {}
    keys = {
        "update-to",
        "is-update-to",
        "has-update",
        "is-retracted-by",
        "has-retraction",
        "is-corrected-by",
        "has-correction",
    }
    return any(key in relation for key in keys)


def apply_crossref_enrichment(record: PaperRecord, message: dict[str, Any]) -> PaperRecord:
    if not message:
        return record
    title = normalize_whitespace(" ".join(message.get("title", [])))
    venue = normalize_whitespace(" ".join(message.get("container-title", [])))
    publication_date = extract_crossref_publication_date(message)
    if not record.title and title:
        record.title = title
    if not record.venue and venue:
        record.venue = venue
    if not record.publisher and message.get("publisher"):
        record.publisher = message.get("publisher")
    if not record.publication_date and publication_date:
        record.publication_date = publication_date
    if not record.year and publication_date:
        record.year = parse_year_from_date(publication_date)
    if not record.landing_page_url and message.get("URL"):
        record.landing_page_url = message.get("URL")
    if record.citation_count is None and isinstance(message.get("is-referenced-by-count"), int):
        record.citation_count = message.get("is-referenced-by-count")
    record.retracted_or_updated = record.retracted_or_updated or has_crossref_update_flag(message)
    return record


def apply_unpaywall_enrichment(record: PaperRecord, payload: dict[str, Any]) -> PaperRecord:
    if not payload:
        return record
    best_location = payload.get("best_oa_location") or {}
    record.open_access = payload.get("is_oa") if record.open_access is None else record.open_access
    if not record.oa_status and payload.get("oa_status"):
        record.oa_status = payload.get("oa_status")
    if not record.pdf_url and best_location.get("url_for_pdf"):
        record.pdf_url = best_location.get("url_for_pdf")
    if not record.landing_page_url and best_location.get("url"):
        record.landing_page_url = best_location.get("url")
    return record


def compute_rank_score(record: PaperRecord, ranking_cfg: dict[str, Any]) -> tuple[float, list[str]]:
    text = f"{record.title} {record.abstract}".lower()
    keyword_boosts = ranking_cfg.get("keyword_boosts", {})
    soft_penalties = ranking_cfg.get("soft_penalties", {})
    hits: list[str] = []
    score = 0.0

    for keyword, boost in keyword_boosts.items():
        if keyword.lower() in text:
            score += float(boost)
            hits.append(keyword)

    for keyword, penalty in soft_penalties.items():
        if keyword.lower() in text:
            score += float(penalty)

    recency_start = int(ranking_cfg.get("recency_start_year", 2018))
    recency_weight = float(ranking_cfg.get("recency_per_year", 0.15))
    if record.year and record.year >= recency_start:
        score += (record.year - recency_start) * recency_weight

    citation_multiplier = float(ranking_cfg.get("citation_log_multiplier", 1.5))
    citation_max = float(ranking_cfg.get("citation_max_bonus", 4.0))
    if record.citation_count:
        score += min(citation_max, math.log10(record.citation_count + 1) * citation_multiplier)

    score += float(ranking_cfg.get("pdf_bonus", 0.0)) if record.pdf_url else 0.0
    score += float(ranking_cfg.get("open_access_bonus", 0.0)) if record.open_access else 0.0

    if record.retracted_or_updated:
        score -= float(ranking_cfg.get("update_penalty", 0.5))

    return round(score, 3), sorted(set(hits))


def write_ranked_markdown(
    records: Sequence[PaperRecord],
    output_path: Path,
    top_n: int,
    title: str,
) -> None:
    lines = [f"# {title}", "", f"Generated candidates: {len(records)}", ""]
    for index, record in enumerate(records[:top_n], start=1):
        authors = ", ".join(record.authors[:5]) if record.authors else "Unknown authors"
        lines.append(f"## {index}. {record.title}")
        lines.append(f"- Score: {record.rank_score}")
        lines.append(f"- Verification state: {record.verification_state}")
        lines.append(f"- Year: {record.year if record.year is not None else 'N/A'}")
        lines.append(f"- Venue: {record.venue or 'Unknown'}")
        lines.append(f"- Publisher: {record.publisher or 'Unknown'}")
        lines.append(f"- Authors: {authors}")
        lines.append(f"- DOI: {record.doi or 'N/A'}")
        lines.append(f"- arXiv: {record.arxiv_id or 'N/A'}")
        lines.append(f"- Citations: {record.citation_count if record.citation_count is not None else 'N/A'}")
        lines.append(f"- Sources: {', '.join(record.sources_seen)}")
        lines.append(f"- Queries matched: {', '.join(record.queries_matched) if record.queries_matched else 'N/A'}")
        lines.append(f"- Keywords hit: {', '.join(record.keywords_hit) if record.keywords_hit else 'N/A'}")
        lines.append(f"- Landing page: {record.landing_page_url or 'N/A'}")
        lines.append(f"- PDF: {record.pdf_url or 'N/A'}")
        lines.append(f"- Updated/retracted flag: {'yes' if record.retracted_or_updated else 'no'}")
        lines.append(f"- Notes: {', '.join(record.notes) if record.notes else 'N/A'}")
        if record.abstract:
            lines.append("")
            lines.append(f"**Abstract snippet:** {record.abstract[:800].strip()}")
        lines.append("")
    save_text(output_path, "\n".join(lines).strip() + "\n")


def get_research_paths(base_dir: Path) -> dict[str, Path]:
    raw_dir = base_dir / "data" / "raw"
    normalized_dir = base_dir / "data" / "normalized"
    ranked_dir = base_dir / "data" / "ranked"
    return {
        "base": base_dir,
        "raw": raw_dir,
        "raw_openalex": raw_dir / "openalex",
        "raw_semanticscholar": raw_dir / "semanticscholar",
        "raw_arxiv": raw_dir / "arxiv",
        "raw_crossref": raw_dir / "crossref",
        "raw_unpaywall": raw_dir / "unpaywall",
        "normalized": normalized_dir,
        "ranked": ranked_dir,
    }


def enrich_records(
    session: requests.Session,
    records: Sequence[PaperRecord],
    paths: dict[str, Path],
    contact_email: Optional[str],
) -> list[PaperRecord]:
    enriched: list[PaperRecord] = []
    seen_crossref: set[str] = set()
    seen_unpaywall: set[str] = set()
    for record in records:
        if record.doi:
            normalized_doi = normalize_doi(record.doi)
            if normalized_doi and normalized_doi not in seen_crossref:
                crossref_record = get_crossref_record(session, normalized_doi, contact_email)
                if crossref_record:
                    save_json(paths["raw_crossref"] / f"{slugify(normalized_doi)}.json", crossref_record)
                    seen_crossref.add(normalized_doi)
                    apply_crossref_enrichment(record, crossref_record)
            if normalized_doi and contact_email and normalized_doi not in seen_unpaywall:
                unpaywall_record = get_unpaywall_record(session, normalized_doi, contact_email)
                if unpaywall_record:
                    save_json(paths["raw_unpaywall"] / f"{slugify(normalized_doi)}.json", unpaywall_record)
                    seen_unpaywall.add(normalized_doi)
                    apply_unpaywall_enrichment(record, unpaywall_record)
        enriched.append(record)
    return enriched


def finalize_records(records: Sequence[PaperRecord], ranking_cfg: dict[str, Any]) -> list[PaperRecord]:
    finalized: list[PaperRecord] = []
    for record in records:
        record.rank_score, record.keywords_hit = compute_rank_score(record, ranking_cfg)
        record.queries_matched = sorted(set(record.queries_matched))
        record.notes = sorted(set(record.notes))
        finalized.append(record)
    finalized.sort(
        key=lambda item: (
            item.rank_score,
            item.citation_count if item.citation_count is not None else -1,
            item.year if item.year is not None else -1,
        ),
        reverse=True,
    )
    return finalized


def run_ingest(config_path: Path) -> dict[str, int]:
    config = load_yaml(config_path)
    base_dir = config_path.resolve().parents[1]
    paths = get_research_paths(base_dir)
    ensure_dirs(paths.values())

    queries = config.get("queries", [])
    limits = config.get("limits", {})
    min_year = config.get("filters", {}).get("min_year")
    ranking_cfg = config.get("ranking", {})
    top_n = int(config.get("output", {}).get("ranked_top_n", 40))

    openalex_api_key = os.getenv("OPENALEX_API_KEY")
    semantic_scholar_api_key = os.getenv("SEMANTIC_SCHOLAR_API_KEY")
    contact_email = os.getenv("CONTACT_EMAIL")
    session = build_session(contact_email)

    records: list[PaperRecord] = []
    source_failures = 0
    for query in queries:
        query_slug = slugify(query)

        try:
            openalex_items = get_openalex_results(
                session,
                query,
                int(limits.get("openalex_per_query", 25)),
                openalex_api_key,
                contact_email,
            )
            save_json(paths["raw_openalex"] / f"{query_slug}.json", openalex_items)
            records.extend(parse_openalex_work(item, query) for item in openalex_items)
        except Exception as exc:
            source_failures += 1
            save_json(paths["raw_openalex"] / f"{query_slug}.json", [])
            save_error_marker(
                paths["raw_openalex"] / f"{query_slug}.error.txt",
                f"query={query}\nsource=openalex\nerror={exc}",
            )

        try:
            semantic_items = get_semantic_scholar_results(
                session,
                query,
                int(limits.get("semanticscholar_per_query", 25)),
                min_year,
                semantic_scholar_api_key,
            )
            save_json(paths["raw_semanticscholar"] / f"{query_slug}.json", semantic_items)
            records.extend(parse_semantic_scholar_paper(item, query) for item in semantic_items)
        except Exception as exc:
            source_failures += 1
            save_json(paths["raw_semanticscholar"] / f"{query_slug}.json", [])
            save_error_marker(
                paths["raw_semanticscholar"] / f"{query_slug}.error.txt",
                f"query={query}\nsource=semanticscholar\nerror={exc}",
            )

        try:
            arxiv_xml, arxiv_items = get_arxiv_results(
                session,
                query,
                int(limits.get("arxiv_per_query", 15)),
                min_year,
            )
            save_text(paths["raw_arxiv"] / f"{query_slug}.xml", arxiv_xml)
            records.extend(parse_arxiv_entry(item, query) for item in arxiv_items)
        except Exception as exc:
            source_failures += 1
            save_text(paths["raw_arxiv"] / f"{query_slug}.xml", "")
            save_error_marker(
                paths["raw_arxiv"] / f"{query_slug}.error.txt",
                f"query={query}\nsource=arxiv\nerror={exc}",
            )
        time.sleep(0.2)

    save_jsonl(paths["normalized"] / "papers.jsonl", records)
    deduped = dedupe_papers(records)
    enrich_records(session, deduped, paths, contact_email)
    finalized = finalize_records(deduped, ranking_cfg)
    save_jsonl(paths["normalized"] / "papers_deduped.jsonl", finalized)
    write_ranked_markdown(finalized, paths["ranked"] / "ranked_reading_list.md", top_n, "Ranked Reading List")
    return {
        "raw_records": len(records),
        "deduped_records": len(finalized),
        "source_failures": source_failures,
    }


def run_citation_expansion(config_path: Path, seeds_path: Path) -> dict[str, int]:
    config = load_yaml(config_path)
    seeds_config = load_yaml(seeds_path)
    seeds = seeds_config.get("seeds", {})
    base_dir = config_path.resolve().parents[1]
    paths = get_research_paths(base_dir)
    ensure_dirs(paths.values())

    ranking_cfg = config.get("ranking", {})
    top_n = int(config.get("output", {}).get("ranked_top_n", 40))
    expansion_cfg = config.get("citation_expansion", {})
    referenced_limit = int(expansion_cfg.get("referenced_per_seed", 20))
    cited_by_limit = int(expansion_cfg.get("cited_by_per_seed", 20))

    openalex_api_key = os.getenv("OPENALEX_API_KEY")
    contact_email = os.getenv("CONTACT_EMAIL")
    session = build_session(contact_email)

    records: list[PaperRecord] = []
    for seed_slug, seed in seeds.items():
        seed_work = resolve_seed_to_openalex_work(session, seed_slug, seed, openalex_api_key, contact_email)
        if not seed_work:
            continue

        save_json(paths["raw_openalex"] / f"seed_{slugify(seed_slug)}.json", seed_work)
        seed_query = f"seed:{seed_slug}"

        referenced_ids = seed_work.get("referenced_works", [])[:referenced_limit]
        referenced_items = get_openalex_works_by_ids(session, referenced_ids, openalex_api_key, contact_email)
        save_json(paths["raw_openalex"] / f"seed_{slugify(seed_slug)}_referenced.json", referenced_items)
        for item in referenced_items:
            record = parse_openalex_work(item, seed_query)
            add_note(record, f"origin_seed:{seed_slug}")
            add_note(record, "origin_direction:referenced")
            records.append(record)

        citing_items = get_openalex_citing_works(
            session,
            str(seed_work.get("id", "")),
            cited_by_limit,
            openalex_api_key,
            contact_email,
            seed_work.get("cited_by_api_url"),
        )
        save_json(paths["raw_openalex"] / f"seed_{slugify(seed_slug)}_cited_by.json", citing_items)
        for item in citing_items:
            record = parse_openalex_work(item, seed_query)
            add_note(record, f"origin_seed:{seed_slug}")
            add_note(record, "origin_direction:cited_by")
            records.append(record)

    deduped = dedupe_papers(records)
    enrich_records(session, deduped, paths, contact_email)
    finalized = finalize_records(deduped, ranking_cfg)
    save_jsonl(paths["normalized"] / "citation_candidates.jsonl", finalized)
    write_ranked_markdown(
        finalized,
        paths["ranked"] / "citation_ranked_reading_list.md",
        top_n,
        "Citation Expansion Reading List",
    )
    return {"citation_candidates": len(finalized)}
