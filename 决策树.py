import matplotlib.pyplot as plt

decisionNode=dict(boxstyle="round4",fc="0.8")
leafNode=dict(boxstyle="round4",fc="0.8")
arrow_args=dict(arrowstyle="<-")

def plotNode(nodeTxt,centerPt,parentPt,nodeType): #nodeText:注解的字符串，centerPt：对应文本所在的位置, parentPt：箭头所在的位置，nodeType：结点属性
    createPlot.ax1.annotate(nodeTxt,xy=parentPt,xycoords="axes fraction",xytext=centerPt,textcoords="axes fraction",va="center",ha="center",bbox=nodeType,arrowprops=arrow_args)
#annotate(s,xy=arrow_crd,xytext=text_crd,arrowprops=dict) 在图形中增加带箭头的注解。s表示要注解的字符串是什么，xy对应箭头所在的位置，xytext对应文本所在的位置，arrowprops定义显示的属性

def creatPlot():
    fig=plt.figure(1,facecolor='white') #创建一幅图
    fig.clf() #清除绘图区域
    createPlot.ax1=plt.subplot(111,frameon=False) # subplot(numrows,numcols,plotnum)把整个绘图区域分为numrows和numcols，按照从左到右，从上到下的顺序编号，如果numrows，numcols,plotnum都<10，则可以把他们缩写为一个整数supplot(111)
    plotNode=('a decision node',(0.5,0.1),(0.1,0.5),decisionNode) #在绘图区域绘制一个decisionNode
    plotNode=('a leaf node',(0.8,0.1),(0.3,0.8),leafNode) #在绘图区域绘制一个leafNode
    plt.show() #显示绘制的图

def plotMidText(cntrPt,parentPt,txtString): #在父子结点间填充文本信息
    xMid=(parentPt[0]-cntrPt[0])/2.0+cntrPt[0] #文本信息的x坐标
    yMid=(parentPt[1]-cntPt[1])/2.0+contrPt[1] #文本信息的y坐标
    createPlot.ax1.text(xMid,yMid,txtString) #在绘图区按照指定坐标系添加文本

def plotTree(myTree,parentPt,nodeTxt):
    numLeafs=getNumLeafs(myTree) #叶子节点数
    depth=getTreeDepth(myTree) #树的深度
    fistStr=myTree.keys()[0] #第一个分类属性
    cntrPt=(plotTree.xoff+(1.0+float(numLeafs))/2.0/plotTree.totalW,plotTree.yoff) #plotTree.xoff   plotTree.totalw   plotTree.yoff ？？？  横坐标计算依据？？？相当于每次横坐标都取宽度的中间值
    plotMidText(cntrPt,parentPt,nodeTxt) #在父子结点间填充文本信息  ???parentPt  绘制父子结点间的文本信息
    plotNode(firstStr,contrPt,parentPt,decisionNode) # 绘制叶子结点 contrPt带箭头的哪一方（有标签), parentPt为头部
    secondDict=myTree[firstStr]
    plotTree.yoff=plotTree.yoff-1.0/plotTree.totalD # 第二个结点y的偏移量
    for key in secondDict.keys():
        if type(secondDict[key]).__name__=="dict": #如果secondDict依然为字典
            plotTree(secondDict[key],cntrPt,str(key)) #利用plotTree继续画树 str(key)为父子结点中间的文本信息，firstStr:key,而second[key]则为第二棵树，其键值对应的是字符串，或字典
        else:
            plotTree.xoff=plotTree.xoff+1.0/plotTree.totalw #如果是叶子节点，x轴坐标偏移，相对其父节点来说
            plotNode(secondDict[key],(plotTree.xoff,plotTree.yoff),cntrPt,leafNode) #如果不为字典，其为叶子结点
            plotMidText((plotTree.xoff,plotTree.yoff),cntrPt,str(key)) #如果是叶子结点，将key值设置为父子结点之间的文本信息
    plotTree.yoff=plotTree.yoff+1.0/plotTree.totalD  #为什么还要再加这一句？？？ 从递归中再出来时，yoff需要退回原来的状态

    def createPlot(inTree):
        fig=plt.figure(1,facecolor='white')
        fig.clf()
        axprops=dict(xticks=[],yticks=[]) #???
        createPlot.ax1=plt.subplot(111,frameon=False,**axprops) #最后一个参数是什么意思？？？
        plotTree.totalW=float(getNumLeafs(inTree)) #totalW等于树叶子节点数
        plotTree.totalD=float(getTreeDepth(inTree)) #totalD等于树的深度
        plotTree.xoff=-0.5/plotTree.totalW; plotTree.yoff=1.0  #xoff为什么这么算？？？ 作者定义
        plotTree(inTree,(0.5,1.0),'')#起始点头部坐标与尾部坐标重合
        PLT.show()


    #难点：各个结点坐标的计算方法

    
