# acbrightspace
A Python library for interacting with Algonquin College's Learning Management System, Brightspace.

Currently, it can only display course names and codes.

## Getting Setup
1. Extract your TOTP secret from your two-factor authentication app. I recommend using [this tool](https://github.com/scito/extract_otp_secrets).
2. Create a file called `.env` to store your Algonquin College email credentials:
```
BRIGHTSPACE_USERNAME=<Your Algonquin email>
BRIGHTSPACE_PASSWORD=<Your Algonquin email password>
BRIGHTSPACE_TOTP_SECRET=<ABCDEFGHIJKLMNOP123> # The secret you extracted
```
3. Run the `main.py` file to display all your courses in the console.

## Example Output
```
|
`-- 2024 Fall
    |-- Network Programming (24F_CST8109_020)
    |-- BI and Data Analytics (24F_CST8390_010)
    |-- OOP with Design Patterns (24F_CST8288_020)
    |-- Systems Analysis and Design (24F_CST2234_300)
    |-- OOP with Design Patterns (24F_CST8288_021)
    |-- Mobile Graphical Interface Prog. (24F_CST2335_010)
    |-- Network Programming (24F_CST8109_022)
    |-- Mobile Graphical Interface Prog. (24F_CST2335_011)
`-- 2024 Spring/Summer
    |-- Coop Education and Job Readiness (24S_GEP1001_314)
    |-- Object Oriented Programming (Java) (24S_CST8284_300)
    |-- Web Programming (24S_CST8285_300)
    |-- Popular Culture (24S_RAD2001_351)
    |-- Technical Comm. for Eng. Technology (24S_ENL2019T_311)
    |-- Database Systems (24S_CST2355_300)
    |-- Operating Systems Fund (GNU/Linux) (24S_CST8102_300)
    |-- Object Oriented Programming (Java) (24S_CST8284_302)
    |-- Database Systems (24S_CST2355_302)
    |-- Programming and Analysis A02 Homeroom (24S_H_1561X_WO_03_F_A02)
```