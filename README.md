# Syntecxhub SQL Injection Scanner

A Python-based local testing project that sends sample
SQL injection test inputs to a controlled Flask application
and checks responses for possible SQL error indicators.

## Features

- Local target URL validation
- Sample SQL injection test inputs
- HTTP response analysis
- SQL error indicator detection
- Logging of scan results
- Basic concurrency with ThreadPoolExecutor
- Rate limiting
- Request timeout and error handling
- Summary report

## Technologies

- Python
- Flask
- Requests
- ThreadPoolExecutor
- Logging

## Project Files

- scanner.py: Main scanner
- test_app.py: Local simulated test application
- requirements.txt: Required packages
- scan_results.log: Generated scan log

## Setup

Install dependencies:

    python -m pip install -r requirements.txt

## Run the Local Test App

    python test_app.py

## Run the Scanner

Open another terminal and run:

    python scanner.py

Enter this local target:

    http://127.0.0.1:5000

## Important Note

The test application simulates SQL error responses.
Detected indicators demonstrate the scanner's response
analysis and do not prove a real SQL injection vulnerability.

Use this project only on systems you own or have
explicit permission to test.