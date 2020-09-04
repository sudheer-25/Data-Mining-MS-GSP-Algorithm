import re
import operator
import sys
sys.stdout = open('output.txt', 'w')
from copy import copy, deepcopy
print("test")
print("test2")

def inputDataProc():
    newDict = {}
    item = []
    misvalue = []

    with open("para1.txt") as data:
        for line in data:
            item.append(line[line.find("(")+1:line.find(")")])
            misvalue.append(float(line[line.find("=")+1:].strip()))

    for i in range(0, len(item)-1):
        newDict[item[i]] = misvalue[i]

    #SDC
    a, b = re.split('=', item[-1])
    SDC = float(misvalue[-1])

    DATA = []
    with open("data.txt") as f:
        for line in f:
            line = line.strip()[1:-1]
            itemSetList = (re.split(r'[{}]',line))
            while "" in itemSetList:
                itemSetList.remove("")
            all=[]
            for s in itemSetList:
                all.append([i for i in re.split(',| ', s) if i != ''])
            DATA.append(all)

    M = sorted(newDict.items(), key=operator.itemgetter(1))

    return M, DATA, SDC, newDict
'''
def isSubset(subset,superset):
    if len(set(subset + superset)) == len(set(superset)):
        return True
    else:
        return False
'''
def isSubset2(subset,superset):
    for i in range(0,len(subset)):
        for j in range(0,len(superset)):
            if subset[i] == superset[j]:
                subset = subset[0:i]+subset[i+1:]
                superset = superset[0:j]+superset[j+1:]
                return isSubset2(subset, superset)
    if len(subset) == 0:
        return True
    else:
        return False


def isSubsequence(subseq, superseq):

    dict = {}

    next= 0
    for i in subseq:
        flag = False
        j = next
        while j < len(superseq):
            if 'j' in dict:
                pass
            else:
                if isSubset2(i, superseq[j]):
                    dict[j] = True
                    flag = True
                    next = j + 1
                    break
            j += 1
        if not flag:
            return False

    return True

def supportcount(sequence, data):
    #Assuming sequence is a list of list
    count = 0
    for a in data:
        if isSubsequence(sequence, a):
            count = count+1
    return count


def index2d(list2d, value):
    return next((i, j) for i, lst in enumerate(list2d)
                for j, x in enumerate(lst) if x == value)

def L(M, DATA, newDict):
    L =[]
    for item, MIS in M:
        if(supportcount([[item]],DATA)/len(DATA)>= MIS):
            L.append(item)
            ind1, ind2 =index2d(M,item)
            break
    for i in range(ind1+1, len(M)):
        if(supportcount([[M[i][0]]], DATA)/len(DATA)>=newDict[L[-1]]):
            L.append(M[i][0])
    return L


def F1(L, DATA, newDict):
    F1 = []
    for x in L:
        if (supportcount([[x]],DATA)/len(DATA))>=newDict[x]:
            F1.append([x])
    return (F1)

def level2candidategenSPM (L, SDC):
    C2 =[]
    for i in range(0,len(L)):
        if supportcount([[L[i]]], DATA)/len(DATA) >=newDict[L[i]]:
            for j in range(i, len(L)):
                if (supportcount([[L[j]]], DATA)/len(DATA) >=newDict[L[i]]) and (abs(supportcount([[L[j]]], DATA)-supportcount([[L[i]]], DATA))/len(DATA)<= SDC):
                    if int(L[i]) <= int(L[j]):
                        C2.append([[L[i], L[j]]])
                    else:
                        C2.append([[L[j], L[i]]])

                    C2.append([[L[i]], [L[j]]])
                    if L[i] != L[j]:
                        C2.append([[L[j]], [L[i]]])
    return C2

def minMisInCandidate(sequence):
    #sequence is list of list
    minMis = 9999999
    for eachitemset in sequence:
        for eachitem in eachitemset:
            if newDict[eachitem]< minMis:
                minMis = newDict[eachitem]
    return minMis

'''
def TransCandid(sequence):
    #sequence is list of list
    g, k = '-', ""
    for x in sequence:
        s = g.join(x)
        k = k + s
    return k
'''

def generateSubSequences(seq):

    p = []
    for i in range(0,len(seq)):
        for j in range(0,len(seq[i])):
            x = deepcopy(seq)
            del x[i][j]
            x = [a for a in x if a != []]
            p.append(x)
    return p


