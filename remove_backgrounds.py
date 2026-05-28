#!/usr/bin/env python3
"""Batch-remove image backgrounds with rembg.

Reads PNG/JPG/JPEG files from an input folder and writes transparent PNG
results to an output folder.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from rembg import remove


SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg"}


def parse_args() -> argparse.Namespace:
	parser = argparse.ArgumentParser(
		description=(
			"Remove backgrounds from all PNG/JPG/JPEG files in a folder and "
			"save transparent PNG files in another folder."
		)
	)
	parser.add_argument("input_folder", type=Path, help="Folder with source images")
	parser.add_argument("output_folder", type=Path, help="Folder for PNG outputs")
	parser.add_argument(
		"--recursive",
		action="store_true",
		help="Process files in subfolders as well",
	)
	return parser.parse_args()


def iter_image_files(input_folder: Path, recursive: bool) -> list[Path]:
	files = input_folder.rglob("*") if recursive else input_folder.glob("*")
	return sorted(
		file_path
		for file_path in files
		if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS
	)


def unique_output_path(output_folder: Path, file_stem: str) -> Path:
	"""Avoid overwriting when files share the same stem (e.g., a.jpg and a.png)."""
	candidate = output_folder / f"{file_stem}.png"
	if not candidate.exists():
		return candidate

	index = 1
	while True:
		candidate = output_folder / f"{file_stem}_{index}.png"
		if not candidate.exists():
			return candidate
		index += 1


def process_images(input_folder: Path, output_folder: Path, recursive: bool) -> tuple[int, int]:
	if not input_folder.exists() or not input_folder.is_dir():
		raise ValueError(f"Input folder not found or not a directory: {input_folder}")

	output_folder.mkdir(parents=True, exist_ok=True)
	image_files = iter_image_files(input_folder, recursive)

	processed = 0
	failed = 0

	if not image_files:
		print("No PNG/JPG/JPEG files found.")
		return processed, failed

	for src_path in image_files:
		try:
			output_path = unique_output_path(output_folder, src_path.stem)
			input_bytes = src_path.read_bytes()
			output_bytes = remove(input_bytes)
			output_path.write_bytes(output_bytes)
			processed += 1
			print(f"OK: {src_path.name} -> {output_path.name}")
		except Exception as exc:  # noqa: BLE001
			failed += 1
			print(f"FAIL: {src_path.name} ({exc})")

	return processed, failed


def main() -> int:
	args = parse_args()

	try:
		processed, failed = process_images(
			input_folder=args.input_folder,
			output_folder=args.output_folder,
			recursive=args.recursive,
		)
	except ValueError as exc:
		print(exc)
		return 1

	print(f"Done. Processed: {processed}, Failed: {failed}")
	return 0 if failed == 0 else 2


if __name__ == "__main__":
	raise SystemExit(main())
