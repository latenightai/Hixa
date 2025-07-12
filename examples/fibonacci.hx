kam fibonacci(n) {
    jodi (n <= 1) {
        ghurai_diya n;
    }
    ghurai_diya fibonacci(n - 1) + fibonacci(n - 2);
}

kam main() {
    print_kora("Fibonacci sequence:");
    dhora i = 0;
    jetialoike (i < 10); {
        dhora result = fibonacci(i);
        print_kora(result);
        i = i + 1;
    }
} 