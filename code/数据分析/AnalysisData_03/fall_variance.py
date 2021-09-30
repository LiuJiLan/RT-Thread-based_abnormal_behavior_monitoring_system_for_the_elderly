import matplotlib.pyplot as plt
import numpy as np

WINDOWS_SIZE = 400

def falldetection(a_vec):
    # 注意这里暂时没有更改
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

    return tmin, tmax

def fall_decisionsignal(a_vec):
    # 根据 fall_pure_diff.py 中 fall_decisionsignal2() 改写
    l1 = len(a_vec)
    windowSize = WINDOWS_SIZE
    fall_decisionsignal = np.zeros(l1)
    for w in range(0, l1 - windowSize):
        tmin, tmax = falldetection(a_vec[w: w + windowSize])
        if tmin != tmax:
            fall_decisionsignal[tmin + w: tmax + w] = 1

    return fall_decisionsignal