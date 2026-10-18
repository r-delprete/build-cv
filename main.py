import argparse
from pathlib import Path

from reportlab.platypus import Paragraph, Spacer

from builder.courses import build_courses
from builder.document import create_document
from builder.education import build_education
from builder.experience import build_experience
from builder.fonts import register_fonts
from builder.header import build_header
from builder.languages import build_languages
from builder.profile import build_profile
from builder.publications import build_publications
from builder.skills import build_skills
from builder.soft_skills import build_soft_skills
from cv_data import load_cv
from styles import LAYOUT, create_profile_photo, small

PROJECT_DIR = Path(__file__).resolve().parent


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description="Generate a CV PDF from a JSON data file.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--cv",
        type=Path,
        default=PROJECT_DIR / "data" / "cv_data.example.json",
        help="Path to the CV JSON file.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=PROJECT_DIR / "output" / "cv.example.pdf",
        help="Path where the generated PDF will be saved.",
    )
    parser.add_argument(
        "--photo",
        type=Path,
        default=PROJECT_DIR / "assets" / "cv-pic.example.png",
        help="Path to the profile photo.",
    )

    return parser.parse_args()


def main():
    register_fonts()

    args = parse_args()
    cv = load_cv(args.cv)

    story = []

    # ---- header
    profile_photo = create_profile_photo(photo_path=args.photo)
    story.extend(build_header(cv.personal, profile_photo))

    # ---- profile
    story.extend(build_profile(cv.profile))

    # ---- experience
    story.extend(build_experience(cv.experience))

    # ---- skills
    story.extend(build_skills(cv.skills))

    # ---- education
    story.extend(build_education(cv.education))

    # ---- courses
    story.extend(build_courses(cv.courses))

    # ---- publications
    story.extend(build_publications(cv.publications))

    # ---- languages
    story.extend(build_languages(cv.languages))

    # ---- soft skills
    story.extend(build_soft_skills(cv.soft_skills))

    if cv.privacy_note:
        story.extend([Spacer(1, LAYOUT.final_note_gap),
                      Paragraph(cv.privacy_note, small)])

    doc = create_document(cv, args.output)
    doc.build(story)


if __name__ == "__main__":
    main()
