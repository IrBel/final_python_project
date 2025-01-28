# Final python project

## Overview

This project represents the Test Automation Suite that includes Web UI and API testing:
API - https://jsonplaceholder.typicode.com
Web UI - https://demoqa.com/text-box

## Local Setup
1. Install Python 3.8+
2. Clone the repository: `git clone <https://github.com/IrBel/final_python_project>`
3. Navigate into the project directory: `cd final_python_project`
4. Install dependencies: `pip install -r requirements.txt`

## Test Execution and Reporting

To execute the tests locally and get the test result report:

- to execute API test cases and create the appropriate report run
```
python -m pytest tests\test_api\test_api.py
```
- to execute UI test cases and create the appropriate report run
```
python -m pytest tests\test_ui\test_ui.py
```
- to execute all test cases and create the global report that consolidates the results from both the Web UI and API tests run
```
python -m pytest
```

Test reports are automatically generated and stored in the reports/ directory after the execution of the corresponding tests. 
To view the HTML report open the report.html file in any web browser.

## Logging
Log files are generated and stored in the logs/ directory.