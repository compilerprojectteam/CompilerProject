int a[10];

int h(int g[]){
    g[3] = (2);
}

int f(int g[]){
    g[5] = 4;
    h(g);
}

void main(void) {
    int b[10];
    f(b);
    output(b[5]);
    output(b[3]);
}
