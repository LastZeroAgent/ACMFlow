# Python解决方案
a, b, c = map(int, input().split())
sorted_nums = sorted([a, b, c])
print(' '.join(map(str, sorted_nums)))