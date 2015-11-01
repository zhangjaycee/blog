---
layout: post
title: LeetCode第7题:Reverse Integer总结
tags: leetcode 算法 python
categories: LeetCode
---

## 题目
> Reverse digits of an integer.

>Example1: x = 123, return 321
Example2: x = -123, return -321

* 大意：就是把数字倒过来。。。

## 思路和吐槽
只有吐槽：用Python做简直是太简单了，简直就是在作弊，，，如果我十天之内没用c++再做一遍，我肯定是白做了这道题

## 代码
### Python
~~~python
class Solution(object):
    def reverse(self, x):
        """
        :type x: int
        :rtype: int
        """
        if x < 0:
            symbol = -1
        else:
            symbol = 1
        x = abs(x)
        str_x = str(x)
        ans_list = list(str_x)
        ans_list = str_x[len(str_x) - 1::-1]
        ans_str = "".join(ans_list)
        ans = symbol * int(ans_str)
        return 0 if ans > 2147483647 or ans < -2147483648 else ans
~~~
