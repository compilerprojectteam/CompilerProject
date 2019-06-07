int a[10];

int f(){
    int b;
    int g(){
        int c;
        int h(int d){
            c = 2;
            b = d;
        }
        h(7);
        output(b);
        output(c);
        b = 10;
    }
    b = 5;
    output(b);
    g();
    output(b);
}

void main(void) {
    f();
}
