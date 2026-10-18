
import json
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Generic, TypedDict, TypeVar

T = TypeVar("T")
S = TypeVar("S", bound="Section[Any]")


@dataclass(frozen=True)
class Section(Generic[T]):
    """Represent a CV section containing a title and a list of items."""

    title: str
    data: list[T]


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


def _require_object(value: Any, context: str) -> dict[str, Any]:
    """Return a JSON object or raise an informative error."""
    if not isinstance(value, dict):
        raise TypeError(f"'{context}' must be a JSON object.")
    return value


def _require_string(value: Any, context: str) -> str:
    """Return a string or raise an informative error."""
    if not isinstance(value, str):
        raise TypeError(f"'{context}' must be a string.")
    return value


def _require_string_list(value: Any, context: str) -> list[str]:
    """Validate a list containing only strings."""
    if not isinstance(value, list):
        raise TypeError(f"'{context}' must be a list.")

    for index, item in enumerate(value):
        _require_string(item, f"{context}[{index}]")

    return value


def _load_section(
    section_data: dict[str, Any],
    section_type: type[S],
    loader: Callable[[dict[str, Any]], T],
    section_name: str,
) -> S:
    """Build a typed CV section from a dictionary.

    Args:
        section_data: Dictionary containing the section title and items.
        section_type: Section class to instantiate.
        loader: Function that converts each item into a typed data object.
        section_name: Name used to identify errors in the section.

    Returns:
        A section instance containing the converted items.

    Raises:
        ValueError: If the section structure or its items are invalid.
    """
    if "section_title" not in section_data:
        raise ValueError(f"Missing '{section_name}.section_title'.")

    if "data" not in section_data:
        raise ValueError(f"Missing '{section_name}.data'.")

    title = _require_string(
        section_data["section_title"],
        f"{section_name}.section_title",
    )
    items = section_data["data"]

    if not isinstance(items, list):
        raise TypeError(f"'{section_name}.data' must be a list.")

    converted_items = []

    for index, item in enumerate(items):
        context = f"{section_name}.data[{index}]"
        item_data = _require_object(item, context)

        try:
            converted_items.append(loader(item_data))
        except (KeyError, TypeError) as exc:
            raise ValueError(f"Invalid data in '{context}': {exc}") from exc

    return section_type(title=title, data=converted_items)


def _load_project(item: dict[str, Any]) -> ProjectData:
    """Convert a project dictionary into a ProjectData instance."""
    item = _require_object(item, "project")

    _require_string_list(
        item.get("responsibilities"),
        "project.responsibilities",
    )
    _require_string_list(
        item.get("technologies"),
        "project.technologies",
    )

    try:
        return ProjectData(**item)
    except TypeError as exc:
        raise ValueError(f"Invalid project data: {exc}") from exc


def _load_experience_data(item: dict[str, Any]) -> ExperienceData:
    """Convert a work experience dictionary, including its projects."""
    item = _require_object(item, "experience")

    projects = _require_object(
        item.get("projects"),
        "experience.projects",
    )

    project_section = _load_section(
        projects,
        Project,
        _load_project,
        "experience.projects",
    )

    responsibilities = _require_string_list(
        item.get("responsibilities"),
        "experience.responsibilities",
    )

    end_date = item.get("end_date")
    if end_date is not None:
        _require_string(end_date, "experience.end_date")

    try:
        return ExperienceData(
            **{
                **item,
                "responsibilities": responsibilities,
                "end_date": end_date,
                "projects": project_section,
            }
        )
    except TypeError as exc:
        raise ValueError(f"Invalid experience data: {exc}") from exc


def _load_skills_data(item: dict[str, Any]) -> SkillData:
    """Convert a skill dictionary into a SkillData instance."""
    item = _require_object(item, "skill")
    _require_string_list(item.get("items"), "skill.items")

    try:
        return SkillData(**item)
    except TypeError as exc:
        raise ValueError(f"Invalid skill data: {exc}") from exc


def _load_education_data(item: dict[str, Any]) -> EducationData:
    """Convert an education dictionary, allowing a missing end date."""
    item = _require_object(item, "education")
    end_date = item.get("end_date")

    if end_date is not None:
        _require_string(end_date, "education.end_date")

    try:
        return EducationData(**{**item, "end_date": end_date})
    except TypeError as exc:
        raise ValueError(f"Invalid education data: {exc}") from exc


def _load_course_data(item: dict[str, Any]) -> CourseData:
    """Convert a course dictionary, allowing a missing end date."""
    item = _require_object(item, "course")
    end_date = item.get("end_date")

    if end_date is not None:
        _require_string(end_date, "course.end_date")

    try:
        return CourseData(**{**item, "end_date": end_date})
    except TypeError as exc:
        raise ValueError(f"Invalid course data: {exc}") from exc


