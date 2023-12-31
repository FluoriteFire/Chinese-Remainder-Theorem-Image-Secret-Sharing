# 基于中国剩余定理的可视图像秘密共享
本项目基于中国剩余定理实现秘密共享，采用了Asmuth-Bloom共享方案，将原始图像生成多个子秘密以及对应的模值密钥，只要掌握的秘密数大于秘密分发者设定的k值，就可以还原出秘密图像。

---
## 使用介绍
### 秘密分发
将原始图像生成子秘密的代码为share.py，其中有几个重要参数，n:生成的子秘密图像个数、k:恢复原始图像所需要的秘密数、path:读取原始图像的路径以及生成子秘密图像的路径、imgname:想要打开的图像的名字。
#### 特殊说明
##### 1. 数值选取
由于算法限制，选取一个值 p ，秘密值 S 都要在模 p 的剩余类集合中选取，所以对于一个像素点的取值为8bits，即0-255，所以该 p 值应该选取256，然而后续选取的秘密模值需要大于选定的 p 值，因此就会大于256，最后生成的秘密值模上选取的秘密模值就会大于256，超过的像素点的取值，从而无法生成图像。

所以，选取的最大的秘密模值不能大于256，但是这样秘密值的选取就必定小于比所有的秘密模值都小的 p 值，因此解决方案是将一个像素8bits拆分为2个4bits，即最大值取16，这样一来只需要取 p 值为16即可满足所有秘密值选取都在模 p 的剩余类集合中。

数据扩展后，需要将图像的一个维度翻倍，这里选取了图像的宽度

##### 2. 秘密模值的选取
由于 p 值选取了16，而后面秘密模值的选取要求每个都需要两两互素，因此这里进行了简单的取巧，只选取素数作为秘密模值，从而可以轻松满足该条件。

然后是秘密值重构要求的恢复原始图像所需要的秘密数 k 值，需要满足
```
0 * n-k+2 * ··· * n < 1 * ··· * k
# 此处取值为数组下标，其中0代表 p 值
```
而右边第1个秘密模值乘到第k个秘密模值就是秘密恢复条件的关键。

##### 3. 随机数alpha的选取
在整个秘密共享方案中 alpha 的选取非常关键，是决定整个程序是否工作的主要因素。 alpha 的取值范围为 [0,r//16-1]

随机数 alpha 作用于秘密值 k 的生成
```
k = S + alpha * p
``` 
其中 S 是图像的像素值，取值为0-16，p 值为16固定。因此整个秘密值 k 由alpha决定。

在多次实验过程中发现，由于最后 k 需要模上选取的秘密模值，所以如果改值小于256则会使秘密加密变得没有意义，任意一张子秘密图像都可以恢复为原始图像。

因此我们设定 alpha 的最小值为16即可正常工作，即 
```
(0-16) + (16, ) * 16 >= 256
``` 
当然为了使秘密数大于k值即可解，需要满足 k 小于秘密模值1到k的累乘。

---
### 秘密恢复
读取多个子秘密图像并恢复原始图像的代码为recover.py，其中有2个参数需要使用，k:参与恢复图像的秘密图像数，path:子秘密图像的路径。
#### 特殊说明
##### 1. 中国剩余定理求解
在中国剩余定理中需要求逆元，这里选取了快速模求幂来求逆元，根据费马小定理
```
b^(p-1) = 1 ( mod p )
```
所以b的逆元就是b^(-1)即计算出b^(p-2)，通过快速模求幂可以快速求解。

##### 2. 秘密模值的读取
因为将秘密模值放在图片名读取，所以在读文件时，通过正则表达式截取文件名从而获得秘密模值。

##### 3. 秘密值恢复
计算时要首先计算出中国剩余定理的值，再模上公开值 p = 16 ， 如果直接模上16会导致中国剩余定理的计算出错。

---
## 原理分析
中国剩余定理的求解，其实是剩余类环的环同态和交换环导致的。

一次同余方程组，在其剩余类中，有且仅有一个解，但其实可以将结果视为一个一元一次方程：k = S + M * x ( x 为整数 )

因为秘密模值两两互素，所以对于任一大于模值的数，余数无法确定相同或者不相同，所以解出的结果 S 仅仅是在 M 的剩余类中的，如果真实的取值 k , 大于 M 的取值，那么就无法通过 S 来确定真实值 k 。

因此，知道的秘密数越多，即方程组的个数越多，那么秘密值的取值空间就越大，即 M 值越大，而在秘密值 k 的选取中,限定了K个秘密模值相乘作为最大值上限，即在此剩余类中取值，所以我们只需要知道 K 个或以上的秘密模值，那么相乘得到的 M 就必定大于其最大值上限，从而空间包含全部剩余类，从而计算出来的 S 就是真实值 k。

举例：如果在秘密生成时，选取 alpha 为0，那么秘密 k 的取值空间为 [0,15]，导致了任意一个秘密模值都大于其，这会使 S 总是等于 k ， 这样一来任意一张子秘密图像都可以恢复原始图像。