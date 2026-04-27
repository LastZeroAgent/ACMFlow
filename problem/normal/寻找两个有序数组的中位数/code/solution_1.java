import java.util.*;

public class Main {
    public static double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int m = nums1.length, n = nums2.length;
        int total = m + n;
        if (total % 2 == 1) {
            int k = total / 2;
            int i = 0, j = 0;
            while (k-- > 0) {
                if (i < m && (j >= n || nums1[i] <= nums2[j])) {
                    i++;
                } else {
                    j++;
                }
            }
            return Math.min(nums1[i], nums2[j]);
        } else {
            int k1 = total / 2 - 1, k2 = total / 2;
            int i = 0, j = 0;
            int a = 0, b = 0;
            while (k1-- > 0) {
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

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int m = scanner.nextInt();
        int n = scanner.nextInt();
        int[] nums1 = new int[m];
        int[] nums2 = new int[n];
        for (int i = 0; i < m; i++) nums1[i] = scanner.nextInt();
        for (int i = 0; i < n; i++) nums2[i] = scanner.nextInt();
        System.out.printf("%.1f\n", findMedianSortedArrays(nums1, nums2));
    }
}