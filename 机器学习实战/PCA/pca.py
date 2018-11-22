from numpy import *
#特征值、特征向量都是对于方阵而言的
def pca(dataMat,topNfeat=9999999):#第二个参数：应用的N个特征
    meanVals=mean(dataMat,axis=0) #axis=0以列求平均值
    meanRemoved=dataMat-meanVals #减去平均值
    covMat=cov(meanRemoved,rowvar=0) #rowvar=0表示每行为一个样本，cov()求协方差
    eigVals,eigVects=linalg.eig(mat(covMat)) #求协方差矩阵的特征向量和特征值
    eigValInd=argsort(eigVals) #对特征值进行排序，从小到大，并返回对应的index号
    eigValInd=eigValInd[:-(topNfeat+1):-1] #List的切片功能   a[1:4:2]->[起始指标：终止指标：跳跃步长]
    redEigVects=eigVects[:,eigValInd] #返回前n个最大特征值所对应的特征向量  所有行，eigValInd列

    #第一个式子不是将特征缩减到eigValInd，然后就可以直接用这些特征做一些机器学习吗？
    lowDDataMat=meanRemoved * redEigVects #对元数据进行转化； 以n个特征向量为坐标系，将数据转化到新空间
    #第二个式子 重构是什么意思？？？
    reconMat=(lowDDataMat * redEigVects.T)+meanVals #将转化后的数据在进行重构，用于测试？？？
    
    return lowDDataMat,reconMat

#numpy.isnan() 判断数据是否为缺失值
#isnan(data[:,i].A)
#~isnan() 与 isnan()相反
