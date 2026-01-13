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

