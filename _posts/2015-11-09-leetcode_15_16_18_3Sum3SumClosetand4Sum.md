---
layout: post
title: LeetCode第15,16,18题:3Sum, 3Sum Closest and 4Sum总结
tags: leetcode 算法 python
categories: LeetCode
---
这三道题明显是一家子，放到一起。。。

## 题目一 3Sum
> Given an array S of n integers, are there elements a, b, c in S such that a + b + c = 0? Find all unique triplets in the array which gives the sum of zero.
> 
> Note:
Elements in a triplet (a,b,c) must be in non-descending order. (ie, a ≤ b ≤ c)
The solution set must not contain duplicate triplets.

> For example, given array S = {-1 0 1 2 -1 -4},
> A solution set is:
(-1, 0, 1)
(-1, -1, 2)

* 大意：给定一个有n个整数的数组S，数组中是否存在元素a, b, c使得a + b + c = 0? 找出所有的组合。

## 题目二 3Sum Closest
> Given an array S of n integers, find three integers in S such that the sum is closest to a given number, target. Return the sum of the three integers. You may assume that each input would have exactly one solution.

> For example, given array S = {-1 2 1 -4}, and target = 1.
The sum that is closest to the target is 2. (-1 + 2 + 1 = 2).

* 大意：给定一个有n个整数的数组S和一个给定的目标值tatget，找出数组中三个数a, b, c，使得三个数之和a + b + c最接近target，输出这个和。


## 题目三 4Sum
> Given an array S of n integers, are there elements a, b, c, and d in S such that a + b + c + d = target? Find all unique quadruplets in the array which gives the sum of target.

> Note:
Elements in a quadruplet (a,b,c,d) must be in non-descending order. (ie, a ≤ b ≤ c ≤ d)
The solution set must not contain duplicate quadruplets.

> For example, given array S = {1 0 -1 0 -2 2}, and target = 0.
A solution set is:
(-1,  0, 0, 1)
(-2, -1, 1, 2)
(-2,  0, 0, 2)

* 大意： 同题目一，和题目一唯一的不同是从三个数变成了四个数。

## 思路和题解(Python)
### 思路一 (3Sum)
其实，3sum这道题也是和leetcode第一题Two Sum类似的，回顾Two Sum这道题，发现，可以利用哈希的思想，创建一个数组/map（python就可以是dict）把O( n^3 )的复杂度降为( n^4 )。

这里把这种方法用dict实现，具体思路是：
1. 先遍历所给数组，以数为key，数出现的次数为value，创建一个dict；
2. 然后两层循环选定前两个数a, b（O( n^2 )），进行常数查找(0 - a - b)是否存在字典中，若存在，则将这个三元组添加到待返回的list变量ret中。

需要注意两点：
1. 注意选定前两个数时，**暂时**将对应的count值-1；
2. 注意将符合条件的组合添加到ret前，检查ret中是否存在有重复的组合。

代码如下：
~~~python
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        ret = []
        dict_num = {} #dict_num[num] = count
        for value in nums:
            if value in dict_num:
                dict_num[value] += 1
            else:
                dict_num[value] = 1
        for value in dict_num:
            dict_num[value] -= 1
            for value2 in dict_num:
                dict_num[value2] -= 1
                if dict_num[value2] < 0:
                    continue
                value3 = 0 - value2 - value
                if value3 in dict_num and dict_num[value3] > 0:
                    tmp_list = sorted([value, value2, value3])
                    if tmp_list not in ret: 
                        ret.append(sorted(tmp_list))
                dict_num[value2] += 1
            dict_num[value] += 1
        return ret
~~~
### 思路二 (3Sum, 3Sum Closest and 4Sum)
但是，当我再想用这种思路解决问题二(3Sum Closest)时，就会发现目标并不是一个定值，所以查表确定是否符合条件的思路就行不通了，因为这道题是让我们解决最优的问题，而不是确切数值的问题。

