from datetime import datetime
import pytest
from acbrightspace.course import Course

valid_course_strings = [
    (
        "Closed, 24F_CST8109_020 Network Programming, 24F_CST8109_020, 2024 Fall, Ended December 16, 2024 at 12:00 AM",
        {
            "full_code": "24F_CST8109_020",
            "full_name": "Closed, 24F_CST8109_020 Network Programming, 24F_CST8109_020, 2024 Fall, Ended December 16, 2024 at 12:00 AM",
            "name": "Network Programming",
            "semester": "2024 Fall",
            "ends_at": datetime(2024, 12, 16, 0, 0),
            "is_active": False,
            "org_unit_id": 12345,
        }
    ),
    (
        "26W_CST8514_300 Business and Information Technology, 26W_CST8514_300, 2026 Winter, Ends April 27, 2026 at 12:00 AM",
        {
            "full_code": "26W_CST8514_300",
            "full_name": "26W_CST8514_300 Business and Information Technology, 26W_CST8514_300, 2026 Winter, Ends April 27, 2026 at 12:00 AM",
            "name": "Business and Information Technology",
            "semester": "2026 Winter",
            "ends_at": datetime(2026, 4, 27, 0, 0),
            "is_active": True,
            "org_unit_id": 67890,
        }
    )
]

class TestCourseFromString:
    @pytest.mark.parametrize("course_string,expected", valid_course_strings)
    def test_valid_course_string(self, course_string, expected):
        org_unit_id = expected["org_unit_id"]
        course = Course.from_string(course_string, org_unit_id=org_unit_id)
        
        assert course.full_code == expected["full_code"]
        assert course.full_name == expected["full_name"]
        assert course.name == expected["name"]
        assert course.semester.name == expected["semester"]
        assert course.ends_at == expected["ends_at"]
        assert course.is_active == expected["is_active"]
        assert course.org_unit_id == expected["org_unit_id"]

    def test_invalid_course_string_format(self):
        invalid_string = "This is not a valid course string"
        with pytest.raises(ValueError, match="Invalid course string format"):
            Course.from_string(invalid_string, org_unit_id=12345)

    def test_invalid_date_format(self):
        invalid_date_string = "26W_CST8514_300 Business and Information Technology, 26W_CST8514_300, 2026 Winter, Ends 27th April 2026 at 12:00 AM"
        with pytest.raises(ValueError):
            Course.from_string(invalid_date_string, org_unit_id=12345)

    def test_invalid_semester_format(self):
        invalid_semester_string = "26X_CST8514_300 Business and Information Technology, 26X_CST8514_300, 2026 Xterm, Ends April 27, 2026 at 12:00 AM"
        with pytest.raises(ValueError):
            Course.from_string(invalid_semester_string, org_unit_id=12345)

    def test_ignores_homeroom(self):
        course_string = "Computer Programming and Analysis All Levels Homeroom, 26W_H_1561X_WO_01_F_A02, 2026 Winter, Ends April 26, 2026 at 12:00 AM"
        with pytest.raises(ValueError, match="Homeroom courses are not supported"):
            course = Course.from_string(course_string, org_unit_id=12345)
        