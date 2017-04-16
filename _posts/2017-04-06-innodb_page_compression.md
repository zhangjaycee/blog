---
layout: post
title: InnoDB Page Compression MySQL文档翻译：InnoDB透明页压缩
tags:  innodb 翻译 mysql 压缩 透明页压缩
categories: MySQL
---

> 原文：
>
> [MySQL 5.7 Reference Manual  15.9.2 InnoDB Page Compression]
>
> https://dev.mysql.com/doc/refman/5.7/en/innodb-page-compression.html


InnoDB支持file-per-table表空间中的表的页级压缩。 此功能称为透明页压缩。 通过使用CREATE TABLE或ALTER TABLE指定"COMPRESSION"这个表属性来启用页面压缩。 支持的压缩算法包括Zlib和LZ4。

## 支持的平台

页面压缩需要稀疏文件(sparse file)和打洞(hole punching)支持。 页面压缩在使用NTFS的Windows上被支持，并且在以下MySQL支持的Linux平台发行版的内核级别提供了打孔支持：

* RHEL 7 and derived distributions that use kernel version 3.10.0-123 or higher

* OEL 5.10 (UEK2) kernel version 2.6.39 or higher

* OEL 6.5 (UEK3) kernel version 3.8.13 or higher

* OEL 7.0 kernel version 3.8.13 or higher

* SLE11 kernel version 3.0-x

<!--more-->
* SLE12 kernel version 3.12-x

* OES11 kernel version 3.0-x

* Ubuntu 14.0.4 LTS kernel version 3.13 or higher

* Ubuntu 12.0.4 LTS kernel version 3.2 or higher

* Debian 7 kernel version 3.2 or higher

> 注意：对于一个给定的Linux发行版，可能所有可用的文件系统都不支持文件打洞(hole punching)。

## 透明页压缩的如何工作

当页面写入时，使用指定的压缩算法进行压缩。 压缩数据写入磁盘，页面从其末尾被打洞释放空块。 如果压缩失败，数据按原样写出。

## Linux上打洞的大小

在Linux系统上，文件系统块大小是用于打孔的单位大小。 因此，页面压缩仅适用于页面数据可以压缩到小于或等于InnoDB页面大小减去文件系统块大小的大小。 例如，如果innodb_page_size = 16K，文件系统块大小为4K，则页面数据必须压缩到小于或等于12K才能进行打洞。

## Windows上打洞大小

在Windows系统上，稀疏文件(sparse file)的基础架构基于NTFS压缩。打孔尺寸是NTFS压缩单元，是NTFS簇大小的16倍。 簇大小及其压缩单位如下表所示：

|簇大小|压缩单元|
|---|---|
|512 Bytes|	8 KB|
|1 KB|	16 KB|
|2 KB|	32 KB|
|4 KB|	64 KB|

Windows系统上的透明页压缩仅适用于页面数据可压缩到小于或等于InnoDB页面大小减去压缩单位大小的大小。

默认的NTFS簇大小为4K，压缩单位大小为64K。 这意味着页面压缩对于现成的Windows NTFS配置没有任何好处，因为最大`innodb_page_size`也是64K。

要使页面压缩在Windows上工作，文件系统必须以小于4K的簇大小创建，`innodb_page_size`必须至少是压缩单元大小的两倍。 例如，要使页面压缩在Windows上工作，您可以构建群集大小为512字节（其压缩单位为8KB）的文件系统，并初始化`innodb_page_size`值为16K或更大的InnoDB。

## 开启透明页压缩

要启用页面压缩，请在CREATE TABLE语句后指定COMPRESSION表属性。 例如：
```
CREATE TABLE t1 (c1 INT) COMPRESSION="zlib";
```
也可以在ALTER TABLE语句中启用已有表的透明页压缩。 但是，`ALTER TABLE ... COMPRESSION`仅更新表空间压缩属性。 对设置新压缩算法后发生的表空间的写入才会生效，要将新的压缩算法应用于现有页面，则必须使用OPTIMIZE TABLE重建表。如：
```
ALTER TABLE t1 COMPRESSION="zlib";
OPTIMIZE TABLE t1;
```

## 关闭透明页压缩

