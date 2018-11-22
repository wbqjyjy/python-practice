#分布式计算：mapper
import sys
from numpy import mat,mean,power

def read_input(file):
    for line in file:
        yield line.rstrip() #产生生成器， rstrip()删除字符串末尾的指定字符 , yield迭代的对象是行

input=read_input(sys.stdin) #注意函数参数为：sys.stdin,而用 file.txt>sys.stdin，又可以将file导入stdin
input=[float(line) for line in input] #第一行的Input是一个生成器，可以用来迭代
numInputs=len(input) #计算数据条数
input=mat(input) #将数据转为矩阵形式
sqInput=power(input,2)#求数据的平方
print("%d\t%f\t%f"%(numInputs,mean(input),mean(sqInput))
print>>sys.stderr,"report:still alive" #向主节点汇报，子节点依然正常工作


#python mrMeanMapper.py < inputFile.txt


#分布式均值和方差计算的Reduce
import sys
from numpy import mat,mean,power
def read_input(file):
      for line in file:
      yield line.rstrip()
input=read_input(sys.stdin)#读入数据
mapperOut=[line.split('\t') for line in input] #形成数据
cumVal=0.0
cumSumSq=0.0
cumN=0.0
for instance in mapperOut:
      nj=float(instance[0]) #第一个数据为mapper上的数据量
      cumN += nj #计算所有mapper上的数据总数
      cumVal += nj*float(instance[1]) #计算数据总和
      cumSumSq += nj*float(instance[2]) #计算数据平方和
mean=cumVal/cumN #计算平均值
varSum=(cumSumSq - 2*mean*cumVal + cumN*mean*mean)/cumN #计算方差
print("%d\t%f\t%f"%(cumN,mean,varSum))
print>>sys.stderr,"report:still alive"  #向主节点汇报

#python mrMeanMapper.py < inputFile.txt | python mrMeanReducer.py




########################################################################

#分布式均值方差计算的mrjob实现
from mrjob.job import MRJob
class MRmean(MRJob):
    def __init__(self,*args,**kwargs):
      super(MRmean,self).__init__(*args,**kwargs) #???
      self.inCount=0
      self.inSum=0
      self.inSqSum=0

      #接收输入数据流
    def map(self,key,val):#统计一个mapper上的数据个数，总和，平方和
      if False:yield #???
      inVal = float(val) #等于Mapper中的键值
      self.inCount += 1 #并入一条数据
      self.inSum += inVal #计算数据总和
      self.inSqSum += inVal*inVal #计算数据平方和
      
      #在所有输入数据到达后，开始处理
    def map_final(self): #一个Mapper上的数据的 （个数，平均值，方差）
      mn=self.inSum/self.inCount #计算所有数据的均值
      mnSq=self.inSqSum/self.inCount #计算所有数据平方的均值
      yield(1,[self.inCount,mn,mnSq]) #返回生成器   将mapper输出的数据的key值均设为1
      
    def reduce(self,key,packedValues): #packedValues相当于mapper输出的数据（num,mean,sqmean)   参数key设定默认接收的来自Mapper的数据(key,value)中的key为指定参数key；
      cumVal=0.0 
      cumSumSq=0.0
      cumN=0.0
      for valArr in packedValues:
       nj=float(valArr[0])
       cumN+=nj
       cumVal +=nj*float(valArr[1]) #数据总和
       cumSumSq += nj*float(valArr[2]) #数据平方和
      mean=cumVal/cumN  #数据平均值
      var=(cumSumSq -2*mean*cumVal + cumN*mean*mean)/cumN #数据方差
      yield(mean,var) #如果在该reduce之后，不是输出，而是运行另一条mapper，那么key值仍然需要赋值，像map_final中一样
      
    def steps(self):
      return([self.mr(mapper=self.map,reducer=self.reduce,mapper_final=self.map_final)]) #返回 return self.mr()???
      #定义执行的步骤
if __name__=='__main__':
      MRmean.run()


#pegasos算法实现
def predict(w,x):
      return w*x.T
def batchPegasos(dataSet,labels,lam,T,k):#T:迭代次数；k：待处理列表的大小
      m,n=shape(dataSet)
      w=zeros(n) #初始化权重值
      dataIndex=range(m) #数据索引值
      for t in range(1,T+1):#选择另一批样本进行下一次批处理
        wDelta=mat(zeros(n)) #初始化权重值
        eta=1.0/(lam*t) #学习率，代表权重调整的大小    相当于随机梯度下降中，每一次所走的步长
0]        random.shuffle(dataIndex) #将索引号随机打乱重排
        for j in range(k):#执行批处理  开始执行一次批处理   在这次批处理中处理k个样本
          i=dataIndex[j] #从原始样本中随机选择一个样本
          p=predict(w,dataSet[i,:]) #预测第i个数据的分类
          if labels[i]*p<1:#如果第I个样本分类预测错误
            wDelta += labels[i]*dataSet[i,:].A #更新步长的值：w += y*x
        w=(1.0-1/t)*w+(eta/k)*wDelta #第一批样本处理后，更新权重： 权重更新公式  每一次迭代时，更新一次权重w
      #在T次迭代后，返回w值
      return w
      

