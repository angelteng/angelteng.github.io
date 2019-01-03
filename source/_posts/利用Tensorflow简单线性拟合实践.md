---
title: 利用Tensorflow简单线性拟合实践
date: 2018-12-04 11:39:14
tags: 
- Tensorflow
- Python
categories: Python
---
```
import tensorflow as tf
import numpy as np
from sklearn import datasets
from sklearn.model_selection import train_test_split 

print(tf.__version__)

# 流程：
# 1. 数据处理
# 2. 选择模型
# 3. 训练模型
# 4. 模型评估
# 5. 调整参数

iris = datasets.load_iris() # sk自带了的鸢尾花数据集（含有三种鸢尾花，有四种特征数据）

# 载入数据，划分训练/测试集（20%）
train_X, test_X, train_y, test_y = train_test_split(iris.data, iris.target, test_size = 0.2, random_state = 0)

# 所有特征都是实数值
# shape是特征值数量
feature_name = "flower_features"
feature_columns = [tf.feature_column.numeric_column(feature_name, 
                                                    shape=[4])]

classifier = tf.estimator.LinearClassifier(
    feature_columns=feature_columns,
    n_classes=3,
    model_dir="/tmp/iris_model")


# 输入函数，讲导入的数据转换为TensorFlow数据类型
def input_fn(set_split='train'):
    def _fn():
        if set_split == "test":
            features = {feature_name: tf.constant(test_X)}
            label = tf.constant(test_y)
        else:
            features = {feature_name: tf.constant(train_X)}
            label = tf.constant(train_y)
        return features, label
    return _fn


# 训练（拟合）模型
classifier.train(input_fn=input_fn(),
                 steps=1000)
print('fit done')


# 评估准确率
accuracy_score = classifier.evaluate(input_fn=input_fn('test'), 
                                     steps=100)["accuracy"]
print('\nAccuracy: {0:f}'.format(accuracy_score))
```

