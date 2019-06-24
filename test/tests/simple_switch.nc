void main(void) {
    int i;
    i = 0;
    output(123123);
    switch (7 * 2) {
        case 10: output(10);
        case 14: output(14);
        case 12: output(12);
        case 13: output(13); break;
        case 16: output(16);
        default: output(39);
    }
    i = 5;
    output(i);

    switch (i * 3) {
        case 10: output(10);
        case 14: output(14); break;
        default: output(165); output(5461); break;
//
    }
//
    output(11111111);


    switch (1 + 8) {
        case 2: output(4);
        case 9: {
            switch (5 * 4) {
                case 3: output(3);
                case 20: output(200);
                case 40: output(40); break;
                case 13: output(1300);
                default: output(5234);
            }

        }
        case 17: output(17);
        case 10: output(10); break;
        case 130: output(1245312);
        default: output(5000);

    }

    output(222222222);

        switch (1 + 8) {
        case 2: output(4);
        case 9: output(9);
        case 7: {
            switch (5 * 4) {
                case 3: output(3);
                case 20: output(200);
                case 40: output(40);
                case 13: output(1300);
                default: output(5234);
            }

        }
        case 17: output(17);
        case 10: output(10); break;
        case 130: output(1245312);
        default: output(5000);

    }



}