def canPrune(kseq,S):
    minMIS = minMisInCandidate(kseq)
    Listofseq = generateSubSequences(kseq)
    for eachseq in Listofseq:
        if minMisInCandidate(eachseq) == minMIS and eachseq not in S:
            return True
        else:
            return False


#MISCheck returns the min Mis value in sequence and checks if the first element is only element that has min MIS value
def MISCheck(x, newDict, pos):

    if (pos == 0):
        minMIS = newDict[x[0][0]]

    elif (pos == -1):
        minMIS = newDict[x[-1][-1]]
        pos = length(x) - 1

    else:
        print("this is neither the last nor the first position in MISCheck")
        return

    Least = True
    i = 0
    for eachItemSet in x:
        for eachItem in eachItemSet:
            if newDict[eachItem] <= minMIS and pos!=i:

                Least = False
                minMIS = newDict[eachItem]
            i = i + 1

    return Least, minMIS


def seqDrop1(seq, dropPosition):
    seq1 = deepcopy(seq)
    if len(seq1[0]) >= 2:
        seq1[0] = seq1[0][:dropPosition - 1] + seq1[0][dropPosition:]
        return seq1,seq[0][1]
    elif dropPosition == 2 and (len(seq1[1]) >= 2):
        del seq1[1][0]
        return seq1, seq[1][0]
    elif dropPosition == 2 and (len(seq1[1]) == 1):
        del seq1[1]
        return seq1, seq[1]
    elif dropPosition > 2 or dropPosition == 0:
        return 'Please enter a dropPosition value that lies in[1,2] '
    else:
        del seq1[0]
        return seq1, seq[0]


def seqDrop2(seq, dropPosition):
    seq1 = deepcopy(seq)

    if len(seq1[-1]) >= 2:
        x = len(seq1[-1]) - dropPosition
        seq1[-1] = seq1[-1][:x] + seq1[-1][x + 1:]
        return seq1, seq[-1][x]
    elif dropPosition == 2 and (len(seq1[-2]) >= 2):
        del seq1[-2][-1]
        return seq1,seq[-2][-1]
    elif dropPosition == 2 and (len(seq1[-2]) == 1):
        del seq1[-2]
        return seq1,seq[-2]
    elif dropPosition > 2 or dropPosition == 0:
        return 'Please enter a dropPosition value that lies in[1,2] '
    else:
        del seq1[-1]
        return seq1,seq[-1]


def subseqCheck3(s1, s2):
    seq1 = deepcopy(s1)
    seq2 = deepcopy(s2)

    # Remove first element of s1
    if len(seq1[0]) == 1:
        del seq1[0]
        b=[seq1,s1[0]]
    else:
        del seq1[0][0]
        b=[seq1,s1[0][0]]

    # Remove last element of s2
    if len(seq2[-1]) == 1:
        del seq2[-1]
        c=[seq2,s2[-1]]
    else:
        del seq2[-1][-1]
        c=[seq2,s2[-1][-1]]

    if b[0] == c[0]:
        return True
    else:
        return False


def subseqCheck2(s2, s1, dropPositionfors2):
    s1alter = deepcopy(s2)
    dropped_s2 = seqDrop2(s1alter, dropPositionfors2)[0]
    dropped_item_s1 = seqDrop2(s1alter, dropPositionfors2)[1]
    seq1 = deepcopy(s1)

    if len(seq1[0]) == 1:
        del seq1[0]
        b= [seq1,s1[0]]
    else:
        del seq1[0][0]
        b= [seq1,s1[0][0]]
    if dropped_s2 == b[0]:
        return True
    else:
        return False

def subseqCheck1(s1, s2, dropPositionfors1):
    s1alter = deepcopy(s1)
    dropped_s1 = seqDrop1(s1alter, dropPositionfors1)[0]
    dropped_item_s1 = seqDrop2(s1alter, dropPositionfors1)[1]
    seq2 = deepcopy(s2)
    if len(seq2[-1]) == 1:
        del seq2[-1]
        b=[seq2,s2[-1]]
    else:
        del seq2[-1][-1]
        b=[seq2,s2[-1][-1]]
    if dropped_s1 == b[0]:
        return True
    else:
        return False



def cond1MISCheck(s1, s2, newDict):
    lastEleS2MIS = newDict[s2[-1][-1]]
    firstEleS1MIS = newDict[s1[0][0]]
    if lastEleS2MIS >= firstEleS1MIS:
        return True
    else:
        return False


