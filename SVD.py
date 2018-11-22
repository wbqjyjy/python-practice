#linalg.norm(vector1-vector2) #求范数

def pearsSim(inA,inB):
    if len(inA)<3:return 1.0 #如果向量的长度<3，则二者完全相关？？？
    return 0.5+0.5*corrcoef(inA,inB,rowvar=0)[0][1] #rowvar=0,采用列向量的方式计算相似度
#(x1,x2) (y1,y2)两个向量完全相关，是因为他们都在同一平面；
#而如果(x1,x2,x3) (y1,y2,y3)则这两个向量可能不在同一个平面，(x1,x2,0) (0,y2,y3)

#利用物品相似对  进行推荐
def standEst(dataMat,user,simMeas,item):#数据集，用户编号，相似度计算方法，物品编号  该函数主要是根据物品相似度(item,j)，以及特定user对各物品的评分，来推断出user可能对物品Item的评分
    n=shape(dataMat)[1] #物品数量
    simTotal=0.0 #？？？
    ratSimTotal=0.0

    for j in range(n):
        userRating=dataMat[user,j] #用户对物品j的评分
        if userRating == 0: continue
        overLap=nonzero(logical_and(dataMat[:,item].A>0,dataMat[:,j].A>0))[0]  #检测物品j与物品item的用户评价，如果一个用户同时对这两个物品进行了评分，则返回这些用户的列表

        if len(overLap)==0:similarity=0 #如果没有用户同时对这两个物品进行评价，则这两个物品的相似度记为0
        else:
            similarity=simMeas(dataMat[overLap,item],dataMat[overlap,j]) #计算这两个物品的相似度
        #print('the %d and %d similarity is:%f'%(item,j,similarity))

        simTotal += similarity #计算不同物品与item的相似度，并将这些相似度进行累加
        ratSimTotal += similarity * userRating # sum(物品Item与物品J的相似度*用户对J的评分）
    if simTotal ==0:return 0 #如果其他物品与物品item均没有相似度，返回0
    else:return ratSimTotal/simTotal #否则返回 sum(相似度（item,j)*用户评分j)/总得相似度= 用户可能对item的评分

#这里是以 物品相似度（列向量）来实现系统推荐，物品相似度以列向量来计算，每一个物品的列向量为各个用户的评分，最后一个公式解读：通过计算物品j与物品item的相似度，以及用户对j的评分，从而推断出用户可能对物品item的评分；
        
#注意: a=array(a)  b=nonzero(a[:]==0)[0]   nonzero中参数应该是numpy中的数组array 


#基于SVD的评分估计
def svdEst(dataMat,user,simMeas,item): #数据，客户编号，相似度计算方法，物品编号
    n=shape(dataMat)[1] #物品数量
    simTotal=0.0
    ratSimTotal=0.0
    U,Sigma,VT=la.svd(dataMat) #进行SVD分解
    sig4=mat(eye(4)*Sigma[:4]) #构建奇异值矩阵
    xformedItems=dataMat.T*U[:,:4]*sig4.I #利用U矩阵将物品转换到低维空间中  [n*m]*[n*4]*[4*4]=[n*4]  相当于是减少了用户个数！！！
    for j in range(n):
        userRating=dataMat[user,j] #特定用户对物品J的评分  用户评分是从原始数据中获得的 特定用户对特定物品的评分
        if userRating==0 or j==item:continue
        similarity=simMeas(xformedItems[item,:].T,xformedItems[j,:].T) #xformedItems每一行为一个物品  物品向量里边无论还有没有用户user都没有关系，物品向量只会用来评价物品相似度，而用户user评分可以从原数据中提取
        simTotal += similarity
        ratSimTotal += similarity * userRating #相似度<j,item>*评分<j>
    if simTotal == 0:return 0
    else: return ratSimTotal/simTotal  #返回用户对Item评分的预测值

#上述程序中，并没有保存物品相似度的计算值，因此，没预测一个item的用户评分，就需要重新计算各物品之间的相似度，在实际中，一般离线计算并保存相似度的计算值；

#基于SVD的图像压缩

def imgCompress(numSV=3,thresh=0.8):
    myl=[]
    for line in open('0_5.txt').readlines():
        newRow=[]
        for i in range(32):
            newRow.append(int(line[i])) #将每一行的字符添加到newRow列表
        myl.append(newRow)#将文件中的所有行导入到myl列表
    myMat=mat(myl) #将文件中的数据转为matrix
    printMat(myMat,thresh) #打印矩阵，当矩阵元素>thresh时，赋值为1，否则为0
    U,Sigma,VT=la.svd(myMat) #对原始矩阵进行SVD分解
    SigRecon=mat(zeros((numSV,numSV))) #根据用户需要的奇异值个数numSV，来创建0矩阵
    for k in range(numSV):
        SigRecon[k,k]=Sigma[k] #创建具有numSV个奇异值的奇异矩阵
    reconMat=U[:,:numSV]*SigRecon*VT[:numSV,:] #以numSV个奇异值，重新构建原矩阵
    printMat(reconMat,thresh) #打印重构的矩阵
    
    
    
