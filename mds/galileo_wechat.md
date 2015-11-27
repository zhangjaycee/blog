# Galileo开发板 + 微信公众平台的实现简单的物联网家庭监控


上次写的博客，介绍了下刚拿到galileo开发板的时候如何进行折腾。
上次折腾完后，因为我发现galileo本身和一个装着linux的arduino/pc一样，那么用它来实现一些物联网应用会比较简单，又赶上本学期的工程设计课作业，所以初步实现了一个能用微信监测室内温度和拍摄室内照片的小型物联网系统。

>### 参考：
![鼓捣Galileo开发板的一些吐槽] [galileo_intro]

下记录下实现过程。由于本人表述能力较差，采用简述加大量外部连接的方式进行记录。

## 系统功能

* 用微信获取室内当前温度或者一张较为实时的照片。

* 通过亮度传感器自动自动控制LED的亮、灭。

## 基本结构

系统实现最初的想法，就是让微信公众平台和开发板通过互联网直接进行信息传递，但是因为微信公众平台对我们所搭建服务器采用get和post方法进行通信，所以在没有公网ip的校园网环境，一般只能租云服务器或者VPS进行中转。

这样，系统的基本结构就变成了：
`开发板外围<-->Galileo开发板<-->云服务器<-->微信公众平台<-->手机微信<-->用户`
可见整个通信链将用户和外围器件连接起来，实现了简单的物联网。



## 详细组成

* 外围器件：温度传感器、摄像头、LED、亮度传感器

* Intel Galileo 开发板

* 阿里云服务器(Ubuntu 14.04 64bit)

* 微信公众平台

* 手机微信客户端



## 外围传感器

采用了grove的温度传感器、亮度传感器和LED，它们兼容arduino等单片机，采用模拟或数字采集，样例代码和说明见参考。

> 参考：
> 《(github)intel-iot-devkit/upm/examples/python》 ( https://github.com/intel-iot-devkit/upm/tree/master/examples/python )
> 《seeed wiki》 ( http://www.seeedstudio.com/wiki/Main_Page )


## 摄像头设备
摄像头采用UVC标准的普通网络摄像头(webcam)，这时由于完整版的galileo linux系统已经包含了相应的驱动。插上摄像头后，可以用`ls /dev/viceo*`看到这个外设。

## 开发板端
开发板上所做的工作分开说的话有两个：
### 采集传感器数据
采集数据可以用arduino的c/c++程序，生成sketch下载到galileo开发板中，如上文”外围传感器“小节中的参考2；
也可以在linux中直接用python进行控制和信息获取，如上文"外围传感器"小节中的参考1
这两种方式的例程都很简单，不再赘述。

本系统中，
* 温度传感器采用了sketch程序（代码见下文"与云服务器进行通信"小节）
* 亮度传感器采用了python程序
* LED和亮度传感器是一起用的，所以也是python程序
* 摄像头采用了python程序（用了opencv库python版，代码见下文"与云服务器进行通信"小节）

其中用亮度传感器通过室内亮度控制led亮灭的程序如下：(python)

~~~python
#!/usr/bin/env python
import time
import pyupm_grove as grove

led = grove.GroveLed(3)
light = grove.GroveLight(2)

print "[start....]"

while True:
        light_value = light.raw_value()
        if light_value <= 300:
                led.on()
        else:
                led.off()
        time.sleep(1)
~~~

需要注意的是，如果是用python(比如我这次的摄像头采集和上传脚本，还有我light sensor 控制led的脚本)，我们更希望将这个python脚本设为开机自动启动。
这需要在`/etc/init.d/`中添加一个脚本文件，比如我添加的脚本(shell)：

~~~bash
#!/bin/bash
# /etc/init.d/cap
### BEGIN INIT INFO
# Provides: zjc
# Required-Start: $remote_fs $syslog
# Required-Stop: $remote_fs $syslog
# Default-Start: 2 3 4 5
# Default-Stop: 0 1 6
# Short-Description: upload cap initscript
# Description: This service is used to manage the webcam
### END INIT INFO
case "$1" in
    start)
        echo "Starting cap and upload...."
        /home/root/galileo_pys/cap_upload.py & #这里是我要开机启动的python脚本
        ;;
    stop)
        echo "Stopping cap and upload...."
        kill $(ps aux | grep -m 1 'python /home/root/galileo_pys/cap_upload.py'
        ;;
    *)
        echo "Usage: service cap start|stop"
        exit 1
        ;;
esac
exit 0
~~~

然后，用`chmod +x xx`加入可执行权限，并且在init.d目录下运行`update-rc.d xx defaults yy`(xx为脚本名，yy为启动顺序)


