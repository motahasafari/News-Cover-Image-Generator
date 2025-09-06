# News Cover Image Generator

A Python function to generate square news cover images with optional Persian/Arabic text overlays. Supports **normal**, **breaking news**, and **photo-only** styles.

This project is fully customizable: you can change fonts, overlays, image size, and text formatting to fit your needs.

---

## Features

- Generates 3000×3000px square images.
- Supports Persian/Arabic text with proper shaping (`arabic_reshaper`) and direction (`bidi`).
- Optional overlays:
  - Normal news (`gradient.png`)
  - Breaking news (`breaking_overlay.png`)
- Supports:
  - Local background image
  - Blank template
  - Downloaded images from URLs
- Display image or save to file.
- Wraps long text lines automatically.
- Fully customizable: fonts, overlays, text size, and image output.


---

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd News Cover Image Generator

# Install dependencies
pip install Pillow arabic-reshaper python-bidi requests
```

---

## Project Structure

```
News-Cover-Image-Generator/
├── src/
│   ├── picture.py        # Main function
│   ├── cache/
│   │   └── Download/
│   └── files/
│       ├── font.ttf
│       ├── gradient.png
│       ├── breaking_overlay.png
│       └── blank.png
├── requirements.txt
├── README.md
└── .gitignore

```

---

## Usage

```python
from picture import picture

result = picture(
    bg="blank",  # "cmp:/path/to/image.png" or "url:http://example.com/image.jpg"
    text="Breaking News & Here is the Title",
    text_size=30,
    news_type="normal",  # "normal", "breaking", or "photo"
    replace=None,
    save_at="show"  # path to save or "show" to display
)

print(result)
```

---

### `picture()` Arguments

| Argument    | Type   | Description |
|------------|--------|-------------|
| `bg`       | str    | Background source:<br>• `"cmp:<path>"` → local file<br>• `"url:<http://...>"` → download<br>• `"blank"` → blank template |
| `text`     | str    | Text to display on cover. Use `&` for newline. |
| `text_size`| int    | Base font size (10–50). Default: 27 |
| `news_type`| str    | `"normal"` → standard overlay<br>`anything else` → breaking news overlay<br>`"photo"` → no overlay |
| `replace`  | str    | Existing filename (without extension) to overwrite. Default: None |
| `save_at`  | str    | File path to save image or `"show"` to display. Default: `"show"` |

---

### Return Value

`picture()` returns a dictionary:

- `{"status": "success", "location": "<file_path>"}` → Saved successfully
- `{"status": "success", "message": "Image shown"}` → Displayed only
- `{"status": "error", "message": "<error details>"}` → Any error occurred

---

## Notes

- Requires files in `files/` directory:
  - `gradient.png` → Normal news overlay
  - `breaking_overlay.png` → Breaking news overlay
  - `blank.png` → Blank template
  - `font.ttf` → Custom font
- Long text will be automatically wrapped to fit the image.
- Make sure `cache/Download` exists if using `url:` backgrounds.
- `.gitignore` should include `cache/` to avoid uploading downloaded images.
- **Customizable**: change fonts, overlays, text size, and output image path freely.
- If you want to customize covers:
  - go to `/files` and replace the default overlay to your overlay, but don't change name of files

---

## Example Output

```python
res = picture(
    "blank",
    "Hello world",
    30,
    "normal",
    None,
    "show"
)
print(res)
# -> {"status": "success", "message": "Image shown"}
```

---

## License

MIT License © 2025

