n = int(input())
for _ in range(n):
    num = input().strip()
    sum_odd = 0
    sum_even = 0
    for i, ch in enumerate(num):
        if i % 2 == 0:  # 奇数位
            sum_odd += int(ch)
        else:  # 偶数位
            sum_even += int(ch)
    print("YES" if sum_odd == sum_even else "NO")