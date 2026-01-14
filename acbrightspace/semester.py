class Semester:
    """Represents a semester in Brightspace."""

    year: int
    """Year of the semester (e.g., 2026)."""

    term: str
    """Term of the semester (e.g., "Winter", "Spring", "Fall")."""

    def __init__(self, year: int, term: str) -> None:
        # Validate year
        if not isinstance(year, int) or year < 0:
            raise ValueError(f"Year must be a positive integer, got: {year}")
        
        # Validate term
        valid_terms = {"Winter", "Spring", "Fall"}
        if term not in valid_terms:
            raise ValueError(f"Term must be one of {valid_terms}, got: {term}")

        self.year = year
        self.term = term

    @classmethod
    def from_name(cls, name: str) -> "Semester":
        """Creates a Semester instance from its name (e.g., "Winter 2026").

        Args:
            name: Name of the semester.
        """
        parts = name.split()
        if len(parts) != 2:
            raise ValueError(f"Invalid semester name format: {name}")

        term = parts[0]
        year = int(parts[1])

        return cls(year=year, term=term)


    @classmethod
    def from_code(cls, code: str) -> "Semester":
        """Creates a Semester instance from its code (e.g., "26W").

        Args:
            code: Unique code of the semester.
        """
        if len(code) != 3:
            raise ValueError(f"Invalid semester code format: {code}")

        year_str = code[:2]
        term_char = code[2]

        term_map = {
            "W": "Winter",
            "S": "Spring",
            "F": "Fall",
        }

        if term_char not in term_map:
            raise ValueError(f"Unknown semester term character: {term_char}")

        year = 2000 + int(year_str)
        term = term_map[term_char]

        return cls(year=year, term=term)


        