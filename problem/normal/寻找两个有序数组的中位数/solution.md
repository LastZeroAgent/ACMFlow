# 寻找两个有序数组的中位数 - 题解

## 算法分析

本题可以通过以下步骤解决：
1. **定位中位数位置**：计算合并后数组的总长度 len = m + n，确定中位数的位置。若 len 为奇数，则中位数在第 (len+1)/2 个元素；若为偶数，则需要取第 len/2 和 len/2+1 个元素的平均值。
2. **双指针遍历**：使用两个指针 i 和 j 分别指向 nums1 和 nums2 的起始位置，逐步比较元素大小，模拟合并过程，直到找到中位数位置。
3. **优化处理**：由于只需要找到中位数，可以在遍历过程中提前终止，减少不必要的比较次数。

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    int m = nums1.size(), n = nums2.size();
    int total = m + n;
    if (total % 2 == 1) { // 奇数长度
        int k = total / 2;
        int i = 0, j = 0;
        while (k--) {
            if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                i++;
            } else {
                j++;
            }
        }
        return min(nums1[i], nums2[j]);
    } else { // 偶数长度
        int k1 = total / 2 - 1, k2 = total / 2;
        int i = 0, j = 0;
        int a = 0, b = 0;
        while (k1--) {
            if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                a = nums1[i];
                i++;
            } else {
                a = nums2[j];
                j++;
            }
        }
        if (i < m && (j >= n || nums1[i] <= nums2[j])) {
            b = nums1[i];
        } else {
            b = nums2[j];
        }
        return (a + b) / 2.0;
    }
}

int main() {
    int m, n;
    cin >> m >> n;
    vector<int> nums1(m), nums2(n);
    for (int i = 0; i < m; i++) cin >> nums1[i];
    for (int i = 0; i < n; i++) cin >> nums2[i];
    printf("%.1f\n", findMedianSortedArrays(nums1, nums2));
    return 0;
}
```

```python
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
```

```java
import java.util.*;

public class Main {
    public static double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int m = nums1.length, n = nums2.length;
        int total = m + n;
        if (total % 2 == 1) {
            int k = total / 2;
            int i = 0, j = 0;
            while (k-- > 0) {
                if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                    i++;
                } else {
                    j++;
                }
            }
            return Math.min(nums1[i], nums2[j]);
        } else {
            int k1 = total / 2 - 1, k2 = total / 2;
            int i = 0, j = 0;
            int a = 0, b = 0;
            while (k1-- > 0) {
                if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                    a = nums1[i];
                    i++;
                } else {
                    a = nums2[j];
                    j++;
                }
            }
            if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                b = nums1[i];
            } else {
                b = nums2[j];
            }
            return (a + b) / 2.0;
        }
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int m = scanner.nextInt();
        int n = scanner.nextInt();
        int[] nums1 = new int[m];
        int[] nums2 = new int[n];
        for (int i = 0; i < m; i++) nums1[i] = scanner.nextInt();
        for (int i = 0; i < n; i++) nums2[i] = scanner.nextInt();
        System.out.printf("%.1f\n", findMedianSortedArrays(nums1, nums2));
    }
}
```

## 相关知识点
- 算法设计与分析
- 时间复杂度优化
- 数据结构应用

## 扩展思考
1. 是否存在更优的算法？
2. 在不同数据规模下的表现如何？
3. 相关的变形题目有哪些？

---
*生成时间: 2025-10-05 22:24:11*