#程序清单15-6  分布式Pegasos算法的mapper和reducer代码
def map(self,mapperId,inVals):
      if False:yield
      if inVals[0]=='w' #如果inVals中第一个元素为'w'
        self.w=inVals[1] #将self.w赋值权重
      elif inVals[0]=='x':
        self.dataList.append(inVals[1])#样本编号；一次批处理的数据
      elif inVals[0]=='t':self.t=inVals[1] #迭代次数？？？
      
    def map_fin(self):
      #数据存储在磁盘上，当执行脚本时，通过label和X将数据导入到内存中  
      labels=self.data[:,-1] #标签    self.data是存放在硬盘上的？？？
      X=self.data[:,0:-1] #样本数据
      #这里，为什么要改变self.w???
      if self.w==0:self.w=[0.001]*shape(x)[1] #???
      for index in self.dataList:
        p=mat(self.w)*X[index,:].T #计算样本的标签
        if labels[index]*p<1.0:
          yield(1,['u',index]) #如果分类错误，则将该样本编号返回，mapper返回的Key值为1
      yield(1,['w',self.w])
      yield(1,['t',self.t])#返回权重，及迭代次数

    def reduce(self, _,packedVals):
      for valArr in packedVals:
        if valArr[0]=='u':self.dataList.append(valArr[1]) #将分类错误的样本编号加入dataList
        elif valArr[0]=='w':self.w=valArr[1] #保存上次的权重信息
        elif valArr[0]=='t':self.t=valArr[1] #保存迭代次数
      labels=self.data[:,-1]
      X=self.data[:,0:-1]
      wMat=mat(self.w)
      wDelta=mat(zeros(len(self.w))) #类似随机梯度下降中，步长的参数
      for index in self.dataList:
        wDelta += float(labels[index])*X[index,:] #根据这一批次分类错误的样本点，计算累积wDelta
      eta = 1.0/(2.0*self.t)
      wMat=(1.0-1.0/self.t)*wMat + (eta/self.k)*wDelta #重新计算这一批次样本遍历后，wMat的新值
      #下面代码作用   将reduce输出  连入到   mapper输入中
      for mapperNum in range(1,self.numMappers+1):
        yield(mapperNum,['w',wMat.tolist()[0]]) #这里注意tolist的用法，是将Matrix或者array转为list,对于一维矩阵 a=[1,2,3] a=mat(a) a.tolist()[0]，注意不能丢掉[0]
        if self.t<self.options.iterations:
            yield(mapperNum,['t',self.t+1])
            #相当于是将一批数据k，分到numMappers个mapper上进行处理，然后根据每个mapper返回得数据都会对权重进行一次更新，相当于一批数据，会对权重进行k/numMapper次的更新；
            for j in range(self.k/self.numMappers): #numMappers为mapper的个数   k/numMappers 可以理解为  将一批数据 分成几份，分给各个mapper
                yield(mapperNum,['x',random.randint(shape(self.data)[0])]) #通过不同的mapper编号mapperNum，数据会被分送到各个mapper中   批处理数据：为随机分配的k个数据，那这里不应该限定数据编号个数吗？
                                                                           #答：每次输出的是一个数据


