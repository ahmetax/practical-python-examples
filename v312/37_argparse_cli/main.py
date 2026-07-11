# Author: Ahmet Aksoy
# Date: 27.05.2026
# Python3.12 Ubuntu 24.04

"""
Advanced argparse CLI Engine
Demonstrates command-line argument parsing, type enforcement, operational flags,
and automatic help generation while executing a practical file organizer utility.
"""

import argparse
import os
import shutil
from pathlib import Path


def organize_files(source_dir: str, target_dir: str, dry_run: bool) -> None:
    """
    Scans the source directory and categorizes files into subfolders 
    within the target directory based on their extensions.
    """
    src_path = Path(source_dir)
    tgt_path = Path(target_dir)

    if not src_path.exists() or not src_path.is_dir():
        print(f"[Error] Source directory '{source_dir}' does not exist or is not a directory.")
        return

    # Basic extension mapping rules
    extension_map = {
        '.txt': 'Documents', '.pdf': 'Documents', '.docx': 'Documents',
        '.jpg': 'Images', '.jpeg': 'Images', '.png': 'Images',
        '.py': 'Code', '.sh': 'Code', '.js': 'Code'
    }

    print(f"--- Initiating File Organization Layout ---")
    print(f"Source Location : {src_path.resolve()}")
    print(f"Target Location : {tgt_path.resolve()}")
    if dry_run:
        print("[Notice] DRY-RUN MODE ACTIVE: No files will actually be modified.\n")

    files_processed = 0

    for item in src_path.iterdir():
        if item.is_file():
            ext = item.suffix.lower()
            category = extension_map.get(ext, 'Others')
            
            destination_folder = tgt_path / category
            destination_file = destination_folder / item.name

            print(f" -> Mapping: {item.name} -> [{category}] folder")
            
            if not dry_run:
                # Perform actual file operations if not a dry-run
                destination_folder.mkdir(parents=True, exist_ok=True)
                shutil.move(str(item), str(destination_file))
                
            files_processed += 1

    print("-" * 50)
    print(f"Execution complete. Total items logged/processed: {files_processed}")


def main() -> None:
    """Defines the CLI argument architecture and orchestrates program flow."""
    # Initialize the master parser instance
    parser = argparse.ArgumentParser(
        description="A robust CLI tool to organize directory files smoothly by category extensions.",
        epilog="Example: python3 main.py ./downloads ./sorted_archive --dry-run"
    )

    # 1. Positional Arguments (Required parameters by default)
    parser.add_argument(
        "source",
        type=str,
        help="Path to the unsorted source directory containing target items."
    )
    
    parser.add_argument(
        "target",
        type=str,
        help="Path to the destination directory where categorized results will be saved."
    )

    # 2. Optional Arguments / Flags (Prefix with dashes)
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true", # Automatically sets to True if present, False if absent
        help="Simulates execution flow by printing layout actions without moving any files."
    )

    # Parse arguments provided at the command line boundary
    args = parser.parse_args()

    # Route clean parameters to core logic execution domain
    organize_files(source_dir=args.source, target_dir=args.target, dry_run=args.dry_run)


if __name__ == "__main__":
    main()