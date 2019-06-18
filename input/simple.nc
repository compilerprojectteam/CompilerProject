int count;
int result[20];


int f(int a, int result[]) {
    count = count + 1;
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
    result[0] = 0;
    result[1] = 0;
    result[2] = 0;
    result[3] = 0;
    result[4] = 0;
    result[5] = 0;
    result[6] = 0;
    result[7] = 0;
    result[8] = 0;
    result[9] = 0;
    result[10] = 0;
    result[11] = 0;
    result[12] = 0;
    result[13] = 0;
    result[14] = 0;
    result[15] = 0;
    result[16] = 0;
    result[17] = 0;
    result[18] = 0;
    result[19] = 0;

    count = 0;
    output(f(19, result));
    output(count);
}