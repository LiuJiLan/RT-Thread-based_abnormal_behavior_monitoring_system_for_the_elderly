import struct


# 这是一个示例 Python 脚本。

# 按 ⌃R 执行或将其替换为您的代码。
# 按 双击 ⇧ 在所有地方搜索类、文件、工具窗口、操作和设置。


def int16_t(num):
    raw_str = bin(num)
    if len(raw_str) <= 17:
        return num
    extend_str = "0b" + "1" * 17 + raw_str[-15: -1]  # Extend the sign
    print(struct.pack("I", int(extend_str, 0)))
    return struct.unpack("i", struct.pack("I", int(extend_str, 0)))[0]


"""
def int16_t(num):
    raw_str = bin(num)
    extend_str = raw_str
    # 16 Bits Cut
    
    if len(raw_str) > 17:
        if raw_str[-16] == "0":  # 16 Bit == 0, len Must Not Be 18
            extend_str = "0b" + raw_str[-15: -1]
        else:
            extend_str = "0b" + raw_str[-16] * 17 + raw_str[-15: -1]  # Extend the sign
            print(int(extend_str, 0), "\t", ~int(extend_str, 0))
            NOT_num = ~int(extend_str, 0)  # Negate Num
            real_num_str = bin(NOT_num + 1)
            extend_str = real_num_str
            if len(real_num_str) > 34:
                extend_str = "0b" + real_num_str[-32: -1]
            extend_str = "-" + extend_str
    
    return int(extend_str, 0)
"""

def zitai(L, H):
    # 65536 is pow(2, 16) equal to (unsigned_int16_t)
    # return float((int16_t(H << 8) | L) / 32768 * 180)
    extend_num = 0
    if len(bin(struct.unpack("B", H)[0])) == 10:
        extend_num = 255
    return struct.unpack("i", L + H + struct.pack("B", extend_num) + struct.pack("B", extend_num))[0] / 32768 * 180


def get_int(shortL, shortH):
    extend_num = 0
    if len(bin(struct.unpack("B", shortH)[0])) == 10:
        extend_num = 255
    return struct.unpack("i", shortL + shortH + struct.pack("B", extend_num) + struct.pack("B", extend_num))[0]


# 按间距中的绿色按钮以运行脚本。
if __name__ == '__main__':
    f = open("./text.txt", "rb")
    RollL = f.read(1)
    RollH = f.read(1)
    print(zitai(RollL, RollH))
    RollL = f.read(1)
    RollH = f.read(1)
    print(zitai(RollL, RollH))
    if struct.unpack("B", b"\01")[0] == 1:
        print("FUCK YOU")

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
