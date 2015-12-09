---
layout: post
title: LeetCode第20/32题:Valid Parentheses和Longest Valid Parentheses 总结
tags: leetcode 算法 python dp 
categories: LeetCode
---


## 题目一:
>Given a string containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.

>The brackets must close in the correct order, "()" and "()[]{}" are all valid but "(]" and "([)]" are not.

*大意：给定一个字符串，只包含"(){}[]"这些字符，判断字符串的括号是否都匹配。

### 思路

显然是用栈的思想做。

###代码
(Python)
~~~python
class Solution(object):
    def isValid(self, s):
        """
        :type s: str
        :rtype: bool
        """
        l = ['0']
        for ch in s:
            if ch == "(" or ch == "[" or ch == "{":
                l.append(ch)
            elif ch == ")":
                if l.pop() != "(":
                    break;
            elif ch == "]":
                if l.pop() != "[":
                    break;
            elif ch == "}":
                if l.pop() != "{":
                    break;
        else:
            if len(l) == 1:
                return True
        return False
~~~

## 题目二:
>Given a string containing just the characters '(' and ')', find the length of the longest valid (well-formed) parentheses substring.

>For "(()", the longest valid parentheses substring is "()", which has length = 2.

>Another example is ")()())", where the longest valid parentheses substring is "()()", which has length = 4.

* 大意：给定一个只包含"("或者")"的字符串，判断最长的有效括号对，返回长度。比如：")()())"的最长有效括号对为，"()()"，长度为4。

### 思路
DP的思路：dp[i]代表第i个字符处结束的最大匹配串长度，
~~~
如果第i个字符为"(":
	则dp[i]肯定为0;
如果第i个字符为")":
	如果第i-1个字符为"("：
    	则dp[i] = dp[i - 2] + 2;
    如果第i-1个字符为")“且s[i - dp[i - 1] - 1]为"("：
    	则dp[i] = dp[i - 1] + 2 + dp[i - dp[i - 1] - 2]

~~~

> 参考:
> 《My DP, O(n) solution without using stack》( https://leetcode.com/discuss/8092/my-dp-o-n-solution-without-using-stack )
###代码(python):
~~~python
class Solution(object):
    def longestValidParentheses(self, s):
        """
        :type s: str
        :rtype: int
        """
        max_len = 0
        dp = [0 for i in xrange(len(s))]
        for i in xrange(len(s)):
            if s[i] == "(":
                dp[i] = 0
            else: #ch == ")"
                if i - dp[i - 1] -1 >= 0 and s[i - dp[i - 1] - 1] == "(":
                    dp[i] = dp[i - 1] + 2 + (dp[i - dp[i - 1] - 2] if i - dp[i - 1] - 2 >= 0 else 0)
                    max_len = max(max_len, dp[i])
        return max_len
~~~