要禁用页面压缩，请使用ALTER TABLE设置COMPRESSION = None。 写入设置COMPRESSION = None后发生的表空间不再使用页面压缩。 要解压缩现有页面，必须在设置COMPRESSION = None后使用OPTIMIZE TABLE重建表。如：
```
ALTER TABLE t1 COMPRESSION="None";
OPTIMIZE TABLE t1;
```

## 透明页压缩元数据

页面压缩元数据位于INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES表中，具体在以下列：

* FS_BLOCK_SIZE：文件系统块大小，这是用于打洞的单位大小。

* FILE_SIZE：文件表现的大小(apparent size)，表示未压缩文件的最大大小。

* ALLOCATED_SIZE：文件的实际大小，即分配在磁盘上的空间量。

> 注意：
> 
> 在类Unix系统上，`ls -l tablespace_name.ibd`会以字节为单位显示文件的表现大小（等于FILE_SIZE）。 要查看在磁盘上分配的实际空间量（ALLOCATED_SIZE），请使用`du --block-size = 1 tablespace_name.ibd`。 `--block-size = 1`选项以字节为单位打印分配的空间，而不是块，这样可以将其与`ls -l`输出进行对比。
> 
> 使用SHOW CREATE TABLE查看当前页压缩设置（Zlib，Lz4或None）。 一个表可能包含具有不同压缩设置的页面混合。


以下是从INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES表中检索employees表的透明页压缩元数据的示例：
```
# 用使用Zlib算法的透明页压缩功能创建employees表

CREATE TABLE employees (
    emp_no      INT             NOT NULL,
    birth_date  DATE            NOT NULL,
    first_name  VARCHAR(14)     NOT NULL,
    last_name   VARCHAR(16)     NOT NULL,
    gender      ENUM ('M','F')  NOT NULL,  
    hire_date   DATE            NOT NULL,
    PRIMARY KEY (emp_no)
) COMPRESSION="zlib";

# 插入数据的操作(被省略)
  
# 从INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES表请求employees表的透明页压缩元数据
  
mysql> SELECT SPACE, NAME, FS_BLOCK_SIZE, FILE_SIZE, ALLOCATED_SIZE FROM
INFORMATION_SCHEMA.INNODB_SYS_TABLESPACES WHERE NAME='employees/employees'\G
*************************** 1. row ***************************
SPACE: 45
NAME: employees/employees
FS_BLOCK_SIZE: 4096
FILE_SIZE: 23068672
ALLOCATED_SIZE: 19415040
```

employees表的透明页压缩元数据显示，文件的表现大小为23068672字节，而实际文件大小（页面压缩）为19415040字节。 文件系统块大小为4096字节，这是用于打洞的块大小。

## 透明页压缩的局限性和使用的注意事项

* 如果文件系统块大小（或Windows上的压缩单元大小）* 2 > innodb_page_size，则透明页压缩被禁用。

* 驻留在共享表空间中的表不支持页压缩，其中包括系统表空间，临时表空间和通用表空间。

* 撤销日志(undo log)表空间不支持页面压缩。

* 重做日志(redo log)页面不支持页面压缩。

* 用于空间索引的R-tree页面不被压缩。

* 属于压缩表(ROW_FORMAT = COMPRESSED, 表的页级压缩，较老的特性)的页面按原样保留。

* 在恢复期间，更新的页面以未压缩的形式写出。

* 在不支持使用的压缩算法的服务器上加载页面压缩表空间会导致I／O错误。

* 在降级到不支持页面压缩的早期版本的MySQL之前，请解压缩使用页面压缩功能的表。要解压缩表，请运行`ALTER TABLE ... COMPRESSION = None`和`OPTIMIZE TABLE`。

* 如果所使用的压缩算法在两台服务器上都可用，则可以在Linux和Windows服务器之间复制开启透明页压缩功能的空间。

* 将页面压缩表空间文件从一个主机移动到另一个主机时，保留页面压缩需要保留稀疏文件(sparse files)的工具软件。

* NVMFS的Fusion-io硬件可以在其他平台上实现更好的页面压缩，因为NVMFS旨在利用打洞功能达到更高的性能。

* 使用具有大型InnoDB页面大小和相对较小的文件系统块大小的页面压缩功能可能会导致写入放大。例如，具有4KB文件系统块大小的64KB的最大InnoDB页面大小可以提高压缩，但也可能增加对缓冲池的需求，从而增加I/O和潜在的写入放大。


