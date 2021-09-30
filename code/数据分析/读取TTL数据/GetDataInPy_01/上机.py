import utime
import math
import struct

from fpioa_manager import fm
from machine import UART
from board import board_info
from fpioa_manager import fm

def time_tab():
    time_tuple = utime.localtime()
    print("{:0>2d}-{:0>2d}-{:0>2d}".format(time_tuple[3], time_tuple[4], time_tuple[5]))

def get_int(shortL, shortH):
    extend_num = 0
    if len(bin(struct.unpack("B", shortH)[0])) == 10:
        extend_num = 255
    return struct.unpack("i", shortL + shortH + struct.pack("B", extend_num) + struct.pack("B", extend_num))[0]


# maixduino board_info PIN10/PIN11/PIN12/PIN13 or other hardware IO 10/11/4/3
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(11, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

TRASH_BIN = None

while True:
    read_data = uart_A.read(1)
    if read_data == b"\x55":
        if uart_A.read(1) != b"\x55":
            continue

        func_num = uart_A.read(1)

        if func_num == b"\x01":
            AngleData = []
            len_check = struct.unpack("B", uart_A.read(1))[0]
            for i in range(len_check):
                AngleData.append(uart_A.read(1))
            if len(AngleData) == len_check:
                TRASH_BIN = uart_A.read(1)  # 暂时忽略校验和
                Xa = get_int(AngleData[0], AngleData[1]) / 32768 * 180
                Ya = get_int(AngleData[2], AngleData[3]) / 32768 * 180
                Za = get_int(AngleData[4], AngleData[5]) / 32768 * 180
                # print("Angle:\tX: {0}, Y: {1}, Z: {2}".format(Xa, Ya, Za))

        elif func_num == b"\x03":
            AccScale = 4
            GyroScale = 2000

            AccelerationData = []
            len_check = struct.unpack("B", uart_A.read(1))[0]
            for i in range(len_check):
                AccelerationData.append(uart_A.read(1))
            if len(AccelerationData) == len_check:
                TRASH_BIN = uart_A.read(1)  # 暂时忽略校验和
                Xacc = get_int(AccelerationData[0], AccelerationData[1]) / 32768 * AccScale
                Yacc = get_int(AccelerationData[2], AccelerationData[3]) / 32768 * AccScale
                Zacc = get_int(AccelerationData[4], AccelerationData[5]) / 32768 * AccScale
                # print("Acc:\tX: {0}, Y: {1}, Z: {2}".format(Xacc, Yacc, Zacc))
                print("SVM = {0}".format(str(math.sqrt(Xacc * Xacc + Yacc * Yacc + Zacc * Zacc))))
                Xgyro = get_int(AccelerationData[6], AccelerationData[7]) / 32768 * GyroScale
                Ygyro = get_int(AccelerationData[8], AccelerationData[9]) / 32768 * GyroScale
                Zgyro = get_int(AccelerationData[10], AccelerationData[11]) / 32768 * GyroScale
                # print("Gyro:\tX: {0}, Y: {1}, Z: {2}".format(Xgyro, Ygyro, Zgyro))

uart_A.deinit()
del uart_A

# list index out of range的错误并非是因为AccelerationData或AngleData造成的
# 而是由于print造成的


