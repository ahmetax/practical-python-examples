# Author: Ahmet Aksoy
# Date: 27.05.2026
# Python3.12 Ubuntu 24.04

"""
Virtualenv Deployment Target
A production-ready microservice script designed to simulate a final health check 
and environment sanity verification layer inside a deployment pipeline.
"""

import os
import sys

# Attempt to load a third-party module to verify virtualenv isolation status
try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False


def check_deployment_health() -> None:
    """Evaluates host execution parameters to guarantee the environment is safe for production."""
    print("--- Running Production Deployment Sanity Monitor ---")
    
    # 1. Detect if code is executing inside an isolated virtual environment
    # base_prefix changes away from sys.prefix when a virtualenv is active
    in_virtualenv = sys.prefix != getattr(sys, "base_prefix", sys.prefix)
    
    print(f" -> Isolation Layer Status   : {'ACTIVE (.venv)' if in_virtualenv else 'INACTIVE (GLOBAL)'}")
    print(f" -> Python Interpreter Path   : {sys.executable}")
    print(f" -> Python Core Version       : {sys.version.split()[0]}")
    print(f" -> Third-Party Requirements : {'RESOLVED' if REQUESTS_AVAILABLE else 'UNRESOLVED (CRITICAL)'}")
    print("-" * 55)

    if not in_virtualenv:
        print("[Critical Danger] Application is running globally! Aborting pipeline to prevent host pollution.")
        sys.exit(1)
        
    if not REQUESTS_AVAILABLE:
        print("[Deployment Error] Missing required production packages. Run 'pip install -r requirements.txt'.")
        sys.exit(1)

    print("[SUCCESS] Environment sanity check passed. The container/host is safe for heavy web routing operations.")


if __name__ == "__main__":
    check_deployment_health()