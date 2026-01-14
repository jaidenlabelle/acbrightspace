from dataclasses import dataclass


@dataclass
class GradeItem:
    """Represents a grade for an assignment in Brightspace."""

    name: str
    """Name of the grade item."""

    points_achieved: float
    """Points received for the assignment."""

    weight_achieved: float
    """Weight achieved for the assignment."""

    max_points: float
    """Maximum possible points for the assignment."""

    max_weight: float
    """Maximum weight for the assignment."""

    grade: float
    """Percentage grade for the assignment (0-100)."""

    comments: str
    """Comments provided for the assignment."""