
# config.py

"""Typed configuration models and JSON loader for the CV generator."""

import json
import math
import re
from dataclasses import dataclass, fields
from pathlib import Path
from typing import Any, TypeVar

from reportlab.lib.pagesizes import A3, A4, A5, LEGAL, LETTER


@dataclass(frozen=True, slots=True)
class ThemeConfig:
    """Color palette used throughout the CV."""

    ink: str  # Primary text color, in hexadecimal format (#RRGGBB).
    muted: str  # Secondary text color, used for metadata and captions.
    accent: str  # Accent color for headings, links, and highlights.
    tint: str  # Light background color for decorative elements.
    rule: str  # Color used for separators and table borders.


@dataclass(frozen=True, slots=True)
class TypographyConfig:
    """Font families, text sizes, and paragraph spacing."""

    font_family: str  # Base font family registered with ReportLab.
    body_size: float  # Default body font size, in points.
    body_leading: float  # Default body line spacing, in points.
    name_size: float  # Candidate name font size, in points.
    name_leading: float  # Candidate name line spacing, in points.
    role_size: float  # Professional title font size, in points.
    role_leading: float  # Professional title line spacing, in points.
    contact_size: float  # Contact information font size, in points.
    contact_leading: float  # Contact information line spacing, in points.
    section_size: float  # Section heading font size, in points.
    section_leading: float  # Section heading line spacing, in points.
    section_space_before: float  # Space before a section heading, in points.
    section_space_after: float  # Space after a section heading, in points.
    section_rule_thickness: float  # Section divider thickness, in points.
    # Space before a section divider, in points.
    section_rule_space_before: float
    # Space after a section divider, in points.
    section_rule_space_after: float
    subsection_size: float  # Project subsection title size, in points.
    heading_size: float  # Experience and project heading size, in points.
    heading_leading: float  # Experience and project heading line spacing.
    meta_size: float  # Dates and secondary metadata size, in points.
    meta_leading: float  # Dates and metadata line spacing, in points.
    bullet_indent: float  # Bullet text indentation, in points.
    bullet_space_after: float  # Space after each bullet, in points.
    tech_size: float  # Technology summary font size, in points.
    tech_space_before: float  # Space before technology summaries, in points.
    small_size: float  # Small-print font size, in points.
    small_leading: float  # Small-print line spacing, in points.
    body_justified: bool  # Whether body paragraphs use justified alignment.
    # Space after project subsection titles, in points.
    subsection_space_after: float
    footer_font_size: float  # Footer font size, in points.


@dataclass(frozen=True, slots=True)
class LayoutConfig:
    """Page geometry, header, footer, and spacing settings."""

    page_size: str
    left_margin_mm: float
    right_margin_mm: float
    top_margin_mm: float
    bottom_margin_mm: float
    photo_size_mm: float
    top_bar_height_mm: float

    header_photo_column_mm: float
    header_photo_gap_mm: float
    header_name_gap: float
    header_role_gap: float
    header_bottom_gap: float

    footer_bottom_mm: float

    section_gap: float
    project_gap: float
    courses_gap: float
    project_content_gap: float
    final_note_gap: float

    table_horizontal_padding: float
    table_vertical_padding: float

    education_top_padding: float
    education_bottom_padding: float
    skills_label_column_mm: float


@dataclass(frozen=True, slots=True)
class AppConfig:
    """Root configuration for the CV generator."""

    theme: ThemeConfig  # Color palette.
    typography: TypographyConfig  # Typography settings.
    layout: LayoutConfig  # Page and layout settings.


T = TypeVar(
    "T",
    ThemeConfig,
    TypographyConfig,
    LayoutConfig
)

PAGE_SIZES = {
    "A3": A3,
    "A4": A4,
    "A5": A5,
    "LETTER": LETTER,
    "LEGAL": LEGAL,
}

HEX_COLOR = re.compile(r"#[0-9A-Fa-f]{6}$")

NON_NUMERIC_FIELDS = {
    "typography": {"font_family", "body_justified"},
    "layout": {"page_size"},
}

POSITIVE_FIELDS = {
    "left_margin_mm",
    "right_margin_mm",
    "top_margin_mm",
    "bottom_margin_mm",
    "photo_size_mm",
    "header_photo_column_mm",
    "skills_label_column_mm",
    "top_bar_height_mm"
}

