---
title: golang中实现np.frombuffer
date: 2020-09-09 17:39:37
tags:
- golang
---
最近项目全部从python转golang了，之前读图片从缓存读算法存储的buffer再用opencv转，在golang下也要实现相同的功能。
还遗留一个问题：binary.Read传的数组长度不能从变量获得

python代码：
```python
    img = np.frombuffer(imgBuffer, dtype=np.uint8).reshape(data["shape"])
    img =  img[:,:,::-1]
    newImg = Image.fromarray(img)
    newImg.save(filepath)
```

golang代码
```golang
    width := 1080
	height := 1920
	var imgArr [1080][1920][3]uint8 // how to gener array from width&height?
	buf := bytes.NewReader([]byte(imgByte))
	err := binary.Read(buf, binary.LittleEndian, &imgArr) 
	if err != nil {
		return "", err
	}

	img := image.NewRGBA(image.Rectangle{image.Point{0, 0}, image.Point{height, width}})
	for x := 0; x < width; x++ {
		for y := 0; y < height; y++ {
			cyan := color.RGBA{imgArr[x][y][0], imgArr[x][y][1], imgArr[x][y][2], 0xff}
			img.Set(y, x, cyan)
		}
	}
	enc := &png.Encoder{
		CompressionLevel: png.NoCompression,
    }
    f, err := os.Create(filepath)
	defer f.Close()
	err = enc.Encode(f, img)
```

