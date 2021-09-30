//
//  fall.c
//  fall_decision_ver01
//
//  Created by Αυ¶¬³½ on 2021/9/15.
//

#include "fall.h"

#include <rtdevice.h>
#include <rtconfig.h>
#include <rtthread.h>
#include "drv_common.h"

#define BUZZ_PIN GET_PIN(A, 8)

#define G_FORCE_TH 3.5
#define DIFF_TH 1.96 // 2 * 0.98
#define MAX_MIN_TH 2.5
#define STANDARD_DEVIATION_TH 0.75

#define WINDOW_SIZE 200

static float a_vec[WINDOW_SIZE];
static int a_vec_index;
static int tmax, tmin;
static float avg;

int falldetection(void);
void fall_decisionsignal(float acc);

int falldetection(void) {
    int res = 0;
    
    int flag = 0;
    float diff[WINDOW_SIZE - 1];
    tmax = 0;
    tmin = 0;

    for (int i = 0; i < WINDOW_SIZE - 1; i++) {
        diff[i] = a_vec[i + 1] - a_vec[i];
    }

    int l1 = WINDOW_SIZE - 1;
    int i = 0;
    while (i < l1 - 1 && flag != 2) {
        if (flag == 0 && diff[i] < 0 && diff[i + 1] > 0) {
            tmin = i + 1;
            flag += 1;
        }
        if (flag == 1 && diff[i] > 0 && diff[i + 1] < 0) {
            tmax = i + 1;
            flag += 1;
        }
        i++;
    }

    float minmax_attr = a_vec[tmax] - a_vec[tmin];

    if (tmax < tmin || minmax_attr < 2 * 0.98) {
        // nothing to do
    } else {
        res += 1;
    }
    
    float standard_deviation = 0;
    for (int i = 0; i < WINDOW_SIZE; i++) {
        standard_deviation += a_vec[i] - avg;
    }
    standard_deviation /= WINDOW_SIZE;
    if (standard_deviation > STANDARD_DEVIATION_TH) {
        res += 1
    }
    
    return res;
}

void fall_decisionsignal(float acc) {
    if (a_vec_index < WINDOW_SIZE) {
        a_vec[a_vec_index] = acc;
        a_vec_index++;
        return;
    }
    
    float max = a_vec[1];
    float min = a_vec[1];
    avg = 0;

    for (int i = 0; i < WINDOW_SIZE - 1; i++) {
        a_vec[i] = a_vec[i + 1];
        if (max < a_vec[i + 1]) {
            max = a_vec[i + 1];
        }
        if (min > a_vec[i + 1]) {
            min = a_vec[i + 1];
        }
        avg += a_vec[i + 1];
    }
    
    a_vec[WINDOW_SIZE - 1] = acc;
    avg += acc;
    avg /= WINDOW_SIZE;
    
    int res = 0;
    if (acc > G_FORCE_TH) {
        if (max - min > MAX_MIN_TH) {
            res += 1;
        }
        res += falldetection();
    }
    

    if (res >= 2) {
        rt_pin_mode(BUZZ_PIN, PIN_MODE_OUTPUT);
        rt_pin_write(BUZZ_PIN, PIN_LOW);
    }
}

