from reportlab.platypus import Paragraph

from cv_data import Language
from styles import base, section


def build_languages(languages: Language):
    story = list(section(languages.title))

    language_text = "&nbsp;&nbsp;·&nbsp;&nbsp;".join(
        f"<b>{language_data.name}</b>: {language_data.level}" for language_data in languages.data
    )
    story.append(Paragraph(language_text, base))

    return story
