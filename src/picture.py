def picture(bg, text, text_size=27, news_type="normal", replace=None, save_at='show'):
    """
    Generate a news cover image with overlay and optional text.

    This function creates a square-shaped ( 3000px * 3000px )news cover image, applies an overlay 
    (normal or breaking news), and optionally places Persian/Arabic text 
    on it using `arabic_reshaper` and `bidi`. 
    The result can be displayed or saved to disk.

    Args:
        bg (str):
            Background source for the image:
              - "cmp:<path>" → Local image path.
              - "url:<http://...>" → Image from the internet (auto-downloaded & cached).
              - "blank" → Uses a blank image from files.
        text (str):
            The text to display on the cover. 
            Use "&" to force a new line.
        text_size (int, optional):
            Base font size (10-50). Default is 27.
        news_type (str, optional):
            "normal" → Standard news overlay.
            Anything else → Breaking news overlay.
            "photo" → No overlay, only image shown.
        replace (str, optional):
            Existing image name (without extension) to overwrite. Default is None.
        save_at (str, optional):
            Path to save the image. If set to "show", 
            the image will only be displayed. Default is "show".

    Returns:
        dict: A dictionary describing the result, useful for GUI (e.g., PyQt MessageBox):
            - {"status": "success", "location": "<file_path>"} → When saved successfully.
            - {"status": "success", "message": "Image shown"} → When shown only.
            - {"status": "error", "message": "<error details>"} → If an error occurred.

    Raises:
        None explicitly. All errors are caught and returned as {"status": "error"}.

    Notes:
        - Requires the following files in the `files/` directory:
            * gradient.png
            * breaking_overlay.png
            * blank.png
            * font.ttf

    Example:
        >>> result = picture("cmp:C:/images/bg.png", "Breaking News & Title of News")
        >>> if result["status"] == "success":
        ...     print("Done:", result.get("location", result.get("message")))
        ... else:
        ...     print("Error:", result["message"])
    """
    from PIL import Image, ImageDraw, ImageFont
    import arabic_reshaper
    from bidi.algorithm import get_display
    import csv
    import os
    from datetime import datetime
    from requests import get, exceptions

    try:
        datetime_now = datetime.now().strftime("%Y%m%d-%H%M%S")
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        text = text.replace('&', '\n')
        background = None

        try:
            if news_type == "normal":
                overlay = Image.open(os.path.join(BASE_DIR, "files", "gradient.png")).convert("RGBA")
            else:
                overlay = Image.open(os.path.join(BASE_DIR, "files", "breaking_overlay.png")).convert("RGBA")
        except Exception:
            return {"status": "error", "message": "Overlay file not found"}

        if bg[:4] == "cmp:":
            if not os.path.exists(bg[4:]):
                return {"status": "error", "message": f"Background not found: {bg[4:]}"}
            background = Image.open(bg[4:]).convert("RGBA")

        elif bg[:5] == "blank":
            try:
                background = Image.open(os.path.join(BASE_DIR, "files", "blank.png")).convert("RGBA")
                overlay = Image.open(os.path.join(BASE_DIR, "files", "breaking_overlay.png")).convert("RGBA")
            except Exception:
                return {"status": "error", "message": "Blank background not found"}

        elif bg[:4] == "url:":
            url = bg[4:]
            try:
                response = get(url, timeout=10)
            except exceptions.RequestException:
                return {"status": "error", "message": "Failed to download image from URL"}

            if response.status_code != 200:
                return {"status": "error", "message": f"Bad response: {response.status_code}"}

            with open("cache/Download/last_download.png", "wb") as ff:
                ff.write(response.content)

            LIST_DIR = os.listdir("cache/Download")

            if len(LIST_DIR) == 1 or os.path.exists("cache/Download/last_download.png"):
                background = Image.open(f"cache/Download/{LIST_DIR[0]}").convert("RGBA")

            else:
                return {"status": "error", "message": "Faild "}
                

        else:
            return {"status": "error", "message": "Invalid bg parameter"}

        try:
            wallpaper = Image.open(os.path.join(BASE_DIR, "files", "blank.png")).convert("RGBA")
        except Exception:
            return {"status": "error", "message": "Wallpaper file not found"}

        width, height = background.size
        square_size = min(width, height)
        left, top = (width - square_size) // 2, (height - square_size) // 2
        background = background.crop((left, top, left + square_size, top + square_size))
        background = background.resize(wallpaper.size)
        wallpaper.paste(background, (0, 0))
        background = wallpaper

        if news_type != 'photo':
            overlay = overlay.resize(background.size)
            background.paste(overlay, (0, 0), overlay)

            reshaped_text = arabic_reshaper.reshape(text)
            bidi_text = get_display(reshaped_text)

            draw = ImageDraw.Draw(background)
            font_path = os.path.join(BASE_DIR, "files", "font.ttf")
            if not os.path.exists(font_path):
                return {"status": "error", "message": "Font file not found"}

            font = ImageFont.truetype(font_path, int(text_size) * 10)

            lines = bidi_text.split("\n")
            line_spacing = (int(text_size)*10)//3.3
            line_sizes, total_height = [], 0
            for line in lines:
                bbox = draw.textbbox((0, 0), line, font=font)
                w, h = bbox[2]-bbox[0], bbox[3]-bbox[1]
                total_height += h + line_spacing
                line_sizes.append((w, h))
            total_height -= line_spacing

            if news_type == "normal":
                start_y = (background.size[1] - total_height) // 7
            else:
                start_y = (background.size[1] - total_height) // 2
            if bg[:5] == "blank":
                start_y = (background.size[1] - total_height) // 2

            y = start_y
            for i, line in enumerate(lines):
                w, h = line_sizes[i]
                x = (background.size[0] - w) // 2
                draw.text((x, y), line, font=font, fill="white")
                y += h + line_spacing

        if save_at == 'show':
            background.show()
            return {"status": "success", "message": "Image shown"}

        else:
            file_name = (replace if replace else datetime_now) + ".png"
            location = os.path.join(save_at, file_name)
            try:
                background.save(location, format="PNG")
            except Exception:
                return {"status": "error", "message": "Failed to save final image"}

            return {"status": "success", "location": location}

    except Exception as e:
        return {"status": "error", "message": str(e)}

