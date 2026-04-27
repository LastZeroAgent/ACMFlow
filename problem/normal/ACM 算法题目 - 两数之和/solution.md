# ACM 算法题目 - 两数之和 - 题解

## 算法分析

## 解题提示
1. 数组长度范围：2 ≤ n ≤ 10^5
2. 数组元素范围：-10^9 ≤ nums[i] ≤ 10^9
3. 确保返回的索引是唯一的，且不考虑顺序（最终按升序输出）
4. 注意处理重复元素的情况，但保证有且仅有一组解

## 解题思路
本题可通过以下两种主要方法解决：

### 方法一：暴力枚举（不推荐）
- **思路**：双重循环遍历所有可能的元素对，检查它们的和是否等于目标值。
- **时间复杂度**：O(n²)，适用于小规模数据。
- **缺点**：对于大规模数据会超时。

### 方法二：哈希表优化（推荐）
- **思路**：遍历数组时，用哈希表记录已访问元素的值及其索引。对于当前元素 `x`，检查 `target - x` 是否在哈希表中。若存在，则找到解。
- **时间复杂度**：O(n)，只需一次遍历。
- **空间复杂度**：O(n)，用于存储哈希表。

---

```cpp
#include <iostream>
#include <unordered_map>
#include <vector>
using namespace std;

int main() {
    int n, target;
    cin >> n >> target;
    vector<int> nums(n);
    for (int i = 0; i < n; ++i) {
        cin >> nums[i];
    }
    unordered_map<int, int> hash;
    for (int i = 0; i < n; ++i) {
        int complement = target - nums[i];
        if (hash.find(complement) != hash.end()) {
            cout << hash[complement] << " " << i << endl;
            return 0;
        }
        hash[nums[i]] = i;
    }
    return 0;
}
```

```python
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
```

```java
import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int target = scanner.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = scanner.nextInt();
        }
        Map<Integer, Integer> map = new HashMap<>();
        for (int i = 0; i < n; i++) {
            int complement = target - nums[i];
            if (map.containsKey(complement)) {
                System.out.println(map.get(complement) + " " + i);
                return;
            }
            map.put(nums[i], i);
        }
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
*生成时间: 2025-10-05 21:41:12*
