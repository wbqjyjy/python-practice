def square(n):#打印边长为n的正方形
    e = -n //2
    for i in range(e,n+e): #注意对称思想的使用
        if i == e or i == (n+e-1):
            print('*'*n)
        else:
            print('*'+''*(n-2)+'*')
