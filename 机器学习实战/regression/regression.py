#from numpy import *
#linalg.det(matrix) 计算行列式的值
#matrix.T  转置矩阵
#matrix.A  变为数组
#matrix.I  求逆矩阵
#linalg.solve(matrix,matrix1*matrix2) 求解矩阵乘积
#matrix.flatten()  将矩阵所有行都写入一行，输出结果依然为一个矩阵
#matrix.flatten().A[0]  将矩阵转化为数组，并且输出数组的第一行
#numpy.eye(N,M=None,k=0,dtype=<type 'float'>)  输出对角矩阵
#xSort=xMat[srtInd][:,0,:]  [:,:,:]表示去所有，[:,0,:]表示中间的行中行取第一个元素
#var(matrix,0)  以行计算样本方差
#import json   json模块可以将字符串形式的json数据转化为字典，也可以将Python中的字典数据转化为字符串形式的json数据
#lgx1[:,1:5]=mat(lgx) 将lgx1的第1到第5列赋值为lgx矩阵值
#random.shuffle()  将序列的所有元素随机排列

#程序8-6
# yEst=matTestX * mat(wMat[k,:]).T+mean(trainY)
# bestWeights=wMat[nonzero(meanErrors==minMean)]   nonzero(arrayb) 返回数组元素不为0的下标的列表

#岭回归中:
#xMat=(xMat-xMeans)/xVar
#yMat=yMat-yMean
#因此在得出的结果中：w=(XXT+aI)-1*XTy,测得的w比未标准化多了xVar倍，因此，要w/xVar
#而得到的测量结果，由于由于在测w时，y值已经减去其平均值，因此，截距比原来少了yMean，为了还原数据需做如下处理：
# weight=w/xVar
# compute result=result+yMean
