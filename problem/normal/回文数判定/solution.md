# 回文数判定 - 题解

## 算法分析

本题的核心是比较数字的前后对应位是否完全一致。常见解法有两种：
1. **字符串转换法**：将数字转为字符串，通过双指针法比较首尾字符是否一致。时间复杂度 O(d)，其中 d 是数字的位数。
2. **数学运算法**：通过不断取余和整除操作重构逆置数，并与原数比较。该方法避免了类型转换，但实现稍复杂。

```cpp
#include <iostream>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    string s;
    cin >> s;
    string rev = s;
    reverse(rev.begin(), rev.end());
    cout << (s == rev ? "YES" : "NO") << endl;
    return 0;
}
```

```python
n = input().strip()
print("YES" if n == n[::-1] else "NO")
```

```java
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.next();
        System.out.println(new StringBuilder(s).reverse().equals(s) ? "YES" : "NO");
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
*生成时间: 2025-10-05 22:03:58*
