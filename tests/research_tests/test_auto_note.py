from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

from research.scripts.auto_note import (
    YOLO26_FLAG_LEVEL_CONTEXT,
    YOLO26_FLAG_LEVEL_DIRECT,
    derive_draft_filename,
    detect_yolo26_flags,
    main,
    select_candidates,
)


class AutoNoteFlaggingTests(unittest.TestCase):
    def test_detect_yolo26_flags_direct_from_pdf_body(self) -> None:
        flag = detect_yolo26_flags(
            "Patch attacks on end-to-end detectors",
            "We study transfer.",
            "Our method optimizes a Hungarian matching objective with one-to-one assignment.",
        )
        self.assertIsNotNone(flag)
        self.assertEqual(flag["level"], YOLO26_FLAG_LEVEL_DIRECT)
        self.assertIn("hungarian matching", flag["keywords"])

    def test_detect_yolo26_flags_ignores_single_body_context_hit(self) -> None:
        flag = detect_yolo26_flags(
            "Patch attacks on detectors",
            "No architecture details in the abstract.",
            "We compare against RT-DETR in one appendix paragraph.",
        )
        self.assertIsNone(flag)

    def test_detect_yolo26_flags_context_requires_multiple_front_hits(self) -> None:
        flag = detect_yolo26_flags(
            "RT-DETR for End-to-End Object Detection",
            "An NMS-free detector with consistent dual assignments.",
            None,
        )
        self.assertIsNotNone(flag)
        self.assertEqual(flag["level"], YOLO26_FLAG_LEVEL_CONTEXT)
        self.assertGreaterEqual(len(flag["keywords"]), 2)

    def test_detect_yolo26_flags_does_not_flag_set_prediction_alone(self) -> None:
        flag = detect_yolo26_flags(
            "RF-DETR for orchard detection",
            "A detector for fruit detection in the field.",
            "The architecture follows a set prediction formulation.",
        )
        self.assertIsNone(flag)

    def test_select_candidates_breaks_score_ties_deterministically(self) -> None:
        records = [
            {"title": "Zulu", "paper_uid": "b", "rank_score": 5.0},
            {"title": "Alpha", "paper_uid": "c", "rank_score": 5.0},
            {"title": "Alpha", "paper_uid": "a", "rank_score": 5.0},
        ]
        ordered = select_candidates(records, top_n=3)
        self.assertEqual(
            [record["paper_uid"] for record in ordered],
            ["a", "c", "b"],
        )


class AutoNoteMainTests(unittest.TestCase):
    def _write_jsonl(self, path: Path, records: list[dict]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as fh:
            for record in records:
                fh.write(json.dumps(record) + "\n")

    def test_main_writes_flagged_draft_without_pdf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            input_path = root / "research" / "data" / "normalized" / "papers_deduped.jsonl"
            notes_dir = root / "docs" / "notes"
            drafts_dir = root / "research" / "data" / "drafts"

            record = {
                "paper_uid": "oa:1",
                "title": "Hungarian matching for patch attacks",
                "abstract": "This paper studies one-to-one assignment for detector attacks.",
                "authors": ["Alice Smith", "Bob Jones"],
                "year": 2026,
                "venue": "CVPR",
                "rank_score": 9.5,
                "sources_seen": ["openalex"],
                "keywords_hit": ["hungarian matching", "adversarial patch"],
            }
            self._write_jsonl(input_path, [record])

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(
                    [
                        "--input",
                        str(input_path),
                        "--notes-dir",
                        str(notes_dir),
                        "--drafts-dir",
                        str(drafts_dir),
                        "--top-n",
                        "1",
                    ]
                )

            self.assertEqual(exit_code, 0)
            draft_path = drafts_dir / derive_draft_filename(record)
            self.assertTrue(draft_path.exists())
            draft_text = draft_path.read_text(encoding="utf-8")
            self.assertIn("YOLO26 RELEVANCE FLAG", draft_text)
            self.assertIn("direct-loss", draft_text)
            self.assertIn("PDF not available", draft_text)

            summary_path = drafts_dir / "YOLO26_flagged.md"
            self.assertTrue(summary_path.exists())
            summary_text = summary_path.read_text(encoding="utf-8")
            self.assertIn("1 processed | 1 flagged", summary_text)
            self.assertIn("Hungarian matching for patch attacks", summary_text)

    def test_main_reports_skip_counts_for_notes_and_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp_dir:
            root = Path(tmp_dir)
            input_path = root / "research" / "data" / "normalized" / "papers_deduped.jsonl"
            notes_dir = root / "docs" / "notes"
            drafts_dir = root / "research" / "data" / "drafts"
            notes_dir.mkdir(parents=True, exist_ok=True)
            drafts_dir.mkdir(parents=True, exist_ok=True)

            records = [
                {
                    "paper_uid": "oa:1",
                    "title": "Alpha detector paper",
                    "abstract": "A study.",
                    "authors": ["Alice Smith"],
                    "year": 2024,
                    "rank_score": 10.0,
                },
                {
                    "paper_uid": "oa:2",
                    "title": "Bravo detector paper",
                    "abstract": "B study.",
                    "authors": ["Bob Jones"],
                    "year": 2024,
                    "rank_score": 9.0,
                },
                {
                    "paper_uid": "oa:3",
                    "title": "Charlie detector paper",
                    "abstract": "C study.",
                    "authors": ["Carol Lee"],
                    "year": 2024,
                    "rank_score": 8.0,
                },
            ]
            self._write_jsonl(input_path, records)

            (notes_dir / "smith2024_alpha_detector_paper.md").write_text("existing", encoding="utf-8")
            existing_draft = drafts_dir / derive_draft_filename(records[1])
            existing_draft.write_text("existing draft", encoding="utf-8")

            stdout = io.StringIO()
            with contextlib.redirect_stdout(stdout):
                exit_code = main(
                    [
                        "--input",
                        str(input_path),
                        "--notes-dir",
                        str(notes_dir),
                        "--drafts-dir",
                        str(drafts_dir),
                        "--top-n",
                        "3",
                    ]
                )

            self.assertEqual(exit_code, 0)
            report = stdout.getvalue()
            self.assertIn("Skipped existing notes:1", report)
            self.assertIn("Skipped existing drafts:1", report)
            self.assertIn("Processed:             1", report)
            self.assertIn("Drafts written:        1", report)

            new_draft = drafts_dir / derive_draft_filename(records[2])
            self.assertTrue(new_draft.exists())


if __name__ == "__main__":
    unittest.main()
