#!/usr/bin/env python3
"""CLI for the daily paper collection, review, export and validation workflow."""

from __future__ import annotations

import argparse
import json
import sys

from wm_pipeline import build_digest, collect_candidates, export_graph_data, load_config, review_records, validate_all


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="World Model Mapping daily publication pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)
    collect = subparsers.add_parser("collect", help="Fetch sources and append relevant records to the review queue")
    collect.add_argument("--since-hours", type=int, default=None, help="Override the configured lookback; 0 fetches without a date cutoff")
    review = subparsers.add_parser("review", help="Approve or reject queued records")
    action = review.add_mutually_exclusive_group(required=True)
    action.add_argument("--approve", nargs="+", metavar="ID")
    action.add_argument("--reject", nargs="+", metavar="ID")
    review.add_argument("--reviewer", required=True)
    review.add_argument("--route", dest="route_id")
    review.add_argument("--notes", default="")
    subparsers.add_parser("export", help="Generate paper-data.js from approved records")
    subparsers.add_parser("digest", help="Generate the current daily digest")
    subparsers.add_parser("validate", help="Validate curated records and graph references")
    run = subparsers.add_parser("run", help="Run collect, export, digest and validate")
    run.add_argument("--since-hours", type=int, default=None)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    config = load_config()
    if args.command == "collect":
        print_json(collect_candidates(config, since_hours=args.since_hours))
        return 0
    if args.command == "review":
        action = "approve" if args.approve else "reject"
        ids = args.approve or args.reject
        print_json(review_records(action=action, record_ids=ids, reviewer=args.reviewer, route_id=args.route_id, notes=args.notes))
        return 0
    if args.command == "export":
        print_json(export_graph_data(config=config)["meta"])
        return 0
    if args.command == "digest":
        digest = build_digest()
        print_json({key: digest[key] for key in ("date", "generated_at", "pending_total")})
        return 0
    if args.command == "validate":
        errors, warnings = validate_all(config)
        print_json({"ok": not errors, "errors": errors, "warnings": warnings})
        return 1 if errors else 0
    if args.command == "run":
        report = collect_candidates(config, since_hours=args.since_hours)
        graph = export_graph_data(config=config)
        digest = build_digest()
        errors, warnings = validate_all(config)
        print_json({"collection": report, "graph": graph["meta"], "digest": {"date": digest["date"], "pending_total": digest["pending_total"]}, "errors": errors, "warnings": warnings})
        return 1 if errors else 0
    return 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, RuntimeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2)
