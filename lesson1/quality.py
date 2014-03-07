import matplotlib
matplotlib.use('Agg')

__author__ = 'lenk'

from pylab import *

def main():
    with open('test.fastq', 'r') as f:
        format = 0
        l = 33
        for i in range(100):
            readId = f.readline()
            nucl = f.readline()
            f.readline()
            quality = f.readline()
            ident = {"J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                              "[", "]", "`", "a", "b", "c", "d", "e", "f", "g", "h", r"\\", r"\^", r"\_"}
            for i in range(len(quality)):
                if quality[i] in ident:
                    format = 1
                    l = 64
                    break
            if format == 1:
                break

        f.seek(0)
        Q = []
        countAverage = []
        tempLenQ = 0
        while f:
            readId = f.readline()
            if readId == '':
                break
            nucl = f.readline()
            f.readline()
            quality = f.readline()
            if tempLenQ < len(quality):
                for i in range(tempLenQ, len(quality)):
                    Q.append(0)
                    tempLenQ += 1
                    countAverage.append(0)
            for i in range(len(quality)):
                countAverage[i] += 1
                Q[i] += ord(quality[i]) + l
    f.close()
    for j in range(len(Q)):
        Q[j]  = Q[j] * 1.0 / countAverage[j]
    x = []
    y = []
    for i in range(len(Q)):
        x.append(i)
        y.append(10 ** (-Q[i] * 1.0 / 10))
    '''with open('outtestQ.txt', 'w') as f1:
        f1.write(str(x))
        f1.write('\n')
        f1.write(str(y))
    f1.close()'''

    plot(x[:-1], y[:-1], marker='.', linestyle='-', color='b')
    savefig('quality.png')
main()
