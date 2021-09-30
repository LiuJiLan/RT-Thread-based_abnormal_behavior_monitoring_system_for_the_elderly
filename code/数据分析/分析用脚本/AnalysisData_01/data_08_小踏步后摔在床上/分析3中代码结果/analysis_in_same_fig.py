import math

import matplotlib.pyplot as plt
import numpy as np

WINDOWS_SIZE = 25


def max_and_min(ls):
    return max(ls), min(ls)


def average(array):
    array_sum = 0
    for item in array:
        array_sum += item
    return array_sum / len(array)


def analysis_data(data_ls):
    avg = average(data_ls)
    biao_zhun_cha = 0
    fang_cha = 0
    for item in data_ls:
        diff = abs(item - avg)
        biao_zhun_cha += diff
        fang_cha += diff * diff
    biao_zhun_cha = biao_zhun_cha / len(data_ls)
    fang_cha = math.sqrt(fang_cha) / len(data_ls)
    return avg, biao_zhun_cha, fang_cha


def analysis_variances(a_vec, x_labels):
    # 根据 fall_pure_diff.py 中 fall_decisionsignal2() 改写
    avg_ls = []
    biao_zhun_cha_ls = []
    fang_cha_ls = []
    x_axis = []
    l1 = len(a_vec)
    windowSize = WINDOWS_SIZE
    for w in range(0, l1 - windowSize):
        y_slide = a_vec[w: w + windowSize]
        # x_slide = x_labels[w: w + windowSize]
        """
        fig, axes = plt.subplots()
        avg, variances = analysis_data(y_slide)
        axes.plot(x_slide, variances)
        axes.plot(x_slide, np.linspace(avg, avg, len(x_slide)))
        # h = plt.gcf().get_size_inches()[1]
        # w = len(x_slide) / plt.gcf().dpi * 1
        # plt.gcf().set_size_inches(w, h)
        plt.show()
        """
        avg, bzc, fc = analysis_data(y_slide)
        avg_ls.append(avg)
        biao_zhun_cha_ls.append(bzc)
        fang_cha_ls.append(fc)
        # x_axis.append(x_labels[w])
        x_axis.append(x_labels[w + int(windowSize / 2)])
    np_avg = np.array(avg_ls)
    np_bzc = np.array(biao_zhun_cha_ls)
    np_fc = np.array(fang_cha_ls)
    np_x_axis = np.array(x_axis)

    plt.figure()
    plt.plot(np_x_axis, np_avg, label='avg')
    plt.plot(np_x_axis, np_bzc, label='bzc')
    plt.plot(np_x_axis, np_fc, label='fc')
    plt.plot(x_labels, a_vec, label='org')
    plt.grid(True)
    plt.legend()

    # h = plt.gcf().get_size_inches()[1]
    # w = len(x_labels) / plt.gcf().dpi
    # plt.gcf().set_size_inches(w, h)

    plt.show()

    print("org:")
    print(max_and_min(a_vec))
    print("avg:")
    print(max_and_min(avg_ls))
    print("bzc:")
    print(max_and_min(biao_zhun_cha_ls))
    print("fc:")
    print(max_and_min(fang_cha_ls))
