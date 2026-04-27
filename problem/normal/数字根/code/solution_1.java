import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        long n = scanner.nextLong();
        System.out.println(digitalRoot(n));
    }

    private static int digitalRoot(long n) {
        if (n == 0) return 0;
        return (n % 9 == 0) ? 9 : (int)(n % 9);
    }
}