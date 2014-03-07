__author__ = 'lenk'

currentIREF = 0
currentIREAD = 0

def readM(tempCount, tempReference, read, m):
    global currentIREF
    global currentIREAD
    for i in range(tempCount):
        if str(tempReference[i]) != str(read[i]):
            m[currentIREAD + i] = 1
    currentIREF += tempCount
    currentIREAD += tempCount
    return m

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

def scanREAD(cigar, read, reference, inputLine):
    global currentIREF
    global currentIREAD
    number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    currentIREAD = 0
    currentIREF = 0
    m = []
    for i in range(len(read)):
        m.append(0)
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
            #print 'reference=', len(reference), '\r\nread=',  tempRead, '\r\ncigar', cigar, 'i=', i, \
            #    'tempCount=', tempCount
            #print 'currentIREF=', currentIREF, 'currentIREAD=', currentIREAD
            #print int(inputLine[3]) + currentIREF - 1, int(inputLine[3]) + currentIREF + tempCount - 1
            if cigar[i] == 'M':
                m = readM(tempCount, tempReference, tempRead, m)
            if cigar[i] == 'I':
                readI(tempCount)
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
    return m

def quake():
    falsePositives = 0
    falseNegatives = 0
    trueNegatives = 0
    with open('MG1655-K12.first10K.fasta', 'r') as f:
        f.readline()
        reference = ''
        while True:
            temp = f.readline()
            if temp == '':
                break
            reference += temp[:-1]

    with open('out.sam', 'r') as f1:
        f1.readline()
        a, b, c = f1.readline().split()
        L = int(c[3:])
        f1.readline()
        with open('out_cor.sam', 'r') as f2:
            f2.readline()
            a, b, c = f2.readline().split()
            L = int(c[3:])
            f2.readline()
            while True:
                inputLine_err = []
                inputLine_err.extend(f1.readline().split('\t'))
                if inputLine_err[0] == '\n' or inputLine_err[0] == '':
                    break
                cigar_err = str(inputLine_err[5][:])
                read_err = inputLine_err[9][:]

                inputLine_cor = []
                inputLine_cor.extend(f2.readline().split('\t'))
                if inputLine_cor[0] == '\n' or inputLine_cor[0] == '':
                    break
                cigar_cor = str(inputLine_cor[5][:])
                read_cor = inputLine_cor[9][:]

                m_err = scanREAD(cigar_err, read_err, reference, inputLine_err)
                m_cor = scanREAD(cigar_cor, read_cor, reference, inputLine_cor)

                for i in range(min(len(m_err), len(m_cor))):
                    if m_err[i] == 1 and m_cor[i] == 1:
                        falsePositives += 1
                    if m_err[i] == 0 and m_cor[i] == 1:
                        falseNegatives += 1
                    if m_err[i] == 1 and m_cor[i] == 0:
                        trueNegatives +=1

        with open('outputQuake.txt', 'w') as f3:
            f3.write('falsePositives=' + str(falsePositives) + '\r\nfalseNegatives=' + str(falseNegatives) +
                     '\r\ntrueNegatives=' + str(trueNegatives))

quake()