def cond2MISCheck(s2, s1, newDict):
    lastEleS2MIS = newDict[s2[-1][-1]]
    firstEleS1MIS = newDict[s1[0][0]]
    if lastEleS2MIS < firstEleS1MIS:
        return True
    else:
        return False

'''

def joinFirstLeastStrictly(s1, F, newDict):
    joinedSeqs = []
    # s2 for loop
    for s2 in F:
        if (subseqCheck1(s1, s2, 2,SDC) == True)  and (cond1MISCheck(s1, s2, newDict) == True):
            if len(s2[-1]) == 1:
                s_1 = deepcopy(s1)
                s_1.append(s2[-1])
                joinedSeqs.append(s_1)

                if length(s1) == 2 and size(s1) == 2 and int(s2[-1][-1]) > int(s1[-1][-1]):
                    s_11=deepcopy(s1)
                    s_11[-1].append(s2[-1][-1])
                    joinedSeqs.append(s_11)

            elif ((length(s1) == 2 and size(s1) == 1) and (int(s2[-1][-1])>int(s1[-1][-1]))) or (length(s1) > 2):
                s_111=deepcopy(s1)
                s_111[-1].append(s2[-1][-1])
                joinedSeqs.append(s_111)

    if len(joinedSeqs) != 0:
        return joinedSeqs
    else:
        return False


def joinLastLeastStrictly(s1, F, newDict):
    joinedSeqs = []
    for s2 in F:
        if (subseqCheck2(s1, s2, 2,SDC) == True) and (newDict[s1[0][0]]>newDict[s2[-1][-1]]):
            s_1 = deepcopy(s1)

            if len(s2[0]) == 1:
                s_1.insert(0,s2[0])
                joinedSeqs.append(s_1)

                if length(s1) == 2 and size(s1) == 2 and int(s2[0][0]) < int(s1[0][0]):
                    s_11 = deepcopy(s1)
                    s_11[0].insert(0, s2[0][0])
                    joinedSeqs.append(s_11)

            elif ((length(s1) == 2 and size(s1) == 1) and (int(s2[0][0]) < int(s1[0][0]))) or (length(s1) > 2):
                s_111 = deepcopy(s1)
                s_111[0].insert(0, s2[0][0])
                joinedSeqs.append(s_111)

    if len(joinedSeqs) != 0:
        return joinedSeqs
    else:
        return False

'''

def joinGSP(s1, F2, newDict):
    joinedSeqs = []
    for s2 in F2:
        if (subseqCheck3(s1, s2,SDC) == True):
            if len(s2[-1]) == 1:
                s_1 = deepcopy(s1)
                s_1.append(s2[-1])
                joinedSeqs.append(s_1)
            else:
                s_11 = deepcopy(s1)
                s_11[-1].append(s2[-1][-1])
                joinedSeqs.append(s_11)

    if len(joinedSeqs) != 0:
        return joinedSeqs
    else:
        return False

def size(s1):
    return len(s1)


def length(s1):
    size = 0
    for i in range(0, len(s1)):
        size = size + len(s1[i])
    return size


def canJoinMISCheck(s1, s2, newDict):
    lastItems2 = int(s2[-1][-1])
    lastItems1 = int(s1[-1][-1])
    if lastItems2 > lastItems1:
        return True
    else:
        return False


def canJoinMISCheck2(s2, s1, newDict):
    firstItems2 = int(s2[0][0])
    firstItems1 = int(s1[0][0])
    if firstItems1 < firstItems2:
        return True
    else:
        return False

def SDCCheck(sequence):
    # sequence is list of list
    minSup = 9999999
    maxSup = -1
    for eachitemset in sequence:
        for eachitem in eachitemset:
            supItem = supportcount([[eachitem]], DATA) / len(DATA)
            if supItem < minSup:
                minSup = supItem
            if supItem > maxSup:
                maxSup = supItem
    if abs(maxSup - minSup) <= SDC:
        return True
    else:
        return False


