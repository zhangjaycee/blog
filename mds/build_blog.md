# 运用jekyll+Nginx+docker博客的总结

## 博客由来

今年暑假的时候就听说github上可以免费搭建静态博客。当时虽然看了看，但还是因为服务器、网页等知识欠缺太多，几次想动手都没有坚持下去。

最近看了看Nginx的有关知识，算是对http服务器的搭建有了个大概了解。后来看到了docker，就买了《第一本docker书》这本书看了看，发现上边有些例子写的挺不错，其中就有jekyll+Apache搭建静态博客的例子，照着做一遍后，我决定用Nginx作服务器，用docker做载体，用jekyll作为网站生成工具，将这个静态博客搭建在阿里云服务器上。

于是这个博客最终在10月18日时算是初步搭建成功了，现在写这篇总结应该是算有点晚，但是由于很多细节我还欠缺很多，而且搭建博客所涉及的方面太多，很多部分我只是照搬他人成果，所以关于一些细节问题以后还要深入学习，然后再总结出来，请大家和自己期待~

## 资源和费用

#### 服务器：
* 我用了最便宜的那种[阿里云](http://www.aliyun.com/)服务器，但是搭这个博客绰绰有余。
* 价格：学生优惠的9.9元/月。

#### 域名：
* 在[万网](http://wanwang.aliyun.com/)申请的域名（貌似和阿里云并在一起了，所以做域名映射非常友好简单）
* 价格：买了一年，5元/年（但是再续费就贵多了）

#### 代码托管（不是必要的）：
* 用于存我的博客目录，包括这个小的静态网页的所有的一切。
* 价格：免费（github student pack）


——如此看来，搭建个博客费用是很低的，一个月10块。


## 组成一 ：jekyll

~~~
jekyll是一个简单的免费的Blog生成工具，类似WordPress。但是和WordPress又有很大的不同，原因是jekyll只是一个生成静态网页的工具，不需要数据库支持。但是可以配合第三方服务,例如Disqus。最关键的是jekyll可以免费部署在Github上，而且可以绑定自己的域名。				——百度百科
~~~

个人感觉，jekyll是一个像使用模板一样简单的工具，只要你按照他的文件夹结构，将对应的文件放到对应的位置，然后`jekyll build`一下，你的网站就生成好了！。。而且配置可以集中在一个_config.yml文件中，真的很方便，即使像我一样以前没有接触过，把别人写的博客目录拿过来，也可以仿照着改成自己想要的样子。

所以，我这个博客采用的就是[@RainyAlley](https://github.com/dubuyuye)提供的模板（[github页面](https://github.com/dubuyuye/blog)）目录，然后做了一些自己的修改。

关于jekyll的介绍和文档和介绍，这个是官网的中文版:
[http://jekyll.bootcss.com/](http://jekyll.bootcss.com/)

## 组成二 ：nginx

~~~
Nginx ("engine x") 是一个高性能的 HTTP 和 反向代理 服务器，也是一个 IMAP/POP3/SMTP 服务器。 Nginx 是由 Igor Sysoev 为俄罗斯访问量第二的 Rambler.ru 站点开发的，第一个公开版本0.1.0发布于2004年10月4日。其将源代码以类BSD许可证的形式发布，因它的稳定性、丰富的功能集、示例配置文件和低系统资源的消耗而闻名。2011年6月1日，nginx 1.0.4发布78。				——百度百科
~~~

nginx肯定比jekyll的知名度高很多，他就像apache是个服务器软件。nginx可以做网站服务器，反向代理（过几天我还要写个关于反向代理的总结，这里先占位。。过几天贴链接），邮件服务器……

在搭建本博客中，nginx起的作用就是一个静态网站服务器，只要在相关的配置文件中写好网站的目录，写好对应的域名，就可以运行起来了~~

## 组成三 ：docker

~~~
Docker 是一个开源的应用容器引擎，让开发者可以打包他们的应用以及依赖包到一个可移植的容器中，然后发布到任何流行的 Linux 机器上，也可以实现虚拟化。容器是完全使用沙箱机制，相互之间不会有任何接口（类似 iPhone 的 app）。几乎没有性能开销,可以很容易地在机器和数据中心中运行。最重要的是,他们不依赖于任何语言、框架包括系统。				——百度百科
~~~

其实我感觉，docker不能算是一个组成，而是一个载体，为什么用docker呢？
* 第一，我可以灵活的部署和删除我的博客的组成的任意一部分（虽然本博客只有两部分：服务器Nginx和博客生成工具Jekyll）。具体是体现在哪呢？比如，我想换一台服务器，我只要把博客所在的docker容器和服务器所在的docker容器搬到新的服务器主机上就行了，省去了复杂的配置过程；而且，如果我不想用nginx，我想用apache了，只要用`docker stop`停止Nginx的容器，再用`docker start`开启Apache服务器容器，这样只要这两个容器都配置好连接到我的jekyll容器，就可以快速的切换服务器软件了，这样整个服务就像分成了相互通过接口连接的很多小盒子，你只需要关心有联系的部分，不用担心其他地方产生奇怪的冲突，因为每个docker容器里就相当于一个独立的linux系统！
	
* 第二，我正好在看docker的书，所以我就是想试着用用(其实主要是这个原因)。

## 搭建步骤
（还没写完，详细步骤待续，先列个提纲）

1. 申请阿里云服务器，申请域名，并把域名绑定到服务器公网ip

2. 登陆云服务器，安装docker，安装git

3. 通过dockerfile构建Nginx和Jekyll容器

4. fork和clone某一jekyll博客模板到服务器主机上

5. 通过Jekyll容器的运行，生成静态网站文件

6. 让Nginx容器和Jekyll容器通过卷（volume）连接，运行Nginx，网站搭建成功