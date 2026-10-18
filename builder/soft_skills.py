from reportlab.platypus import Paragraph

from cv_data import SoftSkill
from styles import body, section


def build_soft_skills(soft_skills: SoftSkill):
    story = list(section(soft_skills.title))

    story.extend(Paragraph(soft_skills_data.description, body)
                 for soft_skills_data in soft_skills.data)

    return story
