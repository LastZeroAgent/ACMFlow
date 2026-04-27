# 三数排序问题 - 题解

## 算法分析

## 解题提示
1. 本题可通过多次两两比较实现排序，也可借助临时变量辅助交换。
2. 注意处理存在重复数字的情况。
3. 时间复杂度应控制在 O(1)，因输入规模固定为3个数。

## 解题思路
本题的核心是对三个数进行排序。由于输入规模固定为3，可采用以下策略：
1. **双轮比较法**：第一轮比较前两个数，若顺序错误则交换；第二轮比较后两个数，若顺序错误则交换；第三轮再次比较前两个数以确保整体有序。
2. **通用排序法**：将三个数存入数组，调用语言内置的排序函数直接排序。

```cpp
#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int nums[3];
    cin >> nums[0] >> nums[1] >> nums[2];
    sort(nums, nums + 3);
    cout << nums[0] << " " << nums[1] << " " << nums[2] << endl;
    return 0;
}
```

```python
# Python解决方案
a, b, c = map(int, input().split())
sorted_nums = sorted([a, b, c])
print(' '.join(map(str, sorted_nums)))
```

```java
import java.util.Arrays;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int[] nums = new int[3];
        nums[0] = scanner.nextInt();
        nums[1] = scanner.nextInt();
        nums[2] = scanner.nextInt();
        Arrays.sort(nums);
        System.out.println(nums[0] + " " + nums[1] + " " + nums[2]);
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
*生成时间: 2025-10-08 16:42:03*
