"""
Author: Ahmet Aksoy
Date: 2026-04-17
Python 3.12 - Ubuntu 24.04
"""

def main():
    lownum = 0
    highnum = 127
    
    for n in range(lownum, highnum + 1):
        if n > 1:
            for i in range(2, n):
                if n % i == 0:
                    break
            else:
                print(n)
                    
main()