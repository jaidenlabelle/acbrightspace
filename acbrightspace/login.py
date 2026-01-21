import logging

import aiohttp
import pyotp
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from acbrightspace.errors import LoginFailure

logger = logging.getLogger(__name__)


def fill_email_field(driver: WebDriver, email: str) -> None:
    """Fill in the email field on the Brightspace login page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        email (str): The user's email address.

    Raises:
        LoginFailure: If the email field is not found.
    """
    try:
        logger.debug("Waiting for email field to be present.")
        email_field = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "loginfmt"))
        )
        email_field.send_keys(email)
        email_field.send_keys(Keys.RETURN)
    except TimeoutException as error:
        raise LoginFailure("Email entry field not found.") from error


def fill_password_field(driver: WebDriver, password: str) -> None:
    """Fill in the password field on the Brightspace login page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        password (str): The user's password.

    Raises:
        LoginFailure: If the password field is not found.
    """
    try:
        logger.debug("Waiting for password field to be present.")
        password_field = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "passwordInput"))
        )
        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)
    except TimeoutException as error:
        raise LoginFailure("Password entry field not found.") from error


def fill_totp_field(driver: WebDriver, totp_secret: str) -> None:
    """Fill in the TOTP field on the Brightspace login page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        totp_secret (str): The user's TOTP secret.

    Raises:
        LoginFailure: If the TOTP field is not found.
    """
    try:
        logger.debug("Waiting for TOTP field to be present.")
        totp_field = WebDriverWait(driver, 10).until(
            expected_conditions.presence_of_element_located((By.NAME, "otc"))
        )
        logger.debug("TOTP field found, generating and entering TOTP code.")
        totp = pyotp.TOTP(totp_secret)
        totp_code = totp.now()  # Generate current TOTP code
        totp_field.send_keys(totp_code)
        totp_field.send_keys(Keys.RETURN)
    except TimeoutException as error:
        raise LoginFailure("TOTP entry field not found.") from error


def wait_for_login_success(driver: WebDriver) -> None:
    """Wait for the login to be successful by checking for a URL change.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Raises:
        LoginFailure: If login is not successful within the timeout period.
    """
    try:
        logger.debug("Waiting for successful login redirect.")
        WebDriverWait(driver, 10).until(
            expected_conditions.url_contains(
                "brightspace.algonquincollege.com/d2l/home"
            )
        )
        logger.info("Login successful.")
    except TimeoutException as error:
        raise LoginFailure("Login was not successful.") from error


def browser_cookies_to_aiohttp(
    session: aiohttp.ClientSession, driver: WebDriver
) -> None:
    """Transfer cookies from Selenium WebDriver to aiohttp ClientSession.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to update.
        driver (WebDriver): The Selenium WebDriver instance.
    """
    logger.debug("Transferring cookies from browser to aiohttp session.")
    for cookie in driver.get_cookies():
        session.cookie_jar.update_cookies({cookie["name"]: cookie["value"]})


async def login_with_browser(
    session: aiohttp.ClientSession,
    email: str,
    password: str,
    totp_secret: str,
) -> None:
    """Log in to Brightspace using a headless browser and transfer cookies to aiohttp session.

    Args:
        session (aiohttp.ClientSession): The aiohttp session to update with cookies.
        email (str): User's email address.
        password (str): User's password.
        totp_secret (str): User's TOTP secret for two-factor authentication.

    Raises:
        LoginFailure: If login fails due to incorrect credentials or other issues.
    """
    try:
        with webdriver.Chrome() as driver:
            # Navigate to the Brightspace login page
            driver.get("https://brightspace.algonquincollege.com/")

            fill_email_field(driver, email)
            fill_password_field(driver, password)
            fill_totp_field(driver, totp_secret)
            wait_for_login_success(driver)

            # d2lSecureSessionVal and d2lSessionVal are the only cookies needed for aiohttp session
            browser_cookies_to_aiohttp(session, driver)
    except LoginFailure:
        raise
    except Exception as error:
        raise LoginFailure from error
