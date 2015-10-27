## 题目：
> Given a string S, find the longest palindromic substring in S. You may assume that the maximum length of S is 1000, and there exists one unique longest palindromic substring.

* 大意：就是找出字符串中最大的回文子字符串


## 吐槽：
这应该是一道经典的算法题，可是我还是没有什么好办法，可见我真的是太菜了。哎。。。用了一个O( n^2 )的解法，妥妥的超时了。。。后来看了网上的有关文章和discuss里面的代码，修改了版本。

### 暴力超时版Python代码：
（肯定是我自己写的）
~~~python
class Solution(object):
    def longestPalindrome(self, s):
        longest_str = ""
        longest_len = 0
        for i in range(len(s) - 1):
            j = i - 1;
            while(True):
                j = j + 1 if j + 2 - i > longest_len else longest_len + i
                if j > len(s) - 1 or i + longest_len > len(s):
                    break;
                if i == 0:
                    if s[:j+1:1] == s[j::-1]:
                        longest_str = s[i:j+1]
                        longest_len = len(longest_str)
                else:
                    if s[i:j+1:1] == s[j:i-1:-1]:
                        longest_str = s[i:j+1]
                        longest_len = len(longest_str)
        return longest_str
~~~

### Python（修正版）
~~~python
class Solution(object):
    def longestPalindrome(self, s):
        len_s = len(s)
        max_len = 1
        max_left = 0
        start = 0
        while(True):
            if len_s - start <= max_len / 2 or start >= len_s:
                break;
            left = right = start
            while right < len_s - 1 and s[right] == s[right + 1]:
                right += 1
            start = right + 1
            while left > 0 and right < len_s -1 and s[right + 1] == s[left -1]:
                right += 1
                left -= 1
            if right - left + 1 > max_len:
                max_left = left
                max_len = right - left + 1
        return s[max_left:max_left + max_len]
~~~

***************
### 参考：
《[最长回文字符串](http://www.cnblogs.com/houkai/p/3371807.html)》http://www.cnblogs.com/houkai/p/3371807.html
《[Accepted 4ms c++ solution.](https://leetcode.com/discuss/40559/accepted-4ms-c-solution)》https://leetcode.com/discuss/40559/accepted-4ms-c-solution