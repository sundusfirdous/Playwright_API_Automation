# Playwright API Automation Framework – Python & Pytest

## Project Overview

This project is an API automation testing framework developed using **Playwright with Python and Pytest**.

It demonstrates REST API testing, including CRUD operations, Bearer Token Authentication, data-driven testing using JSON and CSV files, and positive and negative test scenarios.

The framework uses Pytest fixtures to manage API request contexts, authentication, and reusable configurations.

## Tech Stack

- Python
- Playwright
- Pytest
- Pytest-Playwright
- Python-Dotenv
- REST API
- JSON
- CSV
- DummyJSON API

## Features

### 1. API Testing

Automated testing of the following HTTP methods:

- **GET:** Retrieve user information.
- **POST:** Create a new user.
- **PUT:** Update user information.
- **PATCH:** Partially update user information.
- **DELETE:** Delete a user.

### 2. Authentication

- Bearer Token Authentication.
- Login API to generate an access token.
- Token extraction from the login response.
- Reusable authentication through Pytest fixtures.
- Invalid token testing.

### 3. Data-Driven Testing

Test data is maintained separately from test scripts.

**JSON Data:**
- Reads test data using Python's `json` module.
- Uses `pytest.mark.parametrize` to execute multiple test scenarios.

**CSV Data:**
- Reads test data using Python's `csv` module.
- Uses `csv.DictReader` to extract test data.
- Executes multiple test cases with different input values.

### 4. Positive Testing

- Validate successful API responses.
- Verify HTTP status codes.
- Validate response body fields.
- Test CRUD operations.

### 5. Negative Testing

- Validate non-existing user IDs.
- Test invalid Bearer tokens.
- Verify authentication failure responses.
- Test requests with missing mandatory fields.

### 6. Pytest Framework

- Fixtures
- Parametrization
- `conftest.py`
- Test discovery
- Assertions
- Command-line test execution

## Project Structure

```text
Playwright_API_Automation/
│
├── reports/
│   └── report.html
│
├── test_data/                  # External test data
│   ├── data.csv                # CSV test data
│   └── data.json               # JSON test data
│
├── tests/                      # API test cases
│   ├── test_api.py             # Basic API tests
│   └── test_api_chaining.py    # Data-driven and chaining tests
│
├── config.py                   # Environment configuration
├── conftest.py                 # Reusable Pytest fixtures
├── pytest.ini                  # Pytest configuration
├── .env                        # Environment variables (not committed)
├── .gitignore                  # Ignored files and folders
├── README.md                   # Project documentation
└── requirements.txt            # Python dependencies / required libraries
```

## Prerequisites

- Python 3.10 or above
- VS Code or any Python IDE
- Git
- Internet connection

## Installation & Setup

### Step 1: Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
```

### Step 2: Navigate to the project directory

```bash
cd Playwright_API_Automation
```

### Step 3: Create a virtual environment

```bash
python -m venv venv
```

### Step 4: Activate the virtual environment

**Windows PowerShell:**

```powershell
venv\Scripts\activate
```

### Step 5: Install dependencies

```bash
pip install pytest playwright pytest-playwright python-dotenv
```

## Environment Configuration

The framework supports environment-based configuration through a `.env` file.

Example configuration:

```ini
ENV=qa

QA_BASE_URL=https://dummyjson.com
QA_USERNAME=emilys
QA_PASSWORD=emilyspass
```

The configuration is loaded through `config.py`.

**Security Note:** Never commit real credentials, access tokens, or sensitive environment variables to GitHub. Keep `.env` in `.gitignore`.

## Running Tests

### Run all test cases

```bash
pytest -v
```

### Run basic API tests

```bash
pytest tests/test_api.py -v
```

### Run API chaining and negative tests

```bash
pytest tests/test_api_chaining.py -v
```

### Run only POST tests

```bash
pytest -k post -v
```

### Run only GET tests

```bash
pytest -k get -v
```

### Run negative test cases

```bash
pytest -k invalid -v
```

### Run tests with detailed output

```bash
pytest -v -s
```

## API Under Test

**DummyJSON API**

- Base URL: https://dummyjson.com
- Documentation: https://dummyjson.com/docs
- Authentication: https://dummyjson.com/docs/auth
- Users API: https://dummyjson.com/docs/users

## Important Note About DummyJSON

DummyJSON is a mock REST API used for learning and testing.

POST, PUT, PATCH, and DELETE operations simulate successful responses but do not permanently modify the underlying database.

Therefore, this project validates API responses and simulated CRUD operations. It does not demonstrate persistent end-to-end database CRUD chaining.

## Learning Outcomes

Through this project, I have practised:

- REST API automation using Playwright Python.
- Pytest framework implementation.
- API authentication using Bearer tokens.
- Reusable fixtures and request contexts.
- Data-driven testing using JSON and CSV.
- Positive and negative API testing.
- HTTP methods and response validation.
- Test execution and debugging using Pytest.

## Future Enhancements

- API response schema validation.
- HTML test reporting.
- API request and response logging.
- Environment-specific test execution.
- CI/CD integration using Jenkins or GitHub Actions.
- API chaining with a persistent test environment.

## Author

**Sundus Firdous**

Automation Engineer | SDET | API Automation | Playwright Python | AI Automation