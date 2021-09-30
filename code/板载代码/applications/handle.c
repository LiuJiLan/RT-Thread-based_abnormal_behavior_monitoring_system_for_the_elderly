//
//  handle.c
//  deal_with_serial_data
//
//  Created by ������ on 2021/9/8.
//

#include "handle.h"
#include "fall.h"
#include <math.h>

#define MAX_DATA_LENGTH 12
#define MAX_DATA_NUM    (MAX_DATA_LENGTH / 2)
// ��ʵ��������������������raw data��һ��

static int check_index; // Use to index not real data things (0 - 4)
static int data_index;  // Use to index the data
//  static char data_head[2];   // Maybe No Need to Store the Head
static unsigned char id_length[2];
static unsigned char data_field[MAX_DATA_LENGTH];
static unsigned char check_sum;

/*
 *  �ڿ����Ƿ񽫵ó�������Ҳ��Ϊstatic����,
 *  ����ͷ�ɢ����ʱ�俼��,
 *  ÿ�õ��㹻�����ݾͼ�ʱ������Է�ֹ���ּ��д������ݲ�����Big Lag.
 *
 *  ���˴����ǻ��Ǽ��д���, ������,
 *  ����Big Lag��ʧ������Ҳ����ʱ�����Ƕ�����
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
                // ���ݲ���ȡ���, ����ֻ�õ���, ���������ౣ��
                check_sum = input;

                unsigned char sum = 0;  // check the sum
                for (int i = 0; i < raw_data_length; i++) {
                    sum += data_field[i];
                }
                sum += 0x55 + 0x55 + id_length[0] +id_length[1];

                if (sum == check_sum) { // У�����ȷ
                    // func to deal with data
                    deal_with_data();
                }

                init_static_data(); // ���������һ��ѭ��
            } else { // ��û�ж�������
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
    // ����û�й������int������, ��ʱ����

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
