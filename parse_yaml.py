"""
Read an input argument to a file path with a list of HTTP endpoints in YAML format.
Test the health of the endpoints every 15 seconds.
Keep track of the availability percentage of the HTTP domain names being monitored by the program.
Log the cumulative availability percentage for each domain to the console after
the completion of each 15-second test cycle.

Setup Virtual Environment:
    - python3 -m venv venv
    - source venv/bin/activate (if on Windows: venv/Scripts/activate)

Install Python Packages:
    - Import PyYAML: pip install pyyaml
    - Import requests: pip install requests
    - Import tcp_latency: pip install tcp_latency
"""

from tcp_latency import measure_latency
import time
import requests
import yaml
import math

def parse_yaml(yml_input):
    # Read YAML file
    with open(yml_input, 'r') as f:
        get_http = yaml.safe_load(f)

        # Store urls in an array
        urls = []
        for links in get_http:
            urls.append(links['url'])

    return urls

def verify_http_service(urls):
    # Create empty array to store status
    status_codes = []
    count_up = 0
    count_down = 0
    # Iterate through each URL
    for url in urls:
        response = requests.get(url)
        # String formatting
        url = url.rstrip('/')
        url_split = url.split('://')
        # Get the latency of each URL
        latency = measure_latency(host=url_split[1])
        if not latency:
            print("DOWN")
            status_codes.append("DOWN")
        elif 200 <= response.status_code < 299 and latency[0] < 500:
            print("UP")
            status_codes.append("UP")
        else:
            print("DOWN")
            status_codes.append("DOWN")
        time.sleep(15)

        # Calculations for health status
        for s in status_codes:
            if s == 'UP':
                count_up += 1
            else:
                count_down += 1

        calc_percentage = 100 * (count_up / (count_up + count_down))
        print(f"{url_split[1]} has {math.ceil(calc_percentage)}% availability percentage")

def main():
    yml_input = input("Enter YAML file: ")
    verify_http_service(urls=parse_yaml(yml_input))

if __name__ == "__main__":
    main()

