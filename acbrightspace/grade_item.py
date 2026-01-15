from dataclasses import dataclass

from acbrightspace.fraction import Fraction


@dataclass
class GradeItem:
    """Represents a grade for an assignment in Brightspace."""

    name: str
    """Name of the grade item."""

    points: Fraction | None
    """Points achieved for the assignment."""

    weight: Fraction | None
    """Weight of the assignment in the overall course grade."""

    comments: str | None
    """Comments provided for the assignment."""