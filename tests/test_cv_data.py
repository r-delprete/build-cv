
import json

import pytest

from cv_data import load_cv


def test_load_cv_data(tmp_path):
    cv_data = {
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
        "experience": [
            {
                "company": "Example Company",
                "role": "Full Stack Developer",
                "start_date": "01/2023",
                "end_date": "oggi",
                "responsibilities": [
                    "Developed web applications.",
                    "Maintained existing software.",
                ],
                "projects": [
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
            }
        ],
        "skills": [
            {
                "category": "Programming",
                "items": ["Python", "JavaScript"],
            }
        ],
        "education": [
            {
                "title": "Computer Science Degree",
                "institution": "Example University",
                "period": "2021 – 2026",
            }
        ],
        "courses": [
            {
                "title": "Python Course",
                "institution": "Example Academy",
                "period": "01/2024 – 03/2024",
                "description": "Introduction to Python development.",
            }
        ],
        "publications": [
            {
                "title": "Example Research Paper",
                "authors": ["Rossi, M.", "Bianchi, L."],
                "status": "Accepted",
                "event": "Example Conference",
                "location": "Naples",
                "date": "June 2026",
            }
        ],
        "languages": [
            {
                "name": "Italian",
                "level": "Native",
            },
            {
                "name": "English",
                "level": "C1",
            },
        ],
        "soft_skills": [
            {
                "title": "Communication",
                "description": "Clear communication and teamwork.",
            }
        ],
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

    assert len(result.experience) == 1
    assert result.experience[0].company == "Example Company"
    assert result.experience[0].responsibilities[0] == (
        "Developed web applications."
    )

    project = result.experience[0].projects[0]
    assert project.title == "Enterprise Application"
    assert project.technologies == ["Python", "React"]

    assert result.skills[0].category == "Programming"
    assert result.education[0].institution == "Example University"
    assert result.courses[0].title == "Python Course"
    assert result.publications[0].date == "June 2026"
    assert result.languages[1].level == "C1"
    assert result.soft_skills[0].title == "Communication"
    assert result.privacy_note == "Example privacy notice."


def test_reject_invalid_json(tmp_path):
    cv_path = tmp_path / "invalid.json"
    cv_path.write_text("{invalid json", encoding="utf-8")

    with pytest.raises(ValueError, match="Invalid JSON"):
        load_cv(cv_path)
