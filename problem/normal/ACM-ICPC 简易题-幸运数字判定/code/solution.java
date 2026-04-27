import java.util.Scanner;

public class LuckyNumber {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        int n = scanner.nextInt();
        scanner.nextLine(); // 消耗换行符
        for (int i = 0; i < n; i++) {
            String num = scanner.nextLine().trim();
            int sumOdd = 0, sumEven = 0;
            for (int j = 0; j < num.length(); j++) {
                char c = num.charAt(j);
                if (j % 2 == 0) { // 奇数位
                    sumOdd += c - '0';
                } else { // 偶数位
                    sumEven += c - '0';
                }
            }
            System.out.println(sumOdd == sumEven ? "YES" : "NO");
        }
    }
}