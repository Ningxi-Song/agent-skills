from __future__ import annotations

import argparse
import json
from pathlib import Path


def convert(source: Path, output: Path) -> dict[str, object]:
    """Convert one local file to a separate UTF-8 Markdown file."""
    if not source.is_file():
        raise FileNotFoundError(f"Input file does not exist: {source}")

    try:
        from markitdown import MarkItDown
    except ImportError as exc:
        raise RuntimeError(
            "MarkItDown is unavailable; install the required markitdown extras "
            "in the skill's isolated environment"
        ) from exc

    result = MarkItDown(enable_plugins=False).convert_local(source)
    text = result.text_content
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    return {
        "source": str(source.resolve()),
        "output": str(output.resolve()),
        "characters": len(text),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert a local document to Markdown without plugins or cloud services."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("-o", "--output", required=True, type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        metadata = convert(args.source, args.output)
    except (FileNotFoundError, ValueError, RuntimeError, ImportError) as exc:
        parser.exit(2, f"markitdown-local: {exc}\n")

    print(json.dumps(metadata) if args.json else args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
