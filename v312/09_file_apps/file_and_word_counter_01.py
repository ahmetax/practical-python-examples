"""
Author: Ahmet Aksoy
Date: 2026-04-19
Python 3.12 - Ubuntu 24.04
"""

from pathlib import Path

class FileCounter():
    "Used to count total # of files and words."
    count = 0
    total_words = 0
    
    def __init__(self):
        self.count = 0
        self.total_words = 0

def count_words_in_file(filepath):
    f = open(filepath, "r")
    content = f.read()
    f.close()
    
    words = content.split()
    return len(words)

def process_txt_files(path, counter):

    entries = [file for file in path.glob("*") if file.is_file()]
    
    for i in range(len(entries)):
        entry_name = entries[i]
        entry_path = path.joinpath(entry_name)
        
        if entry_path.is_dir():
            process_txt_files(entry_path, counter)
        elif entry_path.is_file() and (entry_name.suffix == ".txt"):
            counter.count += 1
            word_count = count_words_in_file(entry_path)
            counter.total_words += word_count
            print(counter.count, "-", entry_path, "->", word_count, "words")

def main():
    counter = FileCounter()
    path = Path("/home/axax/Desktop/python_projects/gutenberg_org/")
    
    if not path.exists():
        print("Folder not found: ", path)
        return
    
    process_txt_files(path, counter)
    print("\n=== RESULTS ===")
    print("Total number of files: ", counter.count)
    print("Total number of words: ", counter.total_words)

main()