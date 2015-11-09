# Longest Common Prefix

## 题目
> Write a function to find the longest common prefix string amongst an array of strings.

* 大意： 写一个函数，找到一组字符串的公共最长前缀。

## 思路

我的：定义一个不断更新的变量，存储当前的最长前缀，循环时加以一定的优化，比如如果下一个字符串比当前的前缀还长，那么可以截断前缀后在进行比较。
参考的：这道题在discuss上看到了一些运用了python语法的解法，用到了zip,reduce,set等python特有的语法，顺便贴出。

## 代码
### 原创(Python):
~~~python
class Solution(object):
    def longestCommonPrefix(self, strs):
        """
        :type strs: List[str]
        :rtype: str
        """
        if len(strs) == 0:
            return ""
        if len(strs) == 1:
            return strs[0]
        com_str = list(strs[0])
        for i in range(1, len(strs)):
            if len(strs[i]) < len(com_str):
                com_str = com_str[0:len(strs[i])]
            for j in range(len(com_str)):
                if com_str[j] != strs[i][j]:
                    com_str = com_str[0:j]
                    break
~~~

### Python(用了zip)
([《A pythonic solution, 52 ms》](https://leetcode.com/discuss/38113/a-pythonic-solution-52-ms))
~~~python
def longestCommonPrefix(self, strs):
    prefix = '';
    # * is the unpacking operator, essential here
    for z in zip(*strs):
        bag = set(z);
        if len(bag) == 1:
            prefix += bag.pop();
        else:
            break;
    return prefix;
~~~

### Python(用了reduce)
([《Simple Python solution》](https://leetcode.com/discuss/19303/simple-python-solution))
~~~python
class Solution:
    def lcp(self, str1, str2):
        i = 0
        while (i < len(str1) and i < len(str2)):
            if str1[i] == str2[i]:
                i = i+1
            else:
                break
        return str1[:i]
    def longestCommonPrefix(self, strs):
        if not strs:
            return ''
        else:
            return reduce(self.lcp,strs)
~~~