int k[100];


int f(int a) {
    int g(int b) {
        int a;
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
    j = 5;
    switch(j){
        case 5: output(2);
        case 4: output(1);
        case 3: {output(0); break;}
        default: output(8);
    }

}
