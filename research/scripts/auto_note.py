#!/usr/bin/env python3
"""Auto-generate skeleton paper notes from the ranked research pipeline output.

For each top-N paper by rank_score:
  1. Attempt to fetch the PDF (arXiv direct → pdf_url fallback)
  2. Extract text with pymupdf (if installed)
  3. Generate a structured skeleton note (template + metadata + extracted text)
  4. Write draft to research/data/drafts/
  5. Flag papers relevant to the YOLO26 one2one-head paradox

No API key or LLM required. Run ingest_papers.py first to generate the input JSONL.

Usage:
    python research/scripts/auto_note.py [--top-n 40] [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional, Sequence

import requests

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from research.pipeline import build_session, normalize_whitespace, request_with_retry, slugify  # noqa: E402

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# YOLO26 flagging
# The summary should bias toward papers directly relevant to the one2one /
# Hungarian-matching problem, not papers that merely mention DETR-family
# models in passing.
# ---------------------------------------------------------------------------
YOLO26_DIRECT_STRONG_KEYWORDS: list[str] = [
    "hungarian matching",
    "one-to-one assignment",
    "bipartite matching",
    "sinkhorn",
    "matching loss",
]

YOLO26_DIRECT_WEAK_KEYWORDS: list[str] = [
    "one2one",
    "one-to-one",
    "set prediction",
]

YOLO26_CONTEXT_KEYWORDS: list[str] = [
    "rt-detr",
    "nms-free",
    "end-to-end object detection",
    "end-to-end object detector",
    "dual assignments",
    "consistent dual assignments",
]

YOLO26_FLAG_LEVEL_DIRECT = "direct-loss"
YOLO26_FLAG_LEVEL_CONTEXT = "architecture-context"
PDF_MAX_BYTES = 30 * 1024 * 1024


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate skeleton paper notes from the ranked research output."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("research/data/normalized/papers_deduped.jsonl"),
        help="Deduped JSONL produced by ingest_papers.py (default: %(default)s)",
    )
    parser.add_argument(
        "--notes-dir",
        type=Path,
        default=Path("docs/notes"),
        help="Existing hand-written notes directory — read-only scan for skip logic (default: %(default)s)",
    )
    parser.add_argument(
        "--drafts-dir",
        type=Path,
        default=Path("research/data/drafts"),
        help="Output directory for generated skeleton drafts (default: %(default)s)",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=40,
        metavar="N",
        help="Process top-N papers by rank_score (default: %(default)s)",
    )
    parser.add_argument(
        "--pdf-timeout",
        type=int,
        default=20,
        metavar="SEC",
        help="HTTP timeout in seconds for PDF fetch (default: %(default)s)",
    )
    parser.add_argument(
        "--pdf-max-chars",
        type=int,
        default=40_000,
        metavar="CHARS",
        help="Character cap for extracted PDF text (default: %(default)s)",
    )
    parser.add_argument(
        "--pdf-max-pages",
        type=int,
        default=12,
        metavar="PAGES",
        help="Page limit for PDF extraction (default: %(default)s)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would be processed without fetching PDFs or writing files",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing drafts and ignore skip logic",
    )
    return parser


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_papers(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError as exc:
                    logger.warning("Skipping malformed JSONL line: %s", exc)
    return records


def select_candidates(records: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda r: (
            -float(r.get("rank_score", 0.0)),
            str(r.get("title") or "").lower(),
            str(r.get("paper_uid") or ""),
        ),
    )[:top_n]


# ---------------------------------------------------------------------------
# Skip logic
# ---------------------------------------------------------------------------

def build_skip_set(notes_dir: Path) -> set[tuple[str, str]]:
    """Return (lastname, year_str) pairs derived from existing note filenames in notes_dir."""
    skip: set[tuple[str, str]] = set()
    if not notes_dir.exists():
        return skip
    pattern = re.compile(r"^([a-z]+)(\d{4})_")
    for path in notes_dir.glob("*.md"):
        if path.name == "paper_review_template.md":
            continue
        m = pattern.match(path.name)
        if m:
            skip.add((m.group(1), m.group(2)))
    return skip


def derive_note_key(record: dict[str, Any]) -> Optional[tuple[str, str]]:
    """Produce (lastname_lower_alpha, year_str) for skip-set lookup. Returns None if data missing."""
    authors: list[str] = record.get("authors") or []
    year = record.get("year")
    if not authors or year is None:
        return None
    lastname = re.sub(r"[^a-z]", "", authors[0].split()[-1].lower())
    if not lastname:
        return None
    return (lastname, str(int(year)))


# ---------------------------------------------------------------------------
# Filename derivation
# ---------------------------------------------------------------------------

def derive_draft_filename(record: dict[str, Any]) -> str:
    """Produce {lastname}{year}_{short_title}.md matching the docs/notes/ convention."""
    authors: list[str] = record.get("authors") or []
    year = record.get("year")
    title: str = record.get("title") or ""

    if authors and year is not None:
        lastname = re.sub(r"[^a-z]", "", authors[0].split()[-1].lower())[:20]
        year_str = str(int(year))
        short = slugify(title)[:40].rstrip("_")
        if lastname and short:
            return f"{lastname}{year_str}_{short}.md"

    # Fallback: slugify the paper_uid
    uid_slug = re.sub(r"[^a-z0-9]+", "_", (record.get("paper_uid") or "paper").lower())[:60]
    return f"{uid_slug}.md"


# ---------------------------------------------------------------------------
# PDF fetching
# ---------------------------------------------------------------------------

def resolve_pdf_url(record: dict[str, Any]) -> Optional[str]:
    """Priority: arxiv_id (always OA) → pdf_url field → None."""
    arxiv_id: Optional[str] = record.get("arxiv_id")
    if arxiv_id:
        clean_id = re.sub(r"v\d+$", "", arxiv_id.strip())
        return f"https://arxiv.org/pdf/{clean_id}.pdf"
    pdf_url: Optional[str] = record.get("pdf_url")
    if pdf_url:
        return pdf_url
    return None


def fetch_pdf_bytes(url: str, session: requests.Session, timeout: int) -> Optional[bytes]:
    """Fetch URL and return bytes, or None on any error or unsupported response."""
    try:
        resp = request_with_retry(session, "GET", url, timeout=timeout)
        content_type = resp.headers.get("Content-Type", "").lower()
        content_length = resp.headers.get("Content-Length")
        if content_length:
            try:
                if int(content_length) > PDF_MAX_BYTES:
                    logger.warning("PDF too large by Content-Length (>30 MB), skipping: %s", url)
                    return None
            except ValueError:
                logger.debug("Non-integer Content-Length for %s: %s", url, content_length)
        if "html" in content_type:
            logger.info("Soft wall (HTML response): %s", url)
            return None
        pdf_bytes = resp.content
        if len(pdf_bytes) > PDF_MAX_BYTES:
            logger.warning("PDF too large (>30 MB), skipping: %s", url)
            return None
        return pdf_bytes
    except RuntimeError as exc:
        logger.warning("PDF fetch error (%s): %s", exc, url)
    return None


# ---------------------------------------------------------------------------
# PDF text extraction
# ---------------------------------------------------------------------------

def extract_text_from_pdf(
    pdf_bytes: bytes,
    max_pages: int,
    max_chars: int,
) -> Optional[str]:
    """Extract plain text from PDF bytes using pymupdf. Returns None on failure."""
    try:
        import fitz  # type: ignore[import]  # pymupdf
    except ImportError:
        logger.warning(
            "pymupdf not installed — PDF text extraction skipped. "
            "Run: pip install pymupdf"
        )
        return None

    parts: list[str] = []
    try:
        with fitz.open(stream=pdf_bytes, filetype="pdf") as doc:
            for page_num in range(min(len(doc), max_pages)):
                try:
                    text = doc[page_num].get_text()
                    if text.strip():
                        parts.append(f"--- PAGE {page_num + 1} ---\n{text}")
                except Exception as exc:
                    logger.debug("Page %d extraction error: %s", page_num + 1, exc)
    except Exception as exc:
        logger.warning("PDF open failed: %s", exc)
        return None

    if not parts:
        return None

    full_text = "\n\n".join(parts)
    if len(full_text) > max_chars:
        full_text = (
            full_text[:max_chars]
            + f"\n\n[TRUNCATED — use --pdf-max-chars to raise the {max_chars}-char limit]"
        )
    return full_text


# ---------------------------------------------------------------------------
# YOLO26 flagging
# ---------------------------------------------------------------------------

def _find_keywords(text: str, keywords: list[str]) -> list[str]:
    return [kw for kw in keywords if kw in text]


def detect_yolo26_flags(
    title: str,
    abstract: str,
    pdf_text: Optional[str],
) -> Optional[dict[str, Any]]:
    """
    Classify YOLO26 relevance.

    direct-loss:
        Strong one-to-one / Hungarian-matching signals found anywhere in the
        note text, including extracted PDF body text.

    architecture-context:
        Architecture keywords found in title/abstract. These papers are still
        useful context, but are weaker than direct loss-design references.
    """
    front_text = normalize_whitespace(f"{title} {abstract}".lower())
    full_text = normalize_whitespace(f"{front_text} {pdf_text or ''}".lower())

    direct_strong_hits = _find_keywords(full_text, YOLO26_DIRECT_STRONG_KEYWORDS)
    direct_weak_hits = _find_keywords(full_text, YOLO26_DIRECT_WEAK_KEYWORDS)
    direct_hits = direct_strong_hits + direct_weak_hits
    if direct_strong_hits or len(direct_weak_hits) >= 2:
        return {"level": YOLO26_FLAG_LEVEL_DIRECT, "keywords": direct_hits}

    context_hits = _find_keywords(front_text, YOLO26_CONTEXT_KEYWORDS)
    if len(context_hits) >= 2:
        return {"level": YOLO26_FLAG_LEVEL_CONTEXT, "keywords": context_hits}

    return None


# ---------------------------------------------------------------------------
# Skeleton note generation
# ---------------------------------------------------------------------------

def _best_url(record: dict[str, Any]) -> str:
    arxiv_id: Optional[str] = record.get("arxiv_id")
    if arxiv_id:
        clean_id = re.sub(r"v\d+$", "", arxiv_id.strip())
        return f"https://arxiv.org/abs/{clean_id}"
    landing: Optional[str] = record.get("landing_page_url")
    if landing:
        return landing
    doi: Optional[str] = record.get("doi")
    if doi:
        return f"https://doi.org/{doi}"
    return "N/A"


def generate_skeleton_note(
    record: dict[str, Any],
    pdf_text: Optional[str],
    flag_info: Optional[dict[str, Any]],
) -> str:
    """Produce a filled-citation skeleton note ready to open and annotate."""
    title: str = record.get("title") or "Unknown Title"
    authors: list[str] = record.get("authors") or []
    year = record.get("year")
    venue: str = record.get("venue") or "Unknown"
    doi: str = record.get("doi") or "N/A"
    arxiv_id: str = record.get("arxiv_id") or "N/A"
    citation_count = record.get("citation_count")
    abstract: str = record.get("abstract") or "No abstract available."
    rank_score: float = record.get("rank_score", 0.0)
    sources_seen: list[str] = record.get("sources_seen") or []
    keywords_hit: list[str] = record.get("keywords_hit") or []

    authors_str = ", ".join(authors) if authors else "Unknown"
    year_str = str(int(year)) if year is not None else "Unknown"
    first_last = authors[0].split()[-1] if authors else "Unknown"
    header_name = f"{first_last} et al." if len(authors) > 1 else (authors[0] if authors else "Unknown")
    best_url = _best_url(record)
    citations_str = str(citation_count) if citation_count is not None else "N/A"

    lines: list[str] = []

    # Header
    lines.append(f"# {header_name} ({year_str}) — {title}")
    lines.append("")
    lines.append("<!-- AUTO-GENERATED SKELETON — fill in TODO sections from PDF text below -->")
    lines.append(f"<!-- Rank score: {rank_score:.2f} | Sources: {', '.join(sources_seen)} -->")
    if keywords_hit:
        lines.append(f"<!-- Keywords matched: {', '.join(keywords_hit)} -->")
    lines.append("")

    # YOLO26 flag banner (only if flagged)
    if flag_info:
        level = flag_info["level"]
        keywords = ", ".join(flag_info["keywords"])
        lines.append(f"> **⚠️ YOLO26 RELEVANCE FLAG** — `{level}` via `{keywords}`")
        if level == YOLO26_FLAG_LEVEL_DIRECT:
            lines.append("> This paper likely contains direct guidance for one-to-one / Hungarian-matching loss design.")
        else:
            lines.append("> This paper is architecture context for NMS-free / end-to-end detector behavior.")
        lines.append("")

    # Citation
    lines.append("## Citation")
    lines.append(f"- **Title:** {title}")
    lines.append(f"- **Authors:** {authors_str}")
    lines.append(f"- **Venue / Year:** {venue}, {year_str}")
    lines.append(f"- **URL:** {best_url}")
    lines.append(f"- **DOI:** {doi}")
    lines.append(f"- **arXiv:** {arxiv_id}")
    lines.append(f"- **Citations:** {citations_str}")
    lines.append("")

    # Abstract
    lines.append("## Abstract")
    for part in abstract.split("\n"):
        lines.append(f"> {part}" if part.strip() else ">")
    lines.append("")

    # Problem
    lines.append("## Problem")
    lines.append("- What problem is the paper solving? <!-- TODO -->")
    lines.append("- Is this attack, defense, architecture, or benchmarking work? <!-- TODO -->")
    lines.append("- What detector / task / setting is studied? <!-- TODO -->")
    lines.append("")

    # Method
    lines.append("## Method")
    lines.append("- Method family / patch type / model design: <!-- TODO -->")
    lines.append("- Optimization or training method: <!-- TODO -->")
    lines.append("- Loss / objective terms: <!-- TODO -->")
    lines.append("- Data processing / transforms / EoT: <!-- TODO -->")
    lines.append("- Physical-world considerations: <!-- TODO -->")
    lines.append("")

    # Experimental Setup
    lines.append("## Experimental Setup")
    lines.append("- Dataset: <!-- TODO -->")
    lines.append("- Target classes: <!-- TODO -->")
    lines.append("- Model versions: <!-- TODO -->")
    lines.append("- Metrics: <!-- TODO -->")
    lines.append("")

    # Results
    lines.append("## Results")
    lines.append("- Main quantitative result: <!-- TODO -->")
    lines.append("- Key comparison or ablation: <!-- TODO -->")
    lines.append("- What failed or stayed weak: <!-- TODO -->")
    lines.append("")

    # Relevance
    lines.append("## Relevance to My Capstone")
    lines.append("- Direct relevance to YOLOv8: <!-- TODO -->")
    lines.append("- Direct relevance to YOLO11: <!-- TODO -->")
    lines.append("- Direct relevance to YOLO26: <!-- TODO -->")
    lines.append("- What I can reproduce: <!-- TODO -->")
    lines.append("- What I can cite: <!-- TODO -->")
    lines.append("")

    # Open Questions
    lines.append("## Open Questions")
    lines.append("- Does this transfer or generalize across detector families? <!-- TODO -->")
    lines.append("- Is the result digital only, physical, or both? <!-- TODO -->")
    lines.append("- Is code or data available? <!-- TODO -->")
    lines.append("- What is missing for my project? <!-- TODO -->")
    lines.append("")

    # Extracted PDF text
    lines.append("---")
    lines.append("")
    lines.append("## Extracted PDF Text")
    lines.append("")
    if pdf_text:
        lines.append(pdf_text)
    else:
        lines.append("*PDF not available — fetch manually from URL above.*")
    lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# File writing
# ---------------------------------------------------------------------------

def write_draft(drafts_dir: Path, filename: str, content: str) -> Path:
    drafts_dir.mkdir(parents=True, exist_ok=True)
    out = drafts_dir / filename
    out.write_text(content, encoding="utf-8")
    return out


def write_yolo26_summary(
    drafts_dir: Path,
    flagged: list[dict[str, Any]],
    n_processed: int,
) -> Path:
    drafts_dir.mkdir(parents=True, exist_ok=True)
    out = drafts_dir / "YOLO26_flagged.md"
    now = datetime.now(tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines: list[str] = []
    lines.append("# YOLO26 Paradox — Flagged Papers")
    lines.append("")
    lines.append(f"Generated: {now} | {n_processed} processed | {len(flagged)} flagged")
    lines.append("")
    lines.append(
        "Papers containing content relevant to the YOLO26 one-to-one assignment paradox."
    )
    lines.append(
        "These are primary candidates for designing a loss function that targets the `one2one`"
    )
    lines.append("head directly rather than the auxiliary `one2many` head.")
    lines.append("")

    flagged_sorted = sorted(
        flagged,
        key=lambda entry: (
            0 if entry.get("flag_level") == YOLO26_FLAG_LEVEL_DIRECT else 1,
            -float(entry.get("rank_score", 0.0)),
            entry.get("title", ""),
        ),
    )

    if not flagged_sorted:
        lines.append("*No papers flagged in this run.*")
    else:
        for i, entry in enumerate(flagged_sorted, 1):
            lines.append("---")
            lines.append("")
            lines.append(f"## {i}. {entry['title']}")
            lines.append("")
            authors_str = ", ".join(entry.get("authors") or []) or "Unknown"
            year = entry.get("year") or "Unknown"
            arxiv_id = entry.get("arxiv_id") or "N/A"
            rank_score: float = entry.get("rank_score", 0.0)
            flag_kws: list[str] = entry.get("flag_keywords") or []
            abstract: str = entry.get("abstract") or ""
            filename = entry.get("filename") or "N/A"
            flag_level = entry.get("flag_level") or YOLO26_FLAG_LEVEL_CONTEXT
            lines.append(f"- **Draft:** `research/data/drafts/{filename}`")
            lines.append(f"- **Authors:** {authors_str}")
            lines.append(f"- **Year:** {year}  |  **arXiv:** {arxiv_id}")
            lines.append(f"- **Rank score:** {rank_score:.2f}")
            lines.append(f"- **Flag level:** {flag_level}")
            lines.append(f"- **Flag keywords found:** {', '.join(flag_kws)}")
            snippet = abstract[:300].replace("\n", " ")
            if len(abstract) > 300:
                snippet += "..."
            lines.append(f"- **Abstract snippet:** {snippet}")
            lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main(argv: Optional[Sequence[str]] = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
    args = build_parser().parse_args(argv)

    if not args.input.exists():
        logger.error("Input JSONL not found: %s", args.input)
        logger.error("Run ingest_papers.py first to generate the ranked paper list.")
        return 1
    if args.top_n <= 0:
        raise ValueError("--top-n must be >= 1")
    if args.pdf_timeout <= 0:
        raise ValueError("--pdf-timeout must be > 0")
    if args.pdf_max_chars <= 0:
        raise ValueError("--pdf-max-chars must be > 0")
    if args.pdf_max_pages <= 0:
        raise ValueError("--pdf-max-pages must be > 0")

    logger.info("Loading papers from %s", args.input)
    records = load_papers(args.input)
    candidates = select_candidates(records, args.top_n)
    logger.info(
        "Selected top %d candidates (from %d total records)", len(candidates), len(records)
    )

    skip_set = build_skip_set(args.notes_dir) if not args.force else set()
    logger.info(
        "Skip set: %d existing notes found in %s", len(skip_set), args.notes_dir
    )

    # Dry-run: print table and exit
    if args.dry_run:
        print(f"\nDRY RUN — top {len(candidates)} candidates (no fetches or writes)\n")
        col = "{:<3}  {:<7}  {:<5}  {:<6}  {}"
        print(col.format("#", "Skip?", "PDF?", "Score", "Title"))
        print("-" * 80)
        for i, rec in enumerate(candidates, 1):
            key = derive_note_key(rec)
            skip_reason = "note" if (key and key in skip_set) else ""
            draft_fn = derive_draft_filename(rec)
            if not skip_reason and not args.force and (args.drafts_dir / draft_fn).exists():
                skip_reason = "draft"
            has_pdf = "yes" if resolve_pdf_url(rec) else "no"
            score = rec.get("rank_score", 0.0)
            title = (rec.get("title") or "")[:55]
            print(col.format(i, skip_reason or "-", has_pdf, f"{score:.2f}", title))
        print()
        return 0

    session = build_session(os.environ.get("CONTACT_EMAIL"))

    n_processed = 0
    n_skipped_notes = 0
    n_skipped_drafts = 0
    n_pdf_attempted = 0
    n_pdf_fetched = 0
    n_pdf_extracted = 0
    n_written = 0
    n_errors = 0
    flagged: list[dict[str, Any]] = []

    for rec in candidates:
        title_short = (rec.get("title") or "unknown")[:60]

        # Skip: existing hand-written note
        key = derive_note_key(rec)
        if key and key in skip_set:
            logger.info("SKIP (note exists): %s", title_short)
            n_skipped_notes += 1
            continue

        # Skip: draft already written (unless --force)
        draft_fn = derive_draft_filename(rec)
        if not args.force and (args.drafts_dir / draft_fn).exists():
            logger.info("SKIP (draft exists): %s", title_short)
            n_skipped_drafts += 1
            continue

        n_processed += 1

        # PDF fetch
        pdf_text: Optional[str] = None
        pdf_url = resolve_pdf_url(rec)
        if pdf_url:
            n_pdf_attempted += 1
            logger.info("Fetching PDF: %s", pdf_url)
            pdf_bytes = fetch_pdf_bytes(pdf_url, session, args.pdf_timeout)
            if pdf_bytes:
                n_pdf_fetched += 1
                pdf_text = extract_text_from_pdf(
                    pdf_bytes, args.pdf_max_pages, args.pdf_max_chars
                )
                if pdf_text:
                    n_pdf_extracted += 1
                else:
                    logger.info("PDF extraction failed (encrypted/corrupt/empty): %s", title_short)

        # YOLO26 flag detection — scan title + abstract + extracted PDF text
        flag_info = detect_yolo26_flags(
            rec.get("title") or "",
            rec.get("abstract") or "",
            pdf_text,
        )
        if flag_info:
            logger.info(
                "YOLO26 FLAG [%s | %s]: %s",
                flag_info["level"],
                ", ".join(flag_info["keywords"]),
                title_short,
            )
            flagged.append(
                {
                    "title": rec.get("title") or "Unknown",
                    "authors": rec.get("authors") or [],
                    "year": rec.get("year"),
                    "arxiv_id": rec.get("arxiv_id"),
                    "rank_score": rec.get("rank_score", 0.0),
                    "abstract": rec.get("abstract") or "",
                    "flag_keywords": flag_info["keywords"],
                    "flag_level": flag_info["level"],
                    "filename": draft_fn,
                }
            )

        # Generate skeleton note
        try:
            note_content = generate_skeleton_note(rec, pdf_text, flag_info)
        except Exception as exc:
            logger.error("Note generation failed for '%s': %s", title_short, exc)
            n_errors += 1
            continue

        # Write draft
        try:
            written = write_draft(args.drafts_dir, draft_fn, note_content)
            logger.info("Written: %s", written.name)
            n_written += 1
        except OSError as exc:
            logger.error("Write failed for '%s': %s", draft_fn, exc)
            n_errors += 1

    # YOLO26 summary — always written
    summary_path = write_yolo26_summary(args.drafts_dir, flagged, n_processed)

    # End-of-run report
    print(
        f"\nAuto-note run complete."
        f"\n  Candidates selected:   {len(candidates)}"
        f"\n  Skipped existing notes:{n_skipped_notes}"
        f"\n  Skipped existing drafts:{n_skipped_drafts}"
        f"\n  Processed:             {n_processed}"
        f"\n  PDFs attempted:        {n_pdf_attempted}"
        f"\n  PDFs fetched:          {n_pdf_fetched} / {n_pdf_attempted}"
        f"\n  PDFs text-extracted:   {n_pdf_extracted} / {n_pdf_fetched}"
        f"\n  Drafts written:        {n_written}"
        f"\n  Errors:                {n_errors}"
        f"\n  YOLO26 flagged:        {len(flagged)}"
        f"\n  Output dir:            {args.drafts_dir}/"
        f"\n  YOLO26 summary:        {summary_path}"
    )
    return 0 if n_errors < max(n_processed, 1) else 1


if __name__ == "__main__":
    raise SystemExit(main())
