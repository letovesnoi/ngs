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

def main():
    list = {}
    with open('s_6.first1000.fastq', 'r') as f:
        while f:
            readId = f.readline()
            if readId == '':
                break
            read = f.readline()[:-1]
            f.readline()
            quality = f.readline()

            k = 13
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

    for i in list:
        print i + '\r\n' + str(list[i])

    edge = {}
    for i in list:
        for j in list[i]:
            edge[i[:] + j[-1:]] = [list[i][j], 0]

    '''with open('edge.fasta', 'w') as fe:
        for i in edge:
            for j in edge[i]:
                fe.write('[' + str(i) + ',' + str(j) + ']\r\n')

    with open('deBruijnGraph.dot', 'w') as f1:
        f1.write('digraph G{\r\n')
        for neighbor in list:
            for i in range(len(list[neighbor])):
                f1.write(' ' + neighbor + '->' + str(list[neighbor].keys()[i]) + ';\r\n')
        f1.write('}')'''

    newEdge = {}
    for i in list:
        if (len(list[i]) != 1 or ('A' + i not in edge.keys() and 'C' + i not in edge.keys() \
                            and 'G' + i not in edge.keys() and 'T' + i not in edge.keys())) \
            or (('A' + i in edge.keys() and 'C' + i in edge.keys())
                or ('A' + i in edge.keys() and 'G' + i in edge.keys())
                or ('A' + i in edge.keys() and 'T' + i in edge.keys())
                or ('C' + i in edge.keys() and 'G' + i in edge.keys())
                or ('C' + i in edge.keys() and 'T' + i in edge.keys())
                or ('G' + i in edge.keys() and 'T' + i in edge.keys())):
            current = i
            currentEdge = i
            for l in list[i].keys():
                currentEdge = i
                if list[i][l] != -1:
                    current = l
                    currentEdge += current[-1:]
                    count = 1
                    w = list[i][l]
                    list[i][l] = -1
                    if l in list:
                        if len(list[l]) == 1 and \
                            (('C' + l not in edge.keys() and 'G' + l not in edge.keys() and 'T' + l not in edge.keys()) or
                             ('A' + l not in edge.keys() and 'G' + l not in edge.keys() and 'T' + l not in edge.keys()) or
                             ('A' + l not in edge.keys() and 'C' + l not in edge.keys() and 'T' + l not in edge.keys()) or
                             ('A' + l not in edge.keys() and 'C' + l not in edge.keys() and 'G' + l not in edge.keys())):
                            current = list[l].keys()[0]
                            currentEdge += current[-1:]
                            count += 1
                            w += list[l][current]
                            list[l][current] = -1
                            if current in list:
                                while len(list[current]) == 1 and \
                                    (('C' + current not in edge.keys() and 'G' + current not in edge.keys() and 'T' + current not in edge.keys()) or
                                     ('A' + current not in edge.keys() and 'G' + current not in edge.keys() and 'T' + current not in edge.keys()) or
                                     ('A' + current not in edge.keys() and 'C' + current not in edge.keys() and 'T' + current not in edge.keys()) or
                                     ('A' + current not in edge.keys() and 'C' + current not in edge.keys() and 'G' + current not in edge.keys())):
                                    w += list[current][list[current].keys()[0]]
                                    current = list[current].keys()[0]
                                    currentEdge += current[-1:]
                                    if current not in list:
                                         break
                                    if len(list[current]) == 1 and \
                                        (('C' + current not in edge.keys() and 'G' + current not in edge.keys() and 'T' + current not in edge.keys()) or
                                         ('A' + current not in edge.keys() and 'G' + current not in edge.keys() and 'T' + current not in edge.keys()) or
                                         ('A' + current not in edge.keys() and 'C' + current not in edge.keys() and 'T' + current not in edge.keys()) or
                                         ('A' + current not in edge.keys() and 'C' + current not in edge.keys() and 'G' + current not in edge.keys())):
                                        list[i][current] = -1
                                    count += 1
                            w = w * 1.0 / count
                            newEdge[currentEdge] = w
                        else:
                            newEdge[currentEdge] = w
                    else:
                        newEdge[i + l[-1:]] = w

    with open('deBruijnGraphEdge_fastq.fasta', 'w') as dBE:
        for i in newEdge:
            dBE.write('[' + str(i) + ',' + str(newEdge[i]) + ']\r\n')

    with open('deBruijnGraphCompress_fastq.dot', 'w') as dBC:
        dBC.write('digraph G{\r\n')
        for i in newEdge:
            dBC.write(' ' + str(i[:k]) + '->' + str(i[-k:]) + ' [label=' + i + '];\r\n')
        dBC.write('}')

main()