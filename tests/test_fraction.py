import pytest
from acbrightspace.fraction import Fraction

class TestFractionFromString:
    """Tests for Fraction.from_string method."""

    def test_from_string_valid_fraction(self):
        """Test parsing a valid fraction string."""
        fraction = Fraction.from_string("85/100")
        assert fraction.numerator == 85.0
        assert fraction.denominator == 100.0

    def test_from_string_with_whitespace(self):
        """Test parsing fraction string with whitespace."""
        fraction = Fraction.from_string(" 3 / 4 ")
        assert fraction.numerator == 3.0
        assert fraction.denominator == 4.0

    def test_from_string_decimal_values(self):
        """Test parsing fraction with decimal values."""
        fraction = Fraction.from_string("1.5/2.5")
        assert fraction.numerator == 1.5
        assert fraction.denominator == 2.5

    def test_from_string_invalid_format_no_slash(self):
        """Test parsing invalid fraction without slash."""
        with pytest.raises(ValueError, match="Invalid fraction string"):
            Fraction.from_string("85100")

    def test_from_string_invalid_format_non_numeric(self):
        """Test parsing invalid fraction with non-numeric values."""
        with pytest.raises(ValueError, match="Invalid fraction string"):
            Fraction.from_string("abc/def")

    def test_from_string_invalid_format_missing_denominator(self):
        """Test parsing invalid fraction missing denominator."""
        with pytest.raises(ValueError, match="Invalid fraction string"):
            Fraction.from_string("85/")

    def test_from_string_invalid_format_missing_numerator(self):
        """Test parsing invalid fraction missing numerator."""
        with pytest.raises(ValueError, match="Invalid fraction string"):
            Fraction.from_string("/100")


class TestFractionToDecimal:
    """Tests for Fraction.to_decimal method."""

    def test_to_decimal_valid_fraction(self):
        """Test converting a valid fraction to decimal."""
        fraction = Fraction.from_string("85/100")
        assert fraction.to_decimal() == 0.85

    def test_to_decimal_whole_number(self):
        """Test converting a fraction that equals a whole number."""
        fraction = Fraction.from_string("10/2")
        assert fraction.to_decimal() == 5.0

    def test_to_decimal_decimal_values(self):
        """Test converting a fraction with decimal values."""
        fraction = Fraction.from_string("1.5/2.5")
        assert fraction.to_decimal() == 0.6

    def test_to_decimal_zero_numerator(self):
        """Test converting a fraction with zero numerator."""
        fraction = Fraction.from_string("0/5")
        assert fraction.to_decimal() == 0.0

    def test_to_decimal_zero_denominator(self):
        """Test converting a fraction with zero denominator raises error."""
        fraction = Fraction.from_string("5/0")
        with pytest.raises(ZeroDivisionError, match="Denominator cannot be zero"):
            fraction.to_decimal()

    def test_to_decimal_negative_values(self):
        """Test converting a fraction with negative values."""
        fraction = Fraction.from_string("-3/4")
        assert fraction.to_decimal() == -0.75


