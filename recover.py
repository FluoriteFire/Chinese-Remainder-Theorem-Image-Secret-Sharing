from PIL import Image
import numpy as np
import re

# 读取图片,图片名就是子秘密的模值
def ReadImage(path):
    # 通过正则表达式找到图片名
    item = re.findall(r"\/(\d+)\.",path)
    # 打开图片存为数组
    img = Image.open(path).convert('RGB')
    ImgArray = np.asarray(img)
    Array = ImgArray.flatten()
    # 返回子秘密的模值, 数组, 图片的长宽
    return int(item[0]), Array, ImgArray.shape

# 快速模求幂
def FastExpMod(b,e,m):
    result = 1
    # 当指数为0时结束
    while(e != 0):
        # 判断最低位
        if(e&1 == 1):
            result = (result * b) % m
        # 移位e,迭代计算b
        e >>= 1
        b = (b*b)%m
    return result

# 根据中国剩余定理计算秘密值
def GetOrigin(Arrays,M,MList,NList,k):
    Num = len(Arrays[0])
    Origin = []
    # 遍历数组每一个值
    for i in range(0,Num):
        n = 0
        # 遍历k个子秘密
        for j in range(0,k):
            # 通过中国剩余定理计算
            n += Arrays[j][i] * MList[j] * NList[j]
            n %= M
        n %= 16    
        Origin.append(n)
    return Origin    
     
# 数组转化为图片   
def OriginToImage(Origin,Shape):
    Data = []
    flag = 1
    n = 0
    for i in Origin:
        if(flag == 1):
            n = 16 * i
            flag = 2
        elif(flag == 2):
            n += i
            Data.append(n)
            n = 0
            flag = 1
    # print(len(Data))
    Shape = list(Shape)
    Shape[0] //= 2
    Img = np.array(Data).reshape((Shape[0],Shape[1],Shape[2]))
    Img = Image.fromarray(Img.astype('uint8')).convert('RGB')
    #Img.show()
    Img.save("Origin.png",quality=100)

if __name__ == "__main__":
    k=4
    path = [
                "./img/211.png",
                "./img/227.png",
                "./img/239.png",
                "./img/241.png"
            ]
    Arrays = []
    Shape = None
    flag = False
    Allp = []
    MList = []
    NList = []
    for pathitem in path:
        p,array,shape = ReadImage(pathitem)
        Allp.append(p)
        Arrays.append(array)
        if(flag == False):
            Shape = shape
        else:
            if(Shape != shape):
                print("尺寸不一样")
    # 将数据扩展为int64防止数据溢出
    Arrays = np.array(Arrays, dtype=np.int64)
    M = 1
    for i in range(0,k):
        M *= Allp[i]

    for i in range(0,k):
        MList.append(M // Allp[i])
        NList.append(FastExpMod(M // Allp[i],Allp[i]-2,Allp[i]))

    Origin = GetOrigin(Arrays,M,MList,NList,k)
    OriginToImage(Origin,Shape)