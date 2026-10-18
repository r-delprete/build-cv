from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from styles import FONT_DIR, FONT_FAMILY


def register_fonts():
    pdfmetrics.registerFont(
        TTFont("Body", str(FONT_DIR / f"{FONT_FAMILY}-Regular.ttf"))
    )

    pdfmetrics.registerFont(
        TTFont("Body-Bold", str(FONT_DIR / f"{FONT_FAMILY}-Bold.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("Body-Italic", str(FONT_DIR / f"{FONT_FAMILY}-Italic.ttf"))
    )
    pdfmetrics.registerFont(
        TTFont("Body-BoldItalic", str(FONT_DIR /
               f"{FONT_FAMILY}-BoldItalic.ttf"))
    )

    pdfmetrics.registerFontFamily(
        "Body",
        normal="Body",
        bold="Body-Bold",
        italic="Body-Italic",
        boldItalic="Body-BoldItalic",
    )
