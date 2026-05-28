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
