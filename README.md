# Restful Booker API Automation Framework

A Python-based API automation framework for testing the [Restful Booker API](https://restful-booker.herokuapp.com), built with **Pytest** and **Requests**.

## Project Overview

This project demonstrates a reusable and maintainable approach to API test automation. It covers authentication, booking operations, positive and negative scenarios, and booking lifecycle validation.

The framework uses reusable API utilities, centralized configuration, shared test data, and Pytest fixtures to reduce duplication and simplify test maintenance.

## Tech Stack

- **Language:** Python 3.12
- **Test Framework:** Pytest
- **HTTP Library:** Requests
- **Test Reports:** Pytest HTML and Allure Pytest
- **IDE:** PyCharm
- **Version Control:** Git and GitHub

## Framework Architecture

| Component | Purpose |
|---|---|
| `APIClient` | Provides reusable methods for GET, POST, PUT, PATCH, and DELETE requests. |
| `ConfigManager` | Loads the API base URL from the configuration file and validates required settings. |
| `booking_helper.py` | Centralizes reusable booking operations. |
| `conftest.py` | Provides shared Pytest fixtures, including the API client and authentication token. |
| `booking_data.py` | Stores reusable booking data and provides a function to return a fresh copy. |
| `tests/api/` | Contains API test cases organized by functionality. |

## Project Structure

```text
restful-booker-api-automation/
├── config/
│   └── settings.ini
├── reports/
├── tests/
│   ├── api/
│   │   ├── test_auth.py
│   │   ├── test_booking_list.py
│   │   ├── test_create_booking.py
│   │   ├── test_get_booking.py
│   │   ├── test_update_booking.py
│   │   ├── test_patch_booking.py
│   │   └── test_delete_booking.py
│   ├── test_data/
│   │   └── booking_data.py
│   └── conftest.py
├── utils/
│   ├── api_client.py
│   ├── booking_helper.py
│   └── config_manager.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Test Coverage

The test suite includes scenarios covering:

- Authentication and token generation
- Creating bookings
- Retrieving individual bookings
- Retrieving and filtering booking collections
- Updating bookings using PUT
- Partially updating bookings using PATCH
- Deleting bookings
- Invalid inputs and booking IDs
- Authentication-related negative scenarios
- Booking lifecycle and response validation

## Prerequisites

- Python 3.12 or a compatible Python version
- Git
- Internet access to reach the public Restful Booker API

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/MandarBhoir/restful-booker-api-automation.git
cd restful-booker-api-automation
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure the API base URL

Check `config/settings.ini`:

```ini
[API]
base_url=https://restful-booker.herokuapp.com
```

## Running Tests

Run the complete suite:

```bash
python -m pytest
```

Run a specific test module:

```bash
python -m pytest tests/api/test_auth.py -v
```

Run the booking creation tests:

```bash
python -m pytest tests/api/test_create_booking.py -v
```

Generate an HTML report:

```bash
python -m pytest --html=reports/report.html --self-contained-html
```

Generate an Allure results directory:

```bash
python -m pytest --alluredir=reports/allure-results
```

Viewing an Allure report requires the Allure command-line tool to be installed:

```bash
allure serve reports/allure-results
```

## Test Reports

The framework supports generating HTML reports with `pytest-html` and collecting Allure results with `allure-pytest`.

Because the project uses a public API, test results may be affected by network availability, API downtime, rate limiting, or changes in remote test data.

## Design Principles

- Reusable API request methods
- Separation of configuration, test data, helpers, and test cases
- Shared fixtures for common setup
- Parameterized tests where appropriate
- Clear response and status-code assertions
- Maintainable test organization

## Future Improvements

Potential enhancements include:

- Automated test execution through GitHub Actions
- Improved logging and failure diagnostics
- Additional response schema validation
- More robust handling of transient public API failures

These are planned enhancements, not claims that they are already implemented.

## Disclaimer

This project uses the publicly available Restful Booker API for learning and demonstration purposes. Its availability and behavior are outside the project's control.