所以经过百度发现，其实这类问题还可以个用另一种方法，步骤如下：
1. 将所给数组排序
2. 定义两个指向最小数和最大数的”游标“，两边移动”游标“向里逼近，逐步找到目标值

由于这种遍历将两个"游标"，放到一趟进行，向中间逼近，所以会将复杂度降为O( n^2 )

这种思路需要注意的是：
因为没有了上一思路的dict或者map来记录数字出现的次数，所以消除可能出现重复组合需要用到一个消除相同值(remove duplicates)的循环的技巧，详见代码。

用这种思路解决问题一(3Sum)的代码如下：
~~~python
class Solution(object):
    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        ret = []
        nums.sort()
        if len(nums) < 3:
            return ret
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            i_left, i_right = i + 1, len(nums) - 1
            target_sum = -nums[i]
            while i_left < i_right:
                test_sum = nums[i_left] + nums[i_right]
                if test_sum < target_sum:
                    i_left += 1
                elif test_sum > target_sum:
                    i_right -= 1
                else:
                    ret.append([nums[i], nums[i_left], nums[i_right]])
                    while i_left < i_right and nums[i_left] == nums[i_left + 1]:
                        i_left += 1
                    while i_right > i_left and nums[i_right] == nums[i_right - 1]:
                        i_right -= 1
                    i_left += 1
                    i_right -= 1
        return ret
~~~
对于问题二(3Sum Closet)，答题思路是相同的我们只需适当修改上题的代码，在每层循环外更新一个最小相差值（这里分别为`closet`和`sub_closet`），并适当优化（比如当相差0时，可以直接return）

用这种思路解决问题二(3Sum Closet)的代码如下：
~~~python
class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums.sort()
        closet = sys.maxint
        for i in range(len(nums) - 2):
            if i > 0 and nums[i] == nums[i-1]:
                continue
            i_left, i_right = i + 1, len(nums) - 1
            sub_closet = sys.maxint
            while i_left < i_right:
                test_sum = nums[i] + nums[i_left] + nums[i_right]
                if test_sum < target:
                    i_left += 1
                elif test_sum > target:
                    i_right -= 1
                else:
                    return test_sum
                if sub_closet > abs(test_sum - target):
                    sub_closet = abs(test_sum - target)
                    sub_closet_sum = test_sum
            else:
                if sub_closet < closet:
                    closet = sub_closet
                    closet_sum = sub_closet_sum
        return closet_sum
~~~

对于问题三(4Sum)，不管我们通过上述哪种思路，都只能再在原来复杂度的基础上*n，即复杂度为O( n^3 )，这里的代码，还是用游标指针向中间逼近的方法，只要在3Sum的代码加一层循环，就可以得到本题的代码：

~~~python
class Solution(object):
    def fourSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[List[int]]
        """
        if len(nums) < 4:
            return []
        nums.sort()
        ret = []
        for i1 in range(len(nums) - 3):
            if i1 > 0 and nums[i1] == nums[i1 - 1]:
                continue
            target_1 = target - nums[i1]
            nums_1 = nums[i1 + 1:]
            for i2 in range(len(nums_1) - 2):
                if i2 > 0 and nums_1[i2] == nums_1[i2 - 1]:
                    continue
                target_2 = target_1 - nums_1[i2]
                i_left, i_right = i2 + 1, len(nums_1) - 1
                while i_left < i_right:
                    test = nums_1[i_left] + nums_1[i_right]
                    if test < target_2:
                        i_left += 1
                    elif test > target_2:
                        i_right -= 1
                    else:
                        ret.append([nums[i1], nums_1[i2], nums_1[i_left], nums_1[i_right]])
                        while i_left < i_right and nums_1[i_left] == nums_1[i_left + 1]:
                            i_left += 1
                        while i_right > i_left and nums_1[i_right] == nums_1[i_right - 1]:
                            i_right -= 1
                        i_left += 1
                        i_right -= 1
        return ret
~~~
