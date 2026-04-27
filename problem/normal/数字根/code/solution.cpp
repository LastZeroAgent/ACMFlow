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