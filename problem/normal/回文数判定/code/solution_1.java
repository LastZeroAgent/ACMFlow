import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        String s = scanner.next();
        System.out.println(new StringBuilder(s).reverse().equals(s) ? "YES" : "NO");
    }
}