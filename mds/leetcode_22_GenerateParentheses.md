# leetcode 22 Generate Parentheses


## 题目
>Given n pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

>For example, given n = 3, a solution set is:

>"((()))", "(()())", "(())()", "()(())", "()()()"


* 大意：给定n对括号，写一个函数来生成所有正确的配对串。


## 思路
生成所有的可能，然后注意检测是不是符合要求。


##代码
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
            if ch == "(":
                l.append(ch)
            elif ch == ")":
                if l.pop() != "(":
                    break;
        else:
            if len(l) == 1:
                return True
        return False
    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        ret = []
        brackets = ["(",")"]
        if n == 0:
            return [""]
        strs = [""]
        leftn, rightn = n - 1, n
        for i in range(n*2):
            tmp = []
            for s in strs:
                for ch in brackets:
                    tmp.append(s + ch)
            strs = tmp
        for s in strs:
            if self.isValid(s):
                ret.append(s)
        return ret
~~~