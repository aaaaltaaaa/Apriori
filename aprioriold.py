import csv
from collections import defaultdict


attribute=['democrat', 'republican','handicapped-infants','water-project-cost-sharing','adoption-of-the-budget-resolution','physician-fee-freeze','el-salvador-aid','religious-groups-in-schools', 'anti-satellite-test-ban','aid-to-nicaraguan-contras','mx-missile','immigration','synfuels-corporation-cutback','education-spending','superfund-right-to-sue,crime','duty-free-exports','export-administration-act-south-africa']

def loadDataSet():
    dataSource=csv.reader(open("house-votes-84.data","r"))
    dataSet=[]
    for transaction in dataSource:
        data=[]
        if transaction[0]=='democrat':
            data.append(0)
        else:
            data.append(1)
        for i in range(1,len(transaction)):
            if transaction[i]!='y':
                data.append(i+1)
        dataSet.append(data)
    return dataSet

def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return C1

def scanD(dataSet, Ck, minSupport=0.3):
    count=defaultdict(int)
    for transactionSet in dataSet:
        C=map(frozenset,Ck)
        for candidateSet in C:
            if candidateSet.issubset(transactionSet):
                count[candidateSet] += 1
    num = float(len(dataSet))
    retList = []
    supportData = {}
    for item in Ck:
        support = count[frozenset(item)] / num
        if support >= minSupport:
            retList.append(item)
        supportData[frozenset(item)] = support
        retList.sort()
    return retList, supportData

def aprioriGen(Lk):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i + 1, lenLk):
            L1 = Lk[i][0:-1]
            L2 = Lk[j][0:-1]
            if L1 == L2:
                ret=list(Lk[i])
                ret.append(Lk[j][-1])
                retList.append(ret)
            else:
                break
    return retList

def apriori(dataSet, minSupport=0.3):
    C1 = createC1(dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    k = 0
    while (len(L[k]) > 0):
        Ck = aprioriGen(L[k])
        Lk, supK = scanD(dataSet, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

def generateRules(L, supportData, minConf=0.9):
    RuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            associationRules(freqSet, supportData, RuleList, 0.9)
    return RuleList

def associationRules(freqSet, supportData, RuleList, minConf=0.9):
    if freqSet==[0,5,6,13]:
        print()
    lenF=len(freqSet)
    C = [[item] for item in freqSet]
    freqSet=frozenset(freqSet)
    i=0
    while len(C)!=0 and i<lenF-1:
        L=[]
        for  conseq in C:
            conseqSet=frozenset(conseq)
            conf = supportData[freqSet] / supportData[freqSet - conseqSet]
            if conf >= minConf:
                ret=list(freqSet - conseqSet)
                ret.sort()
                print ([attribute[i] for i in ret], '-->', [attribute[i] for i in conseq], 'conf:', conf)
                RuleList.append([ret, conseq, conf])
                L.append(list(conseq))
        if i < lenF-2:
            C=aprioriGen(L)
        i+=1
if __name__ == '__main__':
    dataSet=loadDataSet()
    L, suppData = apriori(dataSet,0.3)
    rules = generateRules(L, suppData, minConf=0.9)