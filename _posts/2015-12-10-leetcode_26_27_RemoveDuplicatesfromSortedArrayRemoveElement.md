---
layout: post
title: LeetCode第26/27题:Remove Duplicates from Sorted Array和Remove Element 总结
tags: leetcode 算法 python   
categories: LeetCode
---

##　题目一
>Given a sorted array, remove the duplicates in place such that each element appear only once and return the new length.

>Do not allocate extra space for another array, you must do this in place with constant memory.

>For example,
Given input array nums = [1,1,2],

>Your function should return length = 2, with the first two elements of nums being 1 and 2 respectively. It doesn't matter what you leave beyond the new length.

* 大意：给定一个已排序的数组，在原数组上移除重复元素，让每个元素只出现一次，返回新数组的长度。（注意：不要申请新数组，必须用原数组的常数空间）比如：输入[1, 1, 2]，返回length = 2

### 思路
注意实在原位修改，所以不能定义一个列表然后append。其实我们可以直接在原列表从0开始记录，因为遍历过程中，不可能出现所修改的元素位置比所遍历的位置靠后的情况。
~~~
比如
1 1 2 2 2 3 4
现在遍历到了3的位置，我们把3实际写到了第2个位置（从0开始）
数组此时实际为：
1 2 3 2 2 3 4
遍历位置永远比写入位置靠后或相同
所以只需要记住当前的遍历位置和写入位置两个位置即可
~~~

#### 代码
(Python)
~~~python
class Solution(object):
    def removeDuplicates(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if not nums:
            return 0
        trail_index = 0
        i = 0
        while i < len(nums):
            if nums[i] != nums[trail_index]:
                trail_index += 1
                nums[trail_index] = nums[i]
            i += 1
        return trail_index + 1
~~~

## 题目二
>Given an array and a value, remove all instances of that value in place and return the new length.

>The order of elements can be changed. It doesn't matter what you leave beyond the new length.

* 大意： 和上个题目类似，只不过这次去除的是指定的某个元素

### 思路0
类似上个题目，这次是判断遍历元素是不是指定元素

#### 代码
(Python)
~~~python
class Solution(object):
    def removeElement(self, nums, val):
        """
        :type nums: List[int]
        :type val: int
        :rtype: int
        """
        if not nums:
            return 0
        i = 0
        trail = 0
        while i < len(nums):
            if nums[i] != val:
                nums[trail] = nums[i]
                trail += 1
            i += 1
        return trail
~~~

### 思路1
对于Python，可以直接用remove操作，删除指定元素。

#### 代码
(Pyhton)
~~~python
class Solution(object):
    # not mine
    def removeElement(self, nums, val):
        for x in nums[:]:
            if x == val:
                nums.remove(val)
        return len(nums)
~~~

> 参考:
> 
> 《del remove 和 pop的区别》( http://novell.me/master-diary/2014-06-05/difference-between-del-remove-and-pop-on.html )
