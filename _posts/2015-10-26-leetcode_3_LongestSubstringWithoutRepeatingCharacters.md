---
layout: post
title: LeetCode第3题:Longest Substring Without Repeating Characters总结
tags: leetcode 字典 字符串 算法 python c++ 
categories: LeetCode
---


## 题目：
> Given a string, find the length of the longest substring without repeating characters. For example, the longest substring without repeating letters for "abcabcbb" is "abc", which the length is 3. For "bbbbb" the longest substring is "b", with the length of 1.

**大意**：给出一个字符串，找出不包含重复字母的最长字串，输出字符串的长度。

这道题是一个字符串的题，好久不写明显手生，所以一些细节耗费了很多时间去调试，希望自己慢慢熟悉起来。

## 思路：
我的大概思路就是：
* 对字符串进行一次遍历，用一个大小为256（ascii最多有256种字符）数组记录每个字母最后一次的下标。
* 当当前字符以前出现过时就覆盖原来的数组元素，并且更新start值。
* 每次循环时检查`当前下标i-开始下标start`和一个记录当前最大串长度的`max`变量的关系，将`max`保持或更新。
* 需要注意的是，我更新start和max是在检测到重复字母时进行的，而最后一个字符不一定和前边重复，所以循环外要附加一次更新`max`的操作。

###C++:
第一次提交了C++版本的代码，大概思路就是用一个
~~~cpp
class Solution {
public:
    int lengthOfLongestSubstring(string s) {
        if ( s.empty() )
            return 0;
<!--more-->
        int alphabet[256] = {0};
        memset(alphabet,0,sizeof(alphabet));
        int max = 1;
        int start = 1;
        int ascii;
        int i = 0;
        int flag = 0;
        for (char ascii : s){
            i++; //first index is 1
            if (alphabet[ascii] >=start){
                if (i - start > max){
                    max = i - start;
                }
                start = alphabet[ascii] + 1;
                flag = 1; 
            }else{
                flag = 0;
            } 
            alphabet[ascii] = i;
        }
        if (flag == 0 && i + 1 - start > max){
                    max = i + 1 - start;
        }
        return max;
    }
};
~~~

后来在leetcode的discuss里看到了一种只有9行的cpp版本代码，竟发现思路和我基本一样，只是用了vector容器，并且循环时循环到了下标后的一位，所以既不用添加循环后边的特殊情况，也缩短了代码行数，代码如下:
> 原帖：《[C++ code in 9 lines.](https://leetcode.com/discuss/59051/c-code-in-9-lines)》
> ~~~cpp
> int lengthOfLongestSubstring(string s) {
        vector<int> dict(256, -1);
        int maxLen = 0, start = -1;
        for (int i = 0; i != s.length(); i++) {
            if (dict[s[i]] > start)
                start = dict[s[i]];
            dict[s[i]] = i;
            maxLen = max(maxLen, i - start);
        }
         return maxLen;
     }
> ~~~


### Python

后来又写了Python版本的，看了下discuss发现一个和C++版本思路差不多的，然后我又写了一个用list这个python内置结构的，个人感觉可以体现出python的特点，但是相比之下，我自己写的速度要慢一些。
* 参考版本：

>原帖：《[A Python solution - 85ms - O(n)](https://leetcode.com/discuss/31079/a-python-solution-85ms-o-n)》
~~~python
class Solution:
    # @return an integer
    def lengthOfLongestSubstring(self, s):
        start = maxLength = 0
        usedChar = {}
        for i in range(len(s)):
            if s[i] in usedChar and start <= usedChar[s[i]]:
                start = usedChar[s[i]] + 1
            else:
                maxLength = max(maxLength, i - start + 1)
            usedChar[s[i]] = i
        return maxLength
~~~

* 自己的版本：

~~~python
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        max_len = 0
        subs = []
        for ch in s:
            if ch in subs:
                max_len = max(len(subs), max_len)
                subs = subs[subs.index(ch) + 1:]
            subs.append(ch)
        max_len = max(len(subs), max_len)
        return max_len
~~~
