---
layout: post
title: Table Compression for OLTP Workloads MySQL文档翻译：OLTP工作负载中应用表压缩
tags:  innodb 翻译 mysql 压缩 oltp
categories: MySQL
---

> 原文：
> 
> [MySQL 5.7 Manual 15.9.1.6 Compression for OLTP Workloads]
> 
> https://dev.mysql.com/doc/refman/5.7/en/innodb-performance-compression-oltp.html

传统上，InnoDB压缩功能主要用于只读或大部分读取的工作负载，例如在数据仓库配置中。快速但相对较小和昂贵的SSD存储设备的兴起使得压缩对于OLTP工作负载也越发具有吸引力的：高流量的交互式网站可以通过使用压缩表同时使用具有执行频繁INSERT，UPDATE和DELETE操作的应用程序来减少其存储需求和每秒I/O操作数(IOPS)。

MySQL 5.6中引入的配置选项可让您调节压缩对特定MySQL实例的工作参数，其对于写入密集型操作的性能和可扩展性是很重要的：

* `innodb_compression_level`： 允许你向上或向下调整压缩程度，更高的值可以让你节省更多空间存储更多数据，同时在压缩时牺牲更多CPU周期，比较低的值可以让你在存储空间不重要时或者在数据不太适合被压缩时减小CPU开销。

* `innodb_compression_failure_threshold_pct`： 指定了一个进行页压缩失败的百分比阈值，当它被超过时，MySQL开始在每个新的压缩页中增加一些额外的空闲的保留空间(padding)，动态的调整这个空余空间的大小，padding的上限是由`innodb_compression_pad_pct_max`指定的，它是页面大小的一个百分比。

* `innodb_compression_pad_pct_max`：允许你调整每个页面中用于直接保存更改和插入数据的空闲保留空间(padding)的最大值(这样就无需每次更改和插入都再次压缩整个页面)。 值越高，就可以记录更多的更改(???)，而无需重新压缩页面。MySQL运行时,只有当需要昂贵分割操作的"压缩失败”达到上一个参数所指定的百分比时，才会为每个压缩表中的页面增加一个大小可变的空余空间(padding)。

* `innodb_log_compressed_pages`：默认情况下，此选项被启用，以防止在恢复期间使用不同版本的zlib压缩算法时可能会发生损坏。 如果你确定zlib版本不会更改，请禁用`innodb_log_compressed_pages`以减少为修改压缩数据而生成的重做日志。


由于开启压缩时，内存中可能同时保留存在数据的压缩版本和未压缩版本，所以在OLTP工作负载下进行压缩时，`innodb_buffer_pool_size`配置选项的值可能会需要增加。

<!--more-->
