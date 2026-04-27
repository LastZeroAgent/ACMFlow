def is_palindrome(x: int) -> bool:
    if x < 0 or (x % 10 == 0 and x != 0):
        return False
    reverted = 0
    while x > reverted:
        reverted = reverted * 10 + x % 10
        x //= 10
    return x == reverted or x == reverted // 10

def main():
    import sys
    input = sys.stdin.readline
    T = int(input())
    for _ in range(T):
        n = int(input())
        print("Yes" if is_palindrome(n) else "No")

if __name__ == "__main__":
    main()