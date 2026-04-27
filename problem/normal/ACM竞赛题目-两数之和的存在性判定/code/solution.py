def main():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    n = int(input[ptr])
    ptr += 1
    nums = list(map(int, input[ptr:ptr+n]))
    ptr += n
    k = int(input[ptr])

    if n < 2:
        print("NO")
        return

    seen = set()
    for num in nums:
        complement = k - num
        if complement in seen:
            print("YES")
            return
        seen.add(num)
    print("NO")

if __name__ == "__main__":
    main()