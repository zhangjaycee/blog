---
layout: post
title: Optimizing InnoDB Disk I/O MySQL文档翻译：优化InnoDB磁盘I/O
tags:  innodb 翻译 mysql io
categories: MySQL
---


> 原文：[8.5.8 Optimizing InnoDB Disk I/O](https://dev.mysql.com/doc/refman/5.7/en/optimizing-innodb-diskio.html)

> 这页感觉比较重要，翻译一下。。


如果你遵循了数据库设计和SQL操作调优的最佳实践，但是数据库仍然由于磁盘I/O负载过重而运行慢，请考虑这些磁盘I/O优化方法。如果Unix top工具或Windows任务管理器显示你的工作负载的CPU使用率百分比小于70％，那么你的数据库系统瓶颈在于磁盘。


### 增加缓冲池(buffer pool)的大小

  当表中数据被缓存到InnoDB的buffer pool中时，对它的查询请求就不会引起任何磁盘I/O请求。使用innodb_buffer_pool_size选项就可以指定buffer pool的大小。buffer pool这块内存很重要，所以通常建议将innodb_buffer_pool_size配置为系统内存的50％到75％。 有关更多信息，请参见第9.12.4.1节“MySQL如何使用内存”。

### 调整刷新方法

  在某些版本的Linux或Unix中，使用Unix fsync()调用(InnoDB默认用它)或其他类似调用将文件刷入磁盘的速度是非常慢的。如果数据库的写入性能有问题，请在执行基准测试时将innodb_flush_method参数设置为O_DSYNC。

### noop和deadline两种I/O调度程序的选择

  InnoDB在Linux上使用异步I/O子系统(naive AIO)来执行数据文件页的预读操作和写请求操作。此行为由innodb_use_native_aio选项进行控制，默认情况下是启用的。 对于naive AIO来说，I/O调度程序(I/O Scheduler)的类型对I/O性能有很大的影响。一般来说，建议使用noop和deadline这两种类型的I/O调度程序。这里就应该进行测试以决定当前的环境和工作负载适合使用哪一个I/O调度器。有关更多信息，请参见第15.6.8节“在Linux上使用异步I / O”。

### x86_64架构的Solaris 10上使用direct I/O

<!--more-->
  在Solaris 10 for x86_64(AMD Opteron)系统上使用InnodDB存储引擎时，应使用direct I/O以避免性能降低。要在存储InnoDB相关文件的整个UFS文件系统上使用direct I/O，应在挂载时使用forcedirectio参数，详情参阅mount_ufs(1M)(Solaris 10 / x86_64上默认不使用此选项)。如果只对InnoDB相关文件使用direct I/O而不是对整个文件系统使用direct I/O，可以设置参数innodb_flush_method = O_DIRECT，使用此设置，InnoDB在文件I/O(不包括日志文件的I/O)时调用directio()而不是fcntl()。

### 在Solaris 2.6以上版本上使用raw格式存储数据和日志

  当在Solaris 2.6及以上版本的系统(for sparc / x86 / x64 / amd64等任何平台)上用使用大innodb_buffer_pool_size的InnoDB存储引擎时，应该让InnoDB数据文件和日志文件存储在裸设备(raw devices)或者一个单独的使用direct I/O的UFS文件系统上(像上文所述的那样使用forcedirectio挂载UFS分区，如果需要日志文件也direct I/O，只能这样做而不能通过设置innodb_flush_method达到目的)。使用Veritas文件系统(VxFS)的用户应该使用convosync=direct这个挂载参数。

  注意不要在direct I/O文件系统上放置其他MySQL数据文件，比如MyISAM表的那些。可执行文件或者库不能放在直接I/O文件系统上。

### 使用其它存储设备

  如果你又多余的存储设备可以设置RAID或者软链接到其它的磁盘，可以参看第9.12.2节“优化磁盘I/O”，来了解一些更底层的I/O优化技巧。



### 增加I/O capacity避免积压

  如果InnoDB检查点操作导致吞吐量周期性下降，请考虑增加innodb_io_capacity配置选项的值。这个值越高，flushing操作会越频繁，以减小数据积压，避免降低吞吐量。

###如果flushing没有落后，尽量减小I/O capacity

  如果系统没有落后于InnoDB的冲洗操作，考虑降低innodb_io_capacity配置选项的值。通常，这个值越低越好，前提是没有因此而导致吞吐量周期性下降(如前所述)。对于一些典型的场景，当你看到从SHOW ENGINE INNODB STATUS输出这样的组合时，你可以降低它的值：
 - History list长度较短，低于几千行；
 - 插入缓存处合并接近于插入的行；
 - buffer pool中修改的页始终低于buffer pool的innodb_max_dirty_pages_pct参数。 (在服务器没有执行批量插入操作时，因为在批量插入期间，修改页面百分比明显上升很正常)
 - Log sequence number - Last checkpoint 最后一个检查点小于7/8或者理想情况下小于6/8。


### 在Fusion-io设备上存储系统表空间文件

  你可以通过将系统表空间文件（“ibdata文件”）存储在支持原子写入的Fusion-io设备上，以获得doublewrite缓冲区相关的I/O优化。在这种情况下，doublewrite缓冲(innodb_doublewrite)被自动禁用，所有数据文件转而使用Fusion-io的原子写操作。这项特性仅支持Fusion-io硬件并且仅在Linux上的Fusion-io NVMFS上才能启用。要充分利用这个功能，建议将innodb_flush_method设置为O_DIRECT。
  
  > 注意：
  > 由于doublewrite buffer的设置时全局的，所以对于那些留在非Fusion-io硬件中的数据文件，doublewrite buffer依旧是无法使用的。

### 禁用数据页的日志记录

  当使用InnoDB表压缩功能时，对于压缩数据进行更改时，重新压缩的页面映像将被写入redo log。这个行为由innodb_log_compressed_pages控制，它默认启用以防止在恢复期间由于使用不同版本的zlib压缩算法可能导致的数据损坏。如果你确定zlib版本不会改变，那么可以禁用innodb_log_compressed_pages来减少修改压缩数据的工作负载导致的redo log生成。



