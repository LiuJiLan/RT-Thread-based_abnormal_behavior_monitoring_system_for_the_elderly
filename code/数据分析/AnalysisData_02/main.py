# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。


import math
import serial
import fall

device = "/dev/tty.usbmodem142103"
# device = "/dev/tty.usbmodem14203"

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
            acc_tri_data.write(str(x) + "," + str(x) + "," + str(x) + "\n")
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

    y_array = list(map(lambda x: x - 1, y_array))
    zero_crossing_rate(y_array)

    import matplotlib.pyplot as plt
    import numpy as np

    xpoints = np.array(x_array)
    ypoints = np.array(y_array)

    fig, axes = plt.subplots()
    axes.plot(xpoints, ypoints)
    axes.grid(True)
    # axes.axis([None, None, 0, 2])
    plt.show()


def fall_dec():
    tri_acc_file = open("acc_tri_data.txt", "r")
    svm_file = open("acc_data.txt", "r")

    a_svm = []
    a_tri = []

    while True:
        str_line = tri_acc_file.readline()
        if str_line == "":
            break
        temp_list = str_line.split(",")
        a_tri.append([float(temp_list[0]), float(temp_list[1]), float(temp_list[2])])

    while True:
        str_line = svm_file.readline()
        if str_line == "":
            break
        temp_list = str_line.split(",")
        a_svm.append(float(temp_list[1]))

    tri_acc_file.close()
    svm_file.close()

    import numpy as np

    np_a_tri = np.array(a_tri)
    np_a_svm = np.array(a_svm)

    # fall.posturerecog(a_tri, a_svm)
    fall.fall_decisionsignal(np_a_svm)


def zero_crossing_rate(ls):
    # 见"过零率"wiki
    # 此处计算的实际是过零个数
    sum = 0
    for i in range(1, len(ls)):
        if ls[i - 1] * ls[i] < 0:
            sum += 1
    print("ZC:" + str(sum))


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    # read_from_stm32()
    # read_from_file_and_store()
    # show_chart()
    fall_dec()
    pass

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
