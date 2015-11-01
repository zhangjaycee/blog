---
layout: post
title: LeetCode第6题:ZigZag Conversion总结
tags: leetcode 字符串 找规律 算法 python 
categories: LeetCode
---

## 题目
> The string "PAYPALISHIRING" is written in a zigzag pattern on a given >number of rows like this: (you may want to display this pattern in a >fixed font for better legibility)
>
>P   A   H   N
>A P L S I I G
>Y   I   R
>And then read line by line: "PAHNAPLSIIGYIR"
>Write the code that will take a string and make this conversion given a >number of rows:
>
>string convert(string text, int nRows);
>convert("PAYPALISHIRING", 3) should return "PAHNAPLSIIGYIR".

* 大意：把给定的一个字符串，写成指定行数的N字形（ZigZag形），然后从左到右读成新的字符串：
![problem][problem]

## 思路和吐槽
这道题还是没有什么高深的，只是要去找规律，推通式，我再次鄙视下自己的智商。

##代码
###Python
~~~python
class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        max_index = len(s)
        ans = []
        T = 2 * (numRows - 1)
        if numRows == 1 or max_index <= numRows:
            return s
        i = 0
        while(True):
            if i == 0:
                j = 0
                while(True):
                    if j * T + i < max_index:
                        ans.append(s[j * T + i])
                        j += 1
                    else:
                        break
            elif i == numRows - 1:
                j = 0
                while(True):
                    if j * T + i < max_index:
                        ans.append(s[j * T + i])
                        j += 1
                    else:
                        break
                ans_str = ''.join(ans);
                return ans_str
            else:
                j = 0
                while(True):
                    if j * T + i < max_index:
                        ans.append(s[j * T + i])
                    else:
                        break
                    if (j + 1) * T - i < max_index:
                        ans.append(s[(j + 1) * T - i])
                    else:
                        break
                    j += 1
            i = i + 1
            print i
            
~~~


[problem]:{{"/2014110101.png" | prepend: site.imgrepo }}
