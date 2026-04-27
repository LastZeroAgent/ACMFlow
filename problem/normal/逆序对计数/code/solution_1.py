def merge_and_count(nums, left, mid, right):
    temp = [0] * (right - left + 1)
    i, j, k = left, mid + 1, 0
    count = 0
    while i <= mid and j <= right:
        if nums[i] <= nums[j]:
            temp[k] = nums[i]
            k += 1
            i += 1
        else:
            count += mid - i + 1
            temp[k] = nums[j]
            k += 1
            j += 1
    while i <= mid:
        temp[k] = nums[i]
        k += 1
        i += 1
    while j <= right:
        temp[k] = nums[j]
        k += 1
        j += 1
    for p in range(len(temp)):
        nums[left + p] = temp[p]
    return count

def merge_sort(nums, left, right):
    if left >= right:
        return 0
    mid = (left + right) // 2
    count = merge_sort(nums, left, mid) + merge_sort(nums, mid + 1, right)
    count += merge_and_count(nums, left, mid, right)
    return count

n = int(input())
nums = list(map(int, input().split()))
print(merge_sort(nums, 0, n - 1))