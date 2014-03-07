import matplotlib
matplotlib.use('Agg')

__author__ = 'lenk'

from pylab import *

def cover():
    m = []
    count = 0
    average = 0
    with open('out_ecoli_mda_lane1.sam', 'r') as f:
        f.readline()
        a, b, c = f.readline().split()
        L = c[3:]
        L = int(L)
        f.readline()
        for line in f:
            inputLine = []
            inputLine.extend(line.split('\t'))
            temp = len(m)
            for i in range(temp, (int(inputLine[3]) + len(inputLine[9])) / 1000 + 1):
                m.append(0)
                count += 1
            begin = int(inputLine[3])
            for i in range(int(inputLine[3]) / 1000, (int(inputLine[3]) + len(inputLine[9])) / 1000 + 1):
                if m[i] == 0:
                    count -= 1
                if (i + 1) * 1000 > int(inputLine[3]) + len(inputLine[9]):
                    m[i] += int(inputLine[3]) + len(inputLine[9]) - begin
                    average += int(inputLine[3]) + len(inputLine[9]) - begin
                    break
                m[i] += (i + 1) * 1000 - begin
                average += (i + 1) * 1000 - begin
                begin = (i + 1) * 1000
    f.close()
    for i in range(len(m)):
        m[i] = m[i] * 1.0 / 1000
    x = []
    for i in range(len(m)):
        x.append(i)
    percover = (L - count * 1000.0) / L * 100
    average = average * 1.0 / L
    with open('outputCover.txt', 'w') as f:
        #f.write(str(x) + '\r\n')
        #f.write(str(m))
        f.write('\r\naveragecover=' + str(average) + '\r\n' + 'percover=' + str(percover))
    f.close()
    plot(x, m, marker='.', linestyle='-', color='r')
    savefig('cover.png')

cover()

