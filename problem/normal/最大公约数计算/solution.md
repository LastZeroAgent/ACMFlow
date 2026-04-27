# 最大公约数计算 - 题解

## 算法分析

## 解题提示
1. 推荐使用欧几里得算法（辗转相除法），该算法的时间复杂度为 O(log(min(a,b)))，能够高效处理大数。
2. 注意处理特殊情况：当其中一个数为另一个数的倍数时，直接返回较小的数。
3. 确保算法不会进入无限循环，每次迭代都要缩小问题规模。

## 解题思路
欧几里得算法的核心思想是：gcd(a, b) = gcd(b, a % b)，直到余数为0时，此时的除数即为最大公约数。具体步骤如下：
1. 如果 b == 0，返回 a。
2. 否则，递归计算 gcd(b, a % b)。
也可以使用迭代方式实现，避免递归深度过大导致的栈溢出。

```cpp
#include <iostream>
using namespace std;

int gcd(int a, int b) {
    while (b != 0) {
        int temp = b;
        b = a % b;
        a = temp;
    }
    return a;
}

int main() {
    int a, b;
    while (cin >> a >> b) {
        cout << gcd(a, b) << endl;
    }
    return 0;
}
```

```python
import sys

def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

for line in sys.stdin:
    a, b = map(int, line.split())
    print(gcd(a, b))
```

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        while (scanner.hasNextInt()) {
            int a = scanner.nextInt();
            int b = scanner.nextInt();
            System.out.println(gcd(a, b));
        }
    }
    
    private static int gcd(int a, int b) {
        while (b != 0) {
            int temp = b;
            b = a % b;
            a = temp;
        }
        return a;
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
*生成时间: 2025-10-05 22:31:08*