> 参考:
> 《ubuntu 下 init.d 服务启动脚本编写》 ( http://blog.csdn.net/littlefishzhang/article/details/8203183 )
> 《Linux开机自动启动脚本方法》( http://blog.sina.com.cn/s/blog_70808ace0100o3in.html )
> 《Edison开机自启动运行自己编译好的程序》( http://www.arduino.cn/thread-12535-1-1.html )
> 《基于OpenCV的摄像头脸部识别抓取及格式储存(Python)》（ http://www.linuxidc.com/Linux/2014-12/110482.htm ）

### 与云服务器进行通信

#### 温度数据的上传

由于微信公众平台的服务器和我们的云服务器进行通信用到了post和get的方法，所以对于温度信息的上传，对http几乎一窍不通的我用了一个偷懒的办法：
仿照微信服务器的数据格式，在我云服务器用if-else进行判断，数据是来自腾讯，还是来自我的Galileo开发板。
这样，我们要做的只是用python在开发板上对我们的云服务器进行一个POST，剩下的事情就丢给云服务器那边处理吧~

代码(python)如下：
~~~python
#! /usr/bin/env python
import sys
import urllib2

t = sys.argv[1]
#采用和微信公众平台统一的xml数据格式(其他可选格式还有json)
data = '''<xml>
 <temprature><![CDATA[%s]]></temprature>
</xml>''' % t

cookies = urllib2.HTTPCookieProcessor()
opener = urllib2.build_opener(cookies)

request = urllib2.Request(
        url = r'http://galileo.xdjc.date/?signature=1ce507b0abfa4d231b538988c011
        headers = {'Content-Type' : 'text/xml'},
        data = data)

print opener.open(request).read()
~~~
可以看到，这段程序接收一个参数，这个参数就是要上传的温度。
这段程序并没有涉及到传感器数据的采集或者控制，对于传感器数据的采集，我还是采用的sketch程序（类似arduino，c/c++语言，arduino IDE）的方法。
对于采集后怎么调用这个python脚本自动上传的问题，我用的是linux的system系统调用的。
程序是在温度传感器例程（详见上文中”外围传感器“小节中的参考2）的基础上修改的，代码(c/c++ arduino ide)如下：
~~~cpp
#include <math.h>

const int B=4275;                 // B value of the thermistor
const int R0 = 100000;            // R0 = 100k
const int pinTempSensor = A5;     // Grove - Temperature Sensor connect to A5

void setup()
{
    Serial.begin(9600);
}

void loop()
{
    char str0[50] = "/home/root/galileo_pys/post.py ";//脚本路径
    char str[10];
    int a = analogRead(pinTempSensor );

    float R = 1023.0/((float)a)-1.0;
    R = 100000.0*R;

    float temperature=1.0/(log(R/100000.0)/B+1/298.15)-273.15;//convert to temperature via datasheet ;
    sprintf(str, "%.1f", temperature);
    strcat(str0, str);

    Serial.print("temperature = ");
    Serial.println(temperature);
    Serial.println(str0);
	//调用python程序
    system(str0);
    Serial.println("post done!");
	//每10秒上传一次
    delay(10000);
}
~~~

#### 照片的上传
照片的上传我采用了scp的方式，在python中调用方式为os.system()，这样，我们先用opencv采集一张jpg照片，保存到开发板上，然后再将这张照片传到了云服务器上的特定位置，其他的事情就交给服务器办吧。

代码如下(python)：
~~~python
#!/usr/bin/env python
import sys
import os
import time
import cv2

print "starting camera..."
cam = cv2.VideoCapture(0)
count = 0
while True:
        ret, frame = cam.read()
        if ret:
                cv2.imwrite('/home/root/galileo.jpg',frame)
                #调用scp命令
                os.system("scp /home/root/galileo.jpg root@xdjc.date:/root/wechat_galileo/")
                count += 1
                print "[upload ok],count =", count
        #每15秒上传一次
        time.sleep(15)
~~~

## 云服务器端

### 组成
* 系统：Docker(Ubuntu 14.04基础镜像)
* Web框架：Django（python web框架）
* 语言：Python 2.7
* 微信平台库：wechat_sdk python库

### 环境搭建
因为我用了docker 所以直接贴出Dockerfile，关于Docker的介绍见官网（ http://www.docker.com/ ），或者我的其他相关博文。
Dockerfie如下:
~~~
FROM ubuntu:14.04
MAINTAINER Jaycee Zhang "zhjcyx@gmail.com"

#RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.163\.com\/ubuntu\//g' /etc/apt/sources.list
ADD sources.list /etc/apt/sources.list
RUN apt-get update
RUN apt-get -yq install nginx
RUN apt-get -yq install uwsgi
RUN apt-get -yq install uwsgi-plugin-python
RUN apt-get -yq install python-pip
RUN pip install django
RUN pip install wechat_sdk
RUN mkdir -p /var/www/html
RUN mkdir -p /wechat_galileo
ADD ./doit.sh /doit.sh
ADD ./nginx.conf /etc/nginx/nginx.conf
EXPOSE 80
~~~
此Dockerfile保证我的博客和Django程序能运行在一个nginx服务器中。
Dockerfile中add的其他配置见我的github仓库( https://github.com/zhangjaycee/dockerfiles/tree/master/nginx2 )

详细步骤参考了以下两篇参考，不再重复。增加了上传媒体文件图片的代码和接收Galileo温度POST的代码。
工程详见我的github仓库( https://github.com/zhangjaycee/wechat_galileo/tree/new_version )
views.py 代码如下：(python)
~~~python
# -*- coding: utf-8 -*-
import os
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.template import RequestContext, Template
from django.utils.encoding import smart_str, smart_unicode
import hashlib
from xml.etree import ElementTree as etree
import getinfo
from wechat_sdk import WechatBasic
from wechat_sdk.exceptions import ParseError
from wechat_sdk.messages import TextMessage
import json
'''
WECHAT_TOKEN = 'jcgalileo'
AppID = 'wx4b7943f082770e22'
AppSecret = '60186ab20d8e44bf2e7c496a9e7a34a1'
'''
WECHAT_TOKEN = 'jcgalileo2'
AppID = 'wx5a13781f1ae1b5be'
AppSecret = 'd4624c36b6795d1d99dcf0547af5443d'

fp_tmp = open('log_tmp.txt','a+')

# 实例化 WechatBasic
wechat_instance = WechatBasic(
    token=WECHAT_TOKEN,
    appid=AppID,
    appsecret=AppSecret
)

@csrf_exempt
def index(request):
    if request.method=='GET':
        response=HttpResponse(checkSignature(request))
        return response
    else:
        xmlstr = smart_str(request.body)
        xml = etree.fromstring(xmlstr)
        temprature = xml.find('temprature')
        if temprature != None:
            fp_tmp.seek(0,2)
            fp_tmp.write(temprature.text)
            return HttpResponse("0")
        # 解析本次请求的 XML 数据
        try:
            wechat_instance.parse_data(data=request.body)
        except ParseError:
            return HttpResponseBadRequest('Invalid XML Data')

        # 获取解析好的微信请求信息
        message = wechat_instance.get_message()

        # 关注事件以及不匹配时的默认回复
        response = wechat_instance.response_text(
            content = (
                '感谢您的关注！\n回复【功能】查看支持的功能'
            )
        )
        if isinstance(message, TextMessage):
            # 当前会话内容
            content = message.content.strip()
            if content == u'功能':
                reply_text = (
                        '目前支持的功能：\n1.回复“温度”，查询113室温\n'
                        '2.回复“拍照”，偷窥jc的生活状态\n'
                )
                response = wechat_instance.response_text(content=reply_text)
            if content == u'温度':
                fp_tmp.seek(-4, 2)
                reply_text = fp_tmp.read(4)
                response = wechat_instance.response_text(content=reply_text)
            if content == u'拍照':
                #response = wechat_instance.response_text(content="debug....")
		fp = open('galileo.jpg','rb')
		upload_info = wechat_instance.upload_media("image", fp)
		image_id = upload_info['media_id']
                response = wechat_instance.response_image(image_id)

        return HttpResponse(response, content_type="application/xml")

def checkSignature(request):
    signature=request.GET.get('signature',None)
    timestamp=request.GET.get('timestamp',None)
    nonce=request.GET.get('nonce',None)
    echostr=request.GET.get('echostr',None)
    #这里的token我放在setting，可以根据自己需求修改
    token="jcgalileo2"

    tmplist=[token,timestamp,nonce]
    tmplist.sort()
    tmpstr="%s%s%s"%tuple(tmplist)
    tmpstr=hashlib.sha1(tmpstr).hexdigest()
    if tmpstr==signature:
        return echostr
    else:
        return None
~~~

>参考：
>《基于python(django)+uwsgi+nginx的微信公众平台的实现》( http://www.linuxlearn.net/news/new/97/4851/ )
>《Python/Django 微信接口》( http://www.ziqiangxuetang.com/django/python-django-weixin.html )

[galileo_intro]:  {{"/2015-11-04/introduce_galileo/" | prepend: site.url }}