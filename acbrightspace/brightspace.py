from datetime import datetime
from typing import Any, List
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.select import Select
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.shadowroot import ShadowRoot
import pyotp
import logging
from acbrightspace.course import Course
from acbrightspace.grade_item import GradeItem

logger = logging.getLogger(__name__)

class BrightspaceError(Exception):
    """Exception for Brightspace-related errors."""

class Brightspace:
    """Interface for interacting with Algonquin College Brightspace."""
    
    def __init__(self):
        self.driver = webdriver.Chrome()

    def _get_nested_shadow_root(self, locators: list[tuple[str, str]], root: Any = None) -> ShadowRoot:
        """Helper method to traverse nested shadow DOMs.

        Args:
            locators (list[tuple[str, str]]): List of (By, selector) tuples to traverse.

        Returns:
            The final shadow root WebElement.

        Example:
            >>> shadow_root = self._get_nested_shadow_root([
            ...     (By.CSS_SELECTOR, "parent-element"),
            ...     (By.CSS_SELECTOR, "child-element"),
            ...     (By.CSS_SELECTOR, "target-element")
            ... ])
        """
        root = root or self.driver
        for locator in locators:
            element = WebDriverWait(root, 10).until(
                expected_conditions.presence_of_element_located(locator)
            )
            root = element.shadow_root
        return root

    def login(self, username: str, password: str, totp_secret: str) -> None:
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
            wait = WebDriverWait(self.driver, 10)

            # Navigate to the Brightspace login page
            self.driver.get("https://brightspace.algonquincollege.com/")

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
            except TimeoutException as error:
                raise BrightspaceError("Login failed.") from error
        
        except BrightspaceError:
            raise
        except Exception as error:
            raise BrightspaceError("Failed to log in to Brightspace.") from error
    
    def get_courses(self) -> list[Course]:
        """Fetches the list of courses for the logged-in student.

        Returns:
            list[Course]: A list of Course objects representing the student's courses.
        """
        # Navigate to the Brightspace home page
        self.driver.get("https://brightspace.algonquincollege.com/d2l/home")

        root = self._get_nested_shadow_root([
            (By.CSS_SELECTOR, "d2l-my-courses"),
            (By.CSS_SELECTOR, "d2l-my-courses-container"),
        ])

        tabs = WebDriverWait(root, 10).until(
            expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "d2l-tab-panel"))
        )

        courses = []

        for tab in tabs:
            self.driver.execute_script(
                "arguments[0].setAttribute('selected', '');", tab
            )

            inner_root = self._get_nested_shadow_root([
                (By.CSS_SELECTOR, "d2l-my-courses-content"),
                (By.CSS_SELECTOR, "d2l-my-courses-card-grid"),
            ], tab)

            cards = WebDriverWait(inner_root, 10).until(
                expected_conditions.presence_of_all_elements_located((By.CSS_SELECTOR, "d2l-enrollment-card"))
            )

            for card in cards:
                card = WebDriverWait(card.shadow_root, 10).until(
                    expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "d2l-card"))
                )
                
                print(card.get_attribute("text"))
                course = Course.from_string(card.get_attribute("text"), org_unit_id=int(card.get_attribute("href").split('/')[-1]))
                if course is not None:
                    # Avoid duplicate course codes
                    if all(existing_course.full_code != course.full_code for existing_course in courses):
                        courses.append(course)

        return courses

    def get_grades(self, org_unit_id: str) -> list[GradeItem]:
        """Fetches the grades for a specific course.

        Args:
            org_unit_id (str): The organizational unit ID for the course for which to fetch grades.
        Returns:
            list[GradeItem]: A list of GradeItem objects representing the grades for the course.
        
        """

        # Navigate to the course grades page
        self.driver.get(f"https://brightspace.algonquincollege.com/d2l/lms/grades/my_grades/main.d2l?ou={org_unit_id}")

        grades = []

        # Wait for the grades table to load
        grades_table = WebDriverWait(self.driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, "z_f"))  # Replace with actual table ID
        )

        # Get all rows
        all_rows = grades_table.find_elements(By.TAG_NAME, "tr")

        # Process all rows after header
        for row in all_rows[1:]:
            cells = row.find_elements(By.TAG_NAME, "td")
            name = row.find_element(By.TAG_NAME, "th").text.strip()

            spans = row.find_elements(By.TAG_NAME, "span")

            if len(spans) < 2:
                logger.warning("Unexpected format for grade item: %s", name)
                continue

            # Get points acheived and max points
            try:
                points = spans[0].text.strip()
                points_achieved, max_points = map(float, points.split(" / "))
            except ValueError:
                logger.warning("Failed to parse points for grade item: %s", name)
                points_achieved, max_points = 0.0, 0.0

            # Get weight acheived and max weight
            try:
                weight = spans[1].text.strip()
                weight_achieved, max_weight = map(float, weight.split(" / "))
            except ValueError:
                logger.warning("Failed to parse weight for grade item: %s", name)
                weight_achieved, max_weight = 0.0, 0.0
            
            # Calculate grade percentage, round to 2 decimal places
            grade = round((points_achieved / max_points * 100) if max_points > 0 else 0.0, 2)
        
            
            # Get comments
            comments = cells[4].text.strip()

            grade_item = GradeItem(
                name=name,
                points_achieved=points_achieved,
                weight_achieved=weight_achieved,
                max_points=max_points,
                max_weight=max_weight,
                grade=grade,
                comments=comments
            )

            print(grade_item)

            grades.append(grade_item)
        
        return grades
    
    def get_assignments(self, org_unit_id: str) -> list[Assignment]:
        """Fetches the assignments for a specific course.

        Args:
            org_unit_id (str): The organizational unit ID for the course for which to fetch assignments.
        
        Returns:
            list[Assignment]: A list of Assignment objects representing the assignments for the course.
        """
        pass


            

