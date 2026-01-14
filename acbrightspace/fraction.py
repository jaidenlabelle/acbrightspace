class Fraction:
    """Represents a fraction (numerator/denominator)."""

    numerator: float
    """The numerator of the fraction."""

    denominator: float
    """The denominator of the fraction."""

    def __init__(self, numerator: float, denominator: float) -> None:
        self.numerator = numerator
        self.denominator = denominator

    @classmethod
    def from_string(cls, fraction_str: str) -> "Fraction":
        """Creates a Fraction object from a string representation.

        Args:
            fraction_str: A string representing the fraction (e.g., "85/100").

        Returns:
            A Fraction object.
        """
        try:
            numerator_str, denominator_str = fraction_str.split("/")
            numerator = float(numerator_str.strip())
            denominator = float(denominator_str.strip())
            return cls(numerator=numerator, denominator=denominator)
        except Exception as error:
            raise ValueError(f"Invalid fraction string: {fraction_str}") from error
        
    def to_decimal(self) -> float:
        """Converts the fraction to a decimal value.

        Returns:
            The decimal representation of the fraction.
        """
        if self.denominator == 0:
            raise ZeroDivisionError("Denominator cannot be zero.")
        return self.numerator / self.denominator

    def __str__(self) -> str:
        """Returns the string representation of the fraction.

        Returns:
            A string in the format "numerator/denominator".
        """
        return f"{self.numerator}/{self.denominator}"