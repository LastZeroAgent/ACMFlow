# 数字根 - 题解

## 算法分析

## 解题提示
1. 注意处理 `n = 0` 的特殊情况。
2. 可通过数学性质优化：若 `n % 9 == 0` 且 `n != 0`，则数字根为 `9`；否则为 `n % 9`。
3. 避免直接模拟逐位相加导致的超时问题（尤其对极大数）。

## 解题思路
**方法一：数学性质（推荐）**
观察到数字根具有周期性规律：除 `0` 外，所有数的数字根等于其对 `9` 取模的结果，若余数为 `0` 则数字根为 `9`。此方法时间复杂度为 O(1)。

**方法二：模拟相加**
通过循环不断将当前数的各位相加，直至结果为一位数。适用于教学场景，但对极大数效率较低。

```cpp
#include <iostream>
using namespace std;

int digitalRoot(long long n) {
    if (n == 0) return 0;
    return (n % 9 == 0) ? 9 : n % 9;
}

int main() {
    long long n;
    cin >> n;
    cout << digitalRoot(n) << endl;
    return 0;
}
```

```python
def digital_root(n):
    if n == 0:
        return 0
    return 9 if n % 9 == 0 else n % 9

n = int(input())
print(digital_root(n))
```

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long n = scanner.nextLong();
        System.out.println(digitalRoot(n));
    }

    private static int digitalRoot(long n) {
        if (n == 0) return 0;
        return (n % 9 == 0) ? 9 : (int)(n % 9);
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
*生成时间: 2025-10-05 22:14:11*
