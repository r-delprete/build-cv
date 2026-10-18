from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import KeepTogether, Paragraph, Spacer, Table, TableStyle

from cv_data import Experience
from styles import (
    CONTENT_WIDTH,
    LAYOUT,
    MUTED,
    bullets,
    h3,
    meta,
    section,
    subsection,
    tech,
)


def build_experience(experience: Experience):
    """Build the experience section of the CV."""
    story = list(section(experience.title))

    right_meta = ParagraphStyle(
        "ExperienceDate",
        parent=meta,
        alignment=2,
    )

    client_style = ParagraphStyle(
        "ProjectClient",
        parent=h3,
        textColor=MUTED,
    )

    for exp_index, exp_data in enumerate(experience.data):
        story.append(
            KeepTogether([
                Table(
                    [[
                        Paragraph(exp_data.company, h3),
                        Paragraph(
                            f"{exp_data.start_date} – {exp_data.end_date or 'Present'}",
                            right_meta,
                        ),
                    ]],
                    colWidths=[
                        CONTENT_WIDTH * 0.78,
                        CONTENT_WIDTH * 0.22,
                    ],
                    style=TableStyle([
                        ("LEFTPADDING", (0, 0), (-1, -1), 0),
                        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                        ("TOPPADDING", (0, 0), (-1, -1), 0),
                        ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
                        ("VALIGN", (0, 0), (-1, -1), "BOTTOM"),
                    ]),
                ),
                *bullets(exp_data.responsibilities),
            ])
        )

        story.append(Spacer(1, LAYOUT.section_gap))
        story.append(
            Paragraph(exp_data.projects.title, subsection)
        )

        for proj_index, proj_data in enumerate(exp_data.projects.data):
            story.append(
                KeepTogether([
                    Paragraph(proj_data.title, h3),
                    Paragraph(proj_data.client, client_style),
                    Spacer(1, LAYOUT.project_content_gap),
                    *bullets(proj_data.responsibilities),
                    Paragraph(", ".join(proj_data.technologies), tech),
                ])
            )

            if proj_index < len(exp_data.projects.data) - 1:
                story.append(Spacer(1, LAYOUT.project_gap))

        if exp_index < len(experience.data) - 1:
            story.append(Spacer(1, LAYOUT.section_gap))

    return story
