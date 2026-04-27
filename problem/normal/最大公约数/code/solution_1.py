import sys
import math

def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    a, b = map(int, sys.stdin.readline().split())
    print(gcd(a, b))