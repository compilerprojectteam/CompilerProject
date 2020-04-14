
int abs(int a) {
    if (a < 0) {
        return -a;
    } else {
        return a;
    }
}

int integerDivision(int a, int b) {
    int i;
    int step;
    int flag;
    if (b == 0) {
        return 123456789;
    } else {
        i = 1;
        flag = 0;
    }

    if (a < 0) {
        if (b < 0) {
            i = 1;
            a = a * -1;
            b = b * -1;
        } else {
            i = -1;
            a = a * -1;
            b = b * -1;
        }
    } else {
        if (b < 0) {
            i = -1;
        } else {
            i = 1;
        }
    }
    step = i;
    i = i - abs(i);

    while (abs(i) < abs(a) + 1) {
        if (i * b == a) {
            return i;
        } else {
            int f1;
            int f2;
            f1 = i * b < a;
            f2 = a < (i + step) * b;
            if (f1 == f2) {
                return i + (b == abs(b)) - 1;
            } else {
                i = i + step;
            }

        }
    }
    return 123456789;
}

void merge(int arr[], int l, int m, int r)
{
    int i;
    int j;
    int k;
    int n1;
    int n2;
    int L[100];
    int R[100];

    n1 = m - l + 1;
    n2 = r - m;

    i = 0;
    j = 0;
    while(i < n1){
        L[i] = arr[l + i];
        i = i + 1;
    }
    while(j < n2){
        R[j] = arr[m + 1 + j];
        j = j + 1;
    }
    i = 0;
    j = 0;
    k = l;

    while (1){
        if(n1 < i){ break; } else;
        if(n1 == i){ break; } else;
        if(n2 < j){ break; } else;
        if(n2 == j){ break; } else;


        if (R[j] < L[i]){
            arr[k] = R[j];
            j = j + 1;
        }else{
            arr[k] = L[i];
            i = i + 1;
        }
        k = k + 1;
    }

    while (i < n1)
    {
        arr[k] = L[i];
        i = i + 1;
        k = k + 1;
    }

    while (j < n2)
    {
        arr[k] = R[j];
        j = j + 1;
        k = k + 1;
    }
}

void mergeSort(int arr[], int l, int r)
{
    if (l < r){
        int m;
        m = l + integerDivision(r - l,2);
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    } else;
}

void printArray(int A[], int size)
{
    int i;
    i = 0;
    while(i < size){
        output(A[i]);
        i = i + 1;
    }
}

/* Driver program to test above functions */
void main(void)
{
    int arr[100];
    int arrsize;
    int i;
    arrsize = 100;


    i = 0;
    while(i < arrsize){
        arr[i] = (i - 10) * (i - 25) * (i - 50) * (i - 75);
        i = i + 1;
    }


    printArray(arr, arrsize);

    mergeSort(arr, 0, arrsize - 1);

    printArray(arr, arrsize);
}