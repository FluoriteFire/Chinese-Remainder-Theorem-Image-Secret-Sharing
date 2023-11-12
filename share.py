from PIL import Image
import numpy as np
import random

# 生成从x到y的素数列表
def PrimesInRange(x, y):
    PrimesList = []
    for n in range(x, y):
        IsPrime = True
        for num in range(2, int(pow(n,0.5))):
            if n % num == 0:
                IsPrime = False
        if IsPrime:
            PrimesList.append(n)
    return PrimesList

def GetPrimes(n,k):
    # 生成素数列表，并从中取数
    PrimesList = PrimesInRange(200,255)
    # 判断是否生成满足的输出
    Flag = 1
    Primes = []
    while(Flag):
        Temp = []
        # 生成n+1个素数
        Temp.append(16)
        while(len(Temp)<=n):
            t = random.choice(PrimesList)
            # 唯有不同才加入数组
            if t not in Temp:
                Temp.append(t)
        # 按顺序排序
        Temp.sort()
        # 计算是否满足中国剩余定理秘密共享的条件
        # 计算左边 0 * n-k+2 * ··· * n
        l = Temp[0]
        for i in Temp[n-k+2:n+1]:
            l *= i
        # 计算右边 1 * ··· * k
        r = 1
        for i in Temp[1:k+1]:
            r *= i
        # 判断是否满足条件
        if(l < r):
            Flag = 0
            Primes = Temp
            return r,Primes
    

# 读取图片返回1维数组和原数组长宽
def read_image(path):
    img = Image.open(path).convert('RGB') 
    ImgArray = np.asarray(img)
    # img.show()
    # print(ImgArray.shape)
    Array = ImgArray.flatten()
    # 将每个256的像素拆成2个16的,因为16*16=256
    List = []
    for i in Array:
        List.append(i//16)
        List.append(i%16)
        # 原值 = n%16 + 16*(n//16)
    List = np.asarray(List)
    # print(List.shape)
    # 将数组转化为1维，并且记下数组的长宽就可以恢复
    return List, ImgArray.shape

# 生成秘密数
def GetSecret(r,ImgArray):
    Num = len(ImgArray)
    # 生成从1到Max的随机数，数组长度为ImgArray的长度，即秘密值的个数
    # print(r)
    # print(r//16-1)
    alpha =np.random.randint(16,r//16-1,Num)
    # print(alpha.shape)
    S = []
    for i in range(0,Num):
        while(ImgArray[i] + alpha[i]*16 < 255):
            alpha[i] = random.randint(16,r//16-1)
        S.append(ImgArray[i] + alpha[i]*16)
    # print(ImgArray[1] + alpha[1]*Primes[0])
    # print(r)
    S = np.asarray(S)
    # print(S.shape)
    return S

# 生成子秘密
def GetData(S,Primes):
    Data = []
    for p in Primes:
        Temp = []
        for Secret in S:
            Temp.append(Secret % p)
        Data.append(Temp)
    return Data

# 分配秘密图像
def GetImage(path,Data,Primes,Shape):
    # 将图片尺寸扩展为原来的两倍
    Shape = list(Shape)
    Shape[0] *= 2
    # print(Shape)
    # 将数据分配为图像
    for i in range(1,len(Data)):
        Img = np.array(Data[i]).reshape((Shape[0],Shape[1],Shape[2]))
        # print(Img.shape)
        Img = Image.fromarray(Img.astype('uint8')).convert('RGB')
        # Img.show()
        Img.save(path+str(Primes[i])+".png",quality=100)

if __name__ == "__main__":
    n = 5
    k = 4
    path = "./img/"
    imgname = "test3.jpg"

    # import time
    # T1 = time.time()
    ImgArray, Shape = read_image(path+imgname)
    # T2 = time.time()
    # print((T2 - T1)*1000)
    r,Primes = GetPrimes(n,k)
    # T3 = time.time()
    # print((T3 - T2)*1000)
    S = GetSecret(r,ImgArray)
    # T4 = time.time()
    # print((T4 - T3)*1000)
    Data = GetData(S,Primes)
    # T5 = time.time()
    # print((T5 - T4)*1000)
    GetImage(path,Data,Primes,Shape)
    # T6 = time.time()
    # print((T6 - T5)*1000)