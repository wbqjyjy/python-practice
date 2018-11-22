#numpy.map(frozenset,cl)  将列表冻结，使其不能被修改
#dict.has_key() 用于判断键是否存在于字典中
#list.insert(0,key)  在列表首部插入key值
#numpy.map(set,dataset) 将集合映射到数据集上，使数据集的每一个元素都用set表示

def aprioriGen(Lk,k): #频繁项集列表，项集元素个数   这里假设LK是拥有k-1项的集合，这里要得到k项的集合
    retList=[]
    lenLk=len(Lk) #Lk的长度
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1=list(Lk[i])[:k-2]  #Lk是[[1,2,4],[5,6,7]]状态，L1表示从Lk的第i个列表中，取出0到k-3项
            L2=list(Lk[j])[:k-2]
            L1.sort() #注意一定要排序，因为，之后要进行L1和L2的比较
            L2.sort() 
            if L1==L2: #如果L1和L2的前K-2项都相同，则将其合并，得到一个k项的集合
                retList.append(Lk[i] | Lk[j]) #Lk是集合
    return retList
        
def apriori(dataSet,minSupport=0.5):
    C1=createC1(dataSet) #形成 第一批 候选项，每个候选项只有一个元素
    D=map(set,dataSet)  #将dataSet的每个元素都映射成集合
    L1，supportData=scanD(D,C1,minSupport) #根据第一批候选项形成频繁项，并给出各个候选项的支持率
    L=[L1] #保留每一批的频繁项
    k=2
    #当利用scanD无法形成频繁项时，即没有任何候选项的支持率能够达到要求，此时，len(L[k-2])>0的要求将达不到，停止循环
    while(len(L[k-2])>0):#当第k-2批频繁项个数>0时    L[0]存的是第一批频繁项，每个频繁项有1个元素，L[k-2]存的是第k-1批频繁项，每个频繁项有k-1个元素
    
        CK=aprioriGen(L[k-2],k) #创建第k批候选项，候选项有k个元素   第k批候选项的创建，是基于第K-1批频繁项的
        Lk,supK=scanD(D,CK,minSupport) #得到第k批频繁项，以及第k批候选项的支持率
        supportData.update(supK) #将第k批候选项的支持率添加到supportData中
        L.append(LK) #将第K批频繁项添加到L中
        k+=1
    return L,supportData #返回各个数量的频繁项，以及各个数量的候选项的支持率列表

def generateRules(L,supportData,minConf=0.7):
    bigRuleList=[] #存放高于最低可信度的关联规则
    for i in range(1,len(L)):#L为频繁项集列表，1个元素频繁项集列表，2个元素频繁项集列表  从L中选取第i批的频繁项集列表
        for freqSet in L[i]:#从频繁项集列表中选取其中一个频繁项
            H1=[frozenset([item]) for item in freqSet] #从频繁项中提取单个元素，并形成列表
            if(i>1): #如果频繁项的元素大于2个
                rulesFromConseq(freqSet,H1,supportData,bigRuleList,minConf) #???
            else:
                calcConf(freqSet,H1,supportData,bigRuleList,minConf) #检查一个频繁项freqSet与其 子元素之间的关联度，如果大于minConf，则将这些关联规则保存到bigRuleList中。
    return bigRuleList  #返回这些关联规则
        
def calcConf(freqSet,H,supportData,brl,minConf=0.7):
    prunedH=[] #用于记录符合可信度要求的 关联规则 右侧的  元素 ； 主要为了进一步组合形成新的频繁集 而用；
    for conseq in H:
        conf=supportData[freqSet]/supportData[freqSet-conseq] #supportData存储的是每一个候选项的支持度，这里freqSet/(freqSet-conseq) 是k频繁项在k-1频繁项中的可信度
        if conf>=minConf:
            print(freqSet-conseq,'-->',conseq,'conf:',conf)
            br1.append((freqSet-conseq,conseq,conf))
            purnedH.append(conseq) #???
    return prunedH 

#rulesFromConseq本质还是进行规则处理，主要用于生成 规则右部 的频繁集，然后通过calcConf来 扫描freqSet可能的关联规则，如果从calcConf得到的频繁集 个数>1的话，则进一步组合这些频繁集，查看freqSet是否与这些频繁集有关联
#疑惑地是参数H在这里是频繁集（相当于频繁项列表）,H[0]用来检测H中频繁项的长度，用来和freqSet长度进行比较，如果freqSet能够容纳H中的频繁集，则查看他们二者是否有关联。对于有关联的频繁集 列表，利用rulesFromConseq，进一步组合生成新的频繁集，查看新的频繁集与freqSet的关联情况
#？？？H在generateRules里边，应该是freqSet中的一个元素列表，这里，元素可以是频繁项吗？？？
def rulesFromConseq(freqSet,H,supportData,br1,minConf=0.7):#freqSet相当于是>=3的频繁项，H是频繁项中的元素，supportData是各候选项的支持度，br1是关联规则（待求解问题），minConf是最小可信度
    m=len(H[0]) #在这里H应该是一个频繁项集列表，H[0]为一个频繁项长度
    if (len(freqSet)>(m+1)): #如果频繁项的长度>m+1   只要freqSet的长度>m+1,就利用H生成Hmp1，
        Hmp1=aprioriGen(H,m+1) #H应该是一个频繁项集列表，每个频繁项=m，现要生成具有m+1项的频繁项
        Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf) #一个频繁项,其长度>m+1，Hmp1是具有m+1个元素的频繁项集列表，要得到freqSet->Hmp1的关联规则
        #这里的Hmp1长度为len(H[0])+1，
        if(len(Hmp1)>1):#如果得到的满足关联规则的 频繁集 集合长度>1,则利用RulesFromConseq进一步组合这些频繁集，以查看freqSet频繁项与新组合的频繁集是否有关联规则
            rulesFromConseq(freqSet,Hmp1,supportData,br1,minConf) 
    #H是单元素列表，H的形式类似：[frozenset({'data'}), frozenset({'string'})]，H[0]类似frozenset({'data'}),其长度len(H[0])=1; 如果不用frozenset，而用set也会得到同样的结果；
    #但是，如果使用list,a=['string','data'],b=[item for item in a], len(b[0])=6
    #这里要注意LIst和set的区别；在函数中很重要！！！
    #frozenset不可以随便添加元素，而set可以

    #rulesFromConseq函数中，m给出了H中每个元素的长度，最开始H是由单元素组成，其长度len(H[0])=1
    #对于关联规则左侧的freqSet来说，如果其长度>m+1(最开始>2),及大于频繁集进一步组合频繁集的 长度，表示freqSet足够大，可以包容频繁集，从而测试freqSet->freqSet-H[0]的关联关系
    #Hmp1=aprioriGin(H,m+1) ,用于组合新的频繁集（为关联规则右侧的 元素）
    #Hmp1=calcConf(freqSet,Hmp1,supportData,br1,minConf)，用于返回可信度达标的 关联规则右部 的频繁集 集合
    #如果返回的频繁集 个数>1，则可以进一步组合这些频繁集，测试更长长度频繁集 与freqSet的关联程度
    #递归，直到频繁集的长度+1>=len(freqSet) ,则停止递归，返回 关联规则

    #这里有一点需要注意，当频繁项freqSet的长度>=3时，用rulesFromConseq形成规则， 这里边关联规则右部频繁集的长度是从2开始的，即不测试  freqSet与单元素频繁集 的关联程度  


# apriori() 用于生成符合support的频繁项集合，以及supportData
# generateRules()用于生成符合可信度的 关联规则；


#集合特性： a.intersection(b)  返回值为：a与b的交集


            
            




        
