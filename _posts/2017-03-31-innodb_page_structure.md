---
layout: post
title: InnoDB Page Structure -- High-Altitude View MySQL文档翻译：InnoDB页宏观结构
tags:  innodb 翻译 mysql 页 B树
categories: MySQL
---
> 原文 [MySQL Internals Manual 22.2.1 High-Altitude View] https://dev.mysql.com/doc/internals/en/innodb-page-overview.html

## 0. 概述

InnoDB的页有7个部分：
```
+----------------------------+
| Fil Header                 |
+----------------------------+
| Page Header                |
+----------------------------+
| Infimum + Supremum Records |
+----------------------------+
| User Records               |
+----------------------------+
| Free Space                 |
+----------------------------+
| Page Directory             |
+----------------------------+
| Fil Trailer                |
+----------------------------+
```

你可以发现，每个页有头尾(header/trailer)对。靠内的头尾对(Page Header和Page Directory)主要是由page程序组的所关注的，而外部的头尾对(Fil Header和Fil Trailer)主要是fil程序组的关注 。 Fil Header也被称为“文件页头(File Page Header)”。
<!--more-->

其他中间的夹层是记录(records)和空闲空间， 页面始终以两个称为Infimum和Supremum的不变的记录开头。然后就到了用户记录， 在User Records（向下增长）和Page Directory（向上增长）之间是留给新记录的空间。


## 1. Fil Header

Fil Header分8个部分，如下表：

|Name |Size |Remarks|
|---|---|---|
|FIL_PAGE_SPACE |4|页所在空间的4个ID|
|FIL_PAGE_OFFSET|4|从空间开始处算起的页顺序号|
|FIL_PAGE_PREV|4|以键序排列为标准排序的上一页|
|FIL_PAGE_NEXT|4|以键序排列为标准排序的下一页|
|FIL_PAGE_LSN|8|页的最后一个日志记录的日志序列号|
|FIL_PAGE_TYPE|2|现在定义的类型包括 FIL_PAGE_INDEX, FIL_PAGE_UNDO_LOG, FIL_PAGE_INODE, FIL_PAGE_IBUF_FREE_LIST|
|FIL_PAGE_FILE_FLUSH_LSN|8|至少从LSN(日志序列号)上看，文件已经被刷入磁盘了。(该参数在文件的第一页才有效)|
|FIL_PAGE_ARCH_LOG_NO|4|FIL_PAGE_FILE_FLUSH_LSN被写入(在日志中)时，最后一个被归档的日志文件号|

* `FIL_PAGE_SPACE`是必需的，因为不同的页面可能在同一个文件里的不同空间中。所谓“空间”，是“日志”或“表空间”的通用术语。

* `FIL_PAGE_PREV` 和 `FIL_PAGE_NEXT`是指向后边页和前边页的指针。 为了展示他们是什么，我将画一个两级B树。

~~~
  		+------+
  		| root |
  		+---+--+
    	      |
    +---------+--------+
    |                  |
    v                  v
  +------+          +------+
  | leaf |  <---->  | leaf |
  +------+          +------+
~~~

每个人看到这个B树都知道根页中的条目只想叶子页面。但是很多人经常会忽略叶子页面之间是相互用指针指向的。这个特性使InnoDB能够直接在子页与子页之间索引，而不需要返回根节点的层次。这个特性是不能在经典的B树中看到的，所以这也是为什么InnoDB的这种索引应该被称为B+树吧。

