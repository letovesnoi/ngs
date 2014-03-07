import matplotlib
matplotlib.use('Agg')

__author__ = 'lenk'

from pylab import *

ACGT = {'A', 'C', 'G', 'T'}
dictionary = dict(A=0, C=1, G=2, T=3)
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

def freq():
    global currentIREF
    global currentIREAD

    number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    with open('test.sam', 'r') as f1:
        a, b, c = f1.readline().split()
        L = int(c[3:])
        minlenID = L
        maxlenID = 0
        y = []
        for i in range(L):
            y.append(0)

        while True:
            inputLine = []
            inputLine.extend(f1.readline().split('\t'))
            if inputLine[0] == '\n' or inputLine[0] == '':
                break

            cigar = str(inputLine[5][:])

            currentIREAD = 0
            currentIREF = 0
            i = 0
            while i < len(cigar):
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
                        y[tempCount] += 1
                        if minlenID > tempCount:
                            minlenID = tempCount
                        if maxlenID < tempCount:
                            maxlenID = tempCount
                    if cigar[i] == 'D':
                        readD(tempCount)
                        y[tempCount] += 1
                        if minlenID > tempCount:
                            minlenID = tempCount
                        if maxlenID < tempCount:
                            maxlenID = tempCount
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
    f1.close()

    plot(range(minlenID, maxlenID + 1), y[minlenID:maxlenID + 1], marker='.', linestyle='-', color='b')
    savefig('lenIndels.png')

freq()
