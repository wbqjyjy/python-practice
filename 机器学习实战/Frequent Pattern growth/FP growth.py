#程序清单12-2 FP树构建函数
#返回创建好的树，以及头指针表

#注意：这里的数据集是一个字典，项集为字典的键， 频率为键值
#subdata={frozenset(['data']):1}
def createTree(dataSet,minSup=1): #数据集，最小支持度  其中dataSet的形式{'data':num,'data2':num,'data3':num}
    headerTable={} #存：表头  单个元素的个数   头指针表

    #第一次遍历树：求给个元素支持度，并除去不符合最小支持度的元素
    for trans in dataSet: #取单条数据  
        for item in trans: #取单条数据的单个元素
            headerTable[item]=headerTable.get(item,0)+dataSet[trans] #第一项可以理解为获取item原来的个数，dataSet[trans]是什么意思？？？trans是第一个样本数据，dataSet[trans]是该数据的条数
    for k in headerTable.keys(): #遍历字典headerTable的键
        if headerTable[k]<minSup: #如果键值<最小支持度
            del(headerTable[k]) #删除该元素
    freqItemSet=set(headerTable.keys()) #集合元素 为  key值 （数据元素)
    if len(freqItemSet)==0:return None,None

    #第二次遍历树：
    for k in headerTable: #遍历键
        headerTable[k]=[headerTable[k],None] #将键值改为一个列表，第一个元素为键的个数，第二个元素初始化为None（第二个存放该元素数据的指针）
    retTree=treeNode('Null set',1,None)
    for tranSet,count in dataSet.items(): #遍历dataSet中的每一条 数据 及 出现次数
        localD={}
        #对于每一个数据条来说，如果数据条中的数据元素都在freqItemSet中，赋值localD[item]，并且根据item总的个数排序，返回一个数据条中按照num排序后的列表，将这个列表中的结点跟新到树中
        #如果树中根节点（空集）已经有这个子孩子，则跟新count，否则创建根节点的children，并同时跟新该数据元素的指针。接着在以这个数据元素为根节点，连接下一个数据元素，再以这个数据元素为根节点，连接下一个元素，知道数据条元素读取完。没更新一个结点，都要检查结点对应的指针连接（其指针链接指向数据元素的每一个实例）
        #把一个数据条连到树上后，内循环结束，再次执行外循环，进入下一个数据条，如果该数据条中第一个元素为根节点（空集）的children，则不用重新赋值根节点children，否则从新赋值一个新的children,在完成第一个结点嫁接后，开始第二个结点嫁接，第二个结点的根节点为第一个结点，如果其已经为该根节点的children，则不用创建根节点.children,否则重新赋值一个根节点.children
        #一次类推，创建dataset的FP树
        #其中headerTable为头指针表，表中元素涵盖了dataset中所有的数据元素
        for item in tranSet:
            if item in freqItemSet:
                localD[item]=headerTable[item][0] #如果单个数据元素在原来的表头中，则将localD[item]=个数
            if len(localD)>0: #如果表头元素个数>0
                orderedItems=[v[0] for v in sorted(localD.items(),key=lambda p:p[1],reverse=True)] #首先通过键值来对localD进行排序，然后，遍历localD中的元素，并且取其首字母存于orderedItems中
                updateTree(orderdItems,retTree,headerTable,count) #???
    return retTree,headerTable

def updateTree(items,inTree,headerTable,count):
    if items[0] in inTree.childern: #如果数据元素item[0]在树节点的孩子中
        inTree.childern[items[0]].inc(count) #增加这个孩子节点的 num
    else:
        inTree.children[items[0]]=treeNode(items[0],count,inTree) #否则将Items[0]添加到inTree的孩子节点中。
        if headerTable[items[0]][1]==None: #如果该元素数据 结点的指针为None  实际就是treeNode
                headerTable[items[0]][1]=inTree.children[items[0]] #赋值该数据元素的结点
        else:#如果元素数据的连接不为空时，将指针指向连接尾部，并将尾部空链接赋值为 “同一元素”的指针（该元素为在其他事件其他分支中出现）
            updateHeader(headerTable[items[0]][1],inTree.children[items[0]]) #???
    if len(items)>1: #头指针表中元素个数>1时
        updateTree(items[1::],inTree.children[items[0]],headerTable,count) #???
   
def updateHeader(nodeToTest,targetNode):
    while(nodeToTest.nodeLink != None):
        nodeToTest=nodeToTest.nodeLink #找到连接尾部，将targetNode赋值给尾部空指针
    nodeToTest.nodeLink = targeNode
            

#程序清单12-5 递归查找频繁项集的mineTree函数
#当condPattBases为{}时，myHead==None,递归停止
def mineTree(inTree,headerTable,minSup,preFix,freqItemList): #FP树，头指针表，最小支持度，？set([])？，符合支持度的数据元素
    bigL=[v[0] for v in sorted(headerTable.items(),key=lambda p:p[1])] #对头指针表排序，并将数据元素按排序结果存储在bigL中
    for basePat in bigL:
        newFreqSet = preFix.copy() #??? set([])
        newFreqSet.add(basePat) #将模式加到newFreqSet集合中
        freqItemList.append(newFreqSet) #每一个模式元素以集合的形式存储在list中
        condPattBases=findPrefixPath(basePat,headerTable[basePat][1]) #找到模式 的条件模式基
        mycondTree,myHead=createTree(condPattBases,minSup) #对这一模式的条件模式基建FP树  其中不满足最小支持度的数据元素会被砍掉

        if myHead !=None: #如果该条件模式及 建树后，有 数据元素 满足 最小支持度，则利用生成的FP树，寻找频繁项集
            mineTree(myCondTree,myHead,minSup,newFreqSet,freqItemList)
            
#程序清单12-7 文本解析及合成代码
#urlsRemoved=re.sub('(http[s]?:[/][/]|www.)([a-z]|[A-Z]|[0-9]|[/.]|[~])*','',bigString)   [s]?非贪婪算法，匹配最短项   括号(...)为子模式，标志一个子表达式的开始和结束，子表达式可以获取供以后使用，利用group
#listOfTokens=re.split(r'\W*',urlsRemoved)   根据模式，分割字符串urlsRemoved   \W 等价于：[^a-zA-Z0-9-]    \w等价于[a-zA-Z0-9-]
            
