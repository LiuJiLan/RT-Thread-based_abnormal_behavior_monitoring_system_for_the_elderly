import matplotlib.pyplot as plt
import numpy as np

WINDOWS_SIZE = 400


def falldetection_other(a_vec):
    l1 = len(a_vec)
    flag = 0
    tmax = 1
    tmin = 1
    diff = a_vec - np.hstack(([0], a_vec[0:-1]))
    i = 1
    while i <= (l1 - 1) and flag != 2:
        if diff[i] < 0 and diff[i + 1] > 0 and flag == 0:
            tmin = np.argmin(a_vec[i:i + 1]) + i - 1
            flag += 1
        else:
            if diff[i] > 0 and diff[i + 1] < 0 and flag == 1:
                tmax = np.argmax(a_vec[i:i + 1]) + i - 1
                flag += 1
        i += 1

    minmax_attr = a_vec[tmax] - a_vec[tmin]

    if minmax_attr < 2 * 9.8 or tmax < tmin:
        tmin = 0
        tmax = 0

    return tmin, tmax


def falldetection(a_vec):
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


def posturerecog(a, a_vec):
    windowSize = WINDOWS_SIZE
    th = 10
    th1 = 2
    count = 0
    sigma = 0.5
    g1 = 9.8
    tmin = 0
    tmax = 0

    sig = a[:, 2]
    l1 = len(sig)
    decision_signal = np.zeros(l1)

    a_vec = a_vec - th
    zrc = np.zeros(l1)

    for w in range(0, l1 - windowSize + 1):
        for i in range(w + 2, w + windowSize + 1):
            if a_vec[i] < sigma and a_vec[i - 1] > sigma:
                count += 1
        zrc[1 + w: windowSize + w] = count
        count = 0

    for i in range(1, l1 + 1):
        if zrc[i] == 0:
            if abs(sig[i]) < 5:
                decision_signal[i] = 5  # sitting
            else:
                decision_signal[i] = 10  # standing
        else:
            if zrc[i] > th1:
                decision_signal[i] = 15  # walking
            else:
                decision_signal[i] = 0  # none

    a_vec = a_vec + th
    fall_decisionsignal = np.zeros(l1)

    for w in range(0, l1 - windowSize + 1):
        tmin, tmax = falldetection(a_vec[w+1: w+windowSize])
        if tmin != tmax:
            fall_decisionsignal[tmin+w: tmax+w] = 1

    a = np.array(decision_signal)
    b = np.array(fall_decisionsignal)

    plt.plot(a)
    plt.plot(b)

    # axes.axis([None, None, 0, 2])

    plt.show()


def fall_decisionsignal(a_vec):
    l1 = len(a_vec)
    windowSize = WINDOWS_SIZE
    fall_decisionsignal = np.zeros(l1)
    for w in range(0, l1 - windowSize):
        tmin, tmax = falldetection(a_vec[w: w + windowSize])
        if tmin != tmax:
            fall_decisionsignal[tmin + w: tmax + w] = 1

    ypoints = np.array(fall_decisionsignal)
    xpoints = np.arange(len(fall_decisionsignal))

    plt.scatter(xpoints, ypoints)
    plt.show()

def fall_decisionsignal2(a_vec):
    l1 = len(a_vec)
    windowSize = WINDOWS_SIZE
    fall_decisionsignal = np.zeros(l1)
    for w in range(0, l1 - windowSize):
        tmin, tmax = falldetection(a_vec[w: w + windowSize])
        if tmin != tmax:
            fall_decisionsignal[tmin + w: tmax + w] = 1

    return fall_decisionsignal