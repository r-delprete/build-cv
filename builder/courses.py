from reportlab.platypus import KeepTogether, Paragraph, Spacer

from cv_data import Course
from styles import LAYOUT, body, edu, section


def build_courses(courses: Course):
    story = list(section(courses.title))

    for index, course in enumerate(courses.data):
        story.append(
            KeepTogether([
                edu(course.title, course.institution,
                    course.start_date, course.end_date),
                Paragraph(course.description, body),
            ])
        )

        if index < len(courses.data) - 1:
            story.append(Spacer(1, LAYOUT.courses_gap))

    return story
