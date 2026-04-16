#!/usr/bin/env python3
"""Screen the top-N ranked literature candidates into a working packet.

This script is intentionally repo-first. It does not fetch papers or browse the
network; it works from the normalized pipeline output already in the repo and
cross-references existing notes so the ranked pool can be triaged consistently.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
TODAY_STAMP = date.today().isoformat().replace("-", "_")

INPUT_DEFAULT = Path("research/data/normalized/papers_deduped.jsonl")
NOTES_DIR_DEFAULT = Path("docs/notes")
MARKDOWN_DEFAULT = Path(f"research/data/ranked/top200_screening_packet_{TODAY_STAMP}.md")
JSONL_DEFAULT = Path(f"research/data/ranked/top200_screening_packet_{TODAY_STAMP}.jsonl")
QUEUE_DEFAULT = Path(f"research/data/ranked/top50_fulltext_queue_{TODAY_STAMP}.md")

OPEN_ACCESS_DOMAINS = (
    "arxiv.org",
    "openaccess.thecvf.com",
    "thecvf.com",
    "usenix.org",
    "proceedings.mlr.press",
    "mdpi.com",
    "ijcai.org",
    "cv-foundation.org",
)

OFFTOPIC_TERMS = (
    "impacted tooth",
    "panoramic radiograph",
    "dental",
    "diabetic foot",
    "egyptian currency",
    "greenfruit",
    "orchard",
    "grasping robot",
    "steel surface defect",
    "aircraft recognition",
    "malware detection",
    "wifi human sensing",
    "plant disease",
    "smart city fire detection",
)

DOMAIN_PENALTY_TERMS = (
    "remote sensing",
    "aerial image",
    "uav",
    "visdrone",
    "greenfruit",
    "orchard",
    "grasping robot",
    "steel surface defect",
    "aircraft recognition",
    "railway crossing",
    "fire detection",
    "insulator defect",
    "retail",
    "tea",
    "cotton insect",
    "security check",
    "surface defect",
    "snake detection",
)

DEFENSE_TERMS = (
    " defense",
    "defending",
    "detecting adversarial",
    "detect adversarial",
    "catch you",
    "anomaly localization",
    "patch-agnostic defense",
    "recover",
    "purification",
    "ad-yolo",
    "napguard",
    "patchzero",
    "provably securing",
    "securing object detectors",
)

ARCHITECTURE_TERMS = (
    "detr",
    "rt-detr",
    "hungarian",
    "one-to-one",
    "one2one",
    "assignment",
    "nms-free",
    "anchor-free",
    "fcos",
    "end-to-end object detection",
    "end-to-end detector",
    "eliminating heuristic nms",
    "yolov10",
)

TRANSFER_TERMS = (
    "transfer",
    "cross-model",
    "cross architecture",
    "cross-architecture",
    "universal",
    "ensemble",
    "self-ensemble",
    "multi-model",
    "generalized adversarial patch",
    "top-k",
    "doepatch",
    "t-sea",
    "network transferability",
)

PHYSICAL_TERMS = (
    "physical",
    "real-world",
    "camera-agnostic",
    "camera agnostic",
    "clothing",
    "t-shirt",
    "texture",
    "cloak",
    "surveillance",
    "person stealth",
    "wearable",
    "3d",
)

ATTACK_TERMS = (
    "adversarial patch",
    "patch attack",
    "adversarial texture",
    "invisibility cloak",
    "t-shirt",
    "stealth attack",
    "camouflage",
    "person evasion",
    "object evasion",
    "patch training",
    "adversarial sticker",
)

ATTACK_SIGNAL_TERMS = (
    "adversarial",
    "patch",
    "texture",
    "sticker",
    "camouflage",
    "cloak",
    "t-shirt",
    "stealth",
)

REVIEW_TERMS = (
    "survey",
    "review",
    "comprehensive review",
    "current trends",
    "decadal",
)

QUEUE_ATTACK_TERMS = (
    "person",
    "pedestrian",
    "surveillance",
    "object detector",
    "object detectors",
    "physical adversarial",
    "transferability",
    "camouflage",
    "clothing",
    "t-shirt",
    "cloak",
    "thermal infrared",
    "infrared",
    "yolo",
)

QUEUE_PATCH_TERMS = (
    "patch",
    "camouflage",
    "clothing",
    "t-shirt",
    "tee",
    "cloak",
    "texture",
    "sticker",
)

QUEUE_ARCHITECTURE_TERMS = (
    "hungarian",
    "assignment",
    "nms-free",
    "one-to-one",
    "anchor-free",
    "fcos",
    "detr",
    "rt-detr",
    "up-detr",
    "group detr",
    "yolov10",
    "end-to-end object detection",
)

QUEUE_EXCLUDE_TERMS = (
    "face recognition",
    "multimodal large language models",
    "mllm",
    "lychee",
    "weed detection",
    "water quality",
    "pollution source",
    "low-light object detection",
    "cotton cultivation",
    "deepfake",
    "electrical equipment",
    "image classification",
    "multiple object tracking",
)


@dataclass
class NoteEntry:
    path: str
    title: str | None
    doi: str | None


@dataclass
class ScreenedPaper:
    rank: int
    paper_uid: str
    title: str
    year: int | None
    authors: list[str]
    venue: str | None
    doi: str | None
    citation_count: int | None
    rank_score: float
    category: str
    primary_repo_question: str
    access_state: str
    note_status: str
    matched_note_path: str | None
    domain_penalty: bool
    queue_eligible: bool
    screening_decision: str
    priority_score: float
    expected_output: str
    reason: str
    queries_matched: list[str]
    keywords_hit: list[str]
    pdf_url: str | None
    open_access: bool | None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=INPUT_DEFAULT)
    parser.add_argument("--notes-dir", type=Path, default=NOTES_DIR_DEFAULT)
    parser.add_argument("--top-n", type=int, default=200)
    parser.add_argument("--fulltext-queue-n", type=int, default=50)
    parser.add_argument("--secondary-queue-n", type=int, default=50)
    parser.add_argument("--markdown-out", type=Path, default=MARKDOWN_DEFAULT)
    parser.add_argument("--jsonl-out", type=Path, default=JSONL_DEFAULT)
    parser.add_argument("--queue-out", type=Path, default=QUEUE_DEFAULT)
    return parser


def normalize_whitespace(text: str | None) -> str:
    if not text:
        return ""
    return re.sub(r"\s+", " ", text).strip()


def normalize_title_key(title: str) -> str:
    title = normalize_whitespace(title).lower()
    title = re.sub(r"[^a-z0-9 ]+", " ", title)
    return re.sub(r"\s+", " ", title).strip()


def normalize_doi(doi: str | None) -> str | None:
    if not doi:
        return None
    normalized = doi.strip()
    normalized = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", normalized, flags=re.IGNORECASE)
    normalized = re.sub(r"^doi:\s*", "", normalized, flags=re.IGNORECASE)
    normalized = normalized.strip()
    return normalized or None


def clean_markdown_field(text: str | None) -> str:
    if not text:
        return ""
    cleaned = text.replace("`", "").replace("*", "")
    cleaned = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", cleaned)
    return normalize_whitespace(cleaned)


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line:
                records.append(json.loads(line))
    return records


def select_top_records(records: list[dict[str, Any]], top_n: int) -> list[dict[str, Any]]:
    return sorted(
        records,
        key=lambda record: (
            -float(record.get("rank_score", 0.0)),
            str(record.get("title") or "").lower(),
            str(record.get("paper_uid") or ""),
        ),
    )[:top_n]


def extract_note_title(lines: list[str]) -> str | None:
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("- title:"):
            return clean_markdown_field(stripped.split(":", 1)[1])
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("# "):
            heading = stripped[2:]
            heading = heading.replace("Paper Review:", "").strip()
            if "—" in heading:
                heading = heading.split("—", 1)[1].strip()
            return clean_markdown_field(heading)
    return None


def extract_note_doi(lines: list[str]) -> str | None:
    for line in lines:
        stripped = line.strip()
        if stripped.lower().startswith("- doi:"):
            return normalize_doi(stripped.split(":", 1)[1])
    return None


def build_note_index(notes_dir: Path) -> tuple[dict[str, NoteEntry], dict[str, NoteEntry]]:
    by_doi: dict[str, NoteEntry] = {}
    by_title: dict[str, NoteEntry] = {}
    for path in sorted(notes_dir.glob("*.md")):
        if path.name == "paper_review_template.md":
            continue
        lines = path.read_text(encoding="utf-8").splitlines()[:80]
        title = extract_note_title(lines)
        doi = extract_note_doi(lines)
        entry = NoteEntry(path=str(path.relative_to(ROOT)), title=title, doi=doi)
        if doi:
            by_doi.setdefault(doi, entry)
        if title:
            by_title.setdefault(normalize_title_key(title), entry)
    return by_doi, by_title


def match_existing_note(
    record: dict[str, Any],
    notes_by_doi: dict[str, NoteEntry],
    notes_by_title: dict[str, NoteEntry],
) -> NoteEntry | None:
    doi = normalize_doi(record.get("doi"))
    if doi and doi in notes_by_doi:
        return notes_by_doi[doi]
    title_key = normalize_title_key(record.get("title") or "")
    if title_key and title_key in notes_by_title:
        return notes_by_title[title_key]
    return None


def infer_access_state(record: dict[str, Any]) -> str:
    pdf_url = (record.get("pdf_url") or "").lower()
    if record.get("arxiv_id"):
        return "open_access_pdf"
    if record.get("open_access") is True:
        return "open_access_pdf"
    if any(domain in pdf_url for domain in OPEN_ACCESS_DOMAINS):
        return "open_access_pdf"
    if pdf_url:
        return "pdf_link_unknown"
    if record.get("landing_page_url") or record.get("doi"):
        return "landing_only"
    return "blocked_or_unknown"


def compose_search_text(record: dict[str, Any], *, include_queries: bool = False) -> str:
    parts = [
        record.get("title") or "",
        record.get("abstract") or "",
        " ".join(record.get("keywords_hit") or []),
        record.get("venue") or "",
        record.get("publisher") or "",
    ]
    if include_queries:
        parts.append(" ".join(record.get("queries_matched") or []))
    return normalize_whitespace(" ".join(parts)).lower()


def contains_any(text: str, phrases: tuple[str, ...]) -> bool:
    return any(phrase in text for phrase in phrases)


def is_offtopic(text: str) -> bool:
    if not contains_any(text, OFFTOPIC_TERMS):
        return False
    if contains_any(
        text,
        (
            "person",
            "pedestrian",
            "surveillance",
            "adversarial patch",
            "physical adversarial",
            "stealth attack",
            "t-shirt",
            "cloak",
        ),
    ):
        return False
    return True


def has_domain_penalty(text: str) -> bool:
    return contains_any(text, DOMAIN_PENALTY_TERMS)


def classify_category(record: dict[str, Any]) -> str:
    text = compose_search_text(record)
    if is_offtopic(text):
        return "offtopic_domain"
    review_like = contains_any(text, REVIEW_TERMS)
    if contains_any(text, DEFENSE_TERMS):
        return "defense_core"
    attack_like = contains_any(text, ATTACK_TERMS) or (
        "adversarial" in text and contains_any(text, ATTACK_SIGNAL_TERMS)
    )
    architecture_like = contains_any(text, ARCHITECTURE_TERMS)
    if review_like and not attack_like:
        return "generic_context"
    if architecture_like and not attack_like:
        return "architecture_context"
    if attack_like:
        return "attack_core"
    if architecture_like:
        return "architecture_context"
    return "generic_context"


def map_primary_repo_question(record: dict[str, Any], category: str) -> str:
    text = compose_search_text(record)
    if "yolo11" in text:
        return "yolo11_coverage"
    if contains_any(text, TRANSFER_TERMS):
        return "cross_yolo_transfer"
    if contains_any(text, PHYSICAL_TERMS):
        return "physical_robustness"
    if contains_any(text, ARCHITECTURE_TERMS):
        return "yolo26_architecture_mismatch"
    if category == "defense_core":
        return "physical_robustness"
    return "cross_yolo_transfer"


def build_expected_output(question: str, category: str) -> str:
    if question == "yolo26_architecture_mismatch":
        return "Architecture note tying detector design to patch-loss mismatch"
    if question == "cross_yolo_transfer":
        return "Transfer benchmark or surrogate-training tactic"
    if question == "yolo11_coverage":
        return "YOLO11 comparison point or missing-benchmark blocker"
    if category == "defense_core":
        return "Defense comparator for the capstone risk discussion"
    return "Physical benchmark or robustness method to borrow"


def is_queue_eligible(text: str, *, category: str, domain_penalty: bool) -> bool:
    if contains_any(text, QUEUE_EXCLUDE_TERMS):
        return False
    if category == "offtopic_domain":
        return False
    if category == "architecture_context":
        return contains_any(text, QUEUE_ARCHITECTURE_TERMS) and not domain_penalty
    if category in {"attack_core", "defense_core"}:
        if contains_any(text, QUEUE_PATCH_TERMS) and (
            contains_any(text, QUEUE_ATTACK_TERMS) or "object detection" in text or "detector" in text
        ):
            return True
        if "adversarial" in text and ("object detector" in text or "object detection" in text):
            return True
        return False
    return False


def compute_priority_score(
    record: dict[str, Any],
    *,
    category: str,
    question: str,
    access_state: str,
    note_status: str,
) -> float:
    score = float(record.get("rank_score") or 0.0)
    question_bonus = {
        "yolo26_architecture_mismatch": 4.0,
        "cross_yolo_transfer": 3.0,
        "physical_robustness": 3.0,
        "yolo11_coverage": 4.5,
    }
    category_bonus = {
        "attack_core": 2.0,
        "defense_core": 1.5,
        "architecture_context": 1.0,
        "generic_context": -1.0,
        "offtopic_domain": -12.0,
    }
    score += question_bonus.get(question, 0.0)
    score += category_bonus.get(category, 0.0)
    if access_state == "open_access_pdf":
        score += 2.0
    elif access_state == "pdf_link_unknown":
        score += 1.0
    if has_domain_penalty(compose_search_text(record)):
        score -= 10.0
    citations = int(record.get("citation_count") or 0)
    if citations >= 200:
        score += 2.0
    elif citations >= 50:
        score += 1.0
    if note_status == "existing_note":
        score -= 10.0
    return round(score, 3)


def summarize_reason(
    *,
    category: str,
    question: str,
    access_state: str,
    note_status: str,
    citations: int | None,
) -> str:
    if note_status == "existing_note":
        return "Already represented in docs/notes; keep as coverage, not a new read target."
    if category == "offtopic_domain":
        return "Domain-specific detector context without clear value for person-patch or YOLO transfer questions."
    parts: list[str] = []
    question_reason = {
        "yolo26_architecture_mismatch": "Useful for the YOLO26 architecture-mismatch question.",
        "cross_yolo_transfer": "Useful for cross-YOLO transfer or multi-model patch training.",
        "physical_robustness": "Useful for physical robustness or deployment realism.",
        "yolo11_coverage": "Useful for the thin YOLO11 literature gap.",
    }
    parts.append(question_reason.get(question, "Relevant to the repo's open questions."))
    if category == "attack_core":
        parts.append("Direct attack paper.")
    elif category == "defense_core":
        parts.append("Defense-side comparator.")
    elif category == "architecture_context":
        parts.append("Architecture context rather than an attack benchmark.")
    if access_state == "open_access_pdf":
        parts.append("Open-access full text is likely available.")
    elif access_state == "pdf_link_unknown":
        parts.append("A PDF link exists but access is uncertain.")
    else:
        parts.append("May require library or manual retrieval.")
    if citations and citations >= 100:
        parts.append("Citation count suggests this is a field anchor.")
    return " ".join(parts)


def assign_decisions(
    rows: list[ScreenedPaper],
    *,
    fulltext_queue_n: int,
    secondary_queue_n: int,
) -> None:
    def select_unique(rows_to_rank: list[ScreenedPaper], limit: int) -> set[str]:
        selected: set[str] = set()
        seen_titles: set[str] = set()
        for row in sorted(
            rows_to_rank,
            key=lambda item: (-item.priority_score, item.rank, item.title.lower()),
        ):
            title_key = normalize_title_key(row.title)
            if title_key in seen_titles:
                continue
            selected.add(row.paper_uid)
            seen_titles.add(title_key)
            if len(selected) >= limit:
                break
        return selected

    eligible = [
        row
        for row in rows
        if row.note_status == "new_candidate"
        and row.category in {"attack_core", "defense_core", "architecture_context"}
        and row.queue_eligible
    ]
    deep_read_candidates = [row for row in eligible if row.access_state == "open_access_pdf"]
    deep_read_ids = select_unique(deep_read_candidates, fulltext_queue_n)
    secondary_ids = select_unique(
        [row for row in eligible if row.paper_uid not in deep_read_ids],
        secondary_queue_n,
    )
    for row in rows:
        if row.note_status == "existing_note":
            row.screening_decision = "already_covered"
        elif row.category == "offtopic_domain":
            row.screening_decision = "skip_offtopic"
        elif row.paper_uid in deep_read_ids:
            row.screening_decision = "deep_read_now"
        elif row.paper_uid in secondary_ids:
            row.screening_decision = "queue_for_full_text"
        else:
            row.screening_decision = "metadata_only"


def render_table(counter: Counter[str], label: str) -> list[str]:
    lines = [f"## {label}", "", "| Bucket | Count |", "| --- | ---: |"]
    for key, value in sorted(counter.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| `{key}` | {value} |")
    lines.append("")
    return lines


def render_packet(rows: list[ScreenedPaper], *, top_n: int, notes_count: int) -> str:
    decision_counts = Counter(row.screening_decision for row in rows)
    category_counts = Counter(row.category for row in rows)
    question_counts = Counter(row.primary_repo_question for row in rows)
    overlap = [row for row in rows if row.note_status == "existing_note"]
    deep_read = [row for row in rows if row.screening_decision == "deep_read_now"]
    secondary = [row for row in rows if row.screening_decision == "queue_for_full_text"]

    lines: list[str] = [
        "# Top-200 Screening Packet",
        "",
        f"Generated: {date.today().isoformat()}",
        f"Source: `{INPUT_DEFAULT}`",
        f"Scope: top {top_n} ranked candidates cross-referenced against `{NOTES_DIR_DEFAULT}` ({notes_count} notes).",
        "",
        "## Summary",
        "",
        f"- Screened candidates: {len(rows)}",
        f"- Existing note overlap: {len(overlap)}",
        f"- Immediate full-text queue: {len(deep_read)}",
        f"- Secondary full-text queue: {len(secondary)}",
        f"- Metadata-only rows: {decision_counts.get('metadata_only', 0)}",
        f"- Off-topic skips: {decision_counts.get('skip_offtopic', 0)}",
        "",
        "## Method",
        "",
        "- Match existing coverage by DOI first, then normalized title.",
        "- Bucket candidates into `attack_core`, `defense_core`, `architecture_context`, `generic_context`, or `offtopic_domain` using repo-specific heuristics.",
        "- Map each paper to one primary repo question: `yolo26_architecture_mismatch`, `cross_yolo_transfer`, `physical_robustness`, or `yolo11_coverage`.",
        "- Promote only queue-eligible open-access papers into the immediate queue, deduplicate by normalized title, and park the next tranche as manual retrieval targets.",
        "",
    ]
    lines.extend(render_table(decision_counts, "Decision Counts"))
    lines.extend(render_table(category_counts, "Category Counts"))
    lines.extend(render_table(question_counts, "Primary Repo Questions"))

    lines.extend(
        [
            "## Existing Coverage Overlap",
            "",
            "These candidates already map to repo notes and should not be treated as unread work.",
            "",
        ]
    )
    for row in sorted(overlap, key=lambda item: item.rank):
        lines.append(
            f"- Rank {row.rank}: *{row.title}* -> `{row.matched_note_path}`"
        )
    lines.append("")

    lines.extend(
        [
            "## Immediate Full-Text Queue",
            "",
            "These are the highest-priority open-access candidates not already covered.",
            "",
        ]
    )
    for row in sorted(deep_read, key=lambda item: item.rank):
        lines.append(
            f"{row.rank}. *{row.title}* ({row.year or 'n.d.'}) "
            f"[`{row.category}` | `{row.primary_repo_question}` | priority {row.priority_score}]"
        )
        lines.append(f"   Access: `{row.access_state}`. Expected output: {row.expected_output}.")
        lines.append(f"   Reason: {row.reason}")
    lines.append("")

    lines.extend(
        [
            "## Secondary Full-Text Queue",
            "",
            "These are the next candidates to fetch or read after the immediate queue.",
            "",
        ]
    )
    for row in sorted(secondary, key=lambda item: item.rank):
        lines.append(
            f"{row.rank}. *{row.title}* ({row.year or 'n.d.'}) "
            f"[`{row.category}` | `{row.primary_repo_question}` | priority {row.priority_score}]"
        )
        lines.append(f"   Access: `{row.access_state}`. Expected output: {row.expected_output}.")
        lines.append(f"   Reason: {row.reason}")
    lines.append("")

    lines.extend(
        [
            "## Full Screening Table",
            "",
            "| Rank | Decision | Category | Repo question | Score | Title |",
            "| ---: | --- | --- | --- | ---: | --- |",
        ]
    )
    for row in rows:
        lines.append(
            f"| {row.rank} | `{row.screening_decision}` | `{row.category}` | "
            f"`{row.primary_repo_question}` | {row.priority_score:.1f} | {row.title} |"
        )
    lines.append("")
    return "\n".join(lines)


def render_queue(rows: list[ScreenedPaper]) -> str:
    deep_read = [row for row in rows if row.screening_decision == "deep_read_now"]
    lines = [
        "# Top-50 Full-Text Queue",
        "",
        f"Generated: {date.today().isoformat()}",
        "Selection rule: highest-priority queue-eligible open-access candidates in the top-200 screen, excluding covered notes and title-level duplicates.",
        "",
        "| Rank | Priority | Repo question | Category | Access | Title |",
        "| ---: | ---: | --- | --- | --- | --- |",
    ]
    for row in sorted(deep_read, key=lambda item: item.rank):
        lines.append(
            f"| {row.rank} | {row.priority_score:.1f} | `{row.primary_repo_question}` | "
            f"`{row.category}` | `{row.access_state}` | {row.title} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_jsonl(path: Path, rows: list[ScreenedPaper]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(asdict(row), ensure_ascii=False) + "\n")


def main() -> int:
    args = build_parser().parse_args()

    records = load_jsonl(ROOT / args.input)
    top_records = select_top_records(records, args.top_n)
    notes_by_doi, notes_by_title = build_note_index(ROOT / args.notes_dir)

    rows: list[ScreenedPaper] = []
    for rank, record in enumerate(top_records, start=1):
        note_match = match_existing_note(record, notes_by_doi, notes_by_title)
        note_status = "existing_note" if note_match else "new_candidate"
        category = classify_category(record)
        question = map_primary_repo_question(record, category)
        access_state = infer_access_state(record)
        text = compose_search_text(record)
        domain_penalty = has_domain_penalty(text)
        queue_eligible = is_queue_eligible(text, category=category, domain_penalty=domain_penalty)
        priority_score = compute_priority_score(
            record,
            category=category,
            question=question,
            access_state=access_state,
            note_status=note_status,
        )
        citations = record.get("citation_count")
        citation_count = int(citations) if citations not in (None, "") else None
        rows.append(
            ScreenedPaper(
                rank=rank,
                paper_uid=str(record.get("paper_uid") or ""),
                title=str(record.get("title") or "").strip(),
                year=int(record["year"]) if record.get("year") not in (None, "") else None,
                authors=list(record.get("authors") or []),
                venue=record.get("venue"),
                doi=normalize_doi(record.get("doi")),
                citation_count=citation_count,
                rank_score=float(record.get("rank_score") or 0.0),
                category=category,
                primary_repo_question=question,
                access_state=access_state,
                note_status=note_status,
                matched_note_path=note_match.path if note_match else None,
                domain_penalty=domain_penalty,
                queue_eligible=queue_eligible,
                screening_decision="metadata_only",
                priority_score=priority_score,
                expected_output=build_expected_output(question, category),
                reason=summarize_reason(
                    category=category,
                    question=question,
                    access_state=access_state,
                    note_status=note_status,
                    citations=citation_count,
                ),
                queries_matched=list(record.get("queries_matched") or []),
                keywords_hit=list(record.get("keywords_hit") or []),
                pdf_url=record.get("pdf_url"),
                open_access=record.get("open_access"),
            )
        )

    assign_decisions(
        rows,
        fulltext_queue_n=args.fulltext_queue_n,
        secondary_queue_n=args.secondary_queue_n,
    )

    markdown = render_packet(
        rows,
        top_n=args.top_n,
        notes_count=len(list((ROOT / args.notes_dir).glob("*.md"))) - 1,
    )
    queue_markdown = render_queue(rows)

    markdown_path = ROOT / args.markdown_out
    queue_path = ROOT / args.queue_out
    jsonl_path = ROOT / args.jsonl_out
    markdown_path.parent.mkdir(parents=True, exist_ok=True)
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    markdown_path.write_text(markdown + "\n", encoding="utf-8")
    queue_path.write_text(queue_markdown + "\n", encoding="utf-8")
    write_jsonl(jsonl_path, rows)

    decision_counts = Counter(row.screening_decision for row in rows)
    print(f"screened={len(rows)}")
    print(f"existing_note_overlap={decision_counts.get('already_covered', 0)}")
    print(f"deep_read_now={decision_counts.get('deep_read_now', 0)}")
    print(f"queue_for_full_text={decision_counts.get('queue_for_full_text', 0)}")
    print(f"metadata_only={decision_counts.get('metadata_only', 0)}")
    print(f"skip_offtopic={decision_counts.get('skip_offtopic', 0)}")
    print(f"markdown={args.markdown_out}")
    print(f"queue={args.queue_out}")
    print(f"jsonl={args.jsonl_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