def _load_publication_data(item: dict[str, Any]) -> PublicationData:
    """Convert a publication dictionary and its author entries."""
    item = _require_object(item, "publication")
    authors = item.get("authors")

    if not isinstance(authors, list):
        raise TypeError("'publication.authors' must be a list.")

    converted_authors = []

    for index, author in enumerate(authors):
        context = f"publication.authors[{index}]"
        author_data = _require_object(author, context)

        try:
            converted_authors.append(PublicationAuthor(**author_data))
        except TypeError as exc:
            raise ValueError(f"Invalid data in '{context}': {exc}") from exc

    try:
        return PublicationData(
            **{**item, "authors": converted_authors}
        )
    except TypeError as exc:
        raise ValueError(f"Invalid publication data: {exc}") from exc


def _load_language_data(item: dict[str, Any]) -> LanguageData:
    """Convert a language dictionary into a LanguageData instance."""
    item = _require_object(item, "language")

    try:
        return LanguageData(**item)
    except TypeError as exc:
        raise ValueError(f"Invalid language data: {exc}") from exc


def _load_soft_skill_data(item: dict[str, Any]) -> SoftSkillData:
    """Convert a soft skill dictionary into a SoftSkillData instance."""
    item = _require_object(item, "soft skill")

    try:
        return SoftSkillData(**item)
    except TypeError as exc:
        raise ValueError(f"Invalid soft skill data: {exc}") from exc


def _load_personal_info(value: Any) -> PersonalInfo:
    """Convert and validate personal information."""
    data = _require_object(value, "personal")
    links = data.get("links")

    if not isinstance(links, list):
        raise TypeError("'personal.links' must be a list.")

    converted_links = []

    for index, link in enumerate(links):
        context = f"personal.links[{index}]"
        link_data = _require_object(link, context)

        try:
            link_type = _require_string(link_data["type"], f"{context}.type")
            url = _require_string(link_data["url"], f"{context}.url")
        except KeyError as exc:
            raise ValueError(f"Missing field in '{context}': {exc}") from exc

        converted_links.append({"type": link_type, "url": url})

    try:
        return PersonalInfo(**{**data, "links": converted_links})
    except TypeError as exc:
        raise ValueError(f"Invalid personal information: {exc}") from exc


def _load_meta(value: Any) -> Meta:
    """Convert document metadata into a Meta instance."""
    try:
        return Meta(**_require_object(value, "meta"))
    except TypeError as exc:
        raise ValueError(f"Invalid metadata: {exc}") from exc


def _load_profile(value: Any) -> Profile:
    """Convert the professional profile into a Profile instance."""
    try:
        return Profile(**_require_object(value, "profile"))
    except TypeError as exc:
        raise ValueError(f"Invalid profile: {exc}") from exc


REQUIRED_SECTIONS = {
    "meta",
    "personal",
    "profile",
    "experience",
    "skills",
    "education",
    "courses",
    "publications",
    "languages",
    "soft_skills",
}


def load_cv(path: Path) -> CV:
    """Load CV data from a JSON file and convert it into typed objects.

    Args:
        path: Path to the JSON file containing the CV data.

    Returns:
        A CV instance containing the parsed metadata, personal
        information, profile, and all CV sections.

    Raises:
        ValueError: If the JSON is malformed or the CV data has an
            invalid structure or incompatible values.
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
            f"column {exc.colno}: {exc.msg}"
        ) from exc

    if not isinstance(data, dict):
        raise TypeError("The CV file root must be a JSON object.")

    missing = REQUIRED_SECTIONS - data.keys()
    if missing:
        raise ValueError(
            f"Missing CV sections in {path}: {', '.join(sorted(missing))}"
        )

    try:
        privacy_note = data.get("privacy_note")
        if privacy_note is not None:
            _require_string(privacy_note, "privacy_note")

        return CV(
            meta=_load_meta(data["meta"]),
            personal=_load_personal_info(data["personal"]),
            profile=_load_profile(data["profile"]),
            experience=_load_section(
                _require_object(data["experience"], "experience"),
                Experience,
                _load_experience_data,
                "experience",
            ),
            skills=_load_section(
                _require_object(data["skills"], "skills"),
                Skill,
                _load_skills_data,
                "skills",
            ),
            education=_load_section(
                _require_object(data["education"], "education"),
                Education,
                _load_education_data,
                "education",
            ),
            courses=_load_section(
                _require_object(data["courses"], "courses"),
                Course,
                _load_course_data,
                "courses",
            ),
            publications=_load_section(
                _require_object(data["publications"], "publications"),
                Publication,
                _load_publication_data,
                "publications",
            ),
            languages=_load_section(
                _require_object(data["languages"], "languages"),
                Language,
                _load_language_data,
                "languages",
            ),
            soft_skills=_load_section(
                _require_object(data["soft_skills"], "soft_skills"),
                SoftSkill,
                _load_soft_skill_data,
                "soft_skills",
            ),
            privacy_note=privacy_note,
        )
    except KeyError as exc:
        raise ValueError(
            f"Missing required field in CV data from {path}: {exc}"
        ) from exc
