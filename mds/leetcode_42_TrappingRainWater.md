# Trapping Rain Water

## 题目
> Given n non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it is able to trap after raining.

> For example, 
Given [0,1,0,2,1,0,1,3,2,1,2,1], return 6.
![img][img]

* 大意： 有n个非负整数，代表地势图的高度，如图，计算下雨后这个地形能存多少雨水。

## 思路
这道题和第10题非常像，分别从最左边和最右边开始，定义两个游标，移动到过程中，记录左边的最大值和右边的最大值，然后用两个最大值中的小值减去地形高度，就是所积的雨水值（类似第10题思路）。

关于两个游标怎么移动的问题，同第10题思路，还是移动当前最大值较小的边，比如：当前右边最大值right_max为10，左边最大值left_max为5，如果移动right_index，那么左边的最大值只能保持不变，不管right_max变不变，两个最大值的较小一个也还会是left_max，没有可能增加积水量，所以可能会存在错误。（详细可结合代码看）

## 代码

### Python
~~~python
class Solution(object):
    def trap(self, height):
        """
        :type height: List[int]
        :rtype: int
        """
        if not height:
            return 0
        water_sum = 0
        i, j = 0, len(height) - 1
        left_max, right_max = 0, 0
        while True:
            if i == j:
                break
            left_max = max(left_max, height[i])
            right_max = max(right_max, height[j])
            if left_max < right_max:
                water_sum += left_max - height[i]
                i += 1
            else:
                water_sum += right_max - height[j]
                j -= 1
        return water_sum
~~~

### C++
~~~cpp
class Solution {
public:
    int trap(vector<int>& height) {
        if (height.size() == 0){
            return 0;
        }
        int i = 0, j = height.size() - 1;
        int water_sum = 0;
        int right_max = 0, left_max = 0;
        while (i != j){
            left_max = max(left_max, height[i]);
            right_max = max(right_max, height[j]);
            if (left_max < right_max){
                water_sum += left_max - height[i];
                i++;
            } else{
              water_sum += right_max - height[j];
              j--;
            }
        }
        return water_sum;
    }
};
~~~


[img]:{{"/2014110901.png" | prepend: site.imgrepo }}