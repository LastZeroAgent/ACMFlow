def count_distinct_prime_factors(n):
    factors = set()
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factors.add(n)
    return len(factors)

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        n = int(line.strip())
        print(count_distinct_prime_factors(n))