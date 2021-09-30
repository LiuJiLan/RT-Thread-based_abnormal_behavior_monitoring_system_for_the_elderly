//
//  main.c
//  deal_with_serial_data
//
//  Created by 刘冬辰 on 2021/9/8.
//

//
// On ART-Pi
//

#include <stdio.h>

int main(int argc, const char * argv[]) {
    unsigned char test[11] = {0x55, 0x55, 0x01, 0x06, 0x65, 0x00, 0x84, 0x00, 0xC1, 0xC5, 0x20};
    unsigned char sum = 0;
    for (int i = 0; i < 10; i++) {
        sum += test[i];
    }
    
    int int_num = (0x55 << 8) | 0x55;
    int char_num = (test[0] << 8) | test[1];
    
    long test_t = 10;
    printf("%ld\n", test_t);
    
    if (int_num == char_num) {
        printf("OK\n");
    } else {
        printf("FUCK\n");
    }
    printf("Hello, World!\n");
    return 0;
}
