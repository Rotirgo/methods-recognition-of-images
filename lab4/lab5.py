import copy

import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imsave, imshow, show, imread

M1 = [0, 0]
M2 = [1, 1]
M3 = [-1, 1]
M4 = [0, 1]
M5 = [0, 2]


B1 = [[0.035, 0.0], [0.0, 0.018]]
B2 = [[0.015, 0.0], [0.0, 0.03]]
B3 = [[0.02, 0.0], [0.0, 0.035]]
B4 = [[0.03, 0.0], [0.0, 0.03]]
B5 = [[0.035, 0.0], [0.0, 0.025]]
# B1 = [[0.05, 0.0], [0.0, 0.02]]
# B2 = [[0.04, 0.01], [0.01, 0.05]]
# B3 = [[0.02, 0.005], [0.005, 0.05]]
# B4 = [[0.03, -0.01], [0.01, 0.03]]
# B5 = [[0.04, 0.0], [0.0, 0.04]]

N = 50
n = 2


def generate_vectors(A, M, n, N):
    left_border = 0
    right_border = 1
    m = (right_border + left_border) / 2
    k = 20
    Sn = np.zeros((n, N))
    for i in range(0, k, 1):
        Sn += np.random.uniform(left_border, right_border, (n, N)) - m
    # Sn = s1 + s2 + ... + sn - m-m-m-m-m -> (s1-m) + (s2-m) + ... + (sn-m)
    CKO = (right_border - left_border) / np.sqrt(12)
    # CKO = sqrt(D)  D = (b-a)^2/12
    E = Sn / (CKO * np.sqrt(k))
    x = np.matmul(A, E) + np.reshape(M, (2, 1)) * np.ones((1, N))
    return x


def calcMatrixA(B):
    A = np.zeros((2, 2))
    A[0][0] = np.sqrt(B[0][0])
    A[0][1] = 0
    A[1][0] = B[0][1] / np.sqrt(B[0][0])
    A[1][1] = np.sqrt(B[1][1] - (B[0][1] ** 2) / B[0][0])
    return A


def d(x, z):
    dist = np.sum(np.square(x-z))
    return np.sqrt(dist)


Distance = np.vectorize(d, signature='(n),(m)->()')


def maxminMethod(vectors):
    result = copy.copy(vectors)
    clusters = []
    arrM = []
    M_all = vectors.sum(axis=1) / len(vectors[0])
    result = np.transpose(result)

    distances = Distance(result, M_all)
    m0 = result[np.argmax(distances)]
    clusters.append([m0])
    arrM.append(m0)
    result = np.delete(result, np.argmax(distances), axis=0)

    distances = Distance(result, m0)
    m1 = result[np.argmax(distances)]
    arrM.append(m1)
    clusters.append([m1])
    result = np.delete(result, np.argmax(distances), axis=0)

    dtypical = [Distance(m0, m1) / 2]
    dmin = [dtypical[-1] + 1]
    legends = ["M(x)", "class 0", "class 1"]

    # distanceTable
    #             x(0)          x(1)        ...       x(i)        ...       x(N-1)
    # M(0)      d(M0,x0)     d(M0, x1)      ...     d(M0, xi)     ...    d(M0, x(N-1))
    # M(1)      d(M1,x0)     d(M1, x1)      ...     d(M1, xi)     ...    d(M1, x(N-1))
    # ...         ...           ...         ...       ...         ...        ...
    # M(i)      d(Mi,x0)     d(Mi, x1)      ...     d(Mi, xi)     ...    d(Mi, x(N-1))
    # ...         ...           ...         ...       ...         ...        ...
    # M(L-2)  d(M(L-2),x0)  d(M(L-2), x1)   ...   d(M(L-2), xi)   ...   d(M(L-2), x(N-1))
    while dmin[-1] > dtypical[-1]:
        distanceTable = []
        for i in range(0, len(arrM)):
            distanceTable.append(Distance(result, arrM[i]))
        # распределить по существующим кластерам
        l = np.argmin(np.transpose(distanceTable), axis=1)
        tmp = copy.copy(clusters)
        for k in range(0, len(result)):
            tmp[l[k]].append(result[k])

        # отобразить результат
        # arrFig.append(viewClusters(tmp, arrM))
        fig0 = plt.figure(figsize=(10, 10))
        viewClusters(tmp, arrM, fig0, 111, legend=legends)
        # show()

        # создание нового кластера(если надо)
        minDistances = np.min(np.transpose(distanceTable), axis=1)
        M_ = result[np.argmax(minDistances)]
        dmin.append(np.min(Distance(arrM, M_)))
        if dmin[-1] > dtypical[-1]:
            legends.append(f"class {len(arrM)}")
            arrM.append(M_)
            clusters.append([M_])
            result = np.delete(result, np.argmax(minDistances), axis=0)
            dtypical.append(0)
            for j in range(0, len(arrM)):
                # print(f"\t{j}: {Distance(arrM, arrM[j])}")
                dtypical[-1] += np.sum(Distance(arrM, arrM[j]))
            dtypical[-1] /= 2*len(arrM)*(len(arrM) - 1)
    dmin.pop(0)
    return clusters, dmin, dtypical, arrM


def viewClusters(data, arrM, fig, loc, legend):
    viewData = []
    for k in range(0, len(data)):
        viewData.append(np.transpose(data[k]))
    tmp = np.transpose(arrM)

    fig.add_subplot(loc)
    plt.xlim(-1.6, 1.6)
    plt.ylim(-0.6, 2.6)
    plt.plot(tmp[0], tmp[1], 'ko')
    c = ['r.', 'b.', 'g.', 'c.', 'm.', 'y.']
    for i in range(0, len(viewData)):
        plt.plot(viewData[i][0], viewData[i][1], c[i % len(c)])
    plt.legend(legend)
    return fig

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

    A1 = calcMatrixA(B1)
    A2 = calcMatrixA(B2)
    A3 = calcMatrixA(B3)
    A4 = calcMatrixA(B4)
    A5 = calcMatrixA(B5)

    x1 = generate_vectors(A1, M1, n, N)
    x2 = generate_vectors(A2, M2, n, N)
    x3 = generate_vectors(A3, M3, n, N)
    x4 = generate_vectors(A4, M4, n, N)
    x5 = generate_vectors(A5, M5, n, N)

    data = np.concatenate((x1, x2, x3, x4, x5), axis=1)
    clusters, d_min, d_typical, arrM = maxminMethod(data)
    print(d_min)
    print(d_typical)

    fig1 = plt.figure(figsize=(16, 7))
    fig1.add_subplot(121)
    plt.xlim(-1.6, 1.6)
    plt.ylim(-0.6, 2.6)
    plt.plot(x1[0], x1[1], 'r.')
    plt.plot(x2[0], x2[1], 'gx')
    plt.plot(x3[0], x3[1], 'b<')
    plt.plot(x4[0], x4[1], 'm*')
    plt.plot(x5[0], x5[1], 'c+')
    plt.legend(["class 1", "class 2", "class 3", "class 4", "class 5"])
    legs = ["M(x)"]
    for i in range(0, len(clusters)):
        legs.append(f"class {i}")
    viewClusters(clusters, arrM, fig1, 122, legs)
    # imshow(views[-1])

    show()


