"""
Author: Ahmet Aksoy
Date: 2026-04-20
Python 3.12 - Ubuntu 24.04

Description:
    Sending data to a REST API using HTTP POST with a JSON body.
    This example uses the JSONPlaceholder API (https://jsonplaceholder.typicode.com)
    which simulates a real API: it accepts your POST request, echoes back
    the created resource with an assigned ID, but does not actually store it.

    Three patterns are demonstrated:
      1. Simple POST with a JSON body
      2. POST with custom HTTP headers (e.g. Content-Type, Accept)
      3. Checking the response and reading the returned data

    This pattern applies directly to real-world APIs such as
    form submissions, creating records, sending notifications, etc.

Requirements:
    pip install requests
"""

import requests

def create_post(user_id, title, body):

    url = "https://jsonplaceholder.typicode.com/posts"

    # Build the JSON payload as a Python dict.
    # requests will automatically serialize this to JSON
    # and set Content-Type: application/json when json= is used.
    payload = dict()
    payload["userId"] = user_id
    payload["title"]  = title
    payload["body"]   = body

    # Set custom headers explicitly (optional here, but common in real APIs)
    headers = dict()
    headers["Content-Type"] = "application/json"
    headers["Accept"]       = "application/json"

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)

        # A successful POST typically returns HTTP 201 Created
        if response.status_code == 201:
            print("Post created successfully!")
            print("----------------------------------------------")

            result = response.json()

            # The API echoes back the sent data plus an assigned ID
            print("  Assigned ID :", str(result["id"]))
            print("  User ID     :", str(result["userId"]))
            print("  Title       :", str(result["title"]))
            print("  Body        :", str(result["body"]))
        else:
            print("Unexpected status code:", response.status_code)
            print("Response body:", str(response.text))

    except:
        print("Error: Could not connect to the API.")
        print("Check your internet connection and try again.")


def update_post(post_id, title, body):
    """
    PUT request: replaces an entire existing resource.
    Use this when you want to update all fields of a record.
    For partial updates, use PATCH instead (see comments below).
    """

    url = "https://jsonplaceholder.typicode.com/posts/" + str(post_id)

    payload = dict()
    payload["id"]     = post_id
    payload["userId"] = 1
    payload["title"]  = title
    payload["body"]   = body

    headers = dict()
    headers["Content-Type"] = "application/json"

    try:
        # PUT replaces the whole resource
        # For partial update: requests.patch(url, json=payload, ...)
        response = requests.put(url, json=payload, headers=headers, timeout=10)

        # Successful PUT returns HTTP 200 OK
        if response.status_code == 200:
            print("Post updated successfully!")
            print("----------------------------------------------")
            result = response.json()
            print("  Post ID :", str(result["id"]))
            print("  Title   :", str(result["title"]))
            print("  Body    :", str(result["body"]))
        else:
            print("Update failed. HTTP Status:", response.status_code)

    except:
        print("Error: Could not connect to the API.")


def main():
    # Example 1: Create a new post via POST
    print("=== Creating a new post ===")
    print()
    create_post(
        user_id = 5,
        title   = "Mojo and Python working together",
        body    = "Mojo can use any Python library via Python.import_module()."
    )

    print()

    # Example 2: Update an existing post via PUT
    print("=== Updating post with ID: 3 ===")
    print()
    update_post(
        post_id = 3,
        title   = "Updated title",
        body    = "This post was updated using an HTTP PUT request."
    )

main()
