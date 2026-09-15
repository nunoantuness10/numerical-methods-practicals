"""Command-line entry point."""

from __future__ import annotations

import argparse
import json

from .experiments import run_all


def main() -> None:
    parser = argparse.ArgumentParser(description="Experiencias de Metodos Numericos")
    parser.add_argument("--output", default="results")
    parser.add_argument("--figures", default="figures")
    args = parser.parse_args()
    result = run_all(args.output, args.figures)
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
