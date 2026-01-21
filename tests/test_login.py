from unittest.mock import AsyncMock, MagicMock, patch

import aiohttp
import pytest
from selenium.common.exceptions import TimeoutException

from acbrightspace.errors import LoginFailure
from acbrightspace.login import (
    browser_cookies_to_aiohttp,
    fill_email_field,
    fill_password_field,
    fill_totp_field,
    login_with_browser,
    wait_for_login_success,
)


@pytest.mark.asyncio
async def test_login_with_browser_success():
    """Test successful login with browser."""
    session = AsyncMock(spec=aiohttp.ClientSession)
    session.cookie_jar = MagicMock()

    with patch("acbrightspace.login.webdriver.Chrome") as mock_chrome:
        mock_driver = MagicMock()
        mock_chrome.return_value.__enter__.return_value = mock_driver
        mock_driver.get_cookies.return_value = [{"name": "test", "value": "cookie"}]

        with (
            patch("acbrightspace.login.fill_email_field"),
            patch("acbrightspace.login.fill_password_field"),
            patch("acbrightspace.login.fill_totp_field"),
            patch("acbrightspace.login.wait_for_login_success"),
            patch("acbrightspace.login.browser_cookies_to_aiohttp"),
        ):
            await login_with_browser(session, "test@example.com", "password", "secret")


@pytest.mark.asyncio
async def test_login_with_browser_login_failure():
    """Test login with browser raises LoginFailure from fill_email_field."""
    session = AsyncMock(spec=aiohttp.ClientSession)

    with patch("acbrightspace.login.webdriver.Chrome") as mock_chrome:
        mock_driver = MagicMock()
        mock_chrome.return_value.__enter__.return_value = mock_driver

        with patch(
            "acbrightspace.login.fill_email_field",
            side_effect=LoginFailure("Email field not found"),
        ):
            with pytest.raises(LoginFailure):
                await login_with_browser(
                    session, "test@example.com", "password", "secret"
                )


@pytest.mark.asyncio
async def test_login_with_browser_generic_exception():
    """Test login with browser converts generic exception to LoginFailure."""
    session = AsyncMock(spec=aiohttp.ClientSession)

    with patch(
        "acbrightspace.login.webdriver.Chrome", side_effect=RuntimeError("Chrome error")
    ):
        with pytest.raises(LoginFailure):
            await login_with_browser(session, "test@example.com", "password", "secret")


@pytest.mark.asyncio
async def test_fill_email_field_success():
    """Test successful email field filling."""
    mock_driver = MagicMock()
    mock_element = MagicMock()

    with patch("acbrightspace.login.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = mock_element
        fill_email_field(mock_driver, "test@example.com")
        mock_element.send_keys.assert_any_call("test@example.com")


def test_fill_email_field_timeout():
    """Test email field timeout raises LoginFailure."""

    mock_driver = MagicMock()
    with patch("acbrightspace.login.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.side_effect = TimeoutException()
        with pytest.raises(LoginFailure, match="Email entry field not found"):
            fill_email_field(mock_driver, "test@example.com")


def test_fill_password_field_success():
    """Test successful password field filling."""
    mock_driver = MagicMock()
    mock_element = MagicMock()

    with patch("acbrightspace.login.WebDriverWait") as mock_wait:
        mock_wait.return_value.until.return_value = mock_element
        fill_password_field(mock_driver, "password123")
        mock_element.send_keys.assert_any_call("password123")


def test_fill_totp_field_success():
    """Test successful TOTP field filling."""
    mock_driver = MagicMock()
    mock_element = MagicMock()

    with (
        patch("acbrightspace.login.WebDriverWait") as mock_wait,
        patch("acbrightspace.login.pyotp.TOTP") as mock_totp,
    ):
        mock_wait.return_value.until.return_value = mock_element
        mock_totp.return_value.now.return_value = "123456"
        fill_totp_field(mock_driver, "secret")
        mock_element.send_keys.assert_any_call("123456")


def test_wait_for_login_success():
    """Test successful login wait."""
    mock_driver = MagicMock()

    with patch("acbrightspace.login.WebDriverWait") as mock_wait:
        wait_for_login_success(mock_driver)
        mock_wait.assert_called_once()


def test_browser_cookies_to_aiohttp():
    """Test cookie transfer from browser to aiohttp."""
    mock_driver = MagicMock()
    mock_driver.get_cookies.return_value = [{"name": "cookie1", "value": "value1"}]
    mock_session = MagicMock()

    browser_cookies_to_aiohttp(mock_session, mock_driver)
    mock_session.cookie_jar.update_cookies.assert_called_once()
