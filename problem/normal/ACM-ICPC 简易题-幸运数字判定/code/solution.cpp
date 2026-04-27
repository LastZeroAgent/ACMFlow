#include <iostream>
#include <string>
using namespace std;

int main() {
    int n;
    cin >> n;
    while (n--) {
        string num;
        cin >> num;
        int sum_odd = 0, sum_even = 0;
        for (size_t i = 0; i < num.size(); ++i) {
            if (i % 2 == 0) { // 奇数位（第1,3,...位）
                sum_odd += num[i] - '0';
            } else { // 偶数位（第2,4,...位）
                sum_even += num[i] - '0';
            }
        }
        cout << (sum_odd == sum_even ? "YES" : "NO") << endl;
    }
    return 0;
}