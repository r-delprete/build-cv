from pathlib import Path

from reportlab.platypus import BaseDocTemplate, Frame, PageTemplate

from cv_data import CV
from styles import (
    ACCENT,
    BOTTOM_MARGIN,
    CONTENT_WIDTH,
    FOOTER_BOTTOM,
    HEIGHT,
    LEFT_MARGIN,
    MUTED,
    PAGE_SIZE,
    RIGHT_MARGIN,
    TOP_BAR_HEIGHT,
    TOP_MARGIN,
    TYPO,
    WIDTH,
)


def create_document(cv: CV, output_path: Path):
    """Create and configure the CV PDF document."""

    def on_page(c, d):
        c.saveState()
        c.setFillColor(ACCENT)
        c.rect(
            0,
            HEIGHT - TOP_BAR_HEIGHT,
            WIDTH,
            TOP_BAR_HEIGHT,
            stroke=0,
            fill=1,
        )
        c.setFont("Body", TYPO.footer_font_size)
        c.setFillColor(MUTED)
        c.drawRightString(
            WIDTH - RIGHT_MARGIN,
            FOOTER_BOTTOM,
            f"{cv.meta.author} · {d.page}",
        )
        c.restoreState()

    output_path = output_path.with_suffix(".pdf")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    doc = BaseDocTemplate(
        filename=str(output_path),
        pagesize=PAGE_SIZE,
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
        title=cv.meta.title,
        author=cv.meta.author,
        description=cv.meta.description,
    )

    frame = Frame(
        LEFT_MARGIN,
        BOTTOM_MARGIN,
        CONTENT_WIDTH,
        HEIGHT - TOP_MARGIN - BOTTOM_MARGIN,
        id="f",
        leftPadding=0,
        rightPadding=0,
        topPadding=0,
        bottomPadding=0,
    )

    template = PageTemplate(
        id="p",
        frames=[frame],
        onPage=on_page,
    )

    doc.addPageTemplates([template])

    return doc
