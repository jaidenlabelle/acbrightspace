from datetime import datetime
from dataclasses import dataclass

from acbrightspace.fraction import Fraction

@dataclass
class Assignment:
    """Represents an assignment in Brightspace."""

    name: str
    """Name of the assignment."""

    starts_at: datetime | None
    """When availability starts."""

    ends_at: datetime | None
    """When availability ends."""

    due_at: datetime | None
    """When the assignment is due."""

    score: Fraction | None
    """Score achieved for the assignment."""

    completion_status: str | None
    """Completion status of the assignment."""

    evaluation_status: str | None
    """Evaluation status of the assignment."""