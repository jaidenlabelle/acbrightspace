from dataclasses import dataclass
from datetime import datetime
import re

from acbrightspace.semester import Semester


@dataclass
class Course:
    """Represents a course in Brightspace."""

    full_code: str
    """Full code of the course as seen in Brightspace, including semester, course code, and section."""

    full_name: str
    """Full name of the course as seen in Brightspace, including full code and course name."""

    name: str
    """Name of the course, without the code."""

    semester: Semester
    """Semester in which the course is offered."""
    
    ends_at: datetime
    """End date and time of the course."""

    is_active: bool
    """Indicates if the course is currently active."""

    org_unit_id: int
    """Organizational unit ID of the course."""

    @classmethod
    def from_string(cls, course_string: str, org_unit_id: int) -> "Course":
        match = re.match(r"^(Closed, )?(..._.*?_...)? ?(.*?), (.*?), (.*?), (?:.*?) (.*)$", course_string)

        if not match:
            raise ValueError(f"Invalid course string format: {course_string}")
        
        # The code that appears at the start of the name in the listing on Brightspace
        # Typically redundant with full_code, but needed to check if the course is a homeroom to ignore it
        is_homeroom = match.group(2) is None
        if is_homeroom:
            raise ValueError("Homeroom courses are not supported")

        is_active = match.group(1) is None
        name = match.group(3)
        full_code = match.group(4)
        semester = Semester.from_name(match.group(5))
        ends_at_str = match.group(6)
        ends_at = datetime.strptime(ends_at_str, "%B %d, %Y at %I:%M %p")

        return cls(
            full_code=full_code,
            full_name=course_string,
            name=name,
            semester=semester,
            ends_at=ends_at,
            is_active=is_active,
            org_unit_id=org_unit_id,
        )