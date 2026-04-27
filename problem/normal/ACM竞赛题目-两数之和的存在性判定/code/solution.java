import java.util.*;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        int[] nums = new int[n];
        for (int i = 0; i < n; i++) {
            nums[i] = scanner.nextInt();
        }
        int k = scanner.nextInt();

        if (n < 2) {
            System.out.println("NO");
            return;
        }

        Set<Integer> seen = new HashSet<>();
        for (int num : nums) {
            int complement = k - num;
            if (seen.contains(complement)) {
                System.out.println("YES");
                return;
            }
            seen.add(num);
        }
        System.out.println("NO");
    }
}