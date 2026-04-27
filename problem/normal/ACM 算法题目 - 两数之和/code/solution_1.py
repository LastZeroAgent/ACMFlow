def two_sum():
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    n = int(input[ptr])
    ptr += 1
    target = int(input[ptr])
    ptr += 1
    nums = list(map(int, input[ptr:ptr+n]))
    hash_map = {}
    for i in range(n):
        complement = target - nums[i]
        if complement in hash_map:
            print(hash_map[complement], i)
            return
        hash_map[nums[i]] = i

two_sum()