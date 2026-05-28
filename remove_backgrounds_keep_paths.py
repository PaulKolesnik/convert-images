#!/usr/bin/env python3
"""Remove image backgrounds while preserving full directory structure.

Input tree is scanned recursively. Output keeps the same relative folders and
keeps original file names. For JPG/JPEG inputs, output is <original_name>.png
so the original base file name stays visible (for example: photo.jpg.png).
"""

from __future__ import annotations

import argparse
from pathlib import Path

from rembg import remove


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Remove backgrounds from all PNG/JPG/JPEG files recursively and "
            "save outputs while preserving folder structure."
        )
    )
    parser.add_argument("input_root", type=Path, help="Root folder with source images")
    parser.add_argument("output_root", type=Path, help="Root folder for processed images")
    return parser.parse_args()


def iter_image_files(input_root: Path) -> list[Path]:
    return sorted(
        file_path
        for file_path in input_root.rglob("*")
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
    )


def build_output_relative_path(source_relative_path: Path) -> Path:
    suffix = source_relative_path.suffix.lower()
    if suffix == ".png":
        return source_relative_path
    return source_relative_path.with_name(source_relative_path.name + ".png")


def run_conversion(input_root: Path, output_root: Path) -> tuple[int, int]:
    if not input_root.exists() or not input_root.is_dir():
        raise ValueError(f"Input root not found or not a directory: {input_root}")

    output_root.mkdir(parents=True, exist_ok=True)
    image_files = iter_image_files(input_root)
    if not image_files:
        print("No PNG/JPG/JPEG files found.")
        return 0, 0

    processed = 0
    failed = 0

    for source_path in image_files:
        try:
            relative = source_path.relative_to(input_root)
            output_relative = build_output_relative_path(relative)
            output_path = output_root / output_relative

            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_bytes = remove(source_path.read_bytes())
            output_path.write_bytes(output_bytes)

            processed += 1
            print(f"OK: {relative} -> {output_relative}")
        except Exception as exc:  # noqa: BLE001
            failed += 1
            print(f"FAIL: {source_path} ({exc})")

    return processed, failed


def main() -> int:
    args = parse_args()
    try:
        processed, failed = run_conversion(args.input_root, args.output_root)
    except ValueError as exc:
        print(exc)
        return 1

    print(f"Done. Processed: {processed}, Failed: {failed}")
    return 0 if failed == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
