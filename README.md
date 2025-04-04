# Image Optimizer

A retro-styled image optimization tool built with Python and Tkinter. Resize and compress images for web use with a Winamp-era aesthetic.

## Features

- Select a single image or a folder of images
- Maintains folder structure in the output
- Resize images to a desired width
- Choose output format: JPG, PNG, WEBP, etc.
- Displays processing progress
- Clean, retro Winamp-inspired UI

## Requirements

- Python 3.8+
- Pillow (installed via pip)

## Installation

Install dependencies:

```bash
pip install -r requirements.txt
```

## Run the app

```bash
python main.py
```

## Build executable (Windows)

```bash
pyinstaller --noconfirm --onefile --windowed --icon=icon.ico main.py
```

> The final `.exe` will be inside the `dist/` folder.

---

Developed by z1gg1 - enjoy it!
