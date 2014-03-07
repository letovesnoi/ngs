import matplotlib
matplotlib.use('Agg')

__author__ = 'lenk'

from pylab import *

M = []
maxLen = 8
x = []
alphabet = ["A", "C", "G", "T"]


def expand(listP):
    tempL = len(listP)
    for ip in range(tempL):
        for i in range(len(alphabet)):
            k = listP[ip][:]
            k.append(alphabet[i])
            listP.append(k)
    for ip in range(tempL):
        listP.pop(0)

def computePrefixF(P):
    m = len(P)
    pi = []
    pi.append(0)
    pi.append(0)
    k = -1
    for q in range(2, m + 1):
        while k > 0 and P[k + 1] != P[q - 1]:
            k = pi[k] - 1
        if P[k + 1] == P[q - 1]:
            k += 1
        pi.append(k + 1)
    return pi


def KMPMatcher(T, P, j):
    n = len(T)
    m = len(P)
    pi = computePrefixF(P)
    q = 0
    for i in range(0, n):
        while q > 0 and P[q] != T[i]:
            q = pi[q]
        if P[q] == T[i]:
            q += 1
        if q == m:
            M[j] += 1
            q = pi[q]


def main():
    tempCount = 0
    for i in range(2, maxLen + 1):
        tempCount += len(alphabet) ** i
    for i in range(tempCount):
        M.append(0)
    with open('test.fastq', 'r') as f:
        while f:
            list = [["A"], ["C"], ["G"], ["T"]]
            expand(list)
            readId = f.readline()
            if readId == '':
                break
            nucl = f.readline()
            f.readline()
            quality = f.readline()
            current = 0
            for i in range(maxLen - 1):
                T = nucl
                for substring in list:
                    P = substring
                    KMPMatcher(T, P, current)
                    x.append(current)
                    current += 1
                #print list
                expand(list)

    f.close()
    #with open('outputK.txt', 'w') as f1:
        #f1.write(str(x))
        #f1.write('\n')
        #f1.write(str(M))
    #f1.close()

plot(x, M, marker='.', linestyle='-', color='r')
savefig('k_mers.png')


main()
