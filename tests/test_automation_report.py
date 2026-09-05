from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from automation_report import assess_run, render_queue_summary  # noqa: E402


class AutomationReportTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = {
            "sources": [
                {"id": "arxiv", "kind": "arxiv", "enabled": True},
                {"id": "openreview", "kind": "openreview", "enabled": True},
            ]
        }

    def test_one_successful_source_keeps_run_healthy(self) -> None:
        report = {
            "source_counts": {"arxiv": 0},
            "errors": ["openreview: timed out", "llm: unavailable"],
            "queued": 0,
        }
        result = assess_run(self.config, report)
        self.assertTrue(result["healthy"])
        self.assertEqual(result["completed_sources"], 1)

    def test_all_remote_sources_failed_marks_run_unhealthy(self) -> None:
        report = {
            "source_counts": {"manual-inbox": 0},
            "errors": ["arxiv: timed out", "openreview: HTTP 503"],
        }
        self.assertFalse(assess_run(self.config, report)["healthy"])

    def test_queue_summary_contains_review_details(self) -> None:
        queue = {
            "papers": [
                {
                    "id": "arxiv:1234.56789",
                    "title": "A Physical World Model",
                    "source": {"url": "https://arxiv.org/abs/1234.56789"},
                    "taxonomy": {"route_id": "latent_wm", "relevance_score": 8.5},
                    "ai_review": {"decision": "approve", "confidence": 0.92, "reason": "直接研究物理世界建模"},
                }
            ]
        }
        rendered = render_queue_summary(queue, {"run_at": "2026-09-05T00:00:00Z", "queued": 1})
        self.assertIn("A Physical World Model", rendered)
        self.assertIn("arxiv:1234.56789", rendered)
        self.assertIn("待审核总数：1", rendered)
        self.assertIn("建议批准", rendered)
        self.assertIn("置信度 92%", rendered)


if __name__ == "__main__":
    unittest.main()
