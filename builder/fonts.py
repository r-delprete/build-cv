from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PROJECT_DIR = Path(__file__).parent.parent
FONTS_DIR = PROJECT_DIR / "assets" / "fonts"


def register_fonts() -> None:
    """Register the fonts used to generate the CV PDF."""
    font_files = {
        "Body": "Carlito-Regular.ttf",
        "Body-Bold": "Carlito-Bold.ttf",
        "Body-Italic": "Carlito-Italic.ttf",
        "Body-BoldItalic": "Carlito-BoldItalic.ttf",
    }

    for font_name, filename in font_files.items():
        font_path = FONTS_DIR / filename

        if not font_path.is_file():
            raise FileNotFoundError(
                f"Font file not found: {font_path}"
            )

        pdfmetrics.registerFont(
            TTFont(font_name, str(font_path))
        )

    pdfmetrics.registerFontFamily(
        "Body",
        normal="Body",
        bold="Body-Bold",
        italic="Body-Italic",
        boldItalic="Body-BoldItalic",
    )
