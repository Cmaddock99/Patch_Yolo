from __future__ import annotations

import json
import unittest
from pathlib import Path

import feedparser

from research.pipeline import (
    PaperRecord,
    apply_crossref_enrichment,
    apply_unpaywall_enrichment,
    compute_rank_score,
    dedupe_papers,
    load_yaml,
    normalize_doi,
    parse_arxiv_entry,
    parse_openalex_work,
    parse_semantic_scholar_paper,
    rebuild_openalex_abstract,
)


FIXTURES = Path(__file__).resolve().parents[1] / "research" / "fixtures"


class PipelineParsingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.openalex = json.loads((FIXTURES / "openalex_work.json").read_text(encoding="utf-8"))
        self.semantic = json.loads((FIXTURES / "semanticscholar_paper.json").read_text(encoding="utf-8"))
        self.crossref = json.loads((FIXTURES / "crossref_work.json").read_text(encoding="utf-8"))
        self.unpaywall = json.loads((FIXTURES / "unpaywall.json").read_text(encoding="utf-8"))
        self.arxiv_feed = feedparser.parse((FIXTURES / "arxiv_feed.xml").read_text(encoding="utf-8"))

    def test_rebuild_openalex_abstract(self) -> None:
        abstract = rebuild_openalex_abstract(self.openalex["abstract_inverted_index"])
        self.assertEqual(abstract, "Transferable adversarial patch attacks on YOLO detectors")

    def test_parse_openalex_work(self) -> None:
        record = parse_openalex_work(self.openalex, "patch query")
        self.assertEqual(record.title, "Transferable adversarial patch attacks on YOLO detectors")
        self.assertEqual(record.publisher, "CVF")
        self.assertEqual(record.oa_status, "green")
        self.assertEqual(record.verification_state, "candidate")

    def test_parse_semantic_scholar_paper_normalizes_ids(self) -> None:
        record = parse_semantic_scholar_paper(self.semantic, "patch query")
        self.assertEqual(record.doi, "10.1111/example.doi")
        self.assertEqual(record.arxiv_id, "2401.12345")
        self.assertTrue(record.open_access)

    def test_parse_arxiv_entry(self) -> None:
        record = parse_arxiv_entry(self.arxiv_feed.entries[0], "patch query")
        self.assertEqual(record.arxiv_id, "2401.12345v1")
        self.assertEqual(record.doi, "10.1111/example.doi")
        self.assertEqual(record.oa_status, "preprint")

    def test_crossref_and_unpaywall_enrichment(self) -> None:
        record = PaperRecord(
            paper_uid="doi:10.1111/example.doi",
            title="",
            abstract="",
            authors=[],
            year=None,
            publication_date=None,
            venue=None,
            publisher=None,
            doi="10.1111/example.doi",
            arxiv_id=None,
            source_primary="openalex",
            sources_seen=["openalex"],
            source_ids={"openalex": "https://openalex.org/W123"},
            landing_page_url=None,
            pdf_url=None,
            open_access=None,
            oa_status=None,
            citation_count=None,
            retracted_or_updated=False,
            queries_matched=["patch query"],
            keywords_hit=[],
            verification_state="candidate",
            rank_score=0.0,
            notes=[],
        )
        apply_crossref_enrichment(record, self.crossref)
        apply_unpaywall_enrichment(record, self.unpaywall)
        self.assertEqual(record.publisher, "CVF")
        self.assertEqual(record.venue, "CVPR")
        self.assertEqual(record.publication_date, "2024-08-26")
        self.assertEqual(record.citation_count, 21)
        self.assertTrue(record.retracted_or_updated)
        self.assertEqual(record.pdf_url, "https://publisher.example.org/paper.pdf")
        self.assertEqual(record.oa_status, "gold")


