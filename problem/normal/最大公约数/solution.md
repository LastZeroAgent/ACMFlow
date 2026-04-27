# 最大公约数 - 题解

## 算法分析

### 核心思想
采用欧几里得算法：`gcd(a, b) = gcd(b, a % b)`，直至余数为0时，此时的除数即为最大公约数。该算法通过不断缩小问题规模，最终在有限步内得到结果。

### 关键步骤
1. **预处理**：对输入的 `a` 和 `b` 取绝对值，消除负数影响。
2. **迭代计算**：重复用较小数去除较大数的余数，更新两数的值，直到余数为0。
3. **终止条件**：当余数为0时，当前的除数即为最大公约数。

### 边界情况处理
- 若其中一数为0，直接返回另一数的绝对值。
- 若两数均为0，题目已保证不会出现此情况。
- 负数输入通过取绝对值转化为正数处理。

```cpp
#include <iostream>
#include <cstdlib> // For abs function
using namespace std;

int gcd(int a, int b) {
    a = abs(a);
    b = abs(b);
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int a, b;
    cin >> a >> b;
    cout << gcd(a, b) << endl;
    return 0;
}
```

```python
import sys
import math

def gcd(a, b):
    a = abs(a)
    b = abs(b)
    while b != 0:
        a, b = b, a % b
    return a

if __name__ == "__main__":
    a, b = map(int, sys.stdin.readline().split())
    print(gcd(a, b))
```

```java
import java.util.Scanner;

public class Main {
    public static int gcd(int a, int b) {
        a = Math.abs(a);
        b = Math.abs(b);
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int a = scanner.nextInt();
        int b = scanner.nextInt();
        System.out.println(gcd(a, b));
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
*生成时间: 2025-10-05 22:28:27*
