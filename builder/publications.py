from reportlab.platypus import Paragraph

from cv_data import Publication
from styles import body, section


def build_publications(publications: Publication):
    story = list(section(publications.title))

    for publication_data in publications.data:
        authors = ", ".join(
            f"<b>{author.name}</b>" if author.is_me else author.name for author in publication_data.authors
        )
        story.append(
            Paragraph(
                f"{authors} <i>{publication_data.title}</i>. "
                f"{publication_data.status}, {publication_data.event}, "
                f"{publication_data.location}, {publication_data.date}.",
                body,
            )
        )

    return story
