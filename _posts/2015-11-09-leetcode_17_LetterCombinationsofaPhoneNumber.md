---
layout: post
title: LeetCode第17题:Letter Combinations of a Phone Number总结
tags: leetcode 算法 python
categories: LeetCode
---
## 题目
> Given a digit string, return all possible letter combinations that the number could represent.

>A mapping of digit to letters (just like on the telephone buttons) is given below.

> ![img][img]

>Input:Digit string "23"
Output: ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"].

> Note:
Although the above answer is in lexicographical order, your answer could be in any order you want.

* 大意：给定一个全是数字的字符串，按这个顺序按在手机九宫格键盘上，输出可能组成的字符串的所有情况。

## 思路
首先，每个按键对应的字母，肯定存在一个表中供后边查询，这里用到了dict的结构存储。
这里的方案是进行循环遍历这个数字字符串，然后对每个数字对应的字母进行遍历，再对现在已经得出的可能遍历，分别追加新的字符。
虽然是三层循环，但是因为中间的一层遍历最多有4个字母，所以复杂度应该为O( n^2 )。

## 代码
### Python
~~~python
class Solution(object):
    def letterCombinations(self, digits):
        """
        :type digits: str
        :rtype: List[str]
        """
        if len(digits) == 0:
            return []
        digit_map = {
            0:"0",
            1:"1",
            2:"abc",
            3:"def",
            4:"ghi",
            5:"jkl",
            6:"mno",
            7:"pqrs",
            8:"tuv",
            9:"wxyz"
        }
        ret = [""]
        for u in digits:
            tmp_list = []
            for ch in digit_map[int(u)]:
                for str in ret:
                    tmp_list.append(str + ch)
            ret = tmp_list
        return ret
~~~

[img]:{{"/2015110902.png" | prepend: site.imgrepo }}
