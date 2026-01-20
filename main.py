import os
from acbrightspace.brightspace import Brightspace
import logging
from dotenv import load_dotenv
from selenium import webdriver

logging.basicConfig(level=logging.INFO)
load_dotenv()

def main():
    brightspace = Brightspace()
    brightspace.login(
        driver=webdriver.Chrome(),
        username=os.environ["BRIGHTSPACE_USERNAME"],
        password=os.environ["BRIGHTSPACE_PASSWORD"],
        totp_secret=os.environ["BRIGHTSPACE_TOTP_SECRET"]
    )
    #brightspace.get_courses()
    #print(brightspace.get_grades("683274"))
    brightspace.test_thing()

    # Wait for user input before closing
    input("Press Enter to close the browser...")

    brightspace.test_thing()

    # Wait for user input before closing
    input("Press Enter to close the browser...")
    
if __name__ == "__main__":
    main()