def MSCandidateGenSPM(F, newDict):
    F1 = deepcopy(F)
    F2 = deepcopy(F)

    joinedSeqs = []
    for s1 in F1:
        for s2 in F1:

            if MISCheck(s1, newDict, 0)[0]:
                if (subseqCheck1(s1, s2, 2) == True) and (cond1MISCheck(s1, s2, newDict) == True):
                    if len(s2[-1]) == 1:
                        s_1 = deepcopy(s1)
                        s_1.append(s2[-1])
                        joinedSeqs.append(s_1)

                        if length(s1) == 2 and size(s1) == 2 and canJoinMISCheck(s1,s2,newDict):
                            s_11 = deepcopy(s1)
                            s_11[-1].append(s2[-1][-1])
                            joinedSeqs.append(s_11)

                    elif ((length(s1) == 2 and size(s1) == 1) and (canJoinMISCheck(s1,s2,newDict))) or (length(s1) > 2):
                        s_111 = deepcopy(s1)
                        s_111[-1].append(s2[-1][-1])
                        joinedSeqs.append(s_111)

            elif MISCheck(s2, newDict, -1)[0]:
                if (subseqCheck2(s2, s1, 2) == True) and (cond2MISCheck(s2, s1, newDict) == True):
                    s_2 = deepcopy(s2)

                    if len(s1[0]) == 1:
                        s_2.insert(0, s1[0])
                        joinedSeqs.append(s_2)

                        if length(s2) == 2 and size(s2) == 2 and canJoinMISCheck2(s2,s1,newDict):
                            s_22 = deepcopy(s2)
                            s_22[0].insert(0, s1[0][0])
                            joinedSeqs.append(s_22)

                    elif ((length(s2) == 2 and size(s2) == 1) and (canJoinMISCheck2(s2,s1,newDict))) or (length(s2) > 2):
                        s_222 = deepcopy(s2)
                        s_222[0].insert(0, s1[0][0])
                        joinedSeqs.append(s_222)
            else:
                if (subseqCheck3(s1, s2) == True):
                    if len(s2[-1]) == 1:
                        s_1 = deepcopy(s1)
                        s_1.append(s2[-1])
                        joinedSeqs.append(s_1)
                    else:
                        s_11 = deepcopy(s1)
                        s_11[-1].append(s2[-1][-1])
                        joinedSeqs.append(s_11)

    checkedsdc = [x for x in joinedSeqs if SDCCheck(x) == True and canPrune(x , F) == False]

    return checkedsdc

def FkCkGen(F1, C2, DATA, newDict):
    Fk = deepcopy(F1)
    a = []
    F = []
    k = 2
    while (Fk):
        if k == 2:
            Ck = deepcopy(C2)
        else:
            Ck = MSCandidateGenSPM(Fk, newDict)
            a.append(Ck)
        Fk = []
        for i in Ck:
            if (supportcount(i, DATA) / len(DATA)) >= minMisInCandidate(i):
                Fk.append(i)
        if len(Fk) != 0:
            F.append(Fk)
        k = k + 1
    return F

def postProc(listList):
    out = ['<']
    for x in listList:
        for y in x:
            out.append('{')
            z = ''.join(y)
            out.append(z)
            out.append('}')
    out.append('>')
    outString = ''.join(out)
    return outString

def postProc1(listList):
    out = ['<']
    for x in listList:
        out.append('{')
        for y in x:

            z = ''.join(y)
            out.append(z)
            out.append(',')
        out.pop(-1)
        out.append('}')
    out.append('>')
    outString = ''.join(out)
    return outString

def outputProc(F1, num_F, DATA):
    print("Number of Length " + str(num_F) + " Frequent Sequences: " + str(len(F1)))
    for x in F1:
        outString = postProc([x])
        supCount = supportcount([x], DATA)
        print(outString + " count: " + str(supCount))

def outputProc1(F1, num_F, DATA):
    print("Number of Length " + str(num_F) + " Frequent Sequences: " + str(len(F1)))
    for x in F1:
        outString = postProc1(x)
        supCount = supportcount(x, DATA)
        print(outString + " count: " + str(supCount))

if (__name__ == '__main__'):
    M, DATA, SDC, newDict = inputDataProc()
    L = L(M, DATA, newDict)
    F1 = F1(L, DATA, newDict)
    C2 = level2candidategenSPM(L, SDC)
    F = FkCkGen(F1, C2, DATA, newDict)
    num_F = 1
    outputProc(F1, num_F, DATA)
    k = 0
    print("\n")
    while len(F) > k:
        num_F = num_F + 1
        outputProc1(F[k], num_F, DATA)
        print("\n")
        k = k + 1
