---
layout: post
title: 折腾Docker的一些吐槽点
tags: docker
categories: Others
---
<div class="toc"></div>

```
第一次构建Docker镜像，想照着书弄个jekyll的镜像玩玩，结果两天了，到现在还没成功。记录下国内环境实践和书本上的不同。。。
```

# 首先官方的apt-get源太慢了
要换成国内的速度还可以接受一点：([原文链接](http://jamlee.cn/2015/03/22/docker与精彩的shell/))

## 做法：
Dockerfile 中 `RUN apt-get update` 前添加一句：
~~~
RUN sed -i 's/http:\/\/archive\.ubuntu\.com\/ubuntu\//http:\/\/mirrors\.163\.com\/ubuntu\//g' /etc/apt/sources.list
~~~


# gem国内源貌似也不行
([原文链接](http://www.haorooms.com/post/gem_not_use))

## 做法：
Dockerfile中添加：
~~~
RUN gem sources --remove http://rubygems.org/
RUN gem sources -a https://ruby.taobao.org/
<!--more-->
RUN gem sources -l
~~~
