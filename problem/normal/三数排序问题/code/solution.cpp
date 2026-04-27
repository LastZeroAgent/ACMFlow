#include <iostream>
#include <algorithm>
using namespace std;

int main() {
    int nums[3];
    cin >> nums[0] >> nums[1] >> nums[2];
    sort(nums, nums + 3);
    cout << nums[0] << " " << nums[1] << " " << nums[2] << endl;
    return 0;
}