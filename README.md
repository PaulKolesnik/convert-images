# remove background from all images in a folder using rembg

Python script: `remove_backgrounds.py`

This script removes backgrounds from all PNG/JPG/JPEG files in an input folder
and writes transparent PNG files to an output folder.

## Install

```bash
pip install rembg pillow
```

## Usage

```bash
python remove_backgrounds.py <input_folder> <output_folder>
```

Optional recursive mode:

```bash
python remove_backgrounds.py <input_folder> <output_folder> --recursive
```

---

Python script: `compare_excel_images.py`

This script compares expected image file names from Excel with files that exist
in your converted output folder (for example: `Media-without`).

Expected Excel format:
- Column A: product name
- Column C: text containing media entries with `url=...`

## Install for Excel comparison

```bash
pip install openpyxl
```

## Usage

```bash
python compare_excel_images.py <excel_file.xlsx> Media-without
```

Optional flags:

```bash
python compare_excel_images.py <excel_file.xlsx> Media-without --sheet "Sheet1" --report missing_images_report.csv
```

If the first row is not headers:

```bash
python compare_excel_images.py <excel_file.xlsx> Media-without --no-header
```

---

Python script: `filter_images_from_excel.py`

Goal: create a new filtered folder from a very large image folder (for example
8GB), based on paths in Excel column B.

Expected Excel format:
- Column A: product code/name (not used for matching)
- Column B: one file path ending with file name
- Column C: multiple file paths separated by commas

This script preserves original folder names and original file names.

## Usage

```bash
python filter_images_from_excel.py <excel_file.xlsx> <source_root> <filtered_output_root>
```

Example:

```bash
python filter_images_from_excel.py .\files\photos.xlsx .\Media .\Media-filtered
```

Optional:

```bash
python filter_images_from_excel.py .\files\photos.xlsx .\Media .\Media-filtered --sheet "Sheet1" --report filter_copy_report.csv
```

---

Python script: `remove_backgrounds_keep_paths.py`

Goal: remove background recursively from filtered images while preserving full
folder structure from input to output.

For JPG/JPEG input files, output file name is `<original_name>.png` (example:
`photo.jpg` -> `photo.jpg.png`) to keep original name visible and avoid name
collisions.

## Usage

```bash
python remove_backgrounds_keep_paths.py <filtered_input_root> <without_bg_output_root>
```

Example:

```bash
python remove_backgrounds_keep_paths.py .\Media-filtered .\Media-without
```
