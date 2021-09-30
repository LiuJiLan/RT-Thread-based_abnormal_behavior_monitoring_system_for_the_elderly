import math
import struct
from collections import deque

from fpioa_manager import fm
from machine import UART
from board import board_info
from fpioa_manager import fm


def get_int(shortL, shortH):
    extend_num = 0
    if len(bin(struct.unpack("B", shortH)[0])) == 10:
        extend_num = 255
    return struct.unpack("i", shortL + shortH + struct.pack("B", extend_num) + struct.pack("B", extend_num))[0]

def deal_with_que(que, sum, max, data):
    if len(que) < max:
        que.append(data)
        sum += data
    else:
        que.append(data)
        sum = sum + data - que.popleft()
    return sum

def cal_variance(que, avg):
    sum_d = 0
    for svmi in que:
        delta = svmi - avg
        sum_d += delta * delta
    return sum_d / len(que)


# maixduino board_info PIN10/PIN11/PIN12/PIN13 or other hardware IO 10/11/4/3
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(11, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

TRASH_BIN = None
CURRENT_DATA = [None, None, None, None]  # SVM, E(SVM), D(SVM), Angle
# angleQue = deque()
# angleSum = 0
accQue = deque([])
accSum = 0
max_length = 120000  # deque本身就可限定长度
min_length = 60000

while True:
    print(CURRENT_DATA)
    read_data = uart_A.read(1)
    if read_data == b"\x55":
        if uart_A.read(1) != b"\x55":
            continue

        func_num = uart_A.read(1)

        if func_num == b"\x01":
            AngleData = []
            for i in range(struct.unpack("B", uart_A.read(1))[0]):
                AngleData.append(uart_A.read(1))

            TRASH_BIN = uart_A.read(1)  # 暂时忽略校验和
            Xa = get_int(AngleData[0], AngleData[1]) / 32768 * 180
            Ya = get_int(AngleData[2], AngleData[3]) / 32768 * 180
            Za = get_int(AngleData[4], AngleData[5]) / 32768 * 180

            Angle_i = math.sqrt(Xa * Xa + Ya * Ya + Za * Za)
            CURRENT_DATA[-1] = Angle_i




        elif func_num == b"\x03":
            AccScale = 4
            GyroScale = 2000

            AccelerationData = []
            for i in range(struct.unpack("B", uart_A.read(1))[0]):
                AccelerationData.append(uart_A.read(1))
            TRASH_BIN = uart_A.read(1)  # 暂时忽略校验和

            Xacc = get_int(AccelerationData[0], AccelerationData[1]) / 32768 * AccScale
            Yacc = get_int(AccelerationData[2], AccelerationData[3]) / 32768 * AccScale
            Zacc = get_int(AccelerationData[4], AccelerationData[5]) / 32768 * AccScale
            Xgyro = get_int(AccelerationData[6], AccelerationData[7]) / 32768 * GyroScale
            Ygyro = get_int(AccelerationData[8], AccelerationData[9]) / 32768 * GyroScale
            Zgyro = get_int(AccelerationData[10], AccelerationData[11]) / 32768 * GyroScale

            SVMi = math.sqrt(Xacc * Xacc + Yacc * Yacc + Zacc * Zacc)
            E_SVMi = None
            D_SVMi = None
            accSum = deal_with_que(accQue, accSum, max_length, SVMi)
            if len(accQue) >= min_length:
                E_SVMi = accSum / len(accQue)
                D_SVMi = cal_variance(accQue, E_SVMi)
            CURRENT_DATA[0] = SVMi
            CURRENT_DATA[1] = E_SVMi
            CURRENT_DATA[2] = D_SVMi


uart_A.deinit()
del uart_A