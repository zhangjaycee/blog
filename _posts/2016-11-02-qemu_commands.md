---
layout: post
title: qemu/qemu-kvm/qemu-system-x86_64/qemu-x86_64命令的区别？
tags: 虚拟化 qemu kvm linux
categories: 虚拟化
---

刚想玩玩kvm，结果分不清这几个命令。。搜了一下，记录下来，希望对大家有帮助。

## 摘抄

### 1

> 在老版本中有单独的qemu-kvm模块存在，结合qemu一起做虚拟机工作。在后续新版本中，已经将qemu-kvm模块完全合并到qemu中去。因此当需要使用kvm特性时候，只需要qemu-system-x86_64 启动命令中增加参数 --enable-kvm参数使能即可。

(http://blog.csdn.net/tantexian/article/details/41281171)

### 2  

>I asked the mailing list, here's what I got:

>qemu-arch like /usr/local/bin/qemu-x86_64 is for running a program of that arch on the host machine of what ever arch, but not a virtual machine
qemu-system-arch like /usr/local/bin/qemu-system-x86_64 is for running a system of that arch on the host machine to enable kvm support, qemu parameter -enable-kvm is needed, libvirt should have taken care of this if right xml is configured

>Thanks Jakob for the answer in the mailing list.

(http://serverfault.com/questions/767212/difference-between-qemu-kvm-qemu-system-x86-64-qemu-x86-64)

  意思是，类似qemu-x86_64这种命令是运行某种架构的程序的，qemu-system-x86_64是运行某种架构系统的（虚拟机），如果需要kvm支持，需要加上参数 -enable-kvm， 如果使用libvirt可以配置相应的xml来实现kvm支持。

### 3

> Actually, qemu-kvm is a simple wrapper of qemu-system-x86_64. 

> In my x86_64 gentoo OS, the content of qemu-kvm script is 

> \#!/bin/sh$ exec /usr/bin/qemu-system-x86_64 --enable-kvm "$@"

(https://lists.nongnu.org/archive/html/qemu-discuss/2012-02/msg00018.html)

  意思是，gentoo里面的qemu-kvm就是运行“qemu-system-x86_64 --enable-kvm”， 是一个脚本。

### 4

> The KVM project used to maintain a fork of QEMU called qemu-kvm. All feature differences have been merged into QEMU upstream and the development of the fork suspended.

> To use KVM pass --enable-kvm to QEMU.

(http://wiki.qemu.org/Features/KVM)

  官方文档，意思是KVM项目以前fork了一个QEMU的镜像并称为qemu-kvm。现在所有不同的特征都被merge到QEMU的upstream了，称为qemu-kvm的fork版本暂停开发了。


## 暂时的结论


现在的qemu已经整合qemu-kvm，不再有qemu-kvm的说法了。一般创建x86的虚拟机需要用到qemu-system-x86_64这个命令，并需要加上--enable-kvm来支持kvm加速。有些Linux发行版的qemu-kvm命令仅仅是qemu-system-x86_64的软链接或者简单包装。
