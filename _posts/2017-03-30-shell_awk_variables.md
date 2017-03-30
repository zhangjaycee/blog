---
layout: post
title: 在awk中如何使用或赋值shell的变量
tags:  shell awk linux
categories: linux
---

写shell脚本处理文本的时候，经常用到awk来配合shell命令。但是awk的大括号中和shell貌似是两个世界。本文只介绍最容易理解的方法（作者水平有限，复杂的以后可能补充），来实现awk对的shell变量的使用和更改。

如果我们将awk看成变成语言中的函数，或者一个封装，那么要使用或者修改外部的变量，其实就是输入参数和输出返回值的问题。对于使用shell变量，其实就是shell变量怎么作为参数传入awk的问题；而对于awk给shell变量赋值，可以看成awk输出返回值的问题。

## awk中使用shell变量

awk传入参数的选项是`-v [awk_var=$SHELL_VAR]`，应该加在' '包围的awk主体程序之前。

示例脚本1：
```bash
#!/bin/bash

VAR1="~~~!"
echo hello, world|awk -v awk_var1=$VAR1 '{ print $1, "shell", $2, awk_var1 }'
```

输出:
```
hello, shell world ~~~!
```

## awk给shell变量赋值

* 单个变量

既然对于awk给shell变量赋值，可以看成awk输出返回值的问题。对于单变量的返回问题，可以利用shell中反引号的语法。反引号\`\`中的命令的结果的值可以保留下来赋给一个变量，其中的命令当然也可以是awk的。

示例脚本2：
```bash
#!/bin/bash

VAR1="~~~!"
VAR2=`echo hello, world|awk -v awk_var1=$VAR1 '{ print $1, "shell", $2, awk_var1 }'`
echo $VAR2
```

输出:
```
hello, shell world ~~~!
```
* 多个变量

对于多个变量的赋值，需要先简单说明一下要利用的eval命令，eval命令可以将它的参数当作shell命令执行一次，比如:

示例脚本3:
```bash
#!/bin/bash
eval VAR1=hello;VAR2=world
echo $VAR1, $VAR2
```

输出：
```
hello, world
```

但是上面的脚本中不加"eval"的话，结果是一样的，有什么区别吗？ 个人理解，如果遇到脚本每次执行的命令不一定一样的情况，我们只需要在脚本中生成本次要执行命令字符串，然后结合这个eval命令就可以实现。

具体到awk程序，我们可以把awk看成一个生成命令字符串“中间程序”，再对应我们现在的多变量赋值问题，世界上就是生成一个类似"VAR1=123;VAR2=321;VAR3=111"这种字符串了。

所以，虽然这里说的是多变量赋值，但是实际上 **还是利用上面所说的单变量输出的办法，只不过这次的这个单变量是一个字符串变量--包含shell命令的字符串 **。你可能觉得好绕口啊！那就看个例子吧：

示例脚本4:
```bash
#!/bin/bash

eval `echo hello welcome to the shell world | awk '{
    printf("VAR1=%s; VAR2=%s", $1, $6)
}'`
echo $VAR1, $VAR2
```

输出：
```
hello, world
```

> [What is the “eval” command in bash?] http://unix.stackexchange.com/questions/23111/what-is-the-eval-command-in-bash
> [AWK调用SHELL，并将变量传递给SHELL]http://smilejay.com/2014/01/awk-call-shell/



