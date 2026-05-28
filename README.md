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
