#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    int m = nums1.size(), n = nums2.size();
    int total = m + n;
    if (total % 2 == 1) { // 奇数长度
        int k = total / 2;
        int i = 0, j = 0;
        while (k--) {
            if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                i++;
            } else {
                j++;
            }
        }
        return min(nums1[i], nums2[j]);
    } else { // 偶数长度
        int k1 = total / 2 - 1, k2 = total / 2;
        int i = 0, j = 0;
        int a = 0, b = 0;
        while (k1--) {
            if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                a = nums1[i];
                i++;
            } else {
                a = nums2[j];
                j++;
            }
        }
        if (i < m && (j >= n || nums1[i] <= nums2[j])) {
            b = nums1[i];
        } else {
            b = nums2[j];
        }
        return (a + b) / 2.0;
    }
}

int main() {
    int m, n;
    cin >> m >> n;
    vector<int> nums1(m), nums2(n);
    for (int i = 0; i < m; i++) cin >> nums1[i];
    for (int i = 0; i < n; i++) cin >> nums2[i];
    printf("%.1f\n", findMedianSortedArrays(nums1, nums2));
    return 0;
}