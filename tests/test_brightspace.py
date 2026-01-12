
import sys
print(sys.path)

from acbrightspace.brightspace import Brightspace

import pytest

def test_login():

    brightspace = Brightspace()
    try:
        brightspace.login("testuser", "testpassword")
        assert brightspace.driver.current_url == "https://brightspace.algonquincollege.com"
    finally:
        brightspace.quit()