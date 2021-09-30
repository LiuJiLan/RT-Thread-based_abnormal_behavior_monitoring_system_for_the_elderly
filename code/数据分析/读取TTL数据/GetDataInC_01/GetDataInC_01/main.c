//
//  main.c
//  GetDataInC_01
//
//  Created by 刘冬辰 on 2021/9/5.
//

#include <stdio.h>

float zitai(int L, int H) {   
    return  (float) ( (int16_t) (H<<8) | L ) / 32768 * 180;
}

float jiasudu(int L, int H, int scale) {
    return (float) ((int16_t) (H<<8) | L) / 32768 * scale;
}

float tuoluoyi(int L, int H, int scale) {
    return (float) ((int16_t) (H<<8) | L) / 32768 * scale;
}

int main(int argc, const char * argv[]) {
    
    printf("%lu\t%lu\n", sizeof(int), sizeof(int16_t));
    
    int RollL = 0xAA;
    int RollH = 0xDA;
    int PitchL = 0xB0;
    int PitchH = 0x03;
    int YawL = 0xD5;
    int YawH = 0x3E;
    
    int AxL = 0xA2;
    int AxH = 0xFF;
    int AyL = 0x4C;
    int AyH = 0x00;
    int AzL = 0xA2;
    int AzH = 0x1F;
    
    int GxL = 0xFD;
    int GxH = 0xFF;
    int GyL = 0x02;
    int GyH = 0x00;
    int GzL = 0xFF;
    int GzH = 0xFF;
    


                      
    printf("X:%f\tY:%f\tZ:%f\n",zitai(RollL, RollH), zitai(PitchL, PitchH), zitai(YawL, YawH));
    
    printf("X:%f\tY:%f\tZ:%f\n",jiasudu(AxL, AxH, 4), jiasudu(AyL, AyH, 4), jiasudu(AzL, AzH, 4));
    return 0;
}
