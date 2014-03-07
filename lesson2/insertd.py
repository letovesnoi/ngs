import matplotlib
matplotlib.use('Agg')

__author__ = 'lenk'

from pylab import *

def cut(x, y, average, sigma):
    x1 = []
    y1 = []
    newCount = 0
    newAverage = 0
    newSigma = 0
    for i in range(len(x)):
        if y[i] != 0 and x[i] < average + 5 * sigma and x[i] > average - 5 * sigma:
            x1.append(x[i])
            y1.append(y[i])
            newAverage += x[i] * y[i]
            newCount += y[i]
    newAverage = newAverage * 1.0 / newCount
    for i in range(len(x1)):
        newSigma += (x1[i] - newAverage) ** 2 * y1[i]
    newSigma = math.sqrt(newSigma * 1.0 / newCount)
    #interval = []
    #interval.append(newAverage - 1.959964 * newSigma / sqrt(newCount - 1))
    #interval.append(newAverage + 1.959964 * newSigma / sqrt(newCount - 1))
    newBegin = int(newAverage - 2 * newSigma)
    newEnd = int(newAverage + 2 * newSigma)
    inewBegin = 0
    inewEnd = len(x1) - 1
    for i in range(len(x1)):
        if x1[i] <= newBegin:
            inewBegin = i
        if x1[i] >= newEnd:
            inewEnd = i
            break
    x1 = x1[inewBegin:inewEnd + 1]
    y1 = y1[inewBegin:inewEnd + 1]
    with open('outputIns.txt', 'w') as f:
        f.write('interval=[' + str(newBegin) + ';' + str(newEnd) + ']')
        f.write('\r\naverage=' + str(newAverage) + '\r\nsigma=' + str(newSigma))
        f.write('\r\nx=' + str(x1))
    f.close()
    return x1, y1, newAverage, newSigma

def distinsert():
    x = []
    y = []
    m = []
    count = 0
    average = 0
    with open('out_ecoli_mda_lane1.sam', 'r') as f:
        f.readline()
        a, b, c = f.readline().split()
        L = c[3:]
        L = int(L)
        f.readline()
        for i in range(L + 1):
            m.append(0)
        while True:
            inputLine1 = []
            inputLine2 = []
            inputLine1.extend(f.readline().split('\t'))
            if inputLine1[0] == '':
                break
            inputLine2.extend(f.readline().split('\t'))

            m[max(int(inputLine1[3]), int(inputLine2[3])) + len(inputLine1[9]) -
              min(int(inputLine1[3]), int(inputLine2[3]))] += int(1)
            average += max(int(inputLine1[3]), int(inputLine2[3])) + len(inputLine1[9]) - \
                       min(int(inputLine1[3]), int(inputLine2[3]))
            count += 1
    f.close()
    average = average * 1.0 / count
    sigma = 0
    for i in range(len(m)):
        if m[i] != 0:
            x.append(i)
            y.append(m[i])
            sigma += (i - average) * (i - average) * m[i]
    sigma = math.sqrt(sigma * 1.0 / count)
    
    for i in range(5): 
        x1 = cut(x, y, average, sigma)[0]
        y1 = cut(x, y, average, sigma)[1]
        newAverage = cut(x, y, average, sigma)[2]
        newSigma = cut(x, y, average, sigma)[3]
        cut(x1, y1, newAverage, newSigma)
        x = x1
        y = y1
        average = newAverage
        sigma = newSigma
    plot(x1, y1, marker='.', linestyle='-', color='b')
    savefig('insertd.png')

distinsert()


