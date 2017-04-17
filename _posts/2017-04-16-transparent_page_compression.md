---
layout: post
title: MySQL InnoDB透明页压缩的简单分析
tags:  innodb mysql 压缩 LZ4 透明页压缩 源码分析
categories: MySQL
---


从MySQL 5.7版本开始，MySQL不仅支持原有的压缩表格式(Table Compression)，还支持一种称为透明页压缩的特性(Transparent Page Compression)。通过阅资料和源码，我对这个特性有了一定的了解。以下我将从它的使用方法、实现原理等方面对它进行简单分析，并同压缩表格式进行一些对比。


## 1. 开启方法

官方文档对于透明页压缩的特性的说明仅仅一页，主要说明了它的使用方法，我也对这页官方文档进行过翻译，详见：[InnoDB Page Compression MySQL文档翻译：InnoDB透明页压缩](http://blog.jcix.top/2017-04-06/innodb_page_compression/)

对于透明页压缩的使用方法，和压缩表格式相同的是，都是通过`CREATE TABLE`或者`ALTER TABLE`语法对于一个表使用的。不同点是压缩表格式使用`ROW_FORMAT=COMPRESSED`这个字段，而透明页压缩使用`COMPRESSION="zlib"`、`COMPRESSION="lz4"`或者`COMPRESSION="None"`这种字段。分别用两种压缩形式创建一个表的例子：

```
## 创建一个表，启用压缩表格式，块的大小为8K
CREATE TABLE t1(c1 INT) ROW_FORMAT=COMPRESSED KEY_BLOCK_SIZE=8;
# 创建一个表，启用透明页压缩，压缩算法为LZ4
CREATE TABLE t1(c1 INT) COMPRESSION="zlib”(“lz4”…);
```

另外要注意：开启透明页压缩需要文件系统和操作系统支持 Sparse File 和 Hole Punching 特性，并且需要开启InnoDB的file-per-table选项。更详细的使用方法见上边的那篇翻译。

## 2. 原理简述

### 2.1. 先说说以前压缩表格式

<!--more-->
对于传统的压缩表格式，其在开启时指定了一个压缩后的页的大小。比如上节的例子中指定的8KB。若每次UPDATE或者INSERT操作后都进行压缩，必然太浪费计算时间，所以InnoDB就在每个页中保有一个叫mlog的空闲区域，所有的修改和插入就都被保存这个空闲区域，当mlog快被填满时，页就会被重新压缩，如果8K不再足以存储压缩后的页，那么页就会分裂。

可见传统的压缩表格式的实现，和InnoDB的页面结构有很大的耦合性。此外，innodb buffer pool中可能会同时存在某个页的压缩和未压缩的形式，或者只包含这个页面的压缩形式，或者两者都不包含，其优化细节较为复杂。

### 2.2. 介绍透明页压缩原理

透明页压缩虽然是最新特性，但是思想却十分简单，我认为其之所以新，也是因为利用了Linux punch hole的新特性[[3]](#参考)。其大概思路就是在压缩时采用了写入文件后进行打洞操作、读入文件后进行解压操作[[4]](#参考)。如下：
```bash
# 压缩
+---------------+     +---------------+     +---------------+     +----------------+
|               |     |               |     |               |     |                |
|  InnoDB原始页  +----->    某种变换    +----->    写入磁盘   +------>   文件打洞     |
|               |     |               |     |               |     |                |
+---------------+     +---------------+     +---------------+     +----------------+

# 解压
+----------------+     +----------------+     +---------------+
|                |     |                |     |               |
|  从磁盘读入的页  +----->  对应的逆变换    +----->   原始数据页    |
|                |     |                |     |               |
+----------------+     +----------------+     +---------------+
```
框图中的变换和逆变换可以对应加密解密、压缩解压等操作，这里肯定是指的压缩和解压操作了。这种思路简介明了，直接将压缩的工作移动到了文件操作这一层，和页的操作解除了耦合。

当然，这也有缺点，因为读入时就全部解压，写入时全部压缩，所以buffer pool中保有的缓存页都是未压缩的，所以相对于buffer pool中多数为压缩页的“压缩表格式“，可能会需要更大的buffer pool(内存)。

## 3. 源码简析

* MySQL 版本： 5.7.17

`extra/lz4`这个文件夹包含了lz4的库函数，而对于InnoDB的透明页压缩的压缩和解压操作，貌似只用到了LZ4_compress_limitedOutput、LZ4_decompress_safe、LZ4_decompress_fast这三个函数。下面列出调用LZ4函数的函数：



### 3.1. 压缩操作

以LZ4压缩算法为例：

* 第一步，调用了LZ4_compress_limitedOutput，LZ4_compress_limitedOutput是LZ4库中LZ4_compress_default函数的直接封装。

```cpp
//LZ4_compress_default函数原型：
int LZ4_compress_default(const char* source, char* dest, int sourceSize, int maxDestSize);
//参数分别是源数据的指针、分配好空间的压缩后数据的指针、源数据大小和最大的压缩后数据大小
//如果压缩成功，则返回写入dest地址的字节数
//如果压缩后数据大于maxDestSize，则压缩失败，返回0
```



* 第二步，将压缩后数据的大小赋值为文件系统块大小的倍数，方便后续的打洞操作。(比如16KB的数据压缩后为11KB，则把压缩后数据的大小赋值为12KB，并把11KB～12KB的空间全部赋值为空字符)。


在MySQL源码`storage/innobase/os/os0file.cc`中:

```cpp
static
byte*
os_file_compress_page(
	Compression	compression,
	ulint		block_size,
	byte*		src,
	ulint		src_len,
	byte*		dst,
	ulint*		dst_len)
{
        //.......
	switch (compression.m_type) {
	case Compression::NONE:
		ut_error;

	case Compression::ZLIB: {
                //.................
		break;
	}

	case Compression::LZ4:
    //这里LZ4_compress_limitedOutput是对LZ4库中LZ4_compress_default函数的直接封装，相当于改了个名字
		len = LZ4_compress_limitedOutput(
			reinterpret_cast<char*>(src) + FIL_PAGE_DATA,
			reinterpret_cast<char*>(dst) + FIL_PAGE_DATA,
			static_cast<int>(content_len),
			static_cast<int>(out_len));
		ut_a(len <= src_len - FIL_PAGE_DATA);
		if (len == 0  || len >= out_len) {
			*dst_len = src_len;
			return(src);
		}
		break;
	default:
		*dst_len = src_len;
		return(src);
	}
	//..........
        
    //以下代码将len变量round up(向上取)到block_size(文件系统的block)的倍数
	len += FIL_PAGE_DATA;

	*dst_len = ut_calc_align(len, block_size); //zjc: dst_len = round up len to multiple of block_size

	ut_ad(*dst_len >= len && *dst_len <= out_len + FIL_PAGE_DATA);

	/* Clear out the unused portion of the page. */
	if (len % block_size) {
		memset(dst + len, 0x0, block_size - (len % block_size));
	}
	return(dst);
}
```



* 3.2. 打洞(hole punching)操作

在MySQL源码`storage/innobase/os/os0file.cc`中:

```cpp
static
dberr_t
os_file_io_complete(
	const IORequest&type,
	os_file_t	fh,
	byte*		buf,
	byte*		scratch,
	ulint		src_len,
	ulint		offset,
	ulint		len)
{
        //....

	if (!type.is_compression_enabled()) { //对于没有开启压缩的页，什么也不做直接返回
		return(DB_SUCCESS);
	} else if (type.is_read()) { //对于读，需要对页面进行解压
		//....

        //os_file_decompress_page函数会直接调用下面解压小节中所引用的Compression::deserialize函数
		return(os_file_decompress_page(
				type.is_dblwr_recover(),
				buf, scratch, len));
		//....

	} else if (type.punch_hole()) { //对于写，压缩已经完成，需要在这里进行打洞
        //....

        //这里检查压缩后的页大小len和文件偏移量offset是否是block_size(文件系统块大小)的整数倍
		ut_ad((len % block_size) == 0); 
		ut_ad((offset % block_size) == 0);
		ut_ad(len + block_size <= src_len);
        //这里开始进行打洞，比如16K页面压到12K，会被打一个4K的洞
		offset += len;
		return(os_file_punch_hole(fh, offset, src_len - len)); 
	}

        //....

}
```


### 3.3. 解压缩操作

在MySQL源码`storage/innobase/os/os0file.cc`中:

```cpp
dberr_t
Compression::deserialize(
	bool		dblwr_recover,
	byte*		src,
	byte*		dst,
	ulint		dst_len)
{
        //....... 
	switch(compression.m_type) {
	case Compression::ZLIB: {
		//..........
		break;
	}
	case Compression::LZ4:
		if (dblwr_recover) {
			ret = LZ4_decompress_safe( 
				reinterpret_cast<char*>(ptr),
				reinterpret_cast<char*>(dst),
				header.m_compressed_size,
				header.m_original_size);
		} else {
			/* This can potentially read beyond the input
			buffer if the data is malformed. According to
			the LZ4 documentation it is a little faster
			than the above function. When recovering from
			the double write buffer we can afford to us the
			slower function above. */
			ret = LZ4_decompress_fast( //这里进行解压操作
				reinterpret_cast<char*>(ptr),
				reinterpret_cast<char*>(dst),
				header.m_original_size);
		}
		if (ret < 0) {
			if (block != NULL) {
				os_free_block(block);
			}
			return(DB_IO_DECOMPRESS_FAIL);
		}
		break;
	default:
                //..........
		return(DB_UNSUPPORTED);
	}
	//............
	return(DB_SUCCESS);
}
```

---


## 4. 参考

> 1. [InnoDB Page Compression MySQL文档翻译：InnoDB透明页压缩](http://blog.jcix.top/2017-04-06/innodb_page_compression/), blog.jcix.top, 2017
> 2. [How Compression Works for InnoDB Tables MySQL文档翻译：InnoDB表压缩工作原理](http://blog.jcix.top/2017-04-06/innodb_table_compression/), blog.jcix.top, 2017
> 3. [Punching holes in files](https://lwn.net/Articles/415889/), LWN.net, Jonathan Corbet, November 17, 2010
> 4. [InnoDB Transparent Page Compression](http://mysqlserverteam.com/innodb-transparent-page-compression/), mysql server team, August 18, 2015
> 5. [how innodb lost its advantage](https://dom.as/2015/04/09/how-innodb-lost-its-advantage/), Domas Mituzas, 2015/04/09
