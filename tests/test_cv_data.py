
import json

import pytest

from cv_data import load_cv


def test_load_cv_data(tmp_path):
    cv_data = {
        "meta": {
            "title": "Curriculum Vitae – Example",
            "description": "Mario Rossi Curriculum Vitae",
            "author": "Mario Rossi",
        },
        "personal": {
            "name": "Mario Rossi",
            "role": "Developer",
            "email": "mario@example.com",
            "phone": "+39 000 000 0000",
            "links": [
                {
                    "type": "linkedin",
                    "url": "https://www.linkedin.com/in/example/",
                },
                {
                    "type": "github",
                    "url": "https://github.com/example",
                },
            ],
        },
        "profile": {
            "title": "Professional Profile",
            "text": "Experienced software developer.",
        },
        "experience": {
            "section_title": "Work Experience",
            "data": [
                {
                    "company": "Example Company",
                    "role": "Full Stack Developer",
                    "start_date": "01/2023",
                    "end_date": "oggi",
                    "responsibilities": [
                        "Developed web applications.",
                        "Maintained existing software.",
                    ],
                    "projects": {
                        "section_title": "Projects",
                        "data": [
                            {
                                "title": "Enterprise Application",
                                "client": "Example Client",
                                "responsibilities": [
                                    "Designed the backend.",
                                    "Implemented the frontend.",
                                ],
                                "technologies": ["Python", "React"],
                            }
                        ],
                    },
                }
            ],
        },
        "skills": {
            "section_title": "Technical Skills",
            "data": [
                {
                    "category": "Programming",
                    "items": ["Python", "JavaScript"],
                }
            ],
        },
        "education": {
            "section_title": "Education",
            "data": [
                {
                    "title": "Computer Science Degree",
                    "institution": "Example University",
                    "start_date": "2021",
                    "end_date": "2026",
                }
            ],
        },
        "courses": {
            "section_title": "Courses and Training",
            "data": [
                {
                    "title": "Python Course",
                    "institution": "Example Academy",
                    "start_date": "01/2024",
                    "end_date": "03/2024",
                    "description": "Introduction to Python development.",
                }
            ],
        },
        "publications": {
            "section_title": "Publications",
            "data": [
                {
                    "title": "Example Research Paper",
                    "authors": [
                        {"name": "Rossi, M.", "is_me": True},
                        {"name": "Bianchi, L.", "is_me": False},
                    ],
                    "status": "Accepted",
                    "event": "Example Conference",
                    "location": "Naples",
                    "date": "June 2026",
                }
            ],
        },
        "languages": {
            "section_title": "Languages",
            "data": [
                {
                    "name": "Italian",
                    "level": "Native",
                },
                {
                    "name": "English",
                    "level": "C1",
                },
            ],
        },
        "soft_skills": {
            "section_title": "Soft Skills",
            "data": [
                {
                    "description": "Clear communication and teamwork.",
                }
            ],
        },
        "privacy_note": "Example privacy notice.",
    }

    cv_path = tmp_path / "cv.json"
    cv_path.write_text(
        json.dumps(cv_data),
        encoding="utf-8",
    )

    result = load_cv(cv_path)

    assert result.personal.name == "Mario Rossi"
    assert result.personal.links[0]["type"] == "linkedin"
    assert result.profile.title == "Professional Profile"

    experience = result.experience.data
    assert len(experience) == 1
    assert experience[0].company == "Example Company"
    assert experience[0].responsibilities[0] == (
        "Developed web applications."
    )

    project = experience[0].projects.data[0]
    assert project.title == "Enterprise Application"
    assert project.technologies == ["Python", "React"]

    skills = result.skills.data
    assert skills[0].category == "Programming"

    education = result.education.data
    assert education[0].institution == "Example University"

    courses = result.courses.data
    assert courses[0].title == "Python Course"

    publications = result.publications.data
    assert publications[0].date == "June 2026"

    languages = result.languages.data
    assert languages[1].level == "C1"

    soft_skills = result.soft_skills.data
    assert soft_skills[0].description == "Clear communication and teamwork."

    assert result.privacy_note == "Example privacy notice."


def test_reject_invalid_json(tmp_path):
    cv_path = tmp_path / "invalid.json"
    cv_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_cv(cv_path)
