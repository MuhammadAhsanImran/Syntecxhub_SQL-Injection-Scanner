import logging
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests


TEST_INPUTS = [
    "'",
    "''",
    "' OR '1'='1",
    "' OR '1'='1' --"
]

ERROR_INDICATORS = [
    "sql syntax",
    "mysql",
    "sqlite",
    "postgresql",
    "ora-",
    "database error"
]

MAX_WORKERS = 2
REQUEST_DELAY = 0.5
TIMEOUT = 5

rate_lock = threading.Lock()
last_request_time = 0


logging.basicConfig(
    filename="scan_results.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def validate_target(url):
    parsed_url = urlparse(url)

    return (
        parsed_url.scheme in ("http", "https")
        and parsed_url.hostname == "127.0.0.1"
        and parsed_url.port == 5000
    )


def apply_rate_limit():
    global last_request_time

    with rate_lock:
        current_time = time.monotonic()
        wait_time = REQUEST_DELAY - (
            current_time - last_request_time
        )

        if wait_time > 0:
            time.sleep(wait_time)

        last_request_time = time.monotonic()


def scan_input(search_url, test_input):
    apply_rate_limit()

    try:
        response = requests.get(
            search_url,
            params={"q": test_input},
            timeout=TIMEOUT
        )

        response_text = response.text.lower()

        found_indicators = [
            indicator
            for indicator in ERROR_INDICATORS
            if indicator in response_text
        ]

        result = {
            "input": test_input,
            "status": response.status_code,
            "indicators": found_indicators,
            "error": None
        }

        if found_indicators:
            result["finding"] = "Possible SQL error indicator"
        else:
            result["finding"] = "No SQL error indicator"

        logging.info(
            "Input=%r Status=%s Indicators=%s",
            test_input,
            response.status_code,
            found_indicators
        )

        return result

    except requests.RequestException as error:
        logging.error(
            "Input=%r Request failed: %s",
            test_input,
            error
        )

        return {
            "input": test_input,
            "status": None,
            "indicators": [],
            "finding": "Request failed",
            "error": str(error)
        }


def main():
    print("================================")
    print("   SQL Injection Scanner")
    print("================================")

    target_url = input(
        "Enter your local test URL: "
    ).strip().rstrip("/")

    if not validate_target(target_url):
        print("Target rejected.")
        print("Use only http://127.0.0.1:5000")
        return

    search_url = f"{target_url}/search"

    print("\nStarting local test scan...")
    print(f"Target: {search_url}")
    print(f"Test inputs: {len(TEST_INPUTS)}")
    print(f"Workers: {MAX_WORKERS}")
    print(f"Request delay: {REQUEST_DELAY} seconds")

    results = []

    with ThreadPoolExecutor(
        max_workers=MAX_WORKERS
    ) as executor:
        futures = [
            executor.submit(
                scan_input,
                search_url,
                item
            )
            for item in TEST_INPUTS
        ]

        for future in as_completed(futures):
            result = future.result()
            results.append(result)

            print("\n------------------------------")
            print("Input:", result["input"])
            print("Status:", result["status"])
            print("Finding:", result["finding"])

            if result["indicators"]:
                print("Indicators:", result["indicators"])

            if result["error"]:
                print("Error:", result["error"])

    possible_findings = sum(
        bool(result["indicators"])
        for result in results
    )

    print("\n================================")
    print("             REPORT")
    print("================================")
    print("Requests completed:", len(results))
    print("Possible indicators:", possible_findings)
    print("Log file: scan_results.log")
    print("Scan finished.")


if __name__ == "__main__":
    main()