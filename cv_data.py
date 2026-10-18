import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TypedDict, TypeVar

T = TypeVar("T")


@dataclass(frozen=True)
class Section(Generic[T]):
    """Represent a CV section containing a title and a list of items."""

    title: str
    data: list[T]


S = TypeVar("S", bound=Section[Any])


class Link(TypedDict):
    """Represent a link associated with the candidate's personal information."""

    type: str
    url: str


@dataclass(frozen=True)
class PersonalInfo:
    """Store the candidate's personal details and contact information."""

    name: str
    role: str
    email: str
    phone: str
    links: list[Link]


@dataclass(frozen=True)
class Profile:
    """Represent the candidate's professional profile."""

    title: str
    text: str


@dataclass(frozen=True)
class ProjectData:
    """Store a project's title, client, responsibilities, and technologies."""

    title: str
    client: str
    responsibilities: list[str]
    technologies: list[str]


@dataclass(frozen=True)
class Project(Section[ProjectData]):
    """Represent a section containing project details."""


@dataclass(frozen=True)
class ExperienceData:
    """Store a work experience and its associated projects."""

    company: str
    role: str
    start_date: str
    end_date: str | None
    responsibilities: list[str]
    projects: Project


@dataclass(frozen=True)
class Experience(Section[ExperienceData]):
    """Represent the candidate's professional experience."""


@dataclass(frozen=True)
class SkillData:
    """Store a skill category and its associated skills."""

    category: str
    items: list[str]


@dataclass(frozen=True)
class Skill(Section[SkillData]):
    """Represent a section containing categorized skills."""


@dataclass(frozen=True)
class EducationData:
    """Store an educational qualification and its duration."""

    title: str
    institution: str
    start_date: str
    end_date: str | None


@dataclass(frozen=True)
class Education(Section[EducationData]):
    """Represent the candidate's educational background."""


@dataclass(frozen=True)
class CourseData:
    """Store details of a course or training program."""

    title: str
    institution: str
    start_date: str
    end_date: str | None
    description: str


@dataclass(frozen=True)
class Course(Section[CourseData]):
    """Represent a section containing courses and training programs."""


@dataclass(frozen=True)
class PublicationAuthor:
    """Represent a publication author and identify the candidate."""

    name: str
    is_me: bool


@dataclass(frozen=True)
class PublicationData:
    """Store a publication's authorship, status, event, and date."""

    title: str
    authors: list[PublicationAuthor]
    status: str
    event: str
    location: str
    date: str


@dataclass(frozen=True)
class Publication(Section[PublicationData]):
    """Represent a section containing publications."""


@dataclass(frozen=True)
class LanguageData:
    """Store a language and the candidate's proficiency level."""

    name: str
    level: str


@dataclass(frozen=True)
class Language(Section[LanguageData]):
    """Represent the candidate's language skills."""


@dataclass(frozen=True)
class SoftSkillData:
    """Store a description of an interpersonal or soft skill."""

    description: str


@dataclass(frozen=True)
class SoftSkill(Section[SoftSkillData]):
    """Represent a section containing soft skills."""


@dataclass(frozen=True)
class Meta:
    """Store metadata used to describe the CV document."""

    title: str
    description: str
    author: str


@dataclass(frozen=True)
class CV:
    """Represent the complete CV and all its sections."""

    meta: Meta
    personal: PersonalInfo
    profile: Profile
    experience: Experience
    skills: Skill
    education: Education
    courses: Course
    publications: Publication
    languages: Language
    soft_skills: SoftSkill
    privacy_note: str | None = None


def _load_section(
    section_data: dict[str, Any],
    section_type: type[S],
    loader: Callable[[dict[str, Any]], T],
) -> S:
    """Build a typed CV section from a dictionary.

    Args:
        section_data: Dictionary containing the section title and items.
        section_type: Section class to instantiate.
        loader: Function that converts each item into its corresponding
            data object.

    Returns:
        An instance of section_type containing the converted items.
    """
    return section_type(
        title=section_data["section_title"],
        data=[loader(item) for item in section_data["data"]],
    )


def _load_experience_data(item: dict[str, Any]) -> ExperienceData:
    """Convert a work experience dictionary, including its projects.

    Args:
        item: Dictionary containing a work experience and its projects.

    Returns:
        An ExperienceData instance with its projects converted to
        ProjectData objects.
    """
    projects = item["projects"]

    return ExperienceData(
        **{
            **item,
            "end_date": item.get("end_date"),
            "projects": Project(
                title=projects["section_title"],
                data=[
                    ProjectData(**proj_data)
                    for proj_data in projects["data"]
                ],
            ),
        }
    )


def _load_skills_data(item: dict[str, Any]) -> SkillData:
    """Convert a skill dictionary into a SkillData instance."""
    return SkillData(**item)


def _load_education_data(item: dict[str, Any]) -> EducationData:
    """Convert an education dictionary, allowing a missing end date."""
    return EducationData(
        **{
            **item,
            "end_date": item.get("end_date"),
        }
    )


def _load_course_data(item: dict[str, Any]) -> CourseData:
    """Convert a course dictionary, allowing a missing end date."""
    return CourseData(
        **{
            **item,
            "end_date": item.get("end_date"),
        }
    )


def _load_publication_data(item: dict[str, Any]) -> PublicationData:
    """Convert a publication dictionary and its author entries."""
    return PublicationData(
        **{
            **item,
            "authors": [
                PublicationAuthor(**author)
                for author in item["authors"]
            ],
        }
    )


def _load_language_data(item: dict[str, Any]) -> LanguageData:
    """Convert a language dictionary into a LanguageData instance."""
    return LanguageData(**item)


def _load_soft_skill_data(item: dict[str, Any]) -> SoftSkillData:
    """Convert a soft skill dictionary into a SoftSkillData instance."""
    return SoftSkillData(**item)


def load_cv(path: Path) -> CV:
    """Load and convert CV data from a JSON file.

    Args:
        path: Path to the JSON file containing the CV data.
            Defaults to DEFAULT_CV_PATH.

    Returns:
        A CV instance containing the parsed metadata, personal details,
        profile, and all CV sections.

    Raises:
        ValueError: If the JSON is malformed or the data structure
            is missing required fields or contains incompatible values.
        TypeError: If the JSON root is not an object.
        FileNotFoundError: If the specified file does not exist.
        OSError: If the file cannot be opened or read.
    """
    try:
        with path.open(encoding="utf-8") as file:
            data = json.load(file)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Invalid JSON in {path}, line {exc.lineno}, "
            f"column {exc.colno}"
        ) from exc

    if not isinstance(data, dict):
        raise TypeError("The CV file root must be a JSON object.")

    try:
        return CV(
            meta=Meta(**data["meta"]),
            personal=PersonalInfo(**data["personal"]),
            profile=Profile(**data["profile"]),
            experience=_load_section(
                data["experience"],
                Experience,
                _load_experience_data,
            ),
            skills=_load_section(
                data["skills"], Skill, _load_skills_data
            ),
            education=_load_section(
                data["education"], Education, _load_education_data
            ),
            courses=_load_section(
                data["courses"], Course, _load_course_data
            ),
            publications=_load_section(
                data["publications"], Publication,
                _load_publication_data,
            ),
            languages=_load_section(
                data["languages"], Language, _load_language_data
            ),
            soft_skills=_load_section(
                data["soft_skills"], SoftSkill,
                _load_soft_skill_data,
            ),
            privacy_note=data.get("privacy_note"),
        )
    except (KeyError, TypeError) as exc:
        raise ValueError(
            f"Invalid CV data structure in {path}: {exc}"
        ) from exc
