import os
from acbrightspace.brightspace import Brightspace
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
load_dotenv()

def main():
    brightspace = Brightspace()
    brightspace.login(
        username=os.environ["BRIGHTSPACE_USERNAME"],
        password=os.environ["BRIGHTSPACE_PASSWORD"],
        totp_secret=os.environ["BRIGHTSPACE_TOTP_SECRET"]
    )
    #brightspace.get_courses()
    brightspace.get_grades("683274")
    
if __name__ == "__main__":
    main()