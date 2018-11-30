---
title: numpy的使用
date: 2018-11-28 16:27:06
tags: 
- Python
categories: Python
---
向量、矩阵
```
import numpy as np
# 创建矩阵
matrix = np.array([[1, 4],
                   [2, 5]])
# 矩阵变形
matrix.reshape(1,4)   
# 矩阵的逆
np.linalg.inv(matrix)
# 返回对角线元素
matrix.diagonal()
# 创建矩阵的迹
matrix.diagonal().sum()
# 展开矩阵
matrix.flatten()
# 返回矩阵的秩
np.linalg.matrix_rank(matrix)
# 返回最大元素
np.max(matrix)
# 返回最小元素
np.min(matrix)
# 寻找每列的最大元素
np.max(matrix, axis=0)
# 查看行和列数
matrix.shape
# 查看元素数（行乘列）
matrix.size
# 查看维数
matrix.ndim
# 返回均值
np.mean(matrix)
# 返回方差
np.var(matrix)
# 返回标准差
np.std(matrix)

#将字典转换为矩阵
from sklearn.feature_extraction import DictVectorizer
data_dict = [{'Red': 2, 'Blue': 4},
             {'Red': 4, 'Blue': 3},
             {'Red': 1, 'Yellow': 2},
             {'Red': 2, 'Yellow': 2}]

# 创建 DictVectorizer 对象
dictvectorizer = DictVectorizer(sparse=False)
# 将字典转换为特征矩阵
features = dictvectorizer.fit_transform(data_dict)
# 查看特征矩阵的列名
dictvectorizer.get_feature_names()

```