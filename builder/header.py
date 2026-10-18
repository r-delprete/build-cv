from reportlab.lib.units import mm
from reportlab.platypus import Image as RLImage
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

from cv_data import PersonalInfo
from styles import (
    CONTENT_WIDTH,
    HEADER_PHOTO_COLUMN,
    LAYOUT,
    contact,
    link,
    name,
    role,
)


def build_header(personal: PersonalInfo, profile_photo: RLImage):
    """Builds the header of the CV."""

    social_links = [
        link(item["url"], item["type"].capitalize())
        for item in personal.links
    ]

    left = [
        Paragraph(personal.name, name),
        Spacer(1, LAYOUT.header_name_gap),
        Paragraph(personal.role, role),
        Spacer(1, LAYOUT.header_role_gap),
        Paragraph(
            link(f"mailto:{personal.email}",
                 personal.email)
            + "&nbsp;&nbsp;|&nbsp;&nbsp;"
            + link(f"tel:{personal.phone}", personal.phone)
            + "<br/>"
            + "&nbsp;&nbsp;|&nbsp;&nbsp;".join(social_links),
            contact,
        ),
    ]

    head = Table(
        [[left, "", profile_photo]],
        colWidths=[
            CONTENT_WIDTH - HEADER_PHOTO_COLUMN - LAYOUT.header_photo_gap_mm * mm,
            LAYOUT.header_photo_gap_mm * mm,
            HEADER_PHOTO_COLUMN,
        ],
    )

    head.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1),
         LAYOUT.table_vertical_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1),
         LAYOUT.table_vertical_padding),
    ]))

    return [
        head,
        Spacer(1, LAYOUT.header_bottom_gap),
    ]
