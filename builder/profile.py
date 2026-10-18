from reportlab.platypus import Paragraph

from cv_data import Profile
from styles import body, section


def build_profile(profile: Profile):
    return [*section(profile.title), Paragraph(profile.text, body)]