POSITIVE_TYPOGRAPHY_FIELDS = {
    "body_size",
    "body_leading",
    "name_size",
    "name_leading",
    "role_size",
    "role_leading",
    "contact_size",
    "contact_leading",
    "section_size",
    "section_leading",
    "subsection_size",
    "heading_size",
    "heading_leading",
    "meta_size",
    "meta_leading",
    "tech_size",
    "small_size",
    "small_leading",
    "footer_font_size",
    "section_rule_thickness"
}


def _build_section(
    section_name: str,
    section_type: type[T],
    data: dict[str, Any],
) -> T:
    if not isinstance(data, dict):
        raise TypeError(
            f"Section '{section_name}' must be a JSON object."
        )

    expected = {field.name for field in fields(section_type)}
    received = set(data)

    unknown = received - expected
    missing = expected - received

    if unknown:
        raise ValueError(
            f"Unknown keys in '{section_name}': "
            f"{', '.join(sorted(unknown))}"
        )

    if missing:
        raise ValueError(
            f"Missing keys in '{section_name}': "
            f"{', '.join(sorted(missing))}"
        )

    try:
        return section_type(**data)
    except TypeError as exc:
        raise ValueError(
            f"Invalid configuration for section '{section_name}': {exc}"
        ) from exc


def validate_config(config: AppConfig) -> None:
    # Color check
    for field in fields(config.theme):
        value = getattr(config.theme, field.name)

        if not isinstance(value, str) or not HEX_COLOR.fullmatch(value):
            raise ValueError(
                f"Invalid color for '{field.name}': {value!r}. " f"Use #RRGGBB format.")

    # Page format check
    if not isinstance(config.layout.page_size, str):
        raise TypeError("'layout.page_size' must be a string.")

    if config.layout.page_size not in PAGE_SIZES:
        supported = ", ".join(PAGE_SIZES)
        raise ValueError(
            f"Unsupported page format: {config.layout.page_size!r}. "
            f"Supported formats: {supported}"
        )

    # Number values check
    for section_name, section in (
        ("typography", config.typography),
        ("layout", config.layout),
    ):
        excluded_fields = NON_NUMERIC_FIELDS[section_name]

        for field in fields(section):
            if field.name in excluded_fields:
                continue

            value = getattr(section, field.name)

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                raise TypeError(
                    f"'{section_name}.{field.name}' must be a number."
                )

            if not math.isfinite(value) or value < 0:
                raise ValueError(
                    f"'{section_name}.{field.name}' must be finite "
                    "and non-negative."
                )

    # Positive numbers check
    for name in POSITIVE_FIELDS:
        value = getattr(config.layout, name)
        if value <= 0:
            raise ValueError(f"'layout.{name}' must be greater than zero.")

    for name in POSITIVE_TYPOGRAPHY_FIELDS:
        value = getattr(config.typography, name)
        if value <= 0:
            raise ValueError(
                f"'typography.{name}' must be greater than zero."
            )

    if not isinstance(config.typography.font_family, str) or not (
        config.typography.font_family.strip()
    ):
        raise ValueError("'typography.font_family' cannot be empty.")

    if not isinstance(config.typography.body_justified, bool):
        raise TypeError(
            "'typography.body_justified' must be true or false."
        )


def load_config(path: Path) -> AppConfig:
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}, line {exc.lineno}, "
            f"column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(data, dict):
        raise TypeError("Configuration must be JSON object.")

    expected_sections = {"theme", "typography", "layout"}
    received_sections = set(data)

    unknown = received_sections - expected_sections
    missing = expected_sections - received_sections

    if unknown:
        raise ValueError(
            f"Unknown sections: {', '.join(sorted(unknown))}"
        )

    if missing:
        raise ValueError(
            f"Missing sections: {', '.join(sorted(missing))}"
        )

    config = AppConfig(
        theme=_build_section("theme", ThemeConfig, data["theme"]),
        typography=_build_section(
            "typography", TypographyConfig, data["typography"]
        ),
        layout=_build_section("layout", LayoutConfig, data["layout"]),
    )

    validate_config(config)
    return config
