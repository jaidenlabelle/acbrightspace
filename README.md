# Algonquin College Brightspace Python API
A simple Python libary for working with Algonquin College's Brightspace website.

## Features
- Get all courses
- Get assignment grades for each course

## Installation
Requirements: Python 3.14+.
```sh
pip install "git+https://github.com/jaidenlabelle/acbrightspace"
```

## Usage
1. Extract your TOTP secret from your two-factor authentication app. I recommend using [this tool](https://github.com/scito/extract_otp_secrets).
2. Start using acbrightspace
```python
from acbrightspace.brightspace import Brightspace

# Login to the Brightspace website
brightspace = Brightspace()
brightspace.login(
    username=<Brightspace Email>,
    password=<Brightspace Password>,
    totp_secret=<ABCDEFGHIJKLMNOP123> # The secret you extracted
)

# Get all courses (active and closed)
courses = brightspace.get_courses()

# Print the name of each course
for course in courses:
    print(course.name)
```

## More Examples
### Getting all Grade Items from a Course
```python
# Get the grades for the course with org_unit_id = 683274.
# When you open a course on Brightspace the url should look like ".../d2l/home/683274".
grades = brightspace.get_grades("683274")
```

## How to Contribute
### Report Issues
Please report bugs and suggest features via [GitHub Issues](https://github.com/jaidenlabelle/acbrightspace/issues).

Before opening an issue, search the tracker for possible duplicates. If you find a duplicate, please add a comment saying that you encountered the problem as well.

### Contribute Code
Pull requests are welcome! Please add tests for any new functionality you add, and verify that all tests pass.