* `FIL_PAGE_FILE_FLUSH_LSN`、`FIL_PAGE_PREV` 和`FIL_PAGE_NEXT`这三个域都与日志有关，所以我推荐你去看我在devarticles.com上文章“[How Logs Work On MySQL With InnoDB Tables](https://www.devarticles.com/c/a/MySQL/How-Logs-Work-On-MySQL-With-InnoDB-Tables/)”。

* `FIL_PAGE_FILE_FLUSH_LSN`和`FIL_PAGE_ARCH_LOG_NO`仅对数据文件的第一页有效。



## 2. Page Header
Page Header分14个部分，如下表：

|Name |Size |Remarks|
|---|---|---|
|PAGE_N_DIR_SLOTS|2|Page Header部分directory slot的个数，初始值为2|
|PAGE_HEAP_TOP|2|指向堆中的第一个记录的记录指针|
|PAGE_N_HEAP|2|堆记录的个数，初始值为2 |
|PAGE_FREE|2|指向第一个空闲记录(free record)的指针|
|PAGE_GARBAGE|2|已删除记录的字节数|
|PAGE_LAST_INSERT|2|指向最后被插入记录的记录指针|
|PAGE_DIRECTION|2|值为PAGE_LEFT, PAGE_RIGHT, 或 PAGE_NO_DIRECTION的其中一个|
|PAGE_N_DIRECTION|2|连续插入相同方向的次数，比如，“最后5次都是插入到左边”|
|PAGE_N_RECS|2|用户记录的个数|
|PAGE_MAX_TRX_ID|8|在页上可能已改变的事务的最高ID(只对辅助索引secondary index设置)|
|PAGE_LEVEL|2|页的索引层数(0代表子页)|
|PAGE_INDEX_ID|8|该页面所属索引的标识符|
|PAGE_BTR_SEG_LEAF|10|B树中子页的file segment header(和这里无关)|
|PAGE_BTR_SEG_TOP|10|B树中非子页的file segment header(和这里无关)|

(我将在我讨论用户记录部分时，说明什么是堆)

一些Page Header的部分需要更深入的解释：

* `PAGE_FREE`: 已经被释放的记录(可能由于删除或迁移)在一个单向链表中。Page Header中的`PAGE_FREE`指向这个链表的第一个记录。record header中(具体来说在记录的Extra Bytes中)的"next"指针指向链表中的下一个记录。

* `PAGE_DIRECTION`和`PAGE_N_DIRECTION`: 知道插入是不是以不断以一定方向的顺序到来是很有用的，它能影响InnoDB的效率。

* `PAGE_HEAP_TOP`、`PAGE_FREE` 和 `PAGE_LAST_INSERT`: 注意，和其他记录指针一样，它们不指向记录的开始处，而是它的Origin(详情参考以前讨论过的[记录结构](https://dev.mysql.com/doc/internals/en/innodb-record-structure.html))。

* `PAGE_BTR_SEG_LEAF` 和 `PAGE_BTR_SEG_TOP` : 这些变量包含了索引节点文件段(index node file segments)的信息(空间ID, 页号和字节偏移量)。InnoDB用这些信息来重建新页。这里有两个变量是因为InnoDB是分开创建子页和更高层级的页的。

## 3. The Infimum and Supremum Records

“Infimum”和“Supremum”是标示有序集的外边界的数学术语。Infimum是最大下限(GLB)，它低于可能的最低键值。Supremum是最小上限(LUB)，因此它大于可能的最大键值。

InnoDB在首次创建索引时，在根页面中自动设置Infimum和Supremum，并且永远不会删除它们。他们为导航做了一个可靠的边界，所以“get-prev”不会漏过开始的部分，“get-next”也不会漏过结尾的部分。此外，Infimum可以是临时记录锁的哑目标。

InnoDB代码注释区分“最小和最大(Infimum和Supremum)记录”和“用户记录”（所有其他类型的）。

infimum和supremum记录可以被认为是索引页面开销的一部分。最初，它们都存在于根页面上，但是随着索引的增长，最小(infimum)记录将存在于第一页或最低的子页面上，最大(supremum)记录将在最后一个页或最大的键页(greatest key page)上的最后一个记录。


## 4. User Records

在页面的“User Records”部分，你可以找到所有用户插入的记录。

有两种在User Records中浏览的方法，取决于你是否想将其视为有顺序组织的还是没有顺序组织的链表。

无顺序列表被称为“堆”。如果你用“不管我下次捡起哪个石头都会摆在最上面”的方法摆一堆石头，而不是根据石头的颜色和大小，那么你最后就得到了一个“堆”。类似的，InnoDB也不想根据B树的键序插入新行(因为那将涉及昂贵的数据的转移切换)，所以它将InnoDB只是在已经存在的行后面直接插入新行(从空闲空间的最上部开始)或者任何行被删除留下来的空间。

但是根据定义，必须按照键值的顺序来访问B树，所以每个记录都有一个记录指针(Extra Bytes中的"next"域)指向键序的下一记录。换句话说，记录是一个单向链表。所以搜索时，InnoDB可以按照键序来访问行。

## 5. Free Space

我觉得从对页的其他部分的讨论，一个页的Free Space部分是什么已经很清楚了。

## 6. Page Directory

页的Page Directory部分具有可变数量的记录指针。有时记录指针被称为“槽”(slots)或“目录槽”(directory slots)。和其他DBMS不同，InnoDB不一定为页面中的每个记录分配有一个slot，而是维护一个稀疏目录，在页满的情况下，每6个记录会有一个slot。

slot会追踪记录的逻辑顺序(键序而不是堆序)。所以如果记录是"A","B","F","D"的物理顺序，那么slot也会是(指向A的指针)(指向B的指针)(指向D的指针)(指向F的指针)。因为slot是按照键序排列的，所以每个slot都有固定的大小，所以很容易通过slot对页面上的记录进行二进制搜索。

(由于Page Directory不是堆每个记录都保有slot，所以二进制搜索只能给出大概位置然后暗涌"next"记录指针找到具体的记录。InnoDB的"稀疏slot"策略还额外占用记录的Extra Bytes部分中的n_owned域，n_owned表示由于自己没有slot需要有多少记录需要被访问)

## 7. Fil Trailer

Fil Trailer只有1部分，如下表：

|Name |Size |Remarks|
|---|---|---|
|FIL_PAGE_END_LSN|8|前4字节表示page的checksum，后4字节和FIL_PAGE_LSN一样|

因为担心InnoDB的架构的完整性，所以产生了页最后一部分--Fil Trailer。由于日志恢复机制恢复的一致状态，不可能出现页只被写一半或者被崩溃打断的情况。但万一哪里真的出了问题，那么有个校验和，并且页的最后有个值必须和页开始的一个值相等，这样总是好的。


