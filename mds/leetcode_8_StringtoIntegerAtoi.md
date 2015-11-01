# String to Integer (atoi)

## 题目：
> Implement atoi to convert a string to an integer.

* 大意：就是手动实现C语言里常用的atoi函数。。。

## 思路和吐槽：
我最讨厌这种了，完全的信息不对称。。要讨论的情况只有不断提交才知道出题人什么意思，我怎么知道你要求的是什么，况且这是算法题又不是工程题。。。。幸亏这道题比较简单，多试几次也不太费时。

## 代码
### Python

~~~python
class Solution(object):
    def myAtoi(self, str):
        """
        :type str: str
        :rtype: int
        """
        str = str.strip()
        if not str:
            return 0
        ans = []
        neg = "-"
        pos = "+"
        ch = str[0]
        if  ch == neg:
            c = -1
        elif ch == pos:
            c = 1
        elif ch.isdigit():
            ans.append(ch)
            c = 1
        else:
            return 0
        for ch in str[1:]:
            if ch.isdigit():
                ans.append(ch)
            else:
                break
        ans_str = "".join(ans)
        if ans_str:
            ans =  c * int(ans_str)
            if ans > 2147483647:
                return 2147483647
            elif ans < -2147483648:
                return -2147483648
            else:
                return ans
        else:
            return 0  
~~~