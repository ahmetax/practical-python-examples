"""
Author: Ahmet Aksoy
Date: 2026-04-20
Python 3.12 - Ubuntu 24.04

Description:
    Fetching data from a public JSON API using Python's requests module.
    This example uses the JSONPlaceholder API (https://jsonplaceholder.typicode.com)
    which is a free, public REST API for testing and prototyping.

    We fetch a list of posts, filter them by user ID, and display
    selected fields. This pattern is directly applicable to any
    REST API that returns JSON data.

Requirements:
    pip install requests
"""

import requests
import json

def fetch_posts(user_id):
    url = "https://jsonplaceholder.typicode.com/posts"

    # Build query parameters as a Python dict
    params = dict()
    params["userId"] = user_id

    try:
        response = requests.get(url, params=params, timeout=10)

        # Check HTTP status code before processing
        if response.status_code != 200:
            print("Request failed. HTTP Status:", response.status_code)
            return

        posts = response.json()
        count = len(posts)
        print("Found", count, "posts for user ID:", user_id)
        print("----------------------------------------------")

        for post in posts:
            post_id    = str(post["id"])
            title      = str(post["title"])
            body_preview = str(post["body"])[0:60]  # First 60 chars

            print("Post #" + post_id)
            print("  Title  :", title)
            print("  Preview:", body_preview + "...")
            print()

    except:
        print("Error: Could not connect to the API.")
        print("Check your internet connection and try again.")


def fetch_single_post(post_id):

    url = "https://jsonplaceholder.typicode.com/posts/" + str(post_id)

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 404:
            print("Post not found. ID:", post_id)
            return

        if response.status_code != 200:
            print("Request failed. HTTP Status:", response.status_code)
            return

        post = response.json()

        print("Post details")
        print("----------------------------------------------")
        print("  ID    :", str(post["id"]))
        print("  UserID:", str(post["userId"]))
        print("  Title :", str(post["title"]))
        print("  Body  :")
        print(str(post["body"]))

    except:
        print("Error: Could not connect to the API.")


def main():
    # Example 1: Fetch all posts by a specific user
    print("=== Fetching posts for user ID: 2 ===")
    print()
    fetch_posts(2)

    # Example 2: Fetch a single post by its ID
    print()
    print("=== Fetching single post with ID: 7 ===")
    print()
    fetch_single_post(7)

main()