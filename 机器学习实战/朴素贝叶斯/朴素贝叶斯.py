from numpy import *
def trainNBO(trainMatrix,trainCategory): #计算p(w|c) p(c) trainCategory为每个文档的标签类别数组
    numTrainDocs=len(trainMatrix) #训练文档个数；trainMatrix相当于一个文档是一个数组，且每个数组所含的词汇个数相同，因为都每个数组都出自于相同的词汇表
    numWords=len(trainMatrix[0]) #词汇表词汇个数
    pAbusive=sum(trainCategory)/float(numTrainDocs) #侮辱性文档出现概率
    p0Num=zeros(numWords) #拥有numWords个0元素的数组 ??
    p1Num=zeros(numWords) #??
    p0Denom=0.0 #??
    p1Denom=0.0 #??
    for i in range(numTrainDocs):
        if trainCategory[i]==1: #如果第I个文档是侮辱性文档
            p1Num += trainMatrix[i] #p1Num为一个矩阵，当分类为1时，词汇表中每个单词出现的次数
            p1Denom += sum(trainMatrix[i]) #p1Denom为一变量，当分类为1时，所有文档的词汇总数
        else:
            p0Num += trainMatrix[i] #当分类为0时，词汇表中每个单词出现的次数
            p0Denom += sum(trainMatrix[i]) #分类为0时，所有文档词汇总数
    p1Vect=log(p1Num/p1Denom)#取log以免数值下溢 #当分类为1时，每个feature(词汇)出现的概率；p1Vect为一数组
    p0Vect=log(p0Num/p0Denom)#取log以免数值下溢 #当分类为0时，每个feature(词汇)出现的概率；p0Vect为一数组
    return p0Vect,p1Vect,pAbusive  #利用训练文档得出的先验概率pAbusive,p(w)也是先验概率，条件概率p0Vect,p1Vect，后验概率p(y|x)

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1): #vec2Classify为一个文档数组，后3个参数为概率值
    p1=sum(vec2Classify*p1Vec)+log(pClass1)
    p0=sum(vec2Classify*p0Vec)+log(1.0-pClass1)
    if p1>p0:
        return 1
    else:
        return 0

def textParse(bigString):
    import re
    listOfTokens=re.split(r'\W*',bigString) #将bigString分解成字符串列表
    return [tok.lower() for tok in listOfTokens if len(tok)>2] #返回字符串长度大于2的字符串列表

def spamTest():
    docList=[];classList=[];fullText=[]
    for i in range(1,26):#？？？
        wordList=textParse(open('email/spam/%d.txt' % i).read()) #返回文档字符串列表
        docList.append(wordList) #将该文档字符串列表作为一个元素添加到docList中
        fullText.extend(wordList) #将文档字符串列表中元素都添加到fullText列表中
        classList.append(1) #将分类列表中添加一个分类1 垃圾邮件
        wordList=textParse(open('email/ham/%d.txt' % i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0) #同样的操作重复一遍后，将分类值0加入分类列表  非垃圾邮件
    vocabList=createVocabList(docList) #创造文档词汇表（基于所有文档）
    trainingSet=range(50) #训练样本集编号???
    testSet=[]#测试集
    #目前只进行了一次测试迭代，即只生成了一个训练集和一个测试集，实际应用中，最好多次迭代，求错误率的平均值
    #如果要多次迭代：
#for i in range(10): #迭代10次，每次都执行下面的代码，其中错误率的计算需要一些加减乘除，不在coding：计算每次错误率，可将其放入数组，让后求数组中错误率的平均值，作为最后结果
#可以直接重新写一个函数，多次执行spamTest(),获得多个错误率，取平均值
    for i in range(10): #选出10个test样本   
        randIndex=int(random.uniform(0,len(trainingSet))) #从0~trainingSet中随机选取一个样本
        testSet.append(trainingSet[randIndex]) #将随机选取的训练样本加入到testSet中
        del(trainingSet[randIndex]) #将被选中作为test样本的样本删除
    trainMat=[]#文档矩阵，每个文档为一个数组，数组元素个数等于词汇表词汇个数
    trainClasses=[] #文档分类标签
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex])) #将docList中的文档，依次形成一个文档数组，最终形成文档矩阵
        trainClasses.append(classList[docIndex]) #将文档分类标签依次加入trainClasses
    p0V,p1V,pSpam=trainNBO(array(trainMat),array(trainClasses))
    errorCount=0 #出错计数
    for docIndex in testSet:
        wordVector=setOfWords2Vec(vocabList,docList[docIndex]) #为测试文档创建文档数组
        if calssifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]: #如果测试结果与原结果不符合
            errorCount +=1
            #print('the misclassified doc is %s'% wordVector)
        print('the error rate is :',float(errorCount)/len(testSet)) #打印出错率

def getTopWords(ny,sf):
    import operator
    vocabList,p0V,p1V=localWords(ny,sf) #返回词汇表，概率值列表，p(w|c)，词汇列表中每个词对应于p(w|c1) p(w|c2)中的一个概率值
    topNY=[]
    topSF=[]#添加出现频次在**以上的词汇
    for i in range(len(p0V)):
        if p0V[i] > -6.0: topSF.append((vocabList[i],p0V[i])) #如果某词汇在属于某个分类的所有文档字符串中，出现频次超过一定数值，则将该词汇及其出现频次加入到topSF列表
        if p1V[i] > -6.0: topNY.append((vocabList[i],p1V[i]))
    sortedSF=sorted(topSF,key=lambdapair:pair[1],reverse=True)
    print("SF**SF**SF**.......SF**")
    for item in sortedSF:
        print(item[0]) #sortedSF的每个元素是一个元组，打印元组第一个元素
    sortedNY=sorted(topNY,key = lambda pair:pair[1],reverse=True)
    print("NY**NY**NY**.......NY**")
    for item in sortedNY:
        print(item[0])

    
    
    
        

    
    
