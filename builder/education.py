from cv_data import Education
from styles import edu, section


def build_education(education: Education):
    story = list(section(education.title))

    for edu_data in education.data:
        story.append(
            edu(edu_data.title, edu_data.institution,
                edu_data.start_date, edu_data.end_date)
        )

    return story
