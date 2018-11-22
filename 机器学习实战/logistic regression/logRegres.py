from numpy import *
def plotBestFit(wei):
    import matplotlib.pyplot as plt
    weights=wei.getA() #将矩阵转成数组
    dataMat,labelMat=loadDataSet() #赋值input matrix   labelmatrix
    dataArr=array(dataMat) #将input matrix转为数组
    n=shape(dataArr)[0] #参数个数
    xcord1=[];ycord1=[] #label为1时的特征值x1,x2
    xcord2=[];ycord2=[] #label为0时的特征值x1,x2
    for i in range(n):
        if int(labelMat[i])==1: #将label为1时的特征值加入相应的list
            xcord1.append(dataArr[i,1]);ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]);ycord2.append(dataArr[i,2])
    fig=plt.figure()
    ax=fig.add_subplot(111)
    ax.scatter(xcord1,ycord2,s=30,c='red',marker='s') #绘制散点图
    ax.scatter(xcord1,ycord2,s=30,c='green')
    x=arange(-3.0,3.0,0.1) #步长0.1，从-3到3，列出取值，返回对象为数组
    y=(-weights[0]-weights[1]*x)/weights[2] #由来： 0=w0x0+w1x1+w2x2  x0=1
    ax.plot(x,y) #绘制两个特征值的拟合直线
    plt.xlabel('x1');plt.ylabel('x2'); #给坐标轴命名
    plt.show() #显示绘制的图像
