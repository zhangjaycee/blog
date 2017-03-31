---
layout: post
title: python自动化运维笔记(1)----psutil
tags: python linux 运维
categories: Linux
---


## 环境:ubuntu 14.04 32bit
## 工具：psutil
~~~
对应的shell工具：ps  top  lsof  netstat  ifconfig  who 
df kill  nice  free  ionice  iostat  iotop  uptime  pidof  
tty  taskset  pmap
~~~

## 安装：
采用pip可以安装`pip install psutil`。(注意需要安装python-dev:  `sudo apt-get install python-dev`)

## 用法举例：
### 获取信息
##### cpu信息：
~~~python
psutil.cpu_times() #cpu完整信息
psutil.cpu_count(logical=False) #cpu物理个数
~~~
logical默认为True即cpu逻辑个数
##### 内存信息：
~~~python
mem = psutil.virtual_memory()
<!--more-->
print mem.total
print mem.free
print mem.swap_memory() # sswap分区信息
~~~
##### 磁盘信息
##### 网络信息
##### 其他信息

### 进程管理
##### 进程信息：
~~~python
p = psutil.pids() 
print p #列出所有进程号
print p.exe #进程路径
~~~
##### 用popen类运行程序以跟踪程序运行状态:
~~~python
from subprocess import PIPE
p = psutil.Popen(["python", "-c", "print('hello')"], stdout= PIPE)
print p.name()
print p.username()
print p.communicate()
~~~
