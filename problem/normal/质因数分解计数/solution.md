# 质因数分解计数 - 题解

## 算法分析

## 解题提示
1. 注意处理n本身是质数的情况，此时结果应为1。
2. 需去重统计质因数，即使某个质因数出现多次也只计一次。
3. 建议使用埃氏筛法预处理质数表以提高大数分解效率。

## 解题思路
本题核心在于对给定整数进行质因数分解并统计不同质因数的数量。基本思路如下：
1. 初始化一个空集合用于存储质因数。
2. 从最小的质数2开始尝试整除n，若能整除则将该质数加入集合，并持续除以该质数直至不能整除。
3. 逐步增大除数，重复上述过程直到n被分解为1。
4. 最终集合的大小即为所求的不同质因数个数。

该方法的时间复杂度主要取决于n的大小，最坏情况下为O(√n)。

```cpp
#include <iostream>
#include <unordered_set>
using namespace std;

int countDistinctPrimeFactors(int n) {
    unordered_set<int> factors;
    for (int i = 2; i * i <= n; ++i) {
        if (n % i == 0) {
            factors.insert(i);
            while (n % i == 0) {
                n /= i;
            }
        }
    }
    if (n > 1) { // 剩余的n是质数
        factors.insert(n);
    }
    return factors.size();
}

int main() {
    int n;
    while (cin >> n) {
        cout << countDistinctPrimeFactors(n) << endl;
    }
    return 0;
}
```

```python
def count_distinct_prime_factors(n):
    factors = set()
    i = 2
    while i * i <= n:
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
        i += 1
    if n > 1:
        factors.add(n)
    return len(factors)

if __name__ == "__main__":
    import sys
    for line in sys.stdin:
        n = int(line.strip())
        print(count_distinct_prime_factors(n))
```

```java
import java.util.HashSet;
import java.util.Scanner;
import java.util.Set;

public class PrimeFactorCounter {
    public static int countDistinctPrimeFactors(int n) {
        Set<Integer> factors = new HashSet<>();
        for (int i = 2; i * i <= n; i++) {
            if (n % i == 0) {
                factors.add(i);
                while (n % i == 0) {
                    n /= i;
                }
            }
        }
        if (n > 1) {
            factors.add(n);
        }
        return factors.size();
    }

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        while (scanner.hasNextInt()) {
            int n = scanner.nextInt();
            System.out.println(countDistinctPrimeFactors(n));
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
*生成时间: 2025-10-03 23:43:30*
