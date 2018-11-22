#numpy中的  random.rand(3,2)可以构造一个3*2的随机数字数组（取值范围为[0,1])

#程序清单 10-2 k-means
#ptsInClust=dataSet[nonzero(clusterAssment[:,0].A==cent)[0]]  把类别为cent的样本提取出来
#centroids[cent,:]=mean(ptsInClust,axis=0)  求cent类的质心
#注意函数func(par1,par2)中参数也可以是函数

def bikmeans(dataSet,k,distMeas=distEclud):
    m=shape(dataSet)[0] #样本量
    clusterAssment=mat(zeros((m,2))) #各样本分类，及与质心的误差
    centroid0=mean(dataSet,axis=0).tolist()[0] #第一次分类时，第一个质心的值
    centList=[centroid0] #质心的列表
    for j in range(m): #样本循环
        clusterAssment[j,1]=distMeas(mat(centroid0),dataSet[j,:])**2 #各个样本点与质心的距离
    while(len(centList)<k)： #当簇的个数小于k时
        lowestSSE=inf
        for i in range(len(centList)): #以簇的个数作为循环序列
            ptsInCurrCluster=dataSet[nonzero(clusterAssment[:,0].A==i)[0],:] #将第一簇中的数据集提取出来
            centroidMat,splitClustAss=kMeans(ptsInCurrCluster,2,distMeas) #将i个簇中的数据分为两类，返回值为质心数据，该数据集中分类情况:label,误差
            sseSplit=sum(splitClustAss[:,1]) #计算该子数据集与原质心的误差和
            sseNotSplit=sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0],1]) #计算总得数据集中分类不为i的数据与其质心的误差之和
            print("sseSplit, and notSplit:",sseSplit,sseNotSplit)
            if(sseSplit + sseNotSplit)<lowestSSE:
                bestCentToSplit = i
                bestNewCents=centroidMat #对于i簇，将其分类的质心的向量值
                bestClustAss=splitCustAss.copy() #对于i簇，其数据集新的分类情况列表：label,error
                lowestSSE=sseSplit+sseNotSplit #新的最小误差
        bestClustAss[nonzero(bestClustAss[:,0].A==1)[0],0]=len(centList) #由于分类总是从第0位开始计的，所以当将一个簇在分为2类时，多出的那一类可以用len(centlist)标记
        bestClustAss[nonzero(bestClustAss[:,0].A==0)[0],0]=bestCentToSplit #将bestClustAss中的0类标为第i类
        print("the bestCentToSplit is",bestCentToSplit)
        print("the len of bestClustAss is",len(bestClustAss))
        centList[bestCentToSplit]=bestNewCents[0,:] #将分裂的簇的那一栏的元素修改为bestNewCents[0,:]
        centList.append(bestNewCents[1,:]) #将多出来的一个分类，加到质心列表中
        clusterAssment[nonzero(clusterAssment[:,0].A==bestCentToSplit)[0],:]=bestClustAss #将原来分类为i簇的样本列表，赋值为bestClustAss
    return mat(centList),clusterAssment

#程序清单10-5 球面距离计算及簇绘图函数
import matplotlib
import matplotlib.pyplot as plt
def custerClubs(numClust=5):
    datList=[] #存放数据集
    for line in open('places.txt').readlines():
        lineArr=line.split('\t')
        dataList.append([float(lineArr[4]),float(lineArr[3])])
        dataMat=mat(dataList)
        myCentroids,clustAssing=biKmeans(dataMat,numClust,distMeas=distSLC)#给出质心列表，数据分类列表：label,error

        fig=plt.figure() #绘制画布
        rect=[0.1,0.1,0.8,0.8] #坐标轴区域
        scatterMarkers=['s','o','^','8','p','d','v','h','>','<'] #每个簇的标识
        axprops=dict(xticks=[],yticks=[]) #???
        ax0=fig.add_axes(rect,label='ax0',**axprops) #锁定坐标区域，rect为横轴，纵轴的坐标，最后一个参数的作用？？？  最后一个参数的写法？？？
        imgP=plt.imread('Portland.png') #荷兰底图 做为底图   基于一幅图像来创建矩阵
        ax0.imshow(imgP) #显示图片 基于矩阵，显示图像
        ax1=fig.add_axes(rect,label='ax1',frameon=False) #ax0相当于底图，ax1相当于各个地点在底图上的标识位置
        for i in range(numClust):
            ptsInCurrCluster=datMat[nonzero(clustAssing[:,0].A==i)[0],:] #筛出属于第i类的数据集
            markerStyle=scatterMarkers[i % len(scatterMarkers)] #给每一个簇分配一个标识
            ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0],ptsInCurrCluster[:,1].flatten().A[0],marker=markerStyle,s=90) #绘制第I个簇
        ax1.scatter(myCentroids[:,0].flatten().A[0],myCentroids[:,1].flatten().A[0],marker='+',s=300)#绘制质心
        plt.show() #显示绘图区
            
        

        
            
            
            
    
    

    
    
