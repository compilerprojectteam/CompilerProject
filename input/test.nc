int f(int g, int h){
    output(g);
    output(h);
}

void main(void) {
    int g[8];
    g[0] = 2;
    g[1] = 5;
    f(g[0], g[1]);
}
