from __future__ import annotations

import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from research.pipeline import ARXIV_QUERY_URL, CROSSREF_BASE, OPENALEX_BASE, SEMANTIC_SCHOLAR_BASE, UNPAYWALL_BASE
from research.scripts.expand_citations import main as expand_main
from research.scripts.ingest_papers import main as ingest_main


FIXTURES = Path(__file__).resolve().parents[1] / "research" / "fixtures"


class FakeResponse:
    def __init__(self, payload: object | None = None, *, text: str | None = None, status_code: int = 200) -> None:
        self._payload = payload
        self.text = text or ""
        self.status_code = status_code

    def json(self) -> object:
        return self._payload

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class CliSmokeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.openalex = json.loads((FIXTURES / "openalex_work.json").read_text(encoding="utf-8"))
        self.semantic = json.loads((FIXTURES / "semanticscholar_paper.json").read_text(encoding="utf-8"))
        self.crossref = json.loads((FIXTURES / "crossref_work.json").read_text(encoding="utf-8"))
        self.unpaywall = json.loads((FIXTURES / "unpaywall.json").read_text(encoding="utf-8"))
        self.arxiv_xml = (FIXTURES / "arxiv_feed.xml").read_text(encoding="utf-8")

    def test_ingest_cli_writes_outputs_and_avoids_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "research" / "config").mkdir(parents=True)
            (root / "docs").mkdir()
            config_path = root / "research" / "config" / "research_queries.yaml"
            config_path.write_text(
                "\n".join(
                    [
                        "queries:",
                        '  - "adversarial patch object detection"',
                        "filters:",
                        "  min_year: 2018",
                        "limits:",
                        "  openalex_per_query: 1",
                        "  semanticscholar_per_query: 1",
                        "  arxiv_per_query: 1",
                        "ranking:",
                        "  keyword_boosts:",
                        '    adversarial patch: 4.0',
                        '    yolo: 3.0',
                        '    object detection: 3.0',
                        "  soft_penalties:",
                        '    mnist: -2.0',
                        "  recency_start_year: 2018",
                        "  recency_per_year: 0.15",
                        "  citation_log_multiplier: 1.5",
                        "  citation_max_bonus: 4.0",
                        "  pdf_bonus: 0.5",
                        "  open_access_bonus: 0.5",
                        "  update_penalty: 0.5",
                        "output:",
                        "  ranked_top_n: 5",
                        "citation_expansion:",
                        "  referenced_per_seed: 1",
                        "  cited_by_per_seed: 1",
                    ]
                ),
                encoding="utf-8",
            )

            def fake_request(_session, _method, url, **kwargs):  # type: ignore[no-untyped-def]
                params = kwargs.get("params") or {}
                if url == f"{OPENALEX_BASE}/works" and params.get("search"):
                    return FakeResponse({"results": [self.openalex]})
                if url == f"{SEMANTIC_SCHOLAR_BASE}/paper/search":
                    return FakeResponse({"data": [self.semantic]})
                if url == ARXIV_QUERY_URL:
                    return FakeResponse(text=self.arxiv_xml)
                if url.startswith(f"{CROSSREF_BASE}/works/"):
                    return FakeResponse({"message": self.crossref})
                if url.startswith(f"{UNPAYWALL_BASE}/"):
                    return FakeResponse(self.unpaywall)
                raise AssertionError(f"Unexpected request: {url} {params}")

            with patch.dict(os.environ, {"CONTACT_EMAIL": "test@example.com"}, clear=False):
                with patch("research.pipeline.request_with_retry", side_effect=fake_request):
                    exit_code = ingest_main(["--config", str(config_path)])

            self.assertEqual(exit_code, 0)
            self.assertTrue((root / "research" / "data" / "raw" / "openalex").exists())
            self.assertTrue((root / "research" / "data" / "normalized" / "papers.jsonl").exists())
            self.assertTrue((root / "research" / "data" / "normalized" / "papers_deduped.jsonl").exists())
            self.assertTrue((root / "research" / "data" / "ranked" / "ranked_reading_list.md").exists())
            self.assertEqual(list((root / "docs").rglob("*")), [])

    def test_ingest_cli_survives_semantic_scholar_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "research" / "config").mkdir(parents=True)
            (root / "docs").mkdir()
            config_path = root / "research" / "config" / "research_queries.yaml"
            config_path.write_text(
                "\n".join(
                    [
                        "queries:",
                        '  - "adversarial patch object detection"',
                        "filters:",
                        "  min_year: 2018",
                        "limits:",
                        "  openalex_per_query: 1",
                        "  semanticscholar_per_query: 1",
                        "  arxiv_per_query: 1",
                        "ranking:",
                        "  keyword_boosts:",
                        '    adversarial patch: 4.0',
                        '    yolo: 3.0',
                        '    object detection: 3.0',
                        "  soft_penalties: {}",
                        "  recency_start_year: 2018",
                        "  recency_per_year: 0.15",
                        "  citation_log_multiplier: 1.5",
                        "  citation_max_bonus: 4.0",
                        "  pdf_bonus: 0.5",
                        "  open_access_bonus: 0.5",
                        "  update_penalty: 0.5",
                        "output:",
                        "  ranked_top_n: 5",
                        "citation_expansion:",
                        "  referenced_per_seed: 1",
                        "  cited_by_per_seed: 1",
                    ]
                ),
                encoding="utf-8",
            )

            def fake_request(_session, _method, url, **kwargs):  # type: ignore[no-untyped-def]
                params = kwargs.get("params") or {}
                if url == f"{OPENALEX_BASE}/works" and params.get("search"):
                    return FakeResponse({"results": [self.openalex]})
                if url == f"{SEMANTIC_SCHOLAR_BASE}/paper/search":
                    raise RuntimeError("semantic scholar unavailable")
                if url == ARXIV_QUERY_URL:
                    return FakeResponse(text=self.arxiv_xml)
                if url.startswith(f"{CROSSREF_BASE}/works/"):
                    return FakeResponse({"message": self.crossref})
                if url.startswith(f"{UNPAYWALL_BASE}/"):
                    return FakeResponse(self.unpaywall)
                raise AssertionError(f"Unexpected request: {url} {params}")

            with patch.dict(os.environ, {"CONTACT_EMAIL": "test@example.com"}, clear=False):
                with patch("research.pipeline.request_with_retry", side_effect=fake_request):
                    exit_code = ingest_main(["--config", str(config_path)])

            self.assertEqual(exit_code, 0)
            self.assertTrue((root / "research" / "data" / "normalized" / "papers_deduped.jsonl").exists())
            self.assertTrue((root / "research" / "data" / "ranked" / "ranked_reading_list.md").exists())
            self.assertTrue(
                (root / "research" / "data" / "raw" / "semanticscholar" / "adversarial_patch_object_detection.error.txt").exists()
            )
            self.assertEqual(list((root / "docs").rglob("*")), [])

    def test_expand_citations_cli_keeps_outputs_separate_and_tracks_seed_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            (root / "research" / "config").mkdir(parents=True)
            (root / "docs").mkdir()
            config_path = root / "research" / "config" / "research_queries.yaml"
            seeds_path = root / "research" / "config" / "seed_papers.yaml"
            config_path.write_text(
                "\n".join(
                    [
                        "queries: []",
                        "ranking:",
                        "  keyword_boosts:",
                        '    adversarial patch: 4.0',
                        '    yolo: 3.0',
                        "  soft_penalties: {}",
                        "  recency_start_year: 2018",
                        "  recency_per_year: 0.15",
                        "  citation_log_multiplier: 1.5",
                        "  citation_max_bonus: 4.0",
                        "  pdf_bonus: 0.5",
                        "  open_access_bonus: 0.5",
                        "  update_penalty: 0.5",
                        "output:",
                        "  ranked_top_n: 5",
                        "citation_expansion:",
                        "  referenced_per_seed: 1",
                        "  cited_by_per_seed: 1",
                    ]
                ),
                encoding="utf-8",
            )
            seeds_path.write_text(
                "\n".join(
                    [
                        "seeds:",
                        "  demo_seed:",
                        '    label: "Demo Seed"',
                        '    openalex_id: "WSEED"',
                    ]
                ),
                encoding="utf-8",
            )

            seed_work = dict(self.openalex)
            seed_work["id"] = "https://openalex.org/WSEED"
            seed_work["referenced_works"] = ["https://openalex.org/WREF1"]
            seed_work["cited_by_api_url"] = "https://api.openalex.org/works?filter=cites:WSEED"

            referenced_work = dict(self.openalex)
            referenced_work["id"] = "https://openalex.org/WREF1"
            referenced_work["display_name"] = "Referenced adversarial patch work"
            referenced_work["doi"] = "https://doi.org/10.1111/referenced"
            referenced_work["ids"] = {"arxiv": "2401.20001"}

            citing_work = dict(self.openalex)
            citing_work["id"] = "https://openalex.org/WCITE1"
            citing_work["display_name"] = "Citing adversarial patch work"
            citing_work["doi"] = "https://doi.org/10.1111/citing"
            citing_work["ids"] = {"arxiv": "2401.20002"}

            def fake_request(_session, _method, url, **kwargs):  # type: ignore[no-untyped-def]
                params = kwargs.get("params") or {}
                if url == f"{OPENALEX_BASE}/works/WSEED":
                    return FakeResponse(seed_work)
                if url == f"{OPENALEX_BASE}/works" and str(params.get("filter", "")).startswith("openalex:"):
                    return FakeResponse({"results": [referenced_work]})
                if url == "https://api.openalex.org/works?filter=cites:WSEED":
                    return FakeResponse({"results": [citing_work]})
                if url.startswith(f"{CROSSREF_BASE}/works/"):
                    message = dict(self.crossref)
                    message["relation"] = {}
                    return FakeResponse({"message": message})
                if url.startswith(f"{UNPAYWALL_BASE}/"):
                    return FakeResponse(self.unpaywall)
                raise AssertionError(f"Unexpected request: {url} {params}")

            with patch.dict(os.environ, {"CONTACT_EMAIL": "test@example.com"}, clear=False):
                with patch("research.pipeline.request_with_retry", side_effect=fake_request):
                    exit_code = expand_main(["--config", str(config_path), "--seeds", str(seeds_path)])

            self.assertEqual(exit_code, 0)
            candidates_path = root / "research" / "data" / "normalized" / "citation_candidates.jsonl"
            ranked_path = root / "research" / "data" / "ranked" / "citation_ranked_reading_list.md"
            self.assertTrue(candidates_path.exists())
            self.assertTrue(ranked_path.exists())
            self.assertFalse((root / "research" / "data" / "normalized" / "papers_deduped.jsonl").exists())
            payloads = [json.loads(line) for line in candidates_path.read_text(encoding="utf-8").splitlines()]
            self.assertEqual(len(payloads), 2)
            joined_notes = ",".join(",".join(item["notes"]) for item in payloads)
            self.assertIn("origin_seed:demo_seed", joined_notes)
            self.assertEqual(list((root / "docs").rglob("*")), [])
