# map(float,iterable variation)
# map(float,[x for x in range(10)])  将变量映射成浮点数

#一些重要的写法：
#mat=dataset[nonzero(dataset[:,1]>value)[0],:]   返回第2列中值大于value的行
#matrix/array.tolist()  将矩阵或者数组转换成列表

#程序清单9-2
#for featIndex in range(n-1): 这里，dataset包括了特征向量和目标向量，其最后一列为目标向量，因此，这里需要用n-1
#for splitVal in set(dataSet[:,featIndex])   splitVal 不应该是连续的吗？dataset的第featIndex个特征，其值是标称型；回归树中所说的连续型，是指目标变量是连续的
#numpy.power(x1,2) 求x1的2次方

#程序清单9-3
#errorNoMerge=sum(power(lSet[:,-1]-tree['left'],2))+sum(power(rSet[:,-1]-tree['right'],2))  如果tree-right、tree-left是子节点，则求其总方差   两个子节点未合并前的总方差
#treeMean=(tree['left']+tree['right'])/2.0
#errorMerge=sum(power(testData[:,-1]-treeMean,2))
#errorMerge和errorNoMerge是在最后的一个分类上进行比较的，不需要追溯回最开始的地方
#tree里边存的是划分树的一些关键信息，而非实际的dataset；

#程序清单9-4
#x[:,1:n]=dataSet[:,0:n-1]   x矩阵的第一列存的是x0
#numpy库中的命令corrcoef(yHat,y,rowvar=0)用来求预测值与实际值的相关度，相关度越高，则模型效果越好；


#程序清单9-6 用于构建树管理器界面的Tkinter小部件
from numpy import *
from tkinter import * #构建GUI
import regTrees
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def reDraw(tolS,tolN): #后边会编写函数
    reDraw.f.clf()
    reDraw.a=reDraw.f.add_subplot(111)
    if chkBtnVar.get(): #如果选中模型树的话
        if tolN<2:tolN=2
        myTree=regTrees.createTree(reDraw.rawDat,regTrees.modelLeaf,regTrees.modelErr,(tolS,tolN)) #根据指定的规则创建树
        yHat=regTrees.createForeCast(myTree,reDraw.testDat,regTrees.modelTreeEval) #计算测试集的预测集
    else: #如果选中回归树
        myTree=regTrees.createTree(reDraw.rawDat,ops=(tolS,tolN))
        yHat=regTrees.createForeCast(myTree,reDraw.testDat)
    reDraw.a.scatter(reDraw.rawDat[:,0],reDraw.rawDat[:,1],s=5) #绘制样本集的散点图
    reDraw.a.plot(reDraw.testDat,yHat,linewidth=2.0) #绘制测试集的拟合曲线
    reDraw.canvas.show()
    
def drawNewTree(): #后边会编写函数
    tolN,tolS=getInputs()
    reDraw(tolS,tolN)

def getInputs():
    try:tolN=int(tolNentry.get())
    except:
        tolN=10
        print("enter Integer for tolN")
        tolNentry.delete(0,END)
        tolNentry.insert(0,'10')
    try:tolS=float(tolSentry.get())
    except:
        tolS=1.0
        print("enter Float for tolS")
        tolSentry.delete(0,END)
        tolSentry.insert(0,'1.0')
    return tolN,tolS

    
root=Tk()
#Label(root,text="Plot Place Holder").grid(row=0,columnspan=3) #绘制占位符 #在GUI界面显示textlabel标签


#matplotlib后端可以调用TkAgg，TkAgg可以在GUI框架上调用Agg，把Agg呈现在画布上，我们可以在Tk的GUI上放置一个画布，并用.grid()来调整布局
#以下为绘图code
reDraw.f=Figure(figsize=(5,4),dpi=100)
reDraw.canvas=FigureCanvasTkAgg(reDraw.f,master=root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row=0,columnspan=3) #将matplotlib绘的图放置在GUI中
#以上为绘图程序




Label(root,text="tolN").grid(row=1,column=0)
tolNentry=Entry(root) #可以用于用户输入信息  文本输入框
tolNentry.grid(row=1,column=1)
tolNentry.insert(0,'10')#隐式写入 #在文本框（用户输入信息的地方）开始位置处，插入内容  entry.insert(10,'内容一')在文本框第10个索引位置插入内容一

Label(root,text="tolS").grid(row=2,column=0)
tolSentry=Entry(root)
tolSentry.insert(0,'1.0')

Button(root,text="ReDraw",command=drawNewTree).grid(row=1,column=2,rowspan=3) #command为drawNewTree函数

chkBtnVar=IntVar() #用于定义字符串变量类型
chkBtn=Checkbutton(root,text="Model Tree",variable=chkBtnVar)
chkBtn.grid(row=3,column=0,columnspan=2)

reDraw.rawDat=mat(regTrees.loadDataSet('sine.txt')) #导入dataset #reDraw.rawDat是一个变量 
reDraw.testDat=arange(min(reDraw.rawDat[:,0]),max(reDraw.rawDat[:,0]),0.01) #以0.01为步长，min、max为极值构建数字列表   相当于testDat只有一列特征，根据这个特征来判定其目标变量，而rawDat有两个特征，利用reDraw可对其做散点图
#rawDat[:,0]特征1???
#testDat???

reDraw(1.0,10) #执行该函数

root.mainloop()

##########Entry的用法################
#from tkinter import *
#root=Tk()
#e=StringVar()  #是Tk库内部定义的字符串变量类型，在这里用于管理部件上面的字符；不过一般用在按钮button上。改变StringVar,按钮上的文字也随之改变
#entry=Entry(root,textvariable=e)
#e.set('input your text here')
#entry.pack()
#root.mainloop()

