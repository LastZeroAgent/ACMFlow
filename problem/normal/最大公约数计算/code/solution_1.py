import sys

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

for line in sys.stdin:
    a, b = map(int, line.split())
    print(gcd(a, b))