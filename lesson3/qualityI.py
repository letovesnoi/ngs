import matplotlib
matplotlib.use('Agg')

__author__ = 'lenk'

from pylab import *

currentIREF = 0
currentIREAD = 0
l = 33

def readM(tempCount):
    global currentIREF
    global currentIREAD
    currentIREF += tempCount
    currentIREAD += tempCount

def readI(tempCount, y, tempQuality):
    global currentIREF
    global currentIREAD
    for i in range(tempCount):
        y[int(ord(tempQuality[i])) - l] += 1
    currentIREAD += tempCount
    return y

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
    global l
    global currentIREF
    global currentIREAD
    m = dict(A=[0, 0, 0, 0, 0], C=[0, 0, 0, 0, 0], G=[0, 0, 0, 0, 0], T=[0, 0, 0, 0, 0], ID=[0, 0, 0, 0, 0])

    #read reference
    with open('DH10B-K12.fasta', 'r') as f:
        f.readline()
        reference = ''
        while True:
            temp = f.readline()
            if temp == '':
                break
            reference += temp[:-1]
    f.close()

    number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}

    #determine quality format and work with sam
    with open('test.sam', 'r') as f1:
        #determine quality:
        f1.readline()
        format = 0
        for i in range(100):
            inputLine = []
            inputLine.extend(f1.readline().split('\t'))
            quality = inputLine[10][:]
            ident = {"J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z",
                              "[", "]", "`", "a", "b", "c", "d", "e", "f", "g", "h", r"\\", r"\^", r"\_"}
            for i in range(len(quality)):
                if quality[i] in ident:
                    format = 1
                    l = 64
                    break
            if format == 1:
                break

        f1.seek(0)

        x = []
        y = []
        for i in range(40 + 1):
            y.append(0)
            x.append(l + i)

        #read sam:
        a, b, c = f1.readline().split()
        L = int(c[3:])
        while True:
            inputLine = []
            inputLine.extend(f1.readline().split('\t'))
            if inputLine[0] == '\n' or inputLine[0] == '':
                break

            cigar = str(inputLine[5][:])
            read = inputLine[9][:]
            quality = inputLine[10][:]

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

                    tempReference = reference[int(inputLine[3]) + currentIREF - 1:int(inputLine[3]) + currentIREF +
                                                                                  tempCount - 1]
                    tempRead = read[currentIREAD:currentIREAD + tempCount]
                    tempQuality = quality[currentIREAD:currentIREAD + tempCount]
                    #print 'reference=', len(reference), '\r\nread=',  tempRead, '\r\ncigar', cigar, 'i=', i, \
                    #    'tempCount=', tempCount
                    #print 'currentIREF=', currentIREF, 'currentIREAD=', currentIREAD
                    #print int(inputLine[3]) + currentIREF - 1, int(inputLine[3]) + currentIREF + tempCount - 1
                    if cigar[i] == 'M':
                        readM(tempCount)
                    if cigar[i] == 'I':
                        y = readI(tempCount, y, tempQuality)
                    if cigar[i] == 'D':
                        readD(tempCount)
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
                    #print 'currentIREF=', currentIREF, 'currentIREAD=', currentIREAD
                i += 1
    f1.close()
    plot(x[:], y[:], marker='.', linestyle='-', color='b')
    savefig('qualityI.png')

freq()
