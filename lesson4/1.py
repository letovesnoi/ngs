__author__ = 'lenk'

currentIREF_err = 0
currentIREAD_err = 0
currentIREF_cor = 0
currentIREAD_cor = 0
icurrC_err = 0
icurrC_cor = 0

falsePositives, falseNegatives, trueNegatives = 0


def readM(tempCount, tempReference, err, cor, cigar_err, cigar_cor):
    global currentIREF_err, currentIREAD_err
    global currentIREF_cor, currentIREAD_cor
    global falsePositives, falseNegatives, trueNegatives
    global icurrC_err, icurrC_cor

    if cigar_err[icurrC_err] == 'M':
        while True:
            if cigar_cor[icurrC_cor] == 'M'


    for i in range(unCount):
        if err[i] != tempReference[i] and cor[i] != tempReference[i]:
            falsePositives += 1
        if err[i] == tempReference[i] and cor[i] != tempReference[i]:
            falseNegatives += 1
        if err[i] != tempReference[i] and cor[i] == tempReference[i]:
            trueNegatives += 1
    currentIREF_err += unCount
    currentIREAD_err += unCount
    currentIREF_cor += unCount
    currentIREAD_cor += unCount

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
    global currentIREF_err, currentIREAD_err
    global currentIREF_cor, currentIREAD_cor
    global falsePositives, falseNegatives, trueNegatives
    global icurrC_err, icurrC_cor
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
    with open('out.sam', 'r') as f1:
        f1.readline()
        a, b, c = f1.readline().split()
        L = int(c[3:])
        f1.readline()
        with open('out_cor.sam', 'r') as f2:
            f2.readline()
            f2.readline()
            f2.readline()
            while True:
                inputLine_err = []
                inputLine_cor = []
                inputLine_err.extend(f1.readline().split('\t'))
                inputLine_cor.extend(f2.readline().split('\t'))
                if inputLine_err[0] == '\n' or inputLine_err[0] == '':
                    break

                cigar_err = str(inputLine_err[5][:])
                err = inputLine_err[9][:]
                cigar_cor = str(inputLine_cor[5][:])
                cor = inputLine_cor[9][:]

                currentIREAD_err, currentIREF_err = 0
                currentIREAD_cor, currentIREF_cor = 0
                icurrC_err, icurrC_cor = 0

                i = 0
                while icurrC_err < len(cigar_err) or icurrC_cor < len(cigar_cor):
                    tempCount_err = ''
                    while cigar_err[icurrC_err] in number and icurrC_err < len(cigar_err):
                        tempCount += cigar_err[icurrC_err]
                        icurrC_err += 1
                    tempCount_cor = ''
                    while cigar_cor[icurrC_cor] in number and icurrC_cor < len(cigar_cor):
                        tempCount += cigar_cor[icurrC_cor]
                        icurrC_cor += 1

                    if tempCount != '' and tempCount != '0':
                        tempCount = int(tempCount)

                        tempReference = reference[int(inputLine[3]) + currentIREF - 1:int(inputLine[3]) + currentIREF +
                                                                                  tempCount - 1]
                        tempRead = read[currentIREAD:currentIREAD + tempCount]

                        if cigar[i] == 'M':
                            readM(tempCount, tempReference, tempRead, m)
                        if cigar[i] == 'I':
                            readI(tempCount, tempRead, m)
                        if cigar[i] == 'D':
                            readD(tempCount, tempReference, m)
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
        f2.close()
    f1.close()
    with open('output1-3.txt', 'w') as f3:
        for symbolRead in ACGT:
            for symbolRef in ACGT:
                f3.write(str(m[symbolRead][dictionary[symbolRef]]).rjust(10))
            f3.write("\r\n")
    f3.close()

freq()
