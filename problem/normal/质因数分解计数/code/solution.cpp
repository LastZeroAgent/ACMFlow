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