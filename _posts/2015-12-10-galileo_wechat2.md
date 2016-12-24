---
layout: post
title: Galileo开发板+opencv+微信公众平台实现简单的物联网家庭监控(2)  
tags: intel galileo django python 服务器 docker IoT linux 
categories: 服务器 嵌入式
---


紧接上篇文章(《Galileo开发板+微信公众平台实现简单的物联网家庭监控》( http://blog.jcix.top/2015-11-27/galileo_wechat/ ) )，
以下功能做了改进：
* 实现了Galileo开发板上用USB摄像头+python版opencv监控并通过微信公众平台进行异常报警的功能。
* 通过connman实现了wifi网络的自动连接和随时修改功能。
* 通过post到服务器，实现了微信控制led灯亮、灭或者光控的功能。

## 视频监控功能的实现
(完整代码在github: https://github.com/zhangjaycee/galileo_pys/blob/master/cam_wechat.py )
### 1.图像采集
galileo支持python的opencv库，这给简单的图像处理提供了极大的便利。
图像采集：
~~~python
cap = cv2.VideoCapture(0)#打开摄像头
cap.set(3,320)
cap.set(4,240)
while True：
	ret, frame = cap.read()
~~~
### 2.图像处理
我们要做键控，所以可以记录第一帧，然后通过帧间差别进行报警。
~~~python
cap = cv2.VideoCapture(0)
cap.set(3,320)
cap.set(4,240)
avg = None
lastUploaded = datetime.datetime.now()
motionCounter = 0
normal_count = 0
start_flag = 0
time.sleep(10)
while True:
    timestamp = datetime.datetime.now()
    text = "ok"
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    if avg is None:
        print "starting backfground model..."
        avg = gray.copy().astype("float")
        continue

    cv2.accumulateWeighted(gray, avg, 0.5)
    frameDelta = cv2.absdiff(gray, cv2.convertScaleAbs(avg))
    
    # 对变化图像进行阀值化, 膨胀阀值图像来填补
    # 孔洞, 在阀值图像上找到轮廓线
    thresh = cv2.threshold(frameDelta, conf["delta_thresh"], 255,
        cv2.THRESH_BINARY)[1]
    thresh = cv2.dilate(thresh, None, iterations=2)
    (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)
 
    # 遍历轮廓线
    for c in cnts:
        # if the contour is too small, ignore it
        if cv2.contourArea(c) < conf["min_area"]:
            continue
 
        # 计算轮廓线的外框, 在当前帧上画出外框,
        # 并且更新文本
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        text = "Attention!"
    #print "[", text, "]"
    # 在当前帧上标记文本和时间戳
    ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
    #print ts
    cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    cv2.putText(frame, ts, (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX,
        0.35, (0, 0, 255), 1)

    normal_count += 1
~~~
### 3.报警机制和图像上传
~~~python
 if text == "Attention!":
        # 判断上传时间间隔是否已经达到
        if (timestamp - lastUploaded).seconds >= conf["min_upload_seconds"]:
            # 运动检测计数器递增
            motionCounter += 1
 
            # 判断包含连续运动的帧数是否已经
            # 足够多
            if motionCounter >= conf["min_motion_frames"]:
                # 判断Dropbox是否被使用
                if conf["use_wechat"] and start_flag == 1:
			cv2.imwrite('/home/root/galileo_dangerous.jpg',frame)
			os.system("scp /home/root/galileo_dangerous.jpg root@xdjc.date:/root/wechat_galileo/")
			request = urllib2.Request(
			url = r'http://galileo.xdjc.date/?signature=1ce507b0abfa4d231b538988c01127c9e03a02ad&timestamp=1408377801&nonce=959202980',
			headers = {'Content-Type' : 'text/xml'},
			data = data)
			print opener.open(request).read()
                # 更新最近一次上传的时间戳并且重置运动
                # 计数器
                print "[ Dangerous! ]"
                lastUploaded = timestamp
                motionCounter = 0
    #否则, 该房间没有“被占领”
    else:
        motionCounter = 0  
        # 判断安保视频是否需要显示在屏幕上
    if conf["show_video"]:
        # 显示安视频
        cv2.imshow("Security Feed", frame)
        key = cv2.waitKey(1) & 0xFF
 
        # 如果q被按下，跳出循环
        if key == ord("q"):
            break  
~~~

> 参考：
>
> 《用树莓派 + Python + OpenCV 实现家庭监控和移动目标探测（下》( http://python.jobbole.com/81645/ )


## connman wifi功能的详细配置

这个过程我写在了下边这篇博客里：
《Intel Galileo开发版PCI-e无线网卡wifi配置》( http://blog.jcix.top/2015-12-10/galileo_connman/ )

## 实现led灯的亮灭或者光控功能

这个很简单，只要一个post，在服务器端进行相应控制即可。
代码
~~~python
#! /usr/bin/env python
import sys 
import urllib2
import time
import pyupm_grove as grove

led = grove.GroveLed(3)
light = grove.GroveLight(2)

print "[start....]"
time.sleep(20)
while True:
	light_value = light.raw_value()
	
	data = '''<xml>
	 <light><![CDATA[%s]]></light>
	</xml>''' % light_value
	
	cookies = urllib2.HTTPCookieProcessor()
	opener = urllib2.build_opener(cookies)
	
	request = urllib2.Request(
	        url = r'http://galileo.xdjc.date/?signature=1ce507b0abfa4d231b538988c01127c9e03a02ad&timestamp=1408377801&nonce=959202980',
	        headers = {'Content-Type' : 'text/xml'},
	        data = data)
	
	state = int(opener.open(request).read())
	if state == 2:
		if light_value <= 300:
        	        led.on()
        	else:
        	        led.off()
	elif state == 0:
		led.off()
	elif state == 1:
		led.on()
        time.sleep(1)

~~~

## 最终功能
只要Intel Galileo开发板自动连接了家中的WiFi，就开始和我们所搭建的云服务器进行通信，进而通过微信公众号和主人进行双向通信，实现智能家庭监控的一系列功能：
1． 在微信中回复“温度”，查询当前室温。
2． 回复“开灯”，自动打开Galileo开发板所控制的灯（本次设计采用LED代替演示）；回复关闭，则自动关闭；回复“光控”，则开发板根据光线传感器采集的室内亮度信息自动开或者关灯。
3． 回复“状态”，返回一张实时的家中照片。
4． 回复“打开监控”，开发板通过所连接的USB摄像头开始进行视频监控，若检测到有异常情况发生，自动通过微信向主人报警，并返回一张标记有异常目标和具体时间的监控照片；回复“关闭监控”，会暂停监控和报警。

## 功能展示

![show0][show0]

![show1][show1]

![show2][show2]

[show0]:{{"/2015121001.png" | prepend: site.imgrepo }}
[show1]:{{"/2015121002.png" | prepend: site.imgrepo }}
[show2]:{{"/2015121003.png" | prepend: site.imgrepo }}






