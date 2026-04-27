import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long n = Math.abs(scanner.nextLong());
        String s = Long.toString(n);
        int sum = 0;
        for (char c : s.toCharArray()) {
            sum += c - '0';
        }
        System.out.println(sum);
    }
}