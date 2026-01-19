# Algonquin College Brightspace Python API
A simple Python libary for working with Algonquin College's Brightspace website.

## Features
- Get all courses
- Get grades for each course
- Get assignments for each course

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

#### Example Output
```
[GradeItem(name='Lab3', points=<acbrightspace.fraction.Fraction object at 0x00000268F05DE3C0>, weight=<acbrightspace.fraction.Fraction object at 0x00000268F05F65D0>, comments=None), GradeItem(name='Lab4', points=<acbrightspace.fraction.Fraction object at 0x00000268F05F6210>, weight=<acbrightspace.fraction.Fraction object at 0x00000268F067C2B0>, comments=None), GradeItem(name='Lab5', points=<acbrightspace.fraction.Fraction object at 0x00000268F067C510>, weight=<acbrightspace.fraction.Fraction object at 0x00000268F0611B50>, comments=None)]
```

### Getting all Assignments from a Course
```python
# Get the assignments for the course with org_unit_id = 683274.
# When you open a course on Brightspace the url should look like ".../d2l/home/683274".
assignments = brightspace.get_assignments("683274")
```

#### Example Output
```
[Assignment(name='SBA EXAM Upload Section 21', starts_at=None, ends_at=None, due_at=datetime.datetime(2024, 11, 28, 13, 0), score=None, completion_status='Not Submitted', evaluation_status=None), Assignment(name='SBA Exam Upload Section 22', starts_at=None, ends_at=None, due_at=datetime.datetime(2024, 11, 28, 13, 0), score=None, completion_status='1 Submission, 1 File', evaluation_status=None)]
```

## How to Contribute
### Report Issues
Please report bugs and suggest features via [GitHub Issues](https://github.com/jaidenlabelle/acbrightspace/issues).

Before opening an issue, search the tracker for possible duplicates. If you find a duplicate, please add a comment saying that you encountered the problem as well.

### Contribute Code
Pull requests are welcome! Please add tests for any new functionality you add, and verify that all tests pass.

