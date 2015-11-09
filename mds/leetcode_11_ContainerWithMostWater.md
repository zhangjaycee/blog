# Container With Most Water

## 题目
> Given n non-negative integers a1, a2, ..., an, where each represents a point at coordinate (i, ai). n vertical lines are drawn such that the two endpoints of line i is at (i, ai) and (i, 0). Find two lines, which together with x-axis forms a container, such that the container contains the most water.

> Note: You may not slant the container.

* 大意：有n个非负的整数a1到an，ai每个代表i处的高度，(i,ai)和(i,0)是线段i的两个端点，所有任意两个线段i可以和x轴组成一个容器，找出能装最多水的容器。注意：不能倾斜容器。

## 思路
这道题所求的容积和容器下边长度（两个线段的横坐标距离）和侧边最小长度有关（类似木桶效应）。
所以容积 = abs(i2 - i1) * min(ai1, ai2)，我们要找出的就是用那两条线段做边界时，这个容器最大，求出这个最大的容积。

怎么在保证效率的情况下找出这个最大的容积呢？通过查看discuss，发现这个题有一个巧妙的思路：设定两个“游标”，开始分别指向最左和最右。如果一边的线段较低，那么这一边的“游标”就可以向里移动，直到两个“游标”相遇，这样，复杂度就从暴力方法的O( n^2 )变成了O(n)。
为什么可以这样呢？我们可以举个反例：假如最左边线段高度为2，最右边为5，两线段相距为10，如果这时我们向里移动的是右边的线段，那么新容器的容积只会比原来小，而不会比原来大，所以，这样的尝试是没有必要的。

## 代码
### Python
~~~python
class Solution(object):
    def maxArea(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        maxV = 0
        i, j = 0, len(height) - 1
        while True:
            if i == j:
                break
            if height[i] < height[j]:
                maxV = max(maxV, height[i] * (j - i))
                i += 1
            else:
                maxV = max(maxV, height[j] * (j - i))
                j -= 1
        return maxV
~~~
