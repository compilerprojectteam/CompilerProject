int k[100];


int f(int a) {
    int g(int b) {
        output(b);
        return f(b - 1);
    }
    if (a == 1) {
        output(a);
        return 1;
    } else {
        return g(a);
    }
}

void h(int l){
    l * 5;
}

void main(void) {
    int j;
    int g[10];
    f(5);
    f(10);
    if(f(2)){
        j = 2;
    } else ;
}
