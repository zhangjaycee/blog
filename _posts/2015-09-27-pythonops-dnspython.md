---
layout: post
title: python自动化运维笔记(2)----dnspython
tags: python linux 运维
categories: python
---


### 准备工作
* 环境：Ubuntu 14.04 32bit
* 工具：dnspython
> 对应的shell工具：nslookup  dig等

* dns预备知识：
>常用资源记录RR（Resource Records）类型
A记录： 主机名--> IP地址
MX记录： 定义邮件服务器域名
CNAME： 域名间映射
PTR： IP地址 -->主机名（反向解析）
>> 更详细介绍参考博文《[ [DNS]常见资源记录定义（Resource Record) ](http://blog.csdn.net/a19881029/article/details/19486949)》


### 用法举例

* 查询A记录

```python
import dns.resolver

domain = raw_input('input an domain:')
A = dns.resolver.query(domain, 'A')

for i in A.response.answer:
    for j in i.items:
        if 'address' in dir(j):
            print j.address
        else:
            print 'failed to resolver'
```

* 查询MX记录

```python
MX = dns.resolver.query(domain, 'MX')
for i in MX: 
    print 'MX preference =', i.preference, 'mail exchanger =', i.exchange
```

* 域名轮询监控
	step1:查询A记录
	step2:对ip进行http监测

```python
import httplib
import os
import dns.resolver

iplist = []
domain = "www.xidian.edu.cn"

def get_iplist(domain=""):
    try:
        A = dns.resolver.query(domain, 'A')
    except Exception,e:
        print "dns resolver error:" + str(e)
        return

    for i in A.response.answer:
        for j in i.items:
            if 'address' in dir(j):
                iplist.append(j.address)
    return True

def checkip(ip):
    checkurl = ip + ':80'
    getcontent = ''
    httplib.socket.setdefaulttimeout(5)
    conn = httplib.HTTPConnection(checkurl)

    try:
        conn.request("GET", "/", headers = {"Host": domain})
        r = conn.getresponse()
        getcontent = r.read(17)
    finally:
        #print getcontent[3:]
        if getcontent[3:] == "
            print ip + "\t[OK]"
        else:
            print ip + "\t[ERROR]"

if __name__ == "__main__":
    if get_iplist(domain) and len(iplist) > 0:
        for ip in iplist:
            print ip
            checkip(ip)
    else:
        print "dns resolver error."
```