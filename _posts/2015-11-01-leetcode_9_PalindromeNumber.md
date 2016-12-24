---
layout: post
title: LeetCode第9题:Palindrome Number总结
tags: leetcode 算法 python 
categories: LeetCode
---

## 题目
> Determine whether an integer is a palindrome. Do this without extra space.

* 大意：判断一个整数是不是回文的。。

## 吐槽：

同第7题：用Python简直就是作弊啊。。。。。

## 代码
### Python

~~~python
class Solution(object):
    def isPalindrome(self, x):
        """
        :type x: int
        :rtype: bool
        """
        x = str(x)
        x = x.strip()
        if x[::1] == x[::-1]:
            return True
<!--more-->
        else:
            return False
~~~
