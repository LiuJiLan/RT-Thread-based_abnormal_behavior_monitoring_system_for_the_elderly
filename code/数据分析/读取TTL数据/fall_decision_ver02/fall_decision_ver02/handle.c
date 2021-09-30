//
//  handle.c
//  deal_with_serial_data
//
//  Created by 刘冬辰 on 2021/9/8.
//

#include "handle.h"
#include "fall.h"
#include <math.h>

#define MAX_DATA_LENGTH 12
#define MAX_DATA_NUM    (MAX_DATA_LENGTH / 2)
// 真实解析出来的数据数量是raw data的一半

static int check_index; // Use to index not real data things (0 - 4)
static int data_index;  // Use to index the data
//  static char data_head[2];   // Maybe No Need to Store the Head
static unsigned char id_length[2];
static unsigned char data_field[MAX_DATA_LENGTH];
static unsigned char check_sum;

/*
 *  在考虑是否将得出的数据也作为static变量,
 *  如果就分散计算时间考虑,
 *  每得到足够的数据就及时处理可以防止出现集中处理数据产生的Big Lag.
 *
 *  但此处考虑还是集中处理, 方便编程,
 *  由于Big Lag丢失的数据也就暂时把他们丢掉吧
 */

void init_static_data(void);
void handle_data(unsigned char);
void store_data(unsigned char);
float data_to_float(unsigned char, unsigned char);
void deal_with_data(void);

void init_static_data(void) {
    check_index = 0;
    data_index = 0;
    // Real data is no need to initialize.
    // Just using the cur_index to deal with.
    check_sum = 0;
}

void handle_data(unsigned char input) {
    int raw_data_length;    //  Only declare.

    switch (check_index) {
        case 0:
            if (input == 0x55) {
                check_index = 1;
            }
            return;

        case 1:
            if (input == 0x55) {
                check_index = 2;
            } else {
                check_index = 0;
            }
            return;

        case 2:
            id_length[0] = input;
            check_index = 3;
            return;

        case 3:
            id_length[1] = input;
            check_index = 4;
            return;

        case 4:
            raw_data_length = (int)id_length[1];
            if (data_index >= raw_data_length) {
                // 数据部读取完毕, 本身只用等于, 大于是冗余保护
                check_sum = input;

                unsigned char sum = 0;  // check the sum
                for (int i = 0; i < raw_data_length; i++) {
                    sum += data_field[i];
                }
                sum += 0x55 + 0x55 + id_length[0] +id_length[1];

                if (sum == check_sum) { // 校验合正确
                    // func to deal with data
                    deal_with_data();
                }

                init_static_data(); // 清除进入下一次循环
            } else { // 还没有读完数据
                // func to continue reading the data
                store_data(input);
            }
            return;

        default:
            return;
    }
}

void store_data(unsigned char input_data) {
    data_field[data_index] = input_data;
    data_index++;
}

float data_to_float(unsigned char data_L, unsigned char data_H) {
    return (float) ((bits_16_int) (data_H<<8) | data_L);
}

void deal_with_data(void) {
    int raw_data_length = (int)id_length[1];
    int real_data_length = raw_data_length / 2;
    float real_data_array[MAX_DATA_NUM] = {0};
    // 这里没有管最后是int的数据, 暂时忽略

    float acc_vec = 0;

    time_t data_sec;

    switch (id_length[0]) {
        case 0x01:
            for (int i = 0; i < real_data_length; i++) {
                real_data_array[i] = data_to_float(data_field[i * 2], data_field[i * 2 + 1]) / 32768 * 180;
            }

            data_sec = time((time_t *)NULL);
            printf("%d,1", data_sec);

            for (int i = 0; i < real_data_length; i++) {
                printf(",%f", real_data_array[i]);
            }
            printf("\n");
            return;

        case 0x03:
            acc_vec = 0;
            for (int i = 0; i < real_data_length / 2; i++) {
                real_data_array[i] = data_to_float(data_field[i * 2], data_field[i * 2 + 1]) / 32768 * 4;
                acc_vec += real_data_array[i];
            }

            acc_vec = sqrtf(acc_vec);
            // fall_decisionsignal(acc_vec);

            data_sec = time((time_t *)NULL);
            printf("%d,3", data_sec);

            for (int i = 0; i < real_data_length / 2; i++) {
                printf(",%f", real_data_array[i]);
            }
            printf("\n");



            /*
            for (int i = real_data_length / 2; i < real_data_length; i++) {
                real_data_array[i] = data_to_float(data_field[i * 2], data_field[i * 2 + 1]) / 32768 * 4;
            }

            printf("Gyro:\t");
            for (int i = real_data_length / 2; i < real_data_length; i++) {
                printf("%f\t", real_data_array[i]);
            }
            printf("\n");
            */

            return;

        default:
            return;
    }
}
