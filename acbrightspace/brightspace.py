from urllib import response
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
import pyotp
import logging
from acbrightspace.assignment import Assignment
from acbrightspace.course import Course
from acbrightspace.fraction import Fraction
from acbrightspace.grade_item import GradeItem
from acbrightspace.table import Table
import pickle
import requests

logger = logging.getLogger(__name__)

class BrightspaceError(Exception):
    """Exception for Brightspace-related errors."""

class Brightspace:
    """Interface for interacting with Algonquin College Brightspace."""
    
    def __init__(self):
        self.session = requests.Session()

    def _save_cookies(self, driver: WebDriver) -> None:
        """Saves cookies from the WebDriver session to a file."""
        with open("cookies.pkl", "wb") as cookie_file:
            pickle.dump(driver.get_cookies(), cookie_file)

    def _load_cookies(self) -> None:
        """Load cookies from a saved file into the session."""
        with open("cookies.pkl", "rb") as cookie_file:
            self.session.cookies.update(pickle.load(cookie_file))

    def login(self, driver: WebDriver, username: str, password: str, totp_secret: str) -> None:
        """Logs into Brightspace with the provided credentials.

        Args:
            username (str): The Algonquin College email address for the student.
            password (str): The password for the Algonquin College student.
            totp_secret (str): The TOTP secret for two-factor authentication.

        Raises:
            BrightspaceError: If the username field is not found.
            BrightspaceError: If the password field is not found.
            BrightspaceError: If the TOTP field is not found.
            BrightspaceError: If any error occurs during the login process.
        """

        try:
            # Wait up to 10 seconds for elements to load
            wait = WebDriverWait(driver, 10)

            # Navigate to the Brightspace login page
            driver.get("https://brightspace.algonquincollege.com/")

            # Enter username
            try:
                logger.debug("Waiting for username field to be present.")
                username_field = wait.until(
                    expected_conditions.presence_of_element_located((By.NAME, "loginfmt"))
                )
            except TimeoutException as error:
                # Username field not found, likely due to page load issues
                raise BrightspaceError("Email/username entry field not found.") from error
            logger.debug("Username field found, entering username.")
            username_field.send_keys(username)
            username_field.send_keys(Keys.RETURN)

            # Now the page should redirect to the password entry,
            # wait for it and then enter the password
            try:
                logger.debug("Waiting for password field to be present.")
                password_field = wait.until(
                    expected_conditions.presence_of_element_located((By.ID, "passwordInput"))
                )
            except TimeoutException as error:
                # Password field not found, likely due to incorrect email/username
                raise BrightspaceError("Password entry field not found. Check that username matches your Algonquin College email address.") from error
            logger.debug("Password field found, entering password.")
            password_field.send_keys(password)
            password_field.send_keys(Keys.RETURN)

            # Now the page should redirect to the TOTP entry,
            # wait for it and then enter the TOTP code generated from the secret
            try:
                logger.debug("Waiting for TOTP field to be present.")
                totp_field = wait.until(
                    expected_conditions.presence_of_element_located((By.NAME, "otc"))
                )
            except TimeoutException as error:
                # TOTP is currently required to log in
                raise BrightspaceError("TOTP entry field not found.") from error
            logger.debug("TOTP field found, generating and entering TOTP code.")

            totp = pyotp.TOTP(totp_secret)
            totp_code = totp.now() # Generate current TOTP code
            totp_field.send_keys(totp_code)
            totp_field.send_keys(Keys.RETURN)

            # Wait for successful login by checking for the URL to change to the Brightspace homepage
            try:
                logger.debug("Waiting for successful login redirect.")
                wait.until(
                    expected_conditions.url_contains("brightspace.algonquincollege.com/d2l/home")
                )
                logger.info("Login successful.")
                
                # Save cookies after successful login
                self._save_cookies(driver)
                self.session.cookies.update({cookie['name']: cookie['value'] for cookie in driver.get_cookies()})
            except TimeoutException as error:
                raise BrightspaceError("Login failed.") from error
        
        except BrightspaceError:
            raise
        except Exception as error:
            raise BrightspaceError("Failed to log in to Brightspace.") from error
    
    def test_thing(self) -> None:
        """A test method to test requests to Brightspace."""
        r = self.session.get("https://brightspace.algonquincollege.com/d2l/lms/grades/my_grades/main.d2l?ou=847643")