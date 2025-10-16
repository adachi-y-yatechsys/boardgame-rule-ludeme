"""Generate a JSON summary of the latest diff verification archives."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def _resolve_repo_root() -> Path:
    current = Path(__file__).resolve()
    # reports/ludeme/archive -> repo root is three levels up
    return current.parents[3]


def _prepare_sys_path() -> None:
    root = _resolve_repo_root()
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))


def build_summary(archive_dir: Path, count: int) -> list[dict]:
    """Return a serialisable payload describing the latest archives."""

    from tools.ludeme_diff.outputs import list_archives

    summaries = []
    for metadata in list_archives(archive_dir, latest=count):
        summaries.append(metadata.as_dict(relative_to=archive_dir))
    return summaries


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--archive-dir",
        dest="archive_dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory containing archive runs.",
    )
    parser.add_argument(
        "--count",
        dest="count",
        type=int,
        default=5,
        help="Number of latest archives to include.",
    )
    parser.add_argument(
        "--output",
        dest="output_path",
        type=Path,
        default=None,
        help="Optional output path. Defaults to <archive-dir>/latest_summary.json.",
    )

    args = parser.parse_args(argv)

    _prepare_sys_path()

    archive_dir: Path = args.archive_dir
    count: int = max(args.count, 0)
    output_path: Path = (
        args.output_path
        if args.output_path is not None
        else archive_dir / "latest_summary.json"
    )

    archive_dir.mkdir(parents=True, exist_ok=True)
    summary = build_summary(archive_dir, count)
    payload = json.dumps(summary, ensure_ascii=False, indent=2)
    output_path.write_text(payload, encoding="utf-8")

    print(json.dumps({"output": str(output_path), "count": len(summary)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":  # pragma: no cover - manual utility
    sys.exit(main())
