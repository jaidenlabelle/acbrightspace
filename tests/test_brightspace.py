import pytest
from unittest.mock import Mock, MagicMock, patch
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from acbrightspace.brightspace import Brightspace, BrightspaceError

@pytest.fixture
def brightspace():
    """Fixture to create a Brightspace instance with mocked driver."""
    with patch('acbrightspace.brightspace.webdriver.Chrome'):
        bs = Brightspace()
        bs.driver = MagicMock()
        return bs


def test_login_success(brightspace):
    """Test successful login with valid credentials."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait, \
         patch('acbrightspace.brightspace.pyotp.TOTP') as mock_totp:
        
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_totp_instance = MagicMock()
        mock_totp.return_value = mock_totp_instance
        mock_totp_instance.now.return_value = "123456"
        
        mock_username_field = MagicMock()
        mock_password_field = MagicMock()
        mock_totp_field = MagicMock()
        
        mock_wait_instance.until.side_effect = [
            mock_username_field,
            mock_password_field,
            mock_totp_field,
            None
        ]
        
        brightspace.login("test@algonquincollege.com", "password123", "secret")

        # Verify that the fields were used with the correct values
        mock_username_field.send_keys.assert_any_call("test@algonquincollege.com")
        mock_password_field.send_keys.assert_any_call("password123")
        mock_totp_field.send_keys.assert_any_call("123456")



def test_login_username_field_not_found(brightspace):
    """Test login fails when username field is not found."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.side_effect = TimeoutException()
        
        with pytest.raises(BrightspaceError, match="Email/username entry field not found"):
            brightspace.login("test@algonquincollege.com", "password123", "secret")


def test_login_password_field_not_found(brightspace):
    """Test login fails when password field is not found."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_username_field = MagicMock()
        mock_wait_instance.until.side_effect = [
            mock_username_field,
            TimeoutException()
        ]
        
        with pytest.raises(BrightspaceError, match="Password entry field not found"):
            brightspace.login("test@algonquincollege.com", "password123", "secret")


def test_login_totp_field_not_found(brightspace):
    """Test login fails when TOTP field is not found."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_username_field = MagicMock()
        mock_password_field = MagicMock()
        mock_wait_instance.until.side_effect = [
            mock_username_field,
            mock_password_field,
            TimeoutException()
        ]
        
        with pytest.raises(BrightspaceError, match="TOTP entry field not found"):
            brightspace.login("test@algonquincollege.com", "password123", "secret")


def test_login_redirect_timeout(brightspace):
    """Test login fails when redirect to homepage times out."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait, \
         patch('acbrightspace.brightspace.pyotp.TOTP') as mock_totp:
        
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_totp_instance = MagicMock()
        mock_totp.return_value = mock_totp_instance
        mock_totp_instance.now.return_value = "123456"
        
        mock_username_field = MagicMock()
        mock_password_field = MagicMock()
        mock_totp_field = MagicMock()
        
        mock_wait_instance.until.side_effect = [
            mock_username_field,
            mock_password_field,
            mock_totp_field,
            TimeoutException()
        ]
        
        with pytest.raises(BrightspaceError, match="Login failed"):
            brightspace.login("test@algonquincollege.com", "password123", "secret")


def test_login_general_exception(brightspace):
    """Test login fails on unexpected exception."""
    with patch('acbrightspace.brightspace.WebDriverWait', side_effect=Exception("Unexpected error")):
        with pytest.raises(BrightspaceError, match="Failed to log in to Brightspace"):
            brightspace.login("test@algonquincollege.com", "password123", "secret")

def test_get_grades_success(brightspace):
    """Test successful retrieval of grades."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        
        # Mock grade table and rows
        mock_table = MagicMock()
        mock_row1 = MagicMock()
        mock_row2 = MagicMock()
        
        # Mock first row
        mock_th1 = MagicMock()
        mock_th1.text = "Assignment 1"
        mock_td1_4 = MagicMock()
        mock_td1_4.text = "Good work"
        mock_span1_0 = MagicMock()
        mock_span1_0.text = "85.0 / 100.0"
        mock_span1_1 = MagicMock()
        mock_span1_1.text = "8.5 / 10.0"
        
        mock_row1.find_element.return_value = mock_th1
        mock_row1.find_elements.side_effect = [
            [MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), mock_td1_4],
            [mock_span1_0, mock_span1_1]
        ]
        
        # Mock second row
        mock_th2 = MagicMock()
        mock_th2.text = "Assignment 2"
        mock_td2_4 = MagicMock()
        mock_td2_4.text = "Excellent"
        mock_span2_0 = MagicMock()
        mock_span2_0.text = "95.0 / 100.0"
        mock_span2_1 = MagicMock()
        mock_span2_1.text = "9.5 / 10.0"
        
        mock_row2.find_element.return_value = mock_th2
        mock_row2.find_elements.side_effect = [
            [MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), mock_td2_4],
            [mock_span2_0, mock_span2_1]
        ]
        
        mock_table.find_elements.return_value = [MagicMock(), mock_row1, mock_row2]
        mock_wait_instance.until.return_value = mock_table
        
        grades = brightspace.get_grades("12345")
        
        assert len(grades) == 2
        assert grades[0].name == "Assignment 1"
        assert grades[0].points_achieved == 85.0
        assert grades[0].max_points == 100.0
        assert grades[0].grade == 85.0
        assert grades[0].comments == "Good work"
        assert grades[1].name == "Assignment 2"
        assert grades[1].points_achieved == 95.0
        assert grades[1].grade == 95.0

