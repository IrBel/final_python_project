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

To execute the tests locally:

```bash
$  pytest API_tests/ --html=reports/api_report.html
```
```bash
$  pytest UI_tests/ --html=reports/ui_report.html
```
After execution, report will be automatically generated with captured logs for each test in ```reports/``` folder