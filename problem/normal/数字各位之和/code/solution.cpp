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