def test_get_grades_insufficient_spans(brightspace):
    """Test get_grades skips rows with insufficient spans."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_th = MagicMock()
        mock_th.text = "Assignment"
        
        mock_row.find_element.return_value = mock_th
        mock_row.find_elements.return_value = [MagicMock()]  # Only 1 span, need 2
        
        mock_table.find_elements.return_value = [MagicMock(), mock_row]
        mock_wait_instance.until.return_value = mock_table
        
        grades = brightspace.get_grades("12345")
        
        assert len(grades) == 0


def test_get_grades_invalid_points_format(brightspace):
    """Test get_grades handles invalid points format gracefully."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_th = MagicMock()
        mock_th.text = "Assignment"
        mock_td = MagicMock()
        mock_td.text = "No comment"
        
        mock_span0 = MagicMock()
        mock_span0.text = "invalid"
        mock_span1 = MagicMock()
        mock_span1.text = "5.0 / 10.0"
        
        mock_row.find_element.return_value = mock_th
        mock_row.find_elements.side_effect = [
            [MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), mock_td],
            [mock_span0, mock_span1]
        ]
        
        mock_table.find_elements.return_value = [MagicMock(), mock_row]
        mock_wait_instance.until.return_value = mock_table
        
        grades = brightspace.get_grades("12345")
        
        assert len(grades) == 1
        assert grades[0].points_achieved == 0.0
        assert grades[0].max_points == 0.0


def test_get_grades_invalid_weight_format(brightspace):
    """Test get_grades handles invalid weight format gracefully."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_th = MagicMock()
        mock_th.text = "Assignment"
        mock_td = MagicMock()
        mock_td.text = "Comment"
        
        mock_span0 = MagicMock()
        mock_span0.text = "80.0 / 100.0"
        mock_span1 = MagicMock()
        mock_span1.text = "invalid"
        
        mock_row.find_element.return_value = mock_th
        mock_row.find_elements.side_effect = [
            [MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), mock_td],
            [mock_span0, mock_span1]
        ]
        
        mock_table.find_elements.return_value = [MagicMock(), mock_row]
        mock_wait_instance.until.return_value = mock_table
        
        grades = brightspace.get_grades("12345")
        
        assert len(grades) == 1
        assert grades[0].weight_achieved == 0.0
        assert grades[0].max_weight == 0.0


def test_get_grades_zero_max_points(brightspace):
    """Test get_grades handles zero max points correctly."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        
        mock_table = MagicMock()
        mock_row = MagicMock()
        mock_th = MagicMock()
        mock_th.text = "Assignment"
        mock_td = MagicMock()
        mock_td.text = "Comment"
        
        mock_span0 = MagicMock()
        mock_span0.text = "0.0 / 0.0"
        mock_span1 = MagicMock()
        mock_span1.text = "0.0 / 0.0"
        
        mock_row.find_element.return_value = mock_th
        mock_row.find_elements.side_effect = [
            [MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), MagicMock(text=""), mock_td],
            [mock_span0, mock_span1]
        ]
        
        mock_table.find_elements.return_value = [MagicMock(), mock_row]
        mock_wait_instance.until.return_value = mock_table
        
        grades = brightspace.get_grades("12345")
        
        assert len(grades) == 1
        assert grades[0].grade == 0.0


def test_get_grades_table_not_found(brightspace):
    """Test get_grades raises error when table is not found."""
    with patch('acbrightspace.brightspace.WebDriverWait') as mock_wait:
        mock_wait_instance = MagicMock()
        mock_wait.return_value = mock_wait_instance
        mock_wait_instance.until.side_effect = TimeoutException()
        
        with pytest.raises(TimeoutException):
            brightspace.get_grades("12345")


