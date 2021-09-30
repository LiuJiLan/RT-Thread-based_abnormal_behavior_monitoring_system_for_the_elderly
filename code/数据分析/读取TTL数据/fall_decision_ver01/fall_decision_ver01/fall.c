//
//  fall.c
//  fall_decision_ver01
//
//  Created by 刘冬辰 on 2021/9/15.
//

#include "fall.h"


#define WINDOW_SIZE 35

static float a_vec[WINDOW_SIZE];
static int a_vec_index;
static int tmax, tmin;

void falldetection(void);
void fall_decisionsignal(float acc);

void falldetection(void) {
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
        tmin = 0;
        tmax = 0;
    }
}

void fall_decisionsignal(float acc) {
    if (a_vec_index < WINDOW_SIZE) {
        a_vec[a_vec_index] = acc;
        a_vec_index++;
        return;
    }
    
    for (int i = 0; i < WINDOW_SIZE - 1; i++) {
        a_vec[i] = a_vec[i + 1];
    }
    a_vec[WINDOW_SIZE - 1] = acc;
    falldetection();
    
    if (tmin != tmax) {
        // BUZZ!
    }
}

