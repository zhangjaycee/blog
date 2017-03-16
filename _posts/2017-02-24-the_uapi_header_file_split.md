---
layout: post
title: The UAPI header file split 翻译：内核源码中UAPI头文件分割
tags: linux 内核 翻译 lwn.net
categories: Linux
---

在LWN.net上的一篇文章，The UAPI header file split（By Michael Kerrisk July 25, 2012）。原文链接：https://lwn.net/Articles/507794/

这个特性已经在3.7版本中被Linus大神接受[[详情](https://lwn.net/Articles/519762/)]。。。Linus大神如是说：

```
 - the "uapi" include file cleanups. The idea is that the stuff
exported to user space should now be found under include/uapi and
arch/$(ARCH)/include/uapi.

   Let's hope it actually works. Because otherwise this was just a
totally pointless pain in the *ss. And regardless, I'm definitely done
with these kinds of "let's do massive cleanup of the include files"
forever.
```

下面我逐段意译一下文章。。。

---





<!--more-->

为开源软件项目添加新功能或特性的补丁通常会得到最多的关注。 然而，一旦项目达到一定大小，提高代码整体可维护性的重构工作至少也同样重要。虽然这样的工作不能改善用户体验，但是当以后真正添加新功能时，它减轻了开发人员的工作。

在最近的3.5版本中，大约有1500万行代码（包括17161个.c文件和14222个.h文件），Linux内核确实成为了那种足够大的、有必要进行定期重构项目。然而，庞大的代码库意味着重构变成一个难以完成的任务，它几乎不能手动完成。在这一点上，一些有理想的内核hacker就可能转而编写用于重构代码的代码。 David Howell就使用了这种方法，他的UAPI补丁系列，已经提出的在最近几个内核合并窗口中包含了。

UAPI补丁集的想法是David在修改内核代码时的一些观察想到的：

> 我偶尔遇到一个问题，我不能在头文件中写入一个inline函数，因为我需要访问的另一个头文件正好包含我在修改的头文件。 因此，我最终只能把它写为一个#define了。

他继续说明“递归include”这个问题通常发生在inline函数：

> 通常情况是，一个A头文件中的inline函数，需要一个B头文件中的struct，但是同时B中也有一个inline函数需要A中的一个struct。

就像这样的事情，一个小问题可以导致思考更一般化的问题，以及如何解决它们， David已经设计了一个宏伟的九步计划的变化，以实现他的目标，其中当前的补丁集 只是第一步。 然而这个步，对于代码的改动来说，却是很大的一步。

David想要做的是把include和arch/xxxxxx/include目录中的内核头文件中有关用户空间API的内容分割出来，放到新的uapi/子目录中相应的地方。 David指出，分解头文件这一步骤除了解决他原本的问题，并进行一些其他的代码清理，还有许多其他好处。 它简化和减少了仅供内核使用的头文件的大小，而且，将用户空间API分解为单独的头文件具有更令人满意的结果，即它 “简化了**当前**只是部分暴露给用户空间的头文件之间的复杂相互依赖关系“。

UAPI分割的另一个好处是符合更大的Linux生态的一些特定利益。 通过将所有用户空间API相关定义放到专用于相应任务的文件中，跟踪对内核向用户空间呈现的API的更改变得更容易。 在第一种情况下，可以通过翻阅git logs产看uapi/子目录下文件的更改来发现这些改变。 简化用户空间API的变化跟踪，将对Linux生态对很多其他部分有利，例如，C库维护者、包含用户空间API的语言绑定的脚本语言项目、测试项目（如LTP）、文档项目（如man-pages），甚至在LWN的小编在准备写内核发布周期开始时的合并窗口中更改的摘要时。

将每个头文件分解为两个部分的任务原则上是直截了当的。 一般情况下，每个头文件具有以下形式：

```cpp
 /* Header comments (copyright, etc.) */

    #ifndef _XXXXXX_H     /* Guard macro preventing double inclusion */
    #define _XXXXXX_H

    [User-space definitions]

    #ifdef __KERNEL__

    [Kernel-space definitions]

    #endif /* __KERNEL__ */

    [User-space definitions]
  
    #endif /* End prevent double inclusion */
```

上述部分中的每一个可以存在或可以不存在于单独的头文件中，并且可以存在由`#ifdef__KERNEL__`预处理器伪指令管理的多个块。

这个文件最有趣的部分是位于最外面的`#ifndef`块中的代码，它防止了头文件的双重包含，在该块中且未在`#ifdef __KERNEL__`块中的所有内容都应移动到相应的uapi/头文件中。`#ifdef __KERNEL__`块中的内容保留在原始头文件中，但会删除`#ifdef __KERNEL__`及对应的`#endif`。

头部注释的仍保留在原始头文件中，并且在新的uapi/头文件中有一份拷贝。 此外，原头文件中需要新的#include，包含它对应的uapi/头文件，当然一个合适的`git commit`消息需要提供。

目标是把原始头文件改成下面的样子：

```cpp
    /* Header comments (copyright, etc.) */

    #ifndef _XXXXXX_H     /* Guard macro preventing double inclusion */
    #define _XXXXXX_H

    #include <include/uapi/path/to/header.h>

    [Kernel-space definitions]

    #endif /* End prevent double inclusion */
```

同时相应的uapi/ 头文件是这样子:

```cpp
    /* Header comments (copyright, etc.) */

    #ifndef _UAPI__XXXXXX_H     /* Guard macro preventing double inclusion */
    #define _UAPI__XXXXXX_H

    [User-space definitions]

    #endif /* End prevent double inclusion */
```

当然，为了正确地自动化完成这个任务，有各种细节要处理。 首先，如果原始标头中没有`#ifdef __KERNEL__`块，会只产生一个结果文件，即原始头文件会被重命名为uapi/的文件。如果头文件可以分解为两个文件，也有很多其他细节需要处理。 例如，如果有#include指令保留在原始头文件的顶部，那么对uapi/文件的#include应放在原始文件的#include指令之后（以防uapi/文件依赖它们）。此外，还存在一些明确不用于内核空间的代码片段（即它们仅用于用户空间），例如，由`#ifndef__KERNEL__`管理的片段。这些片段应该迁移到uapi/文件，同时保留保护`#ifndef __KERNEL__`的提示。

David的脚本处理所有上述细节，以及许多其他细节，包括对.c源文件和各种内核build文件的更改。 自然地，没有脚本能够正确地处理所有人类创造文件，因此当前补丁集的一部分包括预补丁，其添加标记以“训练”脚本在这些情况下做正确的事情。

编写自动化脚本来执行此类任务成为一个编程项目是有道理的，用于完成任务的shell和Perl脚本（.tar.xz存档）总共超过1800行。 （使用脚本生成补丁集具有显着的好处，即补丁集可以自动刷新，因为相关的内核源文件被其他内核开发人员更改了。由于UAPI补丁可能涉及大量文件，这是很重要的一点 。）

知道这些脚本的大小以及编写它们所需要的努力，我们就知道内核代码的实际变化规模可能更大。 事实上也是这样的， 在其当前的形式中，UAPI补丁系列包括74个提交，其中65个是脚本化的（脚本化的更改以整个目录为单位向内核源代码树提交更改）。 总而言之，这些补丁触及超过3500个文件，并且更改的`diff `超过30万行。

这些变化的规模带来了David的下一个问题：如何让这些更改获得Linus大神的接受。问题是，不可能手动review完这个量级的源码更改。即使是部分审查也需要付出相当大的努力，并且不能对剩余未审查的更改给出保证。 就是在缺少这样的reviews的情况下，当Linus大神收到David在3.5版本的合并窗口pull这些补丁的request后，他采用了一个历史悠久的策略：请求被忽略。😳

虽然David大约一年前开始着手这些变化，但是Linus到现在还没有直接对它们发表评论。然而，在1月份Linus接受了UAPI工作的一些预备补丁，这表明他至少知道这个提议，并可能愿意接受。其他内核开发人员表示支持UAPI拆分。然而，可能是因为变化如此巨大，获得实际的reviews和"Acked-by[[1](http://webcache.googleusercontent.com/search?q=cache:6bX1t2xNTnYJ:linux-kernel.2935.n7.nabble.com/acked-by-meaning-td551744.html+&cd=1&hl=en&ct=clnk&gl=us)]"标签已经证明是一个挑战。考虑到不可能完全手动检查变化，最好的希望似乎是让其他开发人员审查David的脚本使用的概念方法，可能审查脚本本身，审查更改的内核源文件的示例，并在尽可能多的不同架构上执行内核构建。（有抱负的内核hacker可能会注意到，这个相当重要的内核工作的大部分审查任务不需要深入了解内核的工作。）

对任何一组内核补丁来说，获得足够多的审查都是常有的难题，更不用说集合这么大。 事情至少向前迈出了一步，David要求Linus在当前打开的3.6合并窗口接受补丁，当Arnd Bergmann对整个补丁集给出了他的"Acked-by"。无论着是否是足够的，或Linus是否希望在接受补丁之前看到更多开发人员的正式同意是一个悬而未决的问题。 如果它被证明不足在这个合并窗口并入，那么下一次将需要重新思考如何将如此大的改变被接受并入到内核主线中。



