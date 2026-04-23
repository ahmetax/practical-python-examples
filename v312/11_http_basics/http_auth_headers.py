"""
Author: Ahmet Aksoy
Date: 2026-04-20
Python 3.12 - Ubuntu 24.04

Description:
    Accessing protected REST APIs using Authorization headers.
    This example demonstrates three common authentication patterns:

      1. Bearer Token  — most common in modern APIs (OAuth2, JWT)
      2. API Key       — simple key passed in a header (e.g. X-Api-Key)
      3. Basic Auth    — username:password encoded in Base64

    For safe testing without real credentials, we use:
      - https://httpbin.org  : a free HTTP testing service that echoes
                               back exactly what you sent, including headers.
                               Perfect for verifying your auth headers are
                               formatted correctly before hitting a real API.

    In a real project, never hardcode tokens or passwords in source code.
    Use environment variables or a config file instead (see main() below).

Requirements:
    pip install requests
"""

import requests

def bearer_token_request(token):
    """
    Bearer Token is the most widely used auth method today.
    Used by: GitHub API, Twitter/X API, Google APIs, most OAuth2 services.
    Header format: Authorization: Bearer <token>.
    """

    url = "https://httpbin.org/bearer"

    headers = dict()
    headers["Authorization"] = "Bearer " + token

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print("Bearer auth accepted!")
            print("  Authenticated:", str(result["authenticated"]))
            print("  Token        :", str(result["token"]))
        elif response.status_code == 401:
            print("Unauthorized. Token was rejected.")
        else:
            print("Unexpected status:", response.status_code)

    except:
        print("Error: Could not connect to the API.")


def api_key_request(api_key):
    """
    API Key authentication: a static key passed in a custom header.
    Header name varies by API provider, common examples:
      X-Api-Key, X-API-Key, Api-Key, Authorization: ApiKey <key>
    Used by: OpenAI, NewsAPI, WeatherAPI, many SaaS platforms.

    httpbin.org/get echoes back all received headers so we can verify
    the key was sent correctly.
    """

    url = "https://httpbin.org/get"

    headers = dict()
    headers["X-Api-Key"] = api_key
    headers["Accept"]    = "application/json"

    try:
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            result = response.json()
            # httpbin echoes sent headers under result["headers"]
            received_headers = result["headers"]
            print("API Key request successful!")
            print("  Echoed X-Api-Key:", str(received_headers["X-Api-Key"]))
        else:
            print("Request failed. HTTP Status:", response.status_code)

    except:
        print("Error: Could not connect to the API.")


def basic_auth_request(username, password):
    """
    Basic Auth: credentials sent as Base64-encoded "username:password".
    Older method, still used by some internal APIs and services.
    Always use HTTPS with Basic Auth — credentials are only Base64
    encoded, not encrypted.

    requests handles the encoding automatically via the auth= parameter.
    httpbin.org/basic-auth/{user}/{pass} accepts and validates credentials.
    """

    # Build the URL with the expected credentials for httpbin testing
    url = "https://httpbin.org/basic-auth/" + username + "/" + password

    try:
        auth = (lambda u, p: (u, p))(username, password)
        response = requests.get(url, auth=auth, timeout=10)

        if response.status_code == 200:
            result = response.json()
            print("Basic auth accepted!")
            print("  Authenticated:", str(result["authenticated"]))
            print("  User         :", str(result["user"]))
        elif response.status_code == 401:
            print("Unauthorized. Wrong username or password.")
        else:
            print("Unexpected status:", response.status_code)

    except:
        print("Error: Could not connect to the API.")


def main():
    # --- Best practice: read credentials from environment variables ---
    # Never hardcode real tokens or passwords in source code.
    # Set them in your shell before running:
    #   export API_TOKEN="your_real_token_here"
    #   export API_KEY="your_real_key_here"
    # Then read them in os module:
    #
    #   token = str(os.environ.get("API_TOKEN", ""))
    #
    # For this example we use placeholder values that work with httpbin.org.

    # Example 1: Bearer Token
    print("=== Bearer Token Authentication ===")
    print()
    bearer_token_request("my-test-token-12345")

    print()

    # Example 2: API Key in custom header
    print("=== API Key Authentication ===")
    print()
    api_key_request("my-api-key-abcde")

    print()

    # Example 3: Basic Auth with username and password
    print("=== Basic Auth Authentication ===")
    print()
    basic_auth_request("python_user", "secret123")

main()