class PipelineLogicTests(unittest.TestCase):
    def test_dedupe_merges_by_doi_then_arxiv(self) -> None:
        openalex_record = PaperRecord(
            paper_uid="openalex:1",
            title="Transferable adversarial patch attacks on YOLO detectors",
            abstract="openalex abstract",
            authors=["Alice Smith"],
            year=2024,
            publication_date="2024-08-26",
            venue="CVPR",
            publisher="CVF",
            doi="10.1111/example.doi",
            arxiv_id=None,
            source_primary="openalex",
            sources_seen=["openalex"],
            source_ids={"openalex": "https://openalex.org/W1"},
            landing_page_url="https://openalex.org/W1",
            pdf_url=None,
            open_access=None,
            oa_status=None,
            citation_count=10,
            retracted_or_updated=False,
            queries_matched=["q1"],
            keywords_hit=[],
            verification_state="candidate",
            rank_score=0.0,
            notes=[],
        )
        arxiv_record = PaperRecord(
            paper_uid="arxiv:1",
            title="Transferable adversarial patch attacks on YOLO detectors",
            abstract="",
            authors=["Bob Jones"],
            year=2024,
            publication_date="2024-01-15",
            venue="arXiv",
            publisher="arXiv",
            doi=None,
            arxiv_id="2401.12345",
            source_primary="arxiv",
            sources_seen=["arxiv"],
            source_ids={"arxiv": "http://arxiv.org/abs/2401.12345v1"},
            landing_page_url="http://arxiv.org/abs/2401.12345v1",
            pdf_url="http://arxiv.org/pdf/2401.12345v1",
            open_access=True,
            oa_status="preprint",
            citation_count=None,
            retracted_or_updated=False,
            queries_matched=["q2"],
            keywords_hit=[],
            verification_state="candidate",
            rank_score=0.0,
            notes=[],
        )
        semantic_record = PaperRecord(
            paper_uid="s2:1",
            title="Transferable adversarial patch attacks on YOLO detectors",
            abstract="semantic abstract",
            authors=["Alice Smith", "Bob Jones"],
            year=2024,
            publication_date=None,
            venue=None,
            publisher=None,
            doi="10.1111/example.doi",
            arxiv_id="2401.12345",
            source_primary="semanticscholar",
            sources_seen=["semanticscholar"],
            source_ids={"semanticscholar": "S2-1"},
            landing_page_url=None,
            pdf_url="https://example.org/s2.pdf",
            open_access=True,
            oa_status=None,
            citation_count=11,
            retracted_or_updated=False,
            queries_matched=["q3"],
            keywords_hit=[],
            verification_state="candidate",
            rank_score=0.0,
            notes=[],
        )

        deduped = dedupe_papers([openalex_record, arxiv_record, semantic_record])
        self.assertEqual(len(deduped), 1)
        merged = deduped[0]
        self.assertEqual(normalize_doi(merged.doi), "10.1111/example.doi")
        self.assertEqual(merged.arxiv_id, "2401.12345")
        self.assertEqual(sorted(merged.authors), ["Alice Smith", "Bob Jones"])
        self.assertEqual(sorted(merged.queries_matched), ["q1", "q2", "q3"])
        self.assertEqual(sorted(merged.sources_seen), ["arxiv", "openalex", "semanticscholar"])

    def test_ranking_penalizes_classifier_terms(self) -> None:
        config = load_yaml(Path("research/config/research_queries.yaml"))
        ranking_cfg = config["ranking"]

        detector_record = PaperRecord(
            paper_uid="a",
            title="Physical adversarial patch transferability for YOLO object detection",
            abstract="YOLO detector transferability with physical adversarial patch evaluation.",
            authors=[],
            year=2025,
            publication_date=None,
            venue=None,
            publisher=None,
            doi=None,
            arxiv_id=None,
            source_primary="openalex",
            sources_seen=["openalex"],
            source_ids={"openalex": "W1"},
            landing_page_url=None,
            pdf_url="https://example.org/a.pdf",
            open_access=True,
            oa_status=None,
            citation_count=25,
            retracted_or_updated=False,
            queries_matched=[],
            keywords_hit=[],
            verification_state="candidate",
            rank_score=0.0,
            notes=[],
        )
        classifier_record = PaperRecord(
            paper_uid="b",
            title="Adversarial patch image classification on MNIST and CIFAR",
            abstract="Image classification benchmark for adversarial patch on MNIST and CIFAR.",
            authors=[],
            year=2025,
            publication_date=None,
            venue=None,
            publisher=None,
            doi=None,
            arxiv_id=None,
            source_primary="openalex",
            sources_seen=["openalex"],
            source_ids={"openalex": "W2"},
            landing_page_url=None,
            pdf_url=None,
            open_access=False,
            oa_status=None,
            citation_count=25,
            retracted_or_updated=False,
            queries_matched=[],
            keywords_hit=[],
            verification_state="candidate",
            rank_score=0.0,
            notes=[],
        )

        detector_score, detector_hits = compute_rank_score(detector_record, ranking_cfg)
        classifier_score, classifier_hits = compute_rank_score(classifier_record, ranking_cfg)
        self.assertGreater(detector_score, classifier_score)
        self.assertIn("yolo", [hit.lower() for hit in detector_hits])
        self.assertNotIn("yolo", [hit.lower() for hit in classifier_hits])
