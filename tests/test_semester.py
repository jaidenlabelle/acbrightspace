import pytest
from acbrightspace.semester import Semester

valid_semester_names = [
    ("Winter 2026", "Winter", 2026),
    ("Fall 2025", "Fall", 2025),
    ("Spring 2025", "Spring", 2025),
    ("Winter 2025", "Winter", 2025),
    ("Fall 2024", "Fall", 2024),
    ("Spring 2024", "Spring", 2024),
    ("Winter 2024", "Winter", 2024),
]

valid_semester_codes = [
    ("26W", "Winter", 2026),
    ("25F", "Fall", 2025),
    ("25S", "Spring", 2025),
    ("25W", "Winter", 2025),
    ("24F", "Fall", 2024),
    ("24S", "Spring", 2024),
    ("24W", "Winter", 2024),
]

class TestSemesterInit:
    @pytest.mark.parametrize("year,term", [(2026, "Winter"), (2025, "Fall"), (2024, "Spring")])
    def test_valid_initialization(self, year, term):
        semester = Semester(year=year, term=term)
        assert semester.year == year
        assert semester.term == term

    def test_invalid_year_negative(self):
        with pytest.raises(ValueError, match="Year must be a positive integer"):
            Semester(year=-2025, term="Winter")

    def test_invalid_year_non_integer(self):
        with pytest.raises(ValueError, match="Year must be a positive integer"):
            Semester(year="2025", term="Winter")

    def test_invalid_term(self):
        with pytest.raises(ValueError, match="Term must be one of"):
            Semester(year=2025, term="Summer")

class TestSemesterFromName:
    @pytest.mark.parametrize("name,expected_term,expected_year", valid_semester_names)
    def test_valid_semester(self, name, expected_term, expected_year):
        semester = Semester.from_name(name)
        assert semester.term == expected_term
        assert semester.year == expected_year

    def test_invalid_format_missing_year(self):
        with pytest.raises(ValueError, match="Invalid semester name format"):
            Semester.from_name("Winter")

    def test_invalid_format_too_many_parts(self):
        with pytest.raises(ValueError, match="Invalid semester name format"):
            Semester.from_name("Winter 2026 Extra")

    def test_invalid_year_not_integer(self):
        with pytest.raises(ValueError):
            Semester.from_name("Winter ABC")


class TestSemesterFromCode:
    @pytest.mark.parametrize("code,expected_term,expected_year", valid_semester_codes)
    def test_valid_code(self, code, expected_term, expected_year):
        semester = Semester.from_code(code)
        assert semester.term == expected_term
        assert semester.year == expected_year

    def test_invalid_code_too_short(self):
        with pytest.raises(ValueError, match="Invalid semester code format"):
            Semester.from_code("26")

    def test_invalid_code_too_long(self):
        with pytest.raises(ValueError, match="Invalid semester code format"):
            Semester.from_code("26WX")

    def test_invalid_term_character(self):
        with pytest.raises(ValueError, match="Unknown semester term character"):
            Semester.from_code("26X")

    def test_invalid_year_not_integer(self):
        with pytest.raises(ValueError):
            Semester.from_code("ABW")