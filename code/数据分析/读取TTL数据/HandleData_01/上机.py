import math
import struct
import utime

from fpioa_manager import fm
from machine import UART
from board import board_info
from fpioa_manager import fm
from Maix import GPIO

def time_tag():
    time_tuple = utime.localtime()
    # print("{:0>2d}-{:0>2d}-{:0>2d}".format(time_tuple[3], time_tuple[4], time_tuple[5]))
    # file_data.write("{:0>2d}:{:0>2d}\t".format(time_tuple[4], time_tuple[5]))
    # file_rawdata.write(struct.pack("b", time_tuple[4]))
    # file_rawdata.write(struct.pack("b", time_tuple[5]))

def get_int(shortL, shortH):
    extend_num = 0
    if len(bin(struct.unpack("B", shortH)[0])) == 10:
        extend_num = 255
    return struct.unpack("i", shortL + shortH + struct.pack("B", extend_num) + struct.pack("B", extend_num))[0]

def init_file():
    temp_file = open("temp.txt", "r+")
    count = int(temp_file.read())
    temp_file.close()
    count += 1
    str_count = str(count)
    temp_file = open("temp.txt", "w")
    temp_file.write(str_count)
    temp_file.close()
    file_data = open("file_data" + str_count + ".txt", "w")
    file_rawdata = open("file_rawdata" + str_count + ".bin", "wb")
    return [file_data, file_rawdata]

# maixduino board_info PIN10/PIN11/PIN12/PIN13 or other hardware IO 10/11/4/3
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(11, fm.fpioa.UART1_RX, force=True)

fm.register(9, fm.fpioa.GPIO0)

uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)
buzz=GPIO(GPIO.GPIO0, GPIO.OUT)

TRASH_BIN = None
file_list = init_file()
file_data = file_list[0]
file_rawdata = file_list[1]


ANGLE_LIST = []
ACC_LIST = []

TEST_TIMES = int(input("Entry times:"))


buzz.value(1)
utime.sleep(1)
buzz.value(0)

file_data.write(str(utime.localtime()))

for i in range(TEST_TIMES):
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
            time_tag()
            # file_data.write("Ang:\t" + str(Angle_i) + "\n")
            # file_rawdata.write(struct.pack("b", 1))
            # file_rawdata.write(struct.pack("f", Angle_i))
            ANGLE_LIST.append(Angle_i)


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
            time_tag()
            # file_data.write("SVM:\t" + str(SVMi) + "\n")
            # file_rawdata.write(struct.pack("b", 3))
            # file_rawdata.write(struct.pack("f", SVMi))
            ACC_LIST.append(SVMi)

file_data.write(str(utime.localtime()))

buzz.value(1)
utime.sleep(1)
buzz.value(0)

file_data.write("Angle:\n")
for item in ANGLE_LIST:
    file_data.write(str(item))
    file_data.write("\n")
file_data.write("Acc:\n")
for item in ACC_LIST:
    file_data.write(str(item))
    file_data.write("\n")

file_data.write(str(utime.localtime()))

file_data.close()
file_rawdata.close()

file_data.write(str(utime.localtime()))

buzz.value(1)
utime.sleep(1)
buzz.value(0)

# 缓存大小大概500, 600就不够了


# uart_A.deinit()
# del uart_A
