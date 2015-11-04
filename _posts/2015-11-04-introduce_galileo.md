---
layout: post
title: 鼓捣Galileo开发板的一些吐槽
tags: intel galileo linux 嵌入式 IoT
categories: 嵌入式
---

这几天折腾伽利略开发板，写下一些吐槽，以便以后再看到这篇博客，仍然能记起这些值得吐槽的地方。。。也希望看到这篇博客的人能够因此少些吐槽( ╯□╰ )。。网上其实是有不少资源的，但是相对其他更热门的板子，显然找资料并不是和喝白开水一样简单，由于我表达能力较差，所以准备采用简述+大量站外链接的形式，给出一个希望不会让人误入歧途的引导。。。

## 介绍
**Intel Galileo**（[点击查看中文官网](http://www.intel.cn/content/www/cn/zh/do-it-yourself/galileo-maker-quark-board.html)），是一个兼容Arduino的x86平台的开源硬件产品。个人感觉应当注意的是，特点就是兼容Arduino和x86，这样我们既能够利用丰富的Arduino软硬件及社区资源，又能够在上边运行linux甚至windows系统，做出更复杂的系统。

>相关介绍：
>《x86 版的 Arduino 来了，Intel Galileo 开发板的体验、分析和应用【超长文多图】》（http://www.ifanr.com/388835）

>《系出名門：Intel Galileo的十大特性》（http://www.leiphone.com/news/201406/intel-galileo.html）
>（更多请自行百度/google）

## “Arduino模式”

### 略（自行百度）

## Arduino? no，Linux!
Galileo可以在SD卡中装入完整版Linux镜像，一旦在装有完整版Linux镜像的SD卡插入时启动，会进入所安装的完整版Linux系统，否则，则会进入烧写入flash的裁剪版微型Linux系统。而只有安装了完整版Linux，Galileo才不仅仅只是一个Arduino。下图为Galileo开机启动过程：
![galileoboot][galileoboot]

> 参考:

> 《x86 版的 Arduino 来了，Intel Galileo 开发板的体验、分析和应用【超长文多图】》（http://www.ifanr.com/388835）


## 两种完整Linux系统
官方提供了两种可以装在SD卡中的linux系统，但看容量，一个48M左右，另一个210M左右，其实这两个一个基于uclibc编译，一个基于eglibc编译，从事实和容量来看，都是后者更为完整，包含的linux命令工具和第三方库。
我可是被这个坑了很长时间，导致我止步不前，原因在于官网把基于uclibc的版本放在了更显眼的位置，而这个精简的“完整版”，没有gcc等编译工具，没有摄像头驱动，没有。。。。很多常用的linux的工具。

>参考:

>《Different linux images? uclibc verus eglibc images?》（https://communities.intel.com/message/241845#241845）

>《【整理】uclibc,eglibc,glibc之间的区别和联系》（http://bbs.chinaunix.net/thread-3762882-1-1.html）

>镜像下载:

>《Intel® Galileo Board Downloads》（https://software.intel.com/en-us/iot/hardware/galileo/downloads）

>镜像安装：

>《Making a bootable micro SD Card with Linux》（https://software.intel.com/en-us/programming-blank-sd-card-with-yocto-linux-image-linux）

## 连接
ulibc版Linux可以采用usb直接连接通过screen minicom等工具直接进行终端连接，而elibc版试了下不行，可能要连接串口引脚，不过既然有了linux，而且是默认开启了ssh服务的linux，我们只需要利用以太网口和路由器，将自己的pc和Galileo置于同一内网，就可以用`ssh root@192.168.x.x`连接Galileo了。
如果有无线网卡，通过设置，应该就可以拔掉那根网线，采用无线ssh登陆了。
> 参考：

> 《Intel Galileo 2 with USB WiFi Dongle (RT3070)》https://eexe1.wordpress.com/category/computer/iot/

> 《在 Linux 下使用 rfkill 软开关蓝牙及无线功能》: （http://www.linuxidc.com/Linux/2015-08/121119.htm）

## 硬件操作
本人还在学习，先贴出一个方向：**mraa**([官网](http://iotdk.intel.com/docs/master/mraa/))

有了mraa，我们就可以用python直接操作galileo的gpio了，当然arduino IDE进行C/C++编程下载的方式操作硬件的方式依然是可行的！
>参考：

>《mraa github page》(https://github.com/intel-iot-devkit/mraa/tree/master/examples/python)

> 《如何在Linux系统中直接操作GPIO》(http://oszine.com/intel-galileo-gpio-1/)



[galileoboot]:{{"/2015110401.jpg" | prepend: site.imgrepo }}
