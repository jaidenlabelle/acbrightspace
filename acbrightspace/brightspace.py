from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pyotp
import logging

logger = logging.getLogger(__name__)

class Brightspace():
    """Class to interact with Algonquin College Brightspace using Selenium WebDriver."""

    def __init__(self):
        logger.debug("Initializing Brightspace WebDriver")
        self.driver = webdriver.Chrome()

    def quit(self):
        logger.debug("Quitting Brightspace WebDriver")
        self.driver.quit()

    def login(self, username, password, otp_secret=None):
        wait = WebDriverWait(self.driver, 10)  # wait up to 10 seconds

        self.driver.get("https://brightspace.algonquincollege.com")
        
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "loginfmt"))
        )

        username_field.send_keys(username)
        username_field.send_keys(Keys.RETURN)

        password_field = wait.until(
            EC.presence_of_element_located((By.ID, "passwordInput"))
        )

        password_field.send_keys(password)
        password_field.send_keys(Keys.RETURN)

        otc_field = wait.until(
            EC.presence_of_element_located((By.NAME, "otc"))
        )

        otp = pyotp.TOTP(otp_secret)

        otc_field.send_keys(otp.now())
        otc_field.send_keys(Keys.RETURN)
        

    def logout(self):
        raise NotImplementedError("Logout method not implemented yet.")
    
    def grades(self):
        raise NotImplementedError("Grades method not implemented yet.")
    
    def assignments(self):
        raise NotImplementedError("Assignments method not implemented yet.")