---
title: 特征工程_Filter过滤法
date: 2019-05-24 17:36:09
tags:
- 机器学习
categories: 机器学习
---
1. 流程
    - 特征提取
    - 特征创造
    - 特征选择：过滤->嵌入/包装/降维

2. Filter过滤法
    1. 方差过滤
        这是通过特征本身的方差来筛选特征的类。比如一个特征本身的方差很小，就表示样本在这个特征上基本没有差异，可能特征中的大多数值都一样，甚至整个特征的取值都相同，那这个特征对于样本区分没有什么作用。所以无论接下来的特征工程要做什么，都要优先消除方差为0的特征。
        ```
            from sklearn.feature_selection import VarianceThreshold
            selector = VarianceThreshold(threshold=0) #阈值，抛弃所有低于阈值的特征
            X_var0 = selector.fit_transform(X)  
        ```
        影响：最近邻算法KNN，单棵决策树，支持向量机SVM，神经网络，回归算法，都需要遍历特征或升维来进行运算，所以他们本身的运算量就很大，需要的时间就很长，因此方差过滤这样的特征选择对他们来说就尤为重要。但对于不需要遍历特征的算法，比如随机森林，它随机选取特征进行分枝，本身运算就非常快速，因此特征选择对它来说效果平平。
    2. 相关性过滤
        1. 卡方过滤
            - 卡方过滤是专门针对离散型标签（即分类问题）的相关性过滤。
            - 卡方检验类feature_selection.chi2计算每个非负特征和标签之间的卡方统计量，并依照卡方统计量由高到低为特征排名。再结合feature_selection.SelectKBest这个可以输入”评分标准“来选出前K个分数最高的特征的类。
            ```
                from sklearn.feature_selection import SelectKBest
                from sklearn.feature_selection import chi2
                #假设需要300个特征
                X_fschi = SelectKBest(chi2, k=300).fit_transform(X_fsvar, y)
            ```
            - 定义超参数K的值
                - 学习曲线
                - 看p值选择K
                    卡方检验的本质是推测两组数据之间的差异，其检验的原假设是”两组数据是相互独立的”。卡方检验返回卡方值和P值两个统计量，其中卡方值很难界定有效的范围，而p值，我们一般使用0.01或0.05作为显著性水平
                    - P<=0.05/0.01: 拒绝原假设，接受备择假设 
                    - p>0.05/0.01 : 接受原假设

                    从特征工程的角度，我们希望选取卡方值很大，p值小于0.05的特征，即和标签是相关联的特征。
                    ```
                        chivalue, pvalues_chi = chi2(X_fsvar,y)
                        # k取多少？我们想要消除所有p值大于设定值，比如0.05或0.01的特征：
                        k_ = chivalue.shape[0] - (pvalues_chi > 0.05).sum()
                        X_fschi = SelectKBest(chi2, k=k_).fit_transform(X_fsvar, y)
                    ```
        2. F检验
            - 是用来捕捉每个特征与标签之间的线性关系的过滤方法。它即可以做回归(feature_selection.f_regression)也可以做分类(feature_selection.f_classif)。
            - 和卡方检验一样，这两个类需要和类SelectKBest连用.
            - F检验在数据服从正态分布时效果会非常稳定，因此如果使用F检验过滤，我们会先将数据转换成服从正态分布的方式。
            - F检验的本质是寻找两组数据之间的线性关系，其原假设是”数据不存在显著的线性关系“。它返回F值和p值两个统计量。和卡方过滤一样，我们希望选取p值小于0.05或0.01的特征，这些特征与标签时显著线性相关的。
            ```
                from sklearn.feature_selection import f_classif
                F, pvalues_f = f_classif(X_fsvar,y)
                k_ = F.shape[0] - (pvalues_f > 0.05).sum()
                X_fsF = SelectKBest(f_classif, k=k_).fit_transform(X_fsvar, y)
            ```

        3. 互信息法
            - 互信息法是用来捕捉每个特征与标签之间的任意关系（包括线性和非线性关系）的过滤方法。和F检验相似，它既可以做回归也可以做分类，并且包含两个类feature_selection.mutual_info_classif（互信息分类）和feature_selection.mutual_info_regression（互信息回归）。
            - 互信息法不返回p值或F值类似的统计量，它返回“每个特征与目标之间的互信息量的估计”，这个估计量在[0,1]之间取值，为0则表示两个变量独立，为1则表示两个变量完全相关。
            ```
                from sklearn.feature_selection import mutual_info_classif as MIC
                result = MIC(X_fsvar,y)
                k_ = result.shape[0] - sum(result <= 0)
                X_fsmic = SelectKBest(MIC, k=k_).fit_transform(X_fsvar, y)
            ```
3. 总结

| 参数   | 说明 | 超参数配置
| :-------- | --- | -------- |
| VarianceThreshold   | 方差过滤，可输入方差阈值，返回方差大于阈值的新特征矩阵         | 一般使用0/1筛选，可以画学习曲线 |
| SelectKBest         | 用来选取K个统计量结果最佳的矩阵，生成符合统计量要求的新特征矩阵 | 看配合使用的统计量 |
| chi2                | 卡方验证，专用于分类算法                         | 追求p小于显著性水平的特征 |
| f_classif           | F检验分类，只能捕捉线性相关，要求数据服从正态分布    | 追求p小于显著性水平的特征 |
| f_regression        | F检验回归，只能捕捉线性相关，要求数据服从正态分布    | 追求p小于显著性水平的特征 |
| mutual_info_classif | 互信息分类，可以捕捉任何相关性，不能用于稀疏矩阵     | 追求互信息大于0的特征   |
| mutual_info_regression| 互信息回归，可以捕捉任何相关性，不能用于稀疏矩阵   | 追求互信息大于0的特征   |
 
 参考：
[Filter过滤法](https://www.cnblogs.com/zhange000/articles/10750903.html) 