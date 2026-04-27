def digital_root(n):
    if n == 0:
        return 0
    return 9 if n % 9 == 0 else n % 9

n = int(input())
print(digital_root(n))