---
title: Python灰度图转伪彩色图
date: 2019-01-10 10:02:47
tags: 
- Python
categories: Python
---
因项目中算法给出分割图是灰度图，而前端需要展示彩色图，搜了下网上资料，参考了opencv写的[这篇](http://blog.sina.com.cn/s/blog_8924265b0101ext1.html)，改成了Python代码
效果：
原灰度图
![灰度图](0.png)
伪彩色图
![彩色图](1.png)

```
    from PIL import Image
    import requests
    from io import BytesIO
    import numpy as np
    def grayImageTrans(url):
        # url
        # 如果是本地图片
        # img = Image.open('/tmp/test.jpg')
        file = requests.get(url)
        tmpIm = BytesIO(file.content)
        img = Image.open(tmpIm)
        # 图片转矩阵
        img = np.array(img)
        # nparray转list
        imgAry = img.tolist()
        tmp=0
        # 加颜色
        for x in range(img.shape[0]):
            for y in range(img.shape[1]):
                tmp = imgAry[x][y]
                imgAry[x][y] = __grayColorTrans(tmp)
        newImgAry = np.array(imgAry)
        # 矩阵转图片
        newImg = Image.fromarray(np.uint8(newImgAry))
        # newImg.save('/vagrant/test.png')
        # 转base64
        output_buffer = BytesIO()
        newImg.save(output_buffer, format='PNG')
        byte_data = output_buffer.getvalue()
        base64_str = base64.b64encode(byte_data)
        return base64_str
```
参考：
关于Image与Base64转换可以看[这里](https://www.jianshu.com/p/2ff8e6f98257)
[Image图像的convert](https://my.oschina.net/112612/blog/1594140)