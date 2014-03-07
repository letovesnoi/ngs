__author__ = 'lenk'

def reverseComplement(read):
    n = len(read)
    i = n - 1
    rcread = ''
    while i != -1:
        if read[i] == 'A':
            rcread += 'T'
        if read[i] == 'C':
            rcread += 'G'
        if read[i] == 'G':
            rcread += 'C'
        if read[i] == 'T':
            rcread += 'A'
        i -= 1
    return rcread

def formGraph(k):
    list = {}
    with open('s_6.first100000.fastq', 'r') as f:
        while f:
            readId = f.readline()
            if readId == '':
                break
            read = f.readline()[:-1]
            f.readline()
            quality = f.readline()

            rc = reverseComplement(read)
            for i in range(0, len(read) - k):
                if read[i:i + k] not in list:
                    list[read[i:i + k]] = {}
                neighbor = read[i + 1:i + k + 1]
                if neighbor not in list[read[i:i + k]]:
                    list[read[i:i + k]][neighbor] = 1
                else:
                    list[read[i:i + k]][neighbor] += 1

            for i in range(0, len(rc) - k):
                if rc[i:i + k] not in list:
                    list[rc[i:i + k]] = {}
                neighbor = rc[i + 1:i + k + 1]
                if neighbor not in list[rc[i:i + k]]:
                    list[rc[i:i + k]][neighbor] = 1
                else:
                    list[rc[i:i + k]][neighbor] += 1
    return list

def contigs(list, k):

    edge = {}
    for i in list:
        for j in list[i]:
            edge[i[:] + j[-1:]] = list[i][j]
    newEdge = {}

    countIN = {}
    countOUT = {}
    for i in list:
        countOUT[i] = len(list[i])
        for j in list[i]:
            if j not in countIN:
                countIN[j] = 1
            else:
                countIN[j] += 1

    for i in countIN:
        if i not in countOUT:
            countOUT[i] = 0
    for i in countOUT:
        if i not in countIN:
            countIN[i] = 0

    tempCountIn = countIN.copy()
    tempCountOut = countOUT.copy()
    unvertex = list.keys()[:]

    cont = []
    while len(unvertex) != 0:

        newStart = unvertex[0]

        while countOUT[newStart] == 1 and countIN[newStart] == 1:
            if newStart in list and list[newStart].keys() != []:
                if newStart == list[newStart].keys()[0]:
                    newEdge[newStart + newStart[-1:]] = edge[newStart + newStart[-1:]]
                    cont.append(newStart + list[newStart].keys()[0][-1:])
                    unvertex.remove(newStart)
                    break
            unvertex.remove(newStart)
            if len(unvertex) == 0:
                return newEdge
            newStart = unvertex[0]

        tempK = 0
        cont.append(newStart[:])

        currentStart = list[newStart].keys()[0]
        tempK += edge[newStart[:] + currentStart[-1:]]

        list[newStart][currentStart] -= 1

        tempCountIn[currentStart] -= 1

        tempCountOut[newStart] -= 1
        if tempCountOut[newStart] == 0:
            unvertex.remove(newStart)

        if list[newStart][currentStart] == 0:
           del list[newStart][currentStart]

        while countOUT[currentStart] == 1 and countIN[currentStart] == 1:
            if currentStart not in list:
                 break
            if currentStart in list:
                if list[currentStart] == {}:
                    break

            i = list[currentStart].keys()[0]

            tempCountIn[i] -= 1
            tempCountOut[currentStart] -= 1

            list[currentStart][i] -= 1
            if list[currentStart][i] == 0:
                del list[currentStart][i]

            cont[-1] += currentStart[-1]
            tempK += edge[currentStart[:] + i[-1:]]

            if currentStart in unvertex and tempCountOut[currentStart] == 0 and tempCountIn[currentStart] == 0:
                unvertex.remove(currentStart)
            currentStart = i
            if currentStart in unvertex and tempCountOut[currentStart] == 0 and tempCountIn[currentStart] == 0:
                unvertex.remove(currentStart)

        cont[-1] += currentStart[-1:]
        newEdge[cont[-1]] = tempK * 1.0 / (len(cont[-1]) - k)

    cont.sort()
    return newEdge

def main():
    k = 25
    graph = formGraph(k)
    newEdge = contigs(graph, k)

    with open('deBruijnGraphEdge.fasta', 'w') as dBE:
        for i in newEdge:
            dBE.write('[' + str(i) + ',' + str(newEdge[i]) +']\r\n')

    with open('deBruijnGraphCompress.dot', 'w') as dBC:
        dBC.write('digraph G{\r\n')
        for i in newEdge:
            #dBC.write(' ' + str(i[:k]) + '->' + str(i[-k:]) + ' [label=' + i + '];\r\n')
	    dBC.write(' ' + str(i[:k]) + '->' + str(i[-k:]) + ';\r\n')
        dBC.write('}')

main()
