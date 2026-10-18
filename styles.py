from io import BytesIO
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Paragraph, Table, TableStyle
from reportlab.platypus import Image as RLImage

from config import PAGE_SIZES, load_config

CONFIG_PATH = Path(__file__).with_name("config.json")
try:
    CONFIG = load_config(CONFIG_PATH)
except (ValueError, OSError) as exc:
    raise SystemExit(f"Error in configuration file: {exc}") from exc

THEME = CONFIG.theme
TYPO = CONFIG.typography
LAYOUT = CONFIG.layout

INK = colors.HexColor(THEME.ink)
MUTED = colors.HexColor(THEME.muted)
ACCENT = colors.HexColor(THEME.accent)
TINT = colors.HexColor(THEME.tint)
RULE = colors.HexColor(THEME.rule)

PAGE_SIZE = PAGE_SIZES[LAYOUT.page_size]
WIDTH, HEIGHT = PAGE_SIZE

LEFT_MARGIN = LAYOUT.left_margin_mm * mm
RIGHT_MARGIN = LAYOUT.right_margin_mm * mm
TOP_MARGIN = LAYOUT.top_margin_mm * mm
BOTTOM_MARGIN = LAYOUT.bottom_margin_mm * mm

CONTENT_WIDTH = PAGE_SIZE[0] - LEFT_MARGIN - RIGHT_MARGIN

PHOTO_SIZE = LAYOUT.photo_size_mm * mm
HEADER_PHOTO_COLUMN = LAYOUT.header_photo_column_mm * mm
TOP_BAR_HEIGHT = LAYOUT.top_bar_height_mm * mm
FOOTER_BOTTOM = LAYOUT.footer_bottom_mm * mm
SKILLS_LABEL_WIDTH = LAYOUT.skills_label_column_mm * mm

FONT_DIR = Path("/usr/share/fonts/truetype/crosextra/")
FONT_FAMILY = TYPO.font_family

base = ParagraphStyle(
    "base",
    fontName="Body",
    fontSize=TYPO.body_size,
    leading=TYPO.body_leading,
    textColor=INK,
)

name = ParagraphStyle(
    "name",
    parent=base,
    fontName="Body-Bold",
    fontSize=TYPO.name_size,
    leading=TYPO.name_leading,
)

role = ParagraphStyle(
    "role",
    parent=base,
    fontName="Body-Bold",
    fontSize=TYPO.role_size,
    leading=TYPO.role_leading,
    textColor=ACCENT,
)

contact = ParagraphStyle(
    "contact",
    parent=base,
    fontSize=TYPO.contact_size,
    leading=TYPO.contact_leading,
    textColor=INK,
)

h2 = ParagraphStyle(
    "h2",
    parent=base,
    keepWithNext=1,
    fontName="Body-Bold",
    fontSize=TYPO.section_size,
    leading=TYPO.section_leading,
    textColor=ACCENT,
    spaceBefore=TYPO.section_space_before,
    spaceAfter=TYPO.section_space_after,
)

h3 = ParagraphStyle(
    "h3",
    parent=base,
    fontName="Body-Bold",
    fontSize=TYPO.heading_size,
    leading=TYPO.heading_leading,
)

meta = ParagraphStyle(
    "meta",
    parent=base,
    textColor=MUTED,
    fontSize=TYPO.meta_size,
    leading=TYPO.meta_leading,
)

body = ParagraphStyle(
    "body",
    parent=base,
    alignment=(
        TA_JUSTIFY if TYPO.body_justified else TA_LEFT
    ),
)

bul = ParagraphStyle(
    "bul",
    parent=base,
    leftIndent=TYPO.bullet_indent,
    bulletIndent=0,
    spaceAfter=TYPO.bullet_space_after,
)

tech = ParagraphStyle(
    "tech",
    parent=base,
    textColor=MUTED,
    fontName="Body-Italic",
    fontSize=TYPO.tech_size,
    spaceBefore=TYPO.tech_space_before,
)

small = ParagraphStyle(
    "small",
    parent=base,
    fontName="Body-Italic",
    fontSize=TYPO.small_size,
    leading=TYPO.small_leading,
    textColor=MUTED,
)

subsection = ParagraphStyle(
    "sub",
    parent=base,
    fontName="Body-Bold",
    textColor=ACCENT,
    fontSize=TYPO.subsection_size,
    spaceAfter=TYPO.subsection_space_after,
)


def create_profile_photo(photo_path: Path):
    """Crop the profile photo and save it with a circular background."""

    if not photo_path.is_file():
        # Use example photo if not found
        photo_path = photo_path.parent / "cv-pic.example.png"

    if not photo_path.is_file():
        raise FileNotFoundError(
            f"Neither profile photo nor example photo was found in {photo_path}"
        )

    img = Image.open(photo_path).convert("RGB")
    box = (200, 50, 800, 650)
    img = img.crop(box).resize(
        (770, 770),
        Image.Resampling.LANCZOS,
    )

    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).ellipse(
        (0, 0, img.width - 1, img.height - 1),
        fill=255,
    )

    tint_rgb = ImageColor.getrgb(THEME.tint)
    bg = Image.new("RGBA", img.size, (*tint_rgb, 255))

    out = Image.new("RGBA", img.size, (0, 0, 0, 0))
    out.paste(img, (0, 0), mask)
    bg.paste(out, (0, 0), out)

    circ = Image.new("RGBA", img.size, (0, 0, 0, 0))
    circ.paste(bg, (0, 0), mask)

    image_buffer = BytesIO()
    circ.save(image_buffer, format="PNG")
    image_buffer.seek(0)

    return RLImage(
        image_buffer,
        width=PHOTO_SIZE,
        height=PHOTO_SIZE,
    )


def section(title):
    hr = HRFlowable(
        width="100%",
        thickness=TYPO.section_rule_thickness,
        color=RULE,
        spaceBefore=TYPO.section_rule_space_before,
        spaceAfter=TYPO.section_rule_space_after,
    )
    hr.keepWithNext = 1

    return [
        Paragraph(title.upper(), h2),
        hr,
    ]


def bullets(items):
    return [Paragraph(t, bul, bulletText="•") for t in items]


def link(url, text):
    return f'<a href="{url}" color="#4B3FD1">{text}</a>'


def edu(title, org, start_date, end_date):
    year_style = ParagraphStyle(
        "y",
        parent=meta,
        alignment=2,
    )

    table = Table(
        [[
            [
                Paragraph(f"<b>{title}</b>", base),
                Paragraph(org, meta),
            ],
            Paragraph(
                f"{start_date} – {end_date or "Present"}", year_style),
        ]],
        colWidths=[
            CONTENT_WIDTH * 0.78,
            CONTENT_WIDTH * 0.22,
        ],
    )

    table.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1),
         LAYOUT.education_top_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1),
         LAYOUT.education_bottom_padding),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    return table
