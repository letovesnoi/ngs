__author__ = 'lenk'

ACGT = {'A', 'C', 'G', 'T'}
ACGTID = {'A', 'C', 'G', 'T', 'ID'}
dictionary = dict(A=0, C=1, G=2, T=3)
dictionaryID = dict(A=0, C=1, G=2, T=3, ID=4)
currentIREF = 0
currentIREAD = 0

def readM(tempCount, tempReference, read, m):
    global currentIREF
    global currentIREAD
    for i in range(tempCount):
        if str(tempReference[i]) != str(read[i]):
            if str(tempReference[i]) in dictionary and str(read[i]) in ACGT:
                m[read[i]][dictionary[str(tempReference[i])]] += 1
    currentIREF += tempCount
    currentIREAD += tempCount

def readI(tempCount, read, m):
    global currentIREF
    global currentIREAD
    for i in range(tempCount):
        if str(read[i]) in ACGT:
            m[read[i]][4] += 1
    currentIREAD += tempCount

def readD(tempCount, tempReference, m):
    global currentIREF
    global currentIREAD
    for i in range(tempCount):
        if str(tempReference[i]) in ACGT:
            m['ID'][dictionary[str(tempReference[i])]] += 1
    currentIREF += tempCount

def readS(tempCount):
    global currentIREF
    global currentIREAD
    currentIREAD += tempCount
    #currentIREF += tempCount

def readH(tempCount):
    global currentIREF
    global currentIREAD
    #currentIREF += tempCount

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
    m = dict(A=[0, 0, 0, 0, 0], C=[0, 0, 0, 0, 0], G=[0, 0, 0, 0, 0], T=[0, 0, 0, 0, 0], ID=[0, 0, 0, 0, 0])
    with open('MG1655-K12.first10K.fasta', 'r') as f:
        f.readline()
        reference = ''
        while True:
            temp = f.readline()
            if temp == '':
                break
            reference += temp[:-1]
    f.close()
    number = {'0', '1', '2', '3', '4', '5', '6', '7', '8', '9'}
    with open('outTest.sam', 'r') as f1:
        f1.readline()
        a, b, c = f1.readline().split()
        L = int(c[3:])
        f1.readline()
        while True:
            inputLine = []
            inputLine.extend(f1.readline().split('\t'))
            if inputLine[0] == '\n' or inputLine[0] == '':
                break

            cigar = str(inputLine[5][:])
            read = inputLine[9][:]

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
                    print 'reference=', len(reference), '\r\nread=',  tempRead, '\r\ncigar', cigar, 'i=', i, \
                        'tempCount=', tempCount
                    print 'currentIREF=', currentIREF, 'currentIREAD=', currentIREAD
                    print int(inputLine[3]) + currentIREF - 1, int(inputLine[3]) + currentIREF + tempCount - 1
                    if cigar[i] == 'M':
                        readM(tempCount, tempReference, tempRead, m)
                    if cigar[i] == 'I':
                        readI(tempCount, tempRead, m)
                    if cigar[i] == 'D':
                        readD(tempCount, tempReference, m)
                    if cigar[i] == 'S':
                        readS(tempCount)
                    if cigar[i] == 'H':
                        readH(tempCount)
                    if cigar[i] == '=':
                        readEqual(tempCount)
                    if cigar[i] == 'X':
                        readX(tempCount)
                    if cigar[i] == 'N':
                        readN(tempCount)
                    if cigar[i] == 'P':
                        readP(tempCount)
                    print 'currentIREF=', currentIREF, 'currentIREAD=', currentIREAD
                i += 1
    f1.close()
    with open('outputFreq.txt', 'w') as f2:
        for symbolRead in ACGT:
            for symbolRef in ACGT:
                f2.write(str(m[symbolRead][dictionary[symbolRef]]).rjust(10))
            f2.write("\r\n")
    f2.close()

freq()
