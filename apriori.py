import csv
import random
from collections import defaultdict

#属性名
attribute=['democrat', 'republican','handicapped-infants','water-project-cost-sharing','adoption-of-the-budget-resolution','physician-fee-freeze','el-salvador-aid','religious-groups-in-schools', 'anti-satellite-test-ban','aid-to-nicaraguan-contras','mx-missile','immigration','synfuels-corporation-cutback','education-spending','superfund-right-to-sue,crime','duty-free-exports','export-administration-act-south-africa']

#加载数据
def loadDataSet():
    dataSource=csv.reader(open("house-votes-84.data","r"))
    dataSet=[]
    for transaction in dataSource:#为数据编号
        data=[]
        if transaction[0]=='democrat':
            data.append(0)
        else:
            data.append(1)
        for i in range(1,len(transaction)):
            if transaction[i]=='y':
                data.append(i+1)
        dataSet.append(data)
    return dataSet

#生成C1
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:#遍历
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return C1

#通过ci生成li
def scanD(dataSet, Ck, minSupport=0.3):
    count=defaultdict(int)#使用默认数值的字典计数
    for transactionSet in dataSet:#遍历并统计
        C=map(frozenset,Ck)#使用frozenset便于子集判定
        for candidateSet in C:
            if candidateSet.issubset(transactionSet):
                count[candidateSet] += 1
    num = float(len(dataSet))
    retList = []#结果集
    supportData = {}#支持度
    for item in Ck:#计算支持度，筛选结果
        support = count[frozenset(item)] / num#使用frozenset便于hash
        if support >= minSupport:
            retList.append(item)
        supportData[frozenset(item)] = support
        retList.sort()
    return retList, supportData

#apriori从li生成ci+1
def aprioriGen(Lk):
    retList = []#结果集
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

#apriori算法
def apriori(dataSet, minSupport=0.3):
    C1 = createC1(dataSet)
    L1, supportData = scanD(dataSet, C1, minSupport)
    L = [L1]
    k = 0
    while (len(L[k]) > 0):#循环进行知道结束
        Ck = aprioriGen(L[k])
        Lk, supK = scanD(dataSet, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData

#生成频繁项集的关联规则
def generateRules(L, supportData, minConf=0.9):
    RuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            associationRules(freqSet, supportData, RuleList, 0.9)
    return RuleList

#生成一条频繁项集的关联规则
def associationRules(freqSet, supportData, RuleList, minConf=0.9):

    lenF=len(freqSet)
    C = [[item] for item in freqSet]
    freqSet=frozenset(freqSet)
    i=0
    while len(C)!=0 and i<lenF-1:
        L=[]
        for  conseq in C:
            conseqSet=frozenset(conseq)#使用frozenset便于集合运算和hash
            conf = supportData[freqSet] / supportData[freqSet - conseqSet]
            if conf >= minConf:#添加频繁项集
                ret=list(freqSet - conseqSet)
                ret.sort()
                print (ret, '-->',conseq, 'conf:', conf)
                RuleList.append([ret, conseq, conf])
                L.append(list(conseq))
        if i < lenF-2:#推出条件
            C=aprioriGen(L)#使用apriori生成
        i+=1

#补全？
def complete(rules,suppData):
    dataSource=csv.reader(open("house-votes-84.data","r"))
    dataSet=[]
    for transaction in dataSource:
        data=[]
        if transaction[0]=='democrat':
            data.append(0)
        else:
            data.append(1)
        for i in range(1,len(transaction)):
            if transaction[i]=='y':
                data.append(i+1)
        for i in range(1,len(transaction)):#如果是？，通过一定的几率修改数据集
            if transaction[i]=='?':
                D=frozenset(data)
                for rule in rules:
                    R0=frozenset(rule[0])
                    R1=frozenset(rule[1])
                    I=frozenset([i+1])
                    if  R0.issubset(D) in data and (R0-I).issubset(D):
                        if random.random()<suppData[R0|R1]*suppData[R0]/suppData[R0]:
                            data.append(i+1)
                            break
        data.sort()
        dataSet.append(data)
    return dataSet


if __name__ == '__main__':
    dataSet=loadDataSet()
    L, suppData = apriori(dataSet,0.3)
    rules = generateRules(L, suppData, minConf=0.9)
    print("complete:")
    dataSetComplete=complete(rules,suppData)
    L, suppData = apriori(dataSetComplete,0.3)
    rulesComplete = generateRules(L, suppData, minConf=0.9)
