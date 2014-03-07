import matplotlib
matplotlib.use('Agg')

__author__ = 'lenk'

from pylab import *

currentIREF = 0
currentIREAD = 0

def readM(tempCount):
    global currentIREF
    global currentIREAD
    currentIREF += tempCount
    currentIREAD += tempCount

def readI(tempCount):
    global currentIREF
    global currentIREAD
    currentIREAD += tempCount

def readD(tempCount):
    global currentIREF
    global currentIREAD
    currentIREF += tempCount

def readS(tempCount):
    global currentIREF
    global currentIREAD
    currentIREAD += tempCount

def readH():
    global currentIREF
    global currentIREAD

def readEqual(tempCount):
    global currentIREF
    global currentIREAD
    currentIREAD += tempCount
    currentIREF += tempCount

def readX(tempCount):
    global currentIREF
    global currentIREAD
    currentIREAD += tempCount
    currentIREF += tempCount

def readN(tempCount):
    global currentIREF
    global currentIREAD
    currentIREF += tempCount

def readP(tempCount):
    global currentIREF
    global currentIREAD
    currentIREAD += tempCount
    currentIREF += tempCount

def countIndels(cigar, begin, end, y):
    lenG = end - begin + 1
    global currentIREF
    global currentIREAD
    currentIREF = 0
    currentIREAD = 0
    number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    i = 0
    while i < len(cigar) and currentIREAD <= end:
        tempCount = ''
        while cigar[i] in number:
            tempCount += cigar[i]
            i += 1
        if tempCount != '' and tempCount != '0':
            tempCount = int(tempCount)
            if cigar[i] == 'M':
                readM(tempCount)
            if cigar[i] == 'I':
                readI(tempCount)
                if currentIREAD >= begin:
                    y[lenG] += 1
            if cigar[i] == 'D':
                readD(tempCount)
                if currentIREAD >= begin:
                    y[lenG] += 1
            if cigar[i] == 'S':
                readS(tempCount)
            if cigar[i] == 'H':
                readH()
            if cigar[i] == '=':
                readEqual(tempCount)
            if cigar[i] == 'X':
                readX(tempCount)
            if cigar[i] == 'N':
                readN(tempCount)
            if cigar[i] == 'P':
                readP(tempCount)
        i += 1
    return y

def freq():
    global currentIREF
    global currentIREAD

    with open('test.sam', 'r') as f1:
        a, b, c = f1.readline().split()
        L = int(c[3:])

        y = []
        for i in range(L):
            y.append(0)

        xmin = L
        xmax = 0
        while True:
            inputLine = []
            inputLine.extend(f1.readline().split('\t'))
            if inputLine[0] == '\n' or inputLine[0] == '':
                break
            cigar = str(inputLine[5][:])
            currentIREAD = 0
            currentIREF = 0

            j = 0
            while j < len(inputLine[9]) - 1:
                templenG = 1
                while inputLine[9][j] == inputLine[9][j + 1]:
                    templenG += 1
                    j += 1
                    if j + 1 >= len(inputLine[9]):
                        break
                if templenG != 1:
                    begin = j - templenG + 1
                    end = j
                    if xmax < templenG:
                        xmax = templenG
                    if xmin > templenG:
                        xmin = templenG
                    y = countIndels(cigar, begin, end, y)
                j += 1
    f1.close()

    plot(range(xmin, xmax + 1), y[xmin:xmax + 1], marker='.', linestyle='-', color='b')
    savefig('gomoIndels.png')

freq()
