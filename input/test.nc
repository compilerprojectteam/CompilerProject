int a[10];

int f(int a) {
    if (a == 1) {
        return 1;
    } else {
//        return f(a - 1) * a;
        return a * f(a - 1);
    }
}

void main(void) {
    output(f(4));
}
