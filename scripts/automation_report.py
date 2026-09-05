#!/usr/bin/env python3
"""Summaries and health checks for the scheduled paper workflow."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONFIG = ROOT / "config" / "sources.json"
DEFAULT_REPORT = ROOT / "data" / "last_ingest_report.json"
DEFAULT_QUEUE = ROOT / "data" / "review_queue.json"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def assess_run(config: dict[str, Any], report: dict[str, Any]) -> dict[str, Any]:
    enabled_remote = {
        source["id"]
        for source in config.get("sources", [])
        if source.get("enabled", True) and source.get("kind") != "manual"
    }
    completed_remote = enabled_remote.intersection(report.get("source_counts", {}))
    errors = [str(error) for error in report.get("errors", [])]
    source_errors = [
        error
        for error in errors
        if any(error.startswith(f"{source_id}:") for source_id in enabled_remote)
    ]
    healthy = bool(completed_remote) if enabled_remote else True
    return {
        "healthy": healthy,
        "enabled_sources": len(enabled_remote),
        "completed_sources": len(completed_remote),
        "failed_sources": len(source_errors),
        "queued": int(report.get("queued", 0)),
        "pending": int(report.get("pending_total", 0)),
        "fetched": int(report.get("fetched", 0)),
        "duplicates": int(report.get("duplicates", 0)),
        "errors": errors,
    }


def render_run_summary(result: dict[str, Any], report: dict[str, Any]) -> str:
    status = "✅ 可用" if result["healthy"] else "❌ 所有远程来源均失败"
    lines = [
        "## 每日论文采集结果",
        "",
        f"- 状态：{status}",
        f"- 运行时间：{report.get('run_at', 'unknown')}",
        f"- 成功来源：{result['completed_sources']} / {result['enabled_sources']}",
        f"- 获取记录：{result['fetched']}",
        f"- 新增候选：{result['queued']}",
        f"- 当前待审核：{result['pending']}",
        f"- 重复记录：{result['duplicates']}",
    ]
    if result["errors"]:
        lines.extend(["", "### 警告", ""])
        lines.extend(f"- `{error}`" for error in result["errors"])
    return "\n".join(lines) + "\n"


def render_queue_summary(queue: dict[str, Any], report: dict[str, Any]) -> str:
    papers = queue.get("papers", [])
    lines = [
        "## 每日 Physical AI 论文审核队列",
        "",
        "此 PR 由每日任务持续更新。请核对来源、摘要、相关性和技术路线，再批准或拒绝候选。",
        "",
        f"- 最近运行：{report.get('run_at', 'unknown')}",
        f"- 本次新增：{int(report.get('queued', 0))}",
        f"- 待审核总数：{len(papers)}",
        "",
        "### 待审核候选",
        "",
    ]
    if not papers:
        lines.append("当前没有待审核候选。")
    for paper in papers:
        title = str(paper.get("title", "Untitled")).replace("\n", " ")
        paper_id = paper.get("id", "unknown")
        source_url = paper.get("source", {}).get("url", "")
        route = paper.get("taxonomy", {}).get("route_id", "unclassified")
        score = paper.get("taxonomy", {}).get("relevance_score", 0)
        linked_title = f"[{title}]({source_url})" if source_url else title
        lines.extend(
            [
                f"- [ ] **{linked_title}**",
                f"  - ID: `{paper_id}` · 路线: `{route}` · 相关性: `{score}`",
            ]
        )
    lines.extend(
        [
            "",
            "### 审核方式",
            "",
            "使用项目 README 中的 `review --approve` 或 `review --reject` 命令处理候选；处理结果提交到此分支后，本 PR 会自动更新。",
        ]
    )
    return "\n".join(lines) + "\n"


def append_output(values: dict[str, Any]) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return
    with open(output_path, "a", encoding="utf-8") as output:
        for key, value in values.items():
            rendered = str(value).lower() if isinstance(value, bool) else str(value)
            output.write(f"{key}={rendered}\n")


def command_assess(args: argparse.Namespace) -> int:
    report = read_json(args.report)
    result = assess_run(read_json(args.config), report)
    summary = render_run_summary(result, report)
    print(summary, end="")
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as output:
            output.write(summary)
    append_output({key: result[key] for key in ("healthy", "queued", "pending", "fetched")})
    return 0 if result["healthy"] else 1


def command_queue_summary(args: argparse.Namespace) -> int:
    rendered = render_queue_summary(read_json(args.queue), read_json(args.report))
    args.output.write_text(rendered, encoding="utf-8")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    assess = subparsers.add_parser("assess", help="check source health and summarize a run")
    assess.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    assess.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    assess.set_defaults(func=command_assess)

    queue = subparsers.add_parser("queue-summary", help="render the persistent review PR body")
    queue.add_argument("--queue", type=Path, default=DEFAULT_QUEUE)
    queue.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    queue.add_argument("--output", type=Path, required=True)
    queue.set_defaults(func=command_queue_summary)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
