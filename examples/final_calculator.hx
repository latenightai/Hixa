// Final Working Calculator in Hixa Language

kam add_kora(a, b) {
    ghurai_diya (a + b);
}

kam subtract_kora(a, b) {
    ghurai_diya (a - b);
}

kam multiply_kora(a, b) {
    ghurai_diya (a * b);
}

kam divide_kora(a, b) {
    jodi (b == 0) {
        print_kora("Error: Division by zero!");
        ghurai_diya 0;
    }
    ghurai_diya (a / b);
}

print_kora("=== Hixa Calculator ===");
print_kora("Testing with numbers 10 and 3:");

print_kora("Addition: 10 + 3 = ");
dhora sum = add_kora(10, 3);
print_kora(sum);

print_kora("Subtraction: 10 - 3 = ");
dhora diff = subtract_kora(10, 3);
print_kora(diff);

print_kora("Multiplication: 10 * 3 = ");
dhora product = multiply_kora(10, 3);
print_kora(product);

print_kora("Division: 10 / 3 = ");
dhora quotient = divide_kora(10, 3);
print_kora(quotient);

print_kora("Division by zero test: 10 / 0 = ");
dhora zero_result = divide_kora(10, 0);
print_kora(zero_result);

print_kora("=== Calculator Complete ===");