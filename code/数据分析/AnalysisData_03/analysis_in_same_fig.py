import math

import matplotlib.pyplot as plt
import numpy as np

WINDOWS_SIZE = 200
LONG_PIC = True


def diff_detect(a_vec):
    flag = 0
    tmax = 0
    tmin = 0
    diff = a_vec[1: -1] - a_vec[0: -2]
    l1 = len(diff)
    i = 0
    while i < (l1 - 1) and flag != 2:
        if diff[i] < 0 and diff[i + 1] > 0 and flag == 0:
            tmin = i + 1
            flag += 1
        if diff[i] > 0 and diff[i + 1] < 0 and flag == 1:
            tmax = i + 1
            flag += 1
        i += 1

    minmax_attr = a_vec[tmax] - a_vec[tmin]

    if minmax_attr < 2 * 0.98 or tmax < tmin:
        tmin = 0
        tmax = 0

    if tmin != tmax:
        return 1
    else:
        return 0


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
    fang_cha = math.sqrt(fang_cha / len(data_ls))
    max_min_diff = max(data_ls) - min(data_ls)

    judge = 0
    if data_ls[-1] > 3.5:
        if max_min_diff > 2.5:
            judge += 1
        if biao_zhun_cha > 0.75:
            judge += 1
        if diff_detect(data_ls) == 1:
            judge += 1

    if judge >= 2:
        judge = 1

    return avg, biao_zhun_cha, fang_cha, max_min_diff, judge


def analysis_variances(a_vec, x_labels):
    # 根据 fall_pure_diff.py 中 fall_decisionsignal2() 改写
    avg_ls = []
    biao_zhun_cha_ls = []
    fang_cha_ls = []
    max_min_ls = []
    diff_detect_ls = []
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
        avg, bzc, fc, max_min_df, diff = analysis_data(y_slide)
        avg_ls.append(avg)
        biao_zhun_cha_ls.append(bzc)
        fang_cha_ls.append(fc)
        max_min_ls.append(max_min_df)
        diff_detect_ls.append(diff)
        # x_axis.append(x_labels[w])
        x_axis.append(x_labels[w + int(windowSize / 2)])
    np_avg = np.array(avg_ls)
    np_bzc = np.array(biao_zhun_cha_ls)
    np_fc = np.array(fang_cha_ls)
    np_df = np.array(max_min_ls)
    np_diff = np.array(diff_detect_ls)
    np_x_axis = np.array(x_axis)

    plt.figure()
    plt.plot(np_x_axis, np_avg, label='Average')
    plt.plot(np_x_axis, np_bzc, label='Standard Deviation')
    # plt.plot(np_x_axis, np_fc, label='fc')
    plt.plot(np_x_axis, np_df, label='Max - Min')
    plt.scatter(np_x_axis, np_diff, label='Is Fallen?', color='hotpink')
    plt.plot(x_labels, a_vec, label='Original Data')
    plt.grid(True)
    plt.legend()

    if LONG_PIC:
        h = plt.gcf().get_size_inches()[1]
        w = len(x_labels) / plt.gcf().dpi
        plt.gcf().set_size_inches(w, h)

    plt.show()

    print("windows:")
    print(windowSize)
    print("org:")
    print(max_and_min(a_vec))
    print("avg:")
    print(max_and_min(avg_ls))
    print("bzc:")
    print(max_and_min(biao_zhun_cha_ls))
    print("fc:")
    print(max_and_min(fang_cha_ls))
