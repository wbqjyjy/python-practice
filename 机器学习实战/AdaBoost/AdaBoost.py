from numpy import *
import matplotlib.pyplot as plt
def stumpClassify(dataMatrix,dimen,threshVal,threshIneq):#以样本的第dimen个特征进行分类，分类边界值为threshVal
    retArray=ones((shape(dataMatrix)[0],1))  #建立数组，元素个数=样本数
    if threshIneq == 'lt':
        retArray[dataMatrix[:,dimen]<=threshVal] =-1.0 #如果样本第dimen个特征<=指定值，则将其归到-1类。这里，注意code写法
    else:
        retArray[dataMatrix[:,dimen]>threshVal]=-1.0
    return retArray

def plotROC(predStrengths,classLabels):#分类器的预测强度，分类标签
    import matplotlib.pyplot as plt
    cur=(1.0,1.0) #保留绘制光标的位置
    ySum=0.0 #计算AUC值
    numPosClas=sum(array(classLabels)==1.0) #计算正例的数目
    yStep=1/float(numPosClas) #y轴步长
    xStep=1/float(len(classLabels)-numPosClas) #x轴步长
    sortedIndicies=predStrengths.argsort() #argsort返回的是数组值从小到大的索引，在这里按照从小到大的顺序返回预测强度   因此我们需要从（1,1）开始绘制
    #构建画笔
    fig=plt.figure()
    fig.clf()
    ax=plt.subplot(111)
    for index in sortedIndicies.tolist()[0]:#numpy中tolist，将sortedIndicies转换为列表   [0]list的行???   指示的是一个样本编号
        if classLabels[index] == 1.0: #如果是正例，沿y轴方向向下移动一个步长，意味着，真阳例的概率减小了一分
            delX=0
            delY=yStep
        else: #返回的是反例，沿x轴的方向移动一个步长，意味着伪正例的概率减小了一分
            delX=xStep
            delY=0
            ySum+=cur[1] #当x轴移动时，累积y轴的长度值
        ax.plot([cur[0],cur[0]-delX],[cur[1],cur[1]-delY],c='b') #plot(x轴数据，y轴数据，颜色字符） 绘制一条线段  最终画出RUC曲线
        cur=(cur[0]-delX,cur[1]-delY) #重新锁定绘制光标的位置
    ax.plot([0,1],[0,1],'b--') #绘制对角线(0,0)(1,1)
    plt.xlabel('false positive rate')
    plt.ylabel('true positive rate')
    plt.title('ROC curve for AdaBoost Horse Colic Detection System')
    ax.axis([0,1,0,1]) #坐标轴坐标区间的设定 前两个是x轴，后两个是y轴
    plt.show() #显示绘图
    print('the area under the curve is :',ySum*xStep) #AUC是对多个小矩形的面积相加，这些小矩形的宽度是xStep，而高度可通过ySum得到

#ROC曲线可以用来判断将反例错分为正例的严重程度，评价指标为：ROC曲线下的面积AUC，一个完美的分类器AUC为1.0，随机猜测AUC为0.5    

    
        
        
    
    
