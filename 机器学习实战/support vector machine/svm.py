def clipAlpha(aj,H,L):  #目的？？？
    if aj>H:
        aj=H
    if L>aj:
        aj=L
    return aj

def smoSimple(dataMatIn,classLabels,c,toler,maxIter):
    dataMatrix=mat(dataMatIn) #将输入sample data转为矩阵
    labelMat=mat(classLabels).transpose() #将标签项转为矩阵并转置
    b=0 #初始化b值
    m,n=shape(dataMatrix) #m,n分别为样本量和参数个数
    alphas=mat(zeros((m,1))) #将alpha初始化为0，m个alpha（=样本量）
    iter=0 #初始化迭代次数
    while (iter<matIter):#程序迭代次数
        alphaPairsChanged=0 #查看alphas是否得到优化的变量
        for i in range(m):#循环遍历alpha-i,找到违反KKT条件严重的点，首先先查看“支持向量”是否违反KKT条件，然后在查看其它点
            fXi=float(multiply(alphas,labelMat).T*\
                      (dataMatrix*dataMatrix[i,:].T))+b #样本点xi的“预测分类标签”   label=AnXnYn*xi+b
            Ei=fXi-float(labelMat[i]) #样本实际的标签 与 预测标签 之间的误差，
            #如果alpha参数为0或C，说明他们已经被调整过了，不需要优化
            #否则，对于介于0和C之间的alpha,如果：
            #alpha<C and yig(xi)<=1
            #alpha>0 and yig(xi)>=1
            #则alpha需要优化
            if ((labelMat[i]*Ei< -toler) and (alphas[i]<C)) or\ 
               ((labelMat[i]*Ei > toler) and (alpahs[i]>0)):
                j=selectJrand(i,m) #选取另外一个alphas
                fXj=float(multiply(alphas,labelMat).T*
                          (dataMatrix*dataMatrix[j,:].T))+b #获取样本j的预测标签
                Ei=fXj-float(labelMat[j])#求样本点j的实际标签与预测标签之间的误差
                alphaIold=alphas[i].copy() #保留i,jalpha的原始值，注意，这里需要用.copy(),如果直接复制alpha[i]的话，变量会直接引用alpha[i]，即，会链接到alpha[i]的保存地址，当重新赋值alphaIold时，alpha[i]会同时发生改变
                alphaJold=alphas[j].copy()
                #计算alpha的边界值：L和H
                if (labelMat[i] != labelMat[j]):#当两个样本标签不同时，计算此时的L和H
                    L=max(0,alphas[j]-alphas[i])
                    H=min(C，C+alphas[j]-alphas[i])
                else:#当样本标签相同时，计算此时的L和H
                    L=max(0,alphas[j]+alphas[i]-C)
                    H=min(C,alphas[j]+alphas[i])
                if L==H:print("L==H"); continue #跳出本次循环，继续下一轮内循环，寻找新的优化参数alpha
                eta=2.0*dataMatrix[i:]*dataMatrix[j:].T-\ #alpha=alpha-old+label(E1-E2)/(K11+K22-2K12)； eta=2K12-K11-K22
                     dataMatrix[i,:]*dataMatrix[i,:].T-\
                     dataMatrix[j,:]*dataMatrix[j,:].T
                if eta>=0:print("eta>=0");continue #如果eta为0，则退出本次循环，直接开始下一次循环。  此时是否应该去掉eta>0？？？
                alphas[j]-=labelMat[j]*(Ei-Ej)/eta #根据公式计算alpha的值（未受约束）
                alphas[j]=clipAlpha(alphas[j],H,L) #根据情况，选取alpha的最终值
                if(abs(alphas[j]-alphaJold)<0.00001):print("j not moving enough");continue #如果alpha值的变化太小，则进行下一次循环
                alphas[i]+=labelMat[j]*labelMat[i]*(alphaJold-alphas[j]) #计算另一个alpha的值
                #根据b的计算公式，分别求用两个alpha计算得到的b值
                b1=b-Ei-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[i,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2=b-Ej-labelMat[i]*(alphas[i]-alphaIold)*dataMatrix[i,:]*dataMatrix[j,:].T-labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[j,:]*dataMatrix[j,:].T
                if(0<alpahs[i]) and (C>alphas[i]):b=b1 #如果0<alpha<C，求得的b可以优化，赋值b
                elif (0<alphas[j]) and (C>alphas[j]):b=b2
                else:b=(b1+b2)/2.0 #如果alpha=0 或 C,取平均值
                alphaPairsChaged +=1 #此时，成功迭代一次，使得目标函数得到优化，alpha成功改变
                print("iter:%d i:%d,pairschanged %d"%(iter,i,alphaPairsChaged))
        if (alphaPairsChaged==0):iter +=1 #如果这次迭代，没能是alpha成功改变，则迭代次数增加1次，直到Maxiter，如果还是没有优化成功，则停止
        else:iter=0
        print("iteration number:%d"% iter)
    return b,alphas #返回求得的优化值，alpha为一个列表

#如果for循环中，但凡有两个alpha值发生改变，则记做一次循环，当循环maxiter后，停止循环；
#相反，如果for循环中，没有改变alpha，则Iter依然记为0；直到alpha改变的次数达到maxiter后，才停止循环；
#最后，返回优化后的参数；


#完整版的SMO
class optStruct:
    def __init__(self,dataMatIn,classLables,c,toler):
        self.X=dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=shape(dataMatIn)[0]
        self.alphas=mat(zeros((self.m,1)))
        self.b=0
        self.eCache=mat(zeros((self.m,2))) #误差缓冲，第一列给出的是是否有效的标志位，第二列给出的是实际的误差值；这里的有效意味着他已经计算好了；
#选择第二个alpha
    def selectJ(i,oS,Ei): #oS指的是什么？？？
        maxK=-1 #第二个alpha样本的序列号
        maxDeltaE=0 #两个样本误差差的最大值
        Ej=0 #第二个alpha样本的误差
        oS.eCache[i]=[1,Ei] #第I个样本的误差值
        
        validEcacheList= nonzero(oS.eCache[:,0].A)[0] # eCache[:,0].A是什么意思：将矩阵变为数组；连起来就是：选出eCache中所有行中的第一列，并将其转化为数组，在这里，第一行存放有效标志符，nonzero()会将非0的样本的序列号返回，这里非0指的是E值有效，为非0值        
        if(len(validEcacheList))>1:#如果存在非零E值的话
            for k in validEcacheList:
                if k==i:continue #如果k与所选第一个alpha-i重合，则进行下一个循环
                Ek=calcEk(oS,k) #返回所选样本k的误差
                deltaE=abs(Ei-Ek) #保存两个样本误差差
                if(deltaE>maxDeltaE):#如果差值大于目前所存的最大差值，
                    maxK=k #保留该序列号
                    maxDeltaE=deltaE #保留目前最大差值
                    Ej=Ek #保留该样本误差
            return maxK,Ej #返回样本序列，及误差值
        else:#如果不存在非零E值
            j=selectJrand(i,oS.m)#则从除i以外的样本中随机选择一个alpha-j
            Ej=calcEk(oS,j)#计算j的误差
        return j,Ej #将选择的第二个alpha序列，及其误差返回


#完整版Platt SMO的外循环代码
    def smoP(dataMatIn,classLabels,c,toler,maxIter,kTup=('lin',0)):#kTup的作用？？？
        oS=optStruct(mat(dataMatIn),mat(classLabels).transpose(),C,toler)
        iter=0
        entireSet=True #首先第一遍先让程序遍历值，然后第二遍遍历边界值，并且如果遍历边界值可以改变alpha的话，则一直遍历边界值，否则，修改命令，遍历所有值；
        alphaPairsChaged=0
        while(iter<maxIter) and ((alphaPairsChaged>0) or (entireSet)): #如果没有达到迭代次数并且alpha有所修改，则循环；  或者，如果遍历所有值命令为True，则循环；如果alpha没有修改，并且依然选择遍历边界值，则停止循环
            alphaPairsChanged=0
            if entireSet: #遍历所有的值
                for i in range(oS.m):
                    alphaPairsChaged +=innerL(i,oS)
                print("fullSet,iter:%d i:%d,pairs chaged %d"%(iter,i,alphaPairsChanged))
                iter +=1 #遍历一次就iter+=1
            else:#遍历边界值（支持向量）
                nonBoundIs=nonzero((oS.alphas.A>0)*(oS.alphas.A<C))[0] #返回alpha在（0，C)之间的序列号
                for i in nonBoundIs:
                    alphaPairsChaged += innerL(i,oS)
                    print("non-bound, iter: %d i:%d,pairs changed %d"%(iter,i,alphaPairsChanged))
                iter += 1
            if entireSet:entireSet=False #如果命令为遍历所有值，则修改命令，遍历边界值
            elif (alphaPairsChanged ==0):entireSet=True #如果命令为遍历边界值，但是没有alpha改变，则遍历所有值
            print("iteration number: %d"% iter)
        return oS.b,oS.alphas

    #在简单版本里，当alpha没有变化，则将一次完整遍历看成一次迭代，否则iter=0,作用是，如果 达到迭代次数，但是alpha还没有改变，则停止循环
    #优化过程与书中简单版本唯一不同就是选择第二个alpha方式的不同，这样会大大加快计算速度。简单版中，alpha是随机选取，而优化版中，选取的alpha是误差不为0的alpha（证明它确实需要优化），而在简单版中，如果选取误差为0的alpha，则需要通过一系列计算，最后获取alpha优化前后差值，才能判断，他是否是第二个alpha,这样会大大增加程序运行时间
    def kernelTrans(X,A,kTup):#kTup保存核函数信息，第一个元素保存的是核函数类型，第二个是其它需要的信息
        m,n=shape(X) #矩阵X的行列
        K=mat(zeros((m,1))) #m行1列的值
        if kTup[0] == 'lin':K=X*A.T #A行数为n 如果为线性，则Kij
        elif kTup[0] =='rbf':#如果为高斯
            for j in range(m):
                deltaRow=X[j,:]-A # 一个样本减去另一个样本
                K[j]=deltaRow * deltaRow.T #构建高斯核函数分子部分
            K=exp(K/(-1 *kTup[1]**2)) #更新K的值为高斯核函数计算结果 kTup[1]中存储特定类型核函数所需要的一些值（用户自定义的输入）  在numpy中除号/意味着对矩阵展开计算，而matlab中则是计算矩阵的逆矩阵
        else：raise NameError('Houston We Have a problem that kernel is not recognized')
        return K

class optStruct:
    def __init__(self,dataMatIn,classLabels,C,toler,kTup):
        self.X=dataMatIn
        self.labelMat=classLabels
        self.C=C
        self.tol=toler
        self.m=shape(dataMatIn)[0]
        self.aphas=mat(zeros((self.m,1)))
        self.b=0
        self.eCache=mat(zeros((self.m,2)))
        self.K=mat(zeros((self.m,self.m))) #K指核函数矩阵
        for i in range(self.m):
            self.K[:,i]=kernelTrans(self.X,self.X[i,:],kTup) #将K第i列值用kernel值代替？？？ 为什么这么代替？？？ <Xi,Xj>计算，原来是XiXj，后将input转入高维空间，z=fi(x)=(f1(x),f2(x),f3(x)...fN(x)),原来kernel（Xi,Xj)的计算就变为kernel(Zi，Zj)的计算，但是Zi*Zj，可以转为计算函数g(Xi,Xj)的值，因此，利用核函数进行非线性转化时，不用关注映射函数fi，直接计算g(Xi,Xj)即可；
            #从这里也可以看出，核函数（正定核矩阵）指的是：最终的计算结果（利用核函数计算的值，所形成的矩阵）
            #这行代码指的是，第i行与各行计算的核函数值，将其存储在K的第i列；
    
    
    
                
    
                    
        
        

               

                
