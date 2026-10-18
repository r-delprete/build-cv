from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table, TableStyle

from cv_data import Skill
from styles import CONTENT_WIDTH, LAYOUT, RULE, SKILLS_LABEL_WIDTH, base, section


def build_skills(skills: Skill):
    story = list(section(skills.title))
    rows = [
        (skill.category, ", ".join(skill.items))
        for skill in skills.data
    ]
    cell_l = ParagraphStyle("cl", parent=base, fontName="Body-Bold")
    t = Table([[Paragraph(a, cell_l), Paragraph(b, base)]
              for a, b in rows], colWidths=[SKILLS_LABEL_WIDTH, CONTENT_WIDTH - SKILLS_LABEL_WIDTH])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1),
         LAYOUT.table_horizontal_padding),
        ("TOPPADDING", (0, 0), (-1, -1),
         LAYOUT.table_vertical_padding),
        ("BOTTOMPADDING", (0, 0), (-1, -1),
         LAYOUT.table_vertical_padding),
        ("LINEBELOW", (0, 0), (-1, -2), 0.4, RULE),
    ]))
    story.append(t)

    return story
