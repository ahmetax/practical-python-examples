"""
Author: Ahmet Aksoy
Date: 2026-04-16
Python 3.12 - Ubuntu 24.04
"""

# Armstrong number -> abcd... = pow(a,n) + pow(b,n) + pow(c,n) + pow(d,n) + ....

def is_armstrong(n) -> bool:
    nums = str(n)
    digits = len(nums)
    sum = 0

    for digit_char in nums:
        d = int(digit_char)    # convert to integer value of the digit
        sum += d ** digits

    return sum == n

def main():
    for number in range(0, 100000):
        if is_armstrong(number):
            print(number)
       
if __name__ == "__main__":
    main()
