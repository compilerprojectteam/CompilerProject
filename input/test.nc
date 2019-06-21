int f(int a, int c) {
    int g(int b) {
        output(b);
        f(b - 1,5);
    }
    if (a == 1) {
        output(a);
        return 0;
    } else {
        g(a);
    }


}


void main(void) {
    f(10,4);
}