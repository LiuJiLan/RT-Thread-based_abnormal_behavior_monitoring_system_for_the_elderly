# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。


import math
import serial

import fall_pure_diff
import analysis_in_same_fig

# device = "/dev/tty.usbmodem142103"
# device = "/dev/tty.usbmodem14203"
# device = "/dev/tty.usbmodem14403"
# device = "/dev/tty.usbmodem14114403"
device = "/dev/tty.usbmodem14114103"


angle_list = []
acc_list = []

raw_data_temp = []


def read_from_serial():
    ser = serial.Serial(device, 115200, timeout=5)
    ser.flushInput()  # 清空缓冲区

    is_true_data = False

    while True:
        byte_out = ser.readline()
        # 这样读出来的是b'......'
        # 需要再次解码
        str_out = str(byte_out, "ascii", "ignore")
        if str_out == "end\r\n":
            break
        if is_true_data:
            raw_data_temp.append(str_out)
        if (not is_true_data) and (str_out == "start\r\n"):
            is_true_data = True


def store_raw_data():
    raw_data_file = open("raw_data.txt", "w+")
    for item in raw_data_temp:
        raw_data_file.write(item)
    raw_data_file.close()
    raw_data_temp.clear()


def read_from_file_and_store():
    raw_data_file = open("raw_data.txt", "r")
    acc_file = open("acc_data.txt", "w+")
    angle_file = open("angle_data.txt", "w+")
    acc_tri_data = open("acc_tri_data.txt", "w+")
    first_acc_second = None
    first_angle_second = None
    acc_temp_dict = {}  # int to list
    angle_temp_dict = {}

    while True:
        str_line = raw_data_file.readline()
        if str_line == "":
            break
        data_list = str_line.split("\n")[0].split(",")
        if data_list[1] == "1":
            cur_sec = int(data_list[0])
            if first_angle_second is None:
                first_angle_second = cur_sec
            cur_sec -= first_angle_second
            if cur_sec not in angle_temp_dict:
                angle_temp_dict[cur_sec] = []
            x = float(data_list[2])
            y = float(data_list[3])
            z = float(data_list[4])
            angle_temp_dict[cur_sec].append(math.sqrt(x * x + y * y + z * z))
            pass
        elif data_list[1] == "3":
            cur_sec = int(data_list[0])
            if first_acc_second is None:
                first_acc_second = cur_sec
            cur_sec -= first_acc_second
            if cur_sec not in acc_temp_dict:
                acc_temp_dict[cur_sec] = []
            x = float(data_list[2])
            y = float(data_list[3])
            z = float(data_list[4])
            acc_temp_dict[cur_sec].append(math.sqrt(x * x + y * y + z * z))
            acc_tri_data.write(str(x) + "," + str(y) + "," + str(z) + "\n")
            pass

    for cp in angle_temp_dict.items():
        delta = 1 / len(cp[1])
        sec = cp[0]
        for i in range(len(cp[1])):
            now_sec = sec + i * delta
            angle_file.write(str(now_sec) + "," + str(cp[1][i]) + "\n")

    for cp in acc_temp_dict.items():
        delta = 1 / len(cp[1])
        sec = cp[0]
        for i in range(len(cp[1])):
            now_sec = sec + i * delta
            acc_file.write(str(now_sec) + "," + str(cp[1][i]) + "\n")

    raw_data_file.close()
    acc_file.close()
    angle_file.close()
    acc_tri_data.close()


def read_from_stm32():
    read_from_serial()
    store_raw_data()


def show_chart():
    graph_file = open("acc_data.txt", "r")
    # graph_file = open("angle_data.txt", "r")

    x_array = []
    y_array = []

    while True:
        str_line = graph_file.readline()
        if str_line == "":
            break
        temp_list = str_line.split(",")
        x_array.append(float(temp_list[0]))
        y_array.append(float(temp_list[1]))
    graph_file.close()

    # y_array = list(map(lambda x: x - 1, y_array))
    # zero_crossing_rate(y_array)

    import matplotlib.pyplot as plt
    import numpy as np

    xpoints = np.array(x_array)
    ypoints = np.array(y_array)

    yfall = fall_pure_diff.fall_decisionsignal2(ypoints)
    xfall = np.array(x_array[0: len(yfall)])

    """
    # 把大图分成几个小图
    num_fig = int(x_array[-1])
    fig_margin = int(len(x_array) / (num_fig + 1))
    begin, end = 0, 0
    for i in range(num_fig):
        begin, end = i * fig_margin, (i + 1) * fig_margin
        fig, axes = plt.subplots()
        axes.plot(xpoints[begin: end], ypoints[begin: end])
        axes.scatter(xfall[begin: end], yfall[begin: end], color = 'hotpink')
        axes.grid(True)
        # axes.axis([None, None, 0, 2])

    # 最后一个数组直接读到完
    begin, end = end, -1
    fig, axes = plt.subplots()
    axes.plot(xpoints[begin: end], ypoints[begin: end])
    axes.scatter(xfall[begin: end], yfall[begin: end], color='hotpink')
    axes.grid(True)
    # 每个小图的y轴会不一致
    """

    """
    fig, axes = plt.subplots()
    axes.plot(xpoints, ypoints)
    axes.scatter(xfall, yfall, color='hotpink')
    axes.grid(True)
    # axes.axis([None, None, 0, 2])
    # 拉长一下图片
    # fig.set_size_inches(w, h)
    # plt.gcf().set_size_inches()
    # plt.gcf().get_size_inches()
    # image_max_x = 2^16
    # 获取的是
    h = plt.gcf().get_size_inches()[1]
    w = len(xpoints) / plt.gcf().dpi
    plt.gcf().set_size_inches(w, h)
    """

    analysis_in_same_fig.analysis_variances(ypoints, xpoints)


    # plt.show()


def zero_crossing_rate(ls):
    # 见"过零率"wiki
    # 此处计算的实际是过零个数
    sum = 0
    for i in range(1, len(ls)):
        if ls[i - 1] * ls[i] < 0:
            sum += 1
    print("ZC:" + str(sum))

def write_to_serial():
    ser = serial.Serial(device, 115200, timeout=5)
    ser.flushInput()  # 清空缓冲区
    ser.write("AT+RESET\r\n".encode("ASCII"))
    ser.write("AT+ENTM\r\n".encode("ASCII"))


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # read_from_stm32()
    read_from_file_and_store()
    show_chart()
    pass

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
