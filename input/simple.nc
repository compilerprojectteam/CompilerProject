int count;
int result[50];


int f(int a, int result[]) {
    count = count + 1;
    output(a);

    if(result[a - 1]){
        return result[a - 1];
    } else {
        if (a == 1) {
            result[a - 1] = 1;
            return 1;
        } else if (a == 2){
            result[a - 1] = 1;
            return 1;
        } else {
            result[a - 1] = f(a - 2, result) + f(a - 1, result);
            return result[a - 1];
        }
    }
}

void main() {
    int i;
    i = 0;
    while (i < 50) {
        //output(i);
        result[i] = 0;
        output(result[0]);
        i = i + 1;
    }
    output(10000);
    output(result[2]);
    count = 0;
    output(f(1, result));
    output(count);
}