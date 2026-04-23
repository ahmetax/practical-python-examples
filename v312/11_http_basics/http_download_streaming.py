"""
Author: Ahmet Aksoy
Date: 2026-04-20
Python 3.12 - Ubuntu 24.04

Description:
    Downloading files efficiently using HTTP streaming in Python.

    When downloading large files, loading the entire response into memory
    at once is wasteful and can crash your program on low-memory systems.
    Streaming reads the response body in small chunks and writes each
    chunk to disk immediately, keeping memory usage flat regardless of
    file size.

    Three patterns are demonstrated:
      1. Simple download       — small files, no streaming needed
      2. Streaming download    — large files, fixed memory usage
      3. Download with progress — show how many bytes have been received

    For testing we use publicly available files from:
      https://speed.hetzner.de  — test files of various sizes
      https://httpbin.org/bytes/{n} — generates n random bytes on demand

Requirements:
    pip install requests
"""

import requests

def simple_download(url, save_path):
    """
    Download a small file in one shot.
    response.content loads the entire file into memory.
    Fine for small files (images, JSON, small PDFs).
    Not suitable for large files — use streaming_download() instead.
    """
    try:
        print("Downloading:", url)
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            f = open(save_path, "wb")
            f.write(response.content)
            f.close()

            size_kb = len(response.content) // 1024
            print("Saved to:", save_path)
            print("Size    :", size_kb, "KB")
        else:
            print("Download failed. HTTP Status:", response.status_code)

    except:
        print("Error: Could not download the file.")


def streaming_download(url, save_path, chunk_size):
    """
    Download a large file in chunks using stream=True.

    With stream=True, requests does not download the response body
    immediately. Instead, iter_content() yields one chunk at a time.
    Each chunk is written to disk before the next one is fetched,
    so memory usage stays constant at roughly chunk_size bytes.

    chunk_size: number of bytes per chunk. 8192 (8KB) is a common default.
    Larger chunks (e.g. 65536 = 64KB) reduce I/O overhead on fast connections.
    """

    try:
        print("Streaming download:", url)
        print("Chunk size:", chunk_size // 1024, "KB")

        # stream=True tells requests to hold the connection open
        # and not load the body until we ask for it
        response = requests.get(url, stream=True, timeout=30)

        if response.status_code != 200:
            print("Download failed. HTTP Status:", response.status_code)
            return

        f    = open(save_path, "wb")
        total_bytes = 0
        chunk_count = 0

        # iter_content yields raw bytes chunks
        for chunk in response.iter_content(chunk_size=chunk_size):
            # iter_content may yield empty chunks — skip them
            if chunk:
                f.write(chunk)
                total_bytes += len(chunk)
                chunk_count += 1

        f.close()

        print("Download complete!")
        print("  Saved to   :", save_path)
        print("  Total size :", total_bytes // 1024, "KB")
        print("  Chunks read:", chunk_count)

    except:
        print("Error: Streaming download failed.")


def streaming_download_with_progress(url, save_path):
    """
    Streaming download with a simple progress indicator.
    Reads Content-Length header to calculate percentage if available.
    Some servers do not send Content-Length — in that case we show
    only the bytes received so far.
    """

    chunk_size = 8192

    try:
        print("Downloading with progress:", url)

        response = requests.get(url, stream=True, timeout=30)

        if response.status_code != 200:
            print("Download failed. HTTP Status:", response.status_code)
            return

        # Try to read Content-Length header for progress calculation
        total_size  = 0
        has_length  = False

        content_length = response.headers.get("Content-Length", None)

        if content_length != None:
            total_size = len(content_length)
            has_length = True
            print("File size:", total_size // 1024, "KB")
        else:
            print("File size: unknown (no Content-Length header)")

        f        = open(save_path, "wb")
        received      = 0
        last_reported = 0  # track last printed progress step

        for chunk in response.iter_content(chunk_size=chunk_size):
            if chunk:
                f.write(chunk)
                received += len(chunk)

                if has_length:
                    percent = (received * 100) // total_size
                    # Print progress every 10%
                    if percent >= last_reported + 10:
                        last_reported = (percent // 10) * 10
                        print("  Progress:", last_reported, "%  (", received // 1024, "KB )")
                else:
                    # No Content-Length — just report every 50KB
                    if received - last_reported >= 50 * 1024:
                        last_reported = received
                        print("  Received:", received // 1024, "KB")

        f.close()
        print("Download complete! Saved to:", save_path)
        print("Total received:", received // 1024, "KB")

    except:
        print("Error: Download with progress failed.")


def main():
    # Example 1: Simple download — httpbin generates 10KB of random bytes
    print("=== Simple Download ===")
    print()
    simple_download(
        "https://httpbin.org/bytes/10240",
        "/tmp/simple_download.bin"
    )

    print()

    # Example 2: Streaming download — httpbin generates 1MB of random bytes
    # chunk_size = 8192 bytes (8KB per chunk)
    print("=== Streaming Download ===")
    print()
    streaming_download(
        "https://httpbin.org/bytes/1048576",
        "/tmp/streaming_download.bin",
        8192
    )

    print()

    # Example 3: Streaming with progress — 500KB file
    print("=== Streaming Download with Progress ===")
    print()
    streaming_download_with_progress(
        "https://httpbin.org/bytes/512000",
        "/tmp/progress_download.bin"
    )

main()