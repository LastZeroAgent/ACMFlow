def find_median_sorted_arrays(nums1, nums2):
    m, n = len(nums1), len(nums2)
    total = m + n
    if total % 2 == 1:
        k = total // 2
        i, j = 0, 0
        while k > 0:
            if i < m and (j >= n or nums1[i] <= nums2[j]):
                i += 1
            else:
                j += 1
            k -= 1
        return float(min(nums1[i], nums2[j]))
    else:
        k1, k2 = total // 2 - 1, total // 2
        i, j = 0, 0
        a, b = 0, 0
        while k1 > 0:
            if i < m and (j >= n or nums1[i] <= nums2[j]):
                a = nums1[i]
                i += 1
            else:
                a = nums2[j]
                j += 1
            k1 -= 1
        if i < m and (j >= n or nums1[i] <= nums2[j]):
            b = nums1[i]
        else:
            b = nums2[j]
        return (a + b) / 2.0

if __name__ == "__main__":
    import sys
    input = sys.stdin.read().split()
    ptr = 0
    m, n = int(input[ptr]), int(input[ptr+1])
    ptr += 2
    nums1 = list(map(int, input[ptr:ptr+m]))
    ptr += m
    nums2 = list(map(int, input[ptr:ptr+n]))
    print("{0:.1f}".format(find_median_sorted_arrays(nums1, nums2)))