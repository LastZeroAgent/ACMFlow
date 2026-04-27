# 逆序对计数 - 题解

## 算法分析

## 解题提示
- 本题可以通过双重循环暴力枚举所有 i<j 的情况，判断是否构成逆序对。
- 注意数组长度较大时，暴力解法的时间复杂度为 O(n²)，可能会超时，但在本题的限制下仍可接受。
- 如果追求更高效率，可以使用归并排序的思想在 O(n log n) 时间内解决。

## 解题思路
### 方法一：暴力枚举（适用于小规模数据）
遍历数组中的每一对元素 (i, j)，其中 i < j。如果 nums[i] > nums[j]，则计数器加一。最终计数器的值即为答案。该方法直观易懂，但时间复杂度较高。

### 方法二：归并排序优化（推荐）
利用归并排序的过程，在合并两个有序子数组时，统计跨越左右子数组的逆序对数目。具体来说，当右侧元素小于左侧元素时，左侧剩余的所有元素都会与该右侧元素构成逆序对。这种方法的时间复杂度为 O(n log n)。

```cpp
#include <iostream>
#include <vector>
using namespace std;

int mergeAndCount(vector<int>& nums, int left, int mid, int right) {
    vector<int> temp(right - left + 1);
    int i = left, j = mid + 1, k = 0;
    int count = 0;
    while (i <= mid && j <= right) {
        if (nums[i] <= nums[j]) {
            temp[k++] = nums[i++];
        } else {
            count += mid - i + 1; // 关键：统计逆序对
            temp[k++] = nums[j++];
        }
    }
    while (i <= mid) temp[k++] = nums[i++];
    while (j <= right) temp[k++] = nums[j++];
    for (int p = 0; p < k; p++) {
        nums[left + p] = temp[p];
    }
    return count;
}

int mergeSort(vector<int>& nums, int left, int right) {
    if (left >= right) return 0;
    int mid = left + (right - left) / 2;
    int count = mergeSort(nums, left, mid) + mergeSort(nums, mid + 1, right);
    count += mergeAndCount(nums, left, mid, right);
    return count;
}

int main() {
    int n;
    cin >> n;
    vector<int> nums(n);
    for (int i = 0; i < n; i++) {
        cin >> nums[i];
    }
    cout << mergeSort(nums, 0, n - 1) << endl;
    return 0;
}
```

```python
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
```

```java
import java.util.*;

public class ReversePairs {
    private static int mergeAndCount(int[] nums, int left, int mid, int right) {
        int[] temp = new int[right - left + 1];
        int i = left, j = mid + 1, k = 0;
        int count = 0;
        while (i <= mid && j <= right) {
            if (nums[i] <= nums[j]) {
                temp[k++] = nums[i++];
            } else {
                count += mid - i + 1;
                temp[k++] = nums[j++];
            }
        }
        while (i <= mid) temp[k++] = nums[i++];
        while (j <= right) temp[k++] = nums[j++];
        System.arraycopy(temp, 0, nums, left, temp.length);
        return count;
    }

    private static int mergeSort(int[] nums, int left, int right) {
        if (left >= right) return 0;
        int mid = left + (right - left) / 2;
        int count = mergeSort(nums, left, mid) + mergeSort(nums, mid + 1, right);
        count += mergeAndCount(nums, left, mid, right);
        return count;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = scanner.nextInt();
        }
        System.out.println(mergeSort(nums, 0, n - 1));
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
*生成时间: 2025-10-05 22:02:25*
