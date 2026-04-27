# 数字各位之和 - 题解

## 算法分析

## 解题提示
1. 注意处理负数的情况，需先取绝对值再计算
2. 单个数字直接返回该数字本身
3. 对于0的处理应返回0
4. 建议使用字符串转换或数学运算两种方法实现

## 解题思路
本题核心在于分解整数的各个位数并求和。主要有两种实现方式：
1. **数学方法**：通过反复取模(%)和整除(/)操作提取每位数字
2. **字符串转换法**：将数字转为字符串，遍历每个字符转为数字后求和

两种方法的时间复杂度均为O(d)，其中d是数字的位数。推荐使用字符串转换法，逻辑更简洁且不易出错。

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    long long n;
    cin >> n;
    n = abs(n); // 处理负数
    string s = to_string(n);
    int sum = 0;
    for (char c : s) {
        sum += c - '0';
    }
    cout << sum << endl;
    return 0;
}
```

```python
n = int(input())
n = abs(n)
print(sum(int(d) for d in str(n)))
```

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long n = Math.abs(scanner.nextLong());
        String s = Long.toString(n);
        int sum = 0;
        for (char c : s.toCharArray()) {
            sum += c - '0';
        }
        System.out.println(sum);
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
*生成时间: 2025-10-03 23:10:26*
