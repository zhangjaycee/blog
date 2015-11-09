# Integer to Roman and Roman to Integer

这两道题明显是一对。。。放一起

## 题目一 Integer to Roman
> Given an integer, convert it to a roman numeral.

> Input is guaranteed to be within the range from 1 to 3999.

* 大意： 就是把一个1~3999的阿拉伯数字，变成罗马数字表示。

## 题目二 Roman to Integer
> Given a roman numeral, convert it to an integer.

> Input is guaranteed to be within the range from 1 to 3999.

* 大意： 就是把一个1~3999的罗马数字，表示成阿拉伯数字。

## 思路
|基本字符|I|V|X|L|C|D|M|
|------|--|-|-|-|-|-|-|
|对应的阿拉伯数字|1|5|10|50|100|500|1000|
* 相同的数字连写、所表示的数等于这些数字相加得到的数、如：Ⅲ=3；
* 小的数字在大的数字的右边、所表示的数等于这些数字相加得到的数、 如：Ⅷ=8、Ⅻ=12；
* 小的数字、（限于 Ⅰ、X 和 C）在大的数字的左边、所表示的数等于大数减小数得到的数、如：Ⅳ=4、Ⅸ=9；
* 正常使用时、连写的数字重复不得超过三次。（表盘上的四点钟“IIII”例外）；
* 在一个数的上面画一条横线、表示这个数扩大 1000 倍。

>参考：
>百度百科 罗马数字( http://baike.baidu.com/link?url=4ecgQxgBITojNvEqRX9Hc4z4YrkapYje48mZvTu-MWDcdQtcIOj6lw3OX3kymH7m8Itdya7bSZmgsmtlaJXL0_ )

>个位数举例
Ⅰ－1、Ⅱ－2、Ⅲ－3、Ⅳ－4、Ⅴ－5、Ⅵ－6、Ⅶ－7、Ⅷ－8、Ⅸ－9
十位数举例
Ⅹ－10、Ⅺ－11、Ⅻ－12、XIII－13、XIV－14、XV－15、XVI－16、XVII－17、XVIII－18、XIX－19、XX－20、XXI－21、XXII－22、XXIX－29、XXX－30、XXXIV－34、XXXV－35、XXXIX－39、XL－40、L－50、LI－51、LV－55、LX－60、LXV－65、LXXX－80、XC－90、XCIII－93、XCV－95、XCVIII－98、XCIX－99
百位数举例
C－100、CC－200、CCC－300、CD－400、D－500、DC－600、DCC－700、DCCC－800、CM－900、CMXCIX－999
千位数举例
M－1000、MC－1100、MCD－1400、MD－1500、MDC－1600、MDCLXVI－1666、MDCCCLXXXVIII－1888、MDCCCXCIX－1899、MCM－1900、MCMLXXVI－1976、MCMLXXXIV－1984、MCMXC－1990、MM－2000、MMMCMXCIX－3999


## 代码
### 题目一 Integer to Roman（Python）
~~~python
class Solution(object):
    def intToRoman(self, num):
        """
        :type num: int
        :rtype: str
        """
        roman_10 = {
        0: "",
        1: "I",
        2: "II",
        3: "III",
        4: "IV",
        5: "V",
        6: "VI",
        7: "VII",
        8: "VIII",
        9: "IX",
        }
        roman = []
        thousand = num / 1000
        num = num - thousand * 1000
        handred = num / 100
        num = num - handred * 100
        tens = num / 10
        num = num - tens * 10
        ones = num
        '''
        if thousand == 1:
            roman.append("M")
        elif thousand == 2:
            roman.append("MM")
        elif thousand == 3:
            roman.append("MMM")
        else：
            pass #num < 1000
        '''
        roman.append("M" * thousand)
        if handred == 9:
            roman.append("CM")
        elif handred == 4:
            roman.append("CD")
        else:
            if handred > 4:
                roman.append("D")
                handred -= 5
            if handred > 0:
                roman.append("C" * handred)
        if tens == 9:
            roman.append("XC")
        elif tens >= 5:
            roman.append("L")
            tens -= 5
            roman.append("X" * tens)
        elif tens == 4:
            roman.append("XL")
        else:
            roman.append("X" * tens)
        roman.append(roman_10[ones])
        ret = ""
        return ret.join(roman)
~~~

### 题目二 Roman to Integer（Python）
~~~python
class Solution(object):
    def romanToInt(self, s):
        """
        :type s: str
        :rtype: int
        """ 
        sum = 0
        s = list(s[::-1])
        while len(s) > 0:
            ch = s.pop()
            if ch == "M":
                sum += 1000
            elif ch == "D":
                sum += 500
            elif ch == "C":
                if len(s) > 0:
                    if s[-1] == "D":
                        sum += 400
                        s.pop()
                    elif s[-1] == "M":
                        sum += 900
                        s.pop()
                    else:
                        sum += 100
                else:
                    sum += 100
            elif ch == "L":
                sum += 50
            elif ch == "X":
                if len(s) > 0:
                    if s[-1] == "C":
                        sum += 90
                        s.pop()
                    elif s[-1] == "L":
                        sum += 40
                        s.pop()
                    else:
                        sum += 10
                else:
                    sum += 10
            elif ch == "V":
                sum += 5
            else: ## "I"
                if len(s) > 0:
                    if s[-1] == "X":
                        sum += 9
                        s.pop()
                    elif s[-1] == "V":
                        sum += 4
                        s.pop()
                    else:
                        sum += 1
                else:
                    sum += 1
        return sum
~~~

