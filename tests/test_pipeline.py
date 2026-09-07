from __future__ import annotations

import datetime as dt
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from wm_pipeline import (  # noqa: E402
    apply_llm_review,
    build_paper_graph,
    classify_record,
    load_config,
    load_legacy_graph,
    local_date,
    normalize_authors,
    parse_arxiv_feed,
    parse_openreview_payload,
    render_readme_stats,
    validate_all,
)


class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config()

    def test_arxiv_normalization_strips_version_and_detects_venue(self) -> None:
        payload = (ROOT / "tests" / "fixtures" / "arxiv.xml").read_bytes()
        records = parse_arxiv_feed(payload, "fixture", "2026-08-12T00:00:00Z")
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]["id"], "arxiv:2608.01234")
        self.assertEqual(records[0]["publication"]["status"], "accepted")
        self.assertEqual(records[0]["publication"]["venue"], "CoRL 2026")

    def test_openreview_v2_values_are_unwrapped(self) -> None:
        payload = (ROOT / "tests" / "fixtures" / "openreview.json").read_bytes()
        source = {"id": "fixture", "name": "ICLR 2026", "venue_id": "ICLR.cc/2026/Conference", "accepted_only": True}
        records = parse_openreview_payload(payload, source, "2026-08-12T00:00:00Z")
        self.assertEqual(records[0]["authors"][0], "Alice Example")
        self.assertEqual(records[0]["publication"]["status"], "accepted")
        self.assertEqual(records[0]["publication"]["venue"], "ICLR 2026 Poster")

    def test_classifier_scores_and_routes_world_action_model(self) -> None:
        payload = (ROOT / "tests" / "fixtures" / "arxiv.xml").read_bytes()
        record = parse_arxiv_feed(payload, "fixture")[0]
        classify_record(record, self.config)
        self.assertGreaterEqual(record["taxonomy"]["relevance_score"], 4)
        self.assertEqual(record["taxonomy"]["route_id"], "action_ground")

    def test_classifier_routes_embodied_foundation_model_report(self) -> None:
        record = {
            "title": "Embodied Foundation Models are One-Shot Learners",
            "abstract": "A robot learns closed-loop physical skills from demonstrations.",
            "authors": ["Example Team"],
            "affiliations": [],
            "taxonomy": {},
        }
        classify_record(record, self.config)
        self.assertGreaterEqual(record["taxonomy"]["relevance_score"], 4)
        self.assertEqual(record["taxonomy"]["route_id"], "action_ground")

    def test_export_reuses_existing_node_and_links_known_team(self) -> None:
        base = {"nodes": [{"id": "existing", "name": "Existing", "type": "product_paper"}, {"id": "Meta_FAIR", "name": "Meta FAIR", "type": "company"}], "links": []}
        record = {
            "id": "arxiv:1234.56789",
            "graph_node_id": "existing",
            "title": "A World Model",
            "title_zh": "一个世界模型",
            "authors": [],
            "affiliations": ["Meta FAIR"],
            "abstract": "",
            "summary_zh": "摘要",
            "contribution_zh": "贡献",
            "source": {"kind": "arxiv", "external_id": "1234.56789", "url": "https://arxiv.org/abs/1234.56789", "pdf_url": ""},
            "publication": {"status": "preprint", "venue": "arXiv", "published_at": "2026-08-10T00:00:00Z", "updated_at": "2026-08-10T00:00:00Z"},
            "taxonomy": {"route_id": "latent_wm", "topics": [], "relevance_score": 8},
            "team_node_ids": ["Meta_FAIR"],
            "review": {"status": "approved", "reviewed_at": "2026-08-12T00:00:00Z"},
            "provenance": {"discovered_at": "2026-08-12T00:00:00Z", "source_name": "test", "evidence_urls": []}
        }
        graph = build_paper_graph(self.config, [record], base, dt.datetime(2026, 8, 12, tzinfo=dt.timezone.utc))
        self.assertEqual(graph["nodes"][0]["id"], "existing")
        self.assertEqual(graph["meta"]["new_nodes"], 0)
        self.assertEqual(graph["links"][0]["relation_type"], "released_by")

    def test_readme_stats_include_merged_graph_totals(self) -> None:
        base = {
            "nodes": [{"id": "base"}],
            "links": [{"source": "base", "target": "base", "relation_type": "related"}],
        }
        paper = {
            "meta": {"approved_papers": 2, "new_nodes": 1},
            "links": [{"source": "paper", "target": "base", "relation_type": "authored_by"}],
        }
        stats = render_readme_stats(config=self.config, base_graph=base, paper_graph=paper)
        self.assertIn("| 实体数 | 2 |", stats)
        self.assertIn("| 关系数 | 2 |", stats)
        self.assertIn("| 关系类型 | 2 种 |", stats)
        self.assertIn("| 已审核论文/技术报告 | 2 篇 |", stats)

    def test_llm_review_is_shadow_advice_and_validates_fields(self) -> None:
        record = {"taxonomy": {"route_id": "latent_wm", "topics": []}, "review": {"status": "pending"}}
        value = {
            "decision": "approve",
            "confidence": 1.4,
            "reason": "直接研究机器人动作条件世界模型",
            "title_zh": "机器人世界模型",
            "summary_zh": "摘要",
            "contribution_zh": "贡献",
            "route_id": "action_ground",
            "topics": ["机器人", "世界模型"],
        }
        reviewed_at = dt.datetime(2026, 9, 5, tzinfo=dt.timezone.utc)
        apply_llm_review(record, value, self.config["taxonomy"], "test-model", reviewed_at)
        self.assertEqual(record["review"]["status"], "pending")
        self.assertEqual(record["ai_review"]["decision"], "approve")
        self.assertEqual(record["ai_review"]["confidence"], 1.0)
        self.assertEqual(record["ai_review"]["mode"], "shadow")
        self.assertEqual(record["taxonomy"]["route_id"], "action_ground")

    def test_manual_author_string_is_kept_as_one_name(self) -> None:
        self.assertEqual(normalize_authors("Alice Example"), ["Alice Example"])

    def test_pipeline_date_uses_configured_timezone(self) -> None:
        instant = dt.datetime(2026, 9, 5, 16, 30, tzinfo=dt.timezone.utc)
        self.assertEqual(local_date(instant, self.config), dt.date(2026, 9, 6))

    def test_repository_curated_data_is_valid(self) -> None:
        self.assertGreater(len(load_legacy_graph()["nodes"]), 500)
        errors, _warnings = validate_all(self.config)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
