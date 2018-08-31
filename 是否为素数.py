def isprime(n):#判断是否为素数：只能被1和自己整除的数
    for i in range(2,n,1):
        if n % i == 0:
            print('no')
    print('yes')
    
