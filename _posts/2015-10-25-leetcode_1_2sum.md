---
layout: post
title: [LeetCode]第1题:Two Sum总结
tags: leetcode 算法 map python c++
categories: LeetCode
---

> 完事开头难，算是开始刷leetcode了吧，不知道能不能坚持下去！在这放下一局，不坚持是小狗！——jc,15.10.25

第一题能就是一个纯属熟悉环境，从网上找了python版答案走了一遍流程：

##### python [[1]]
~~~python
class Solution:
    # @return a tuple, (index1, index2)
    def twoSum(self, num, target):
        dictMap = {}
        for index, value in enumerate(num):
            if target - value in dictMap:
                return dictMap[target - value] + 1, index + 1
            dictMap[value] = index
~~~

然后看到了题解：
>##### O(n^2) runtime, O(1) space – Brute force:

>The brute force approach is simple. Loop through each element x and find if there is another value that equals to target – x. As finding another value requires looping through the rest of array, its runtime complexity is O(n^2).

>##### O(n) runtime, O(n) space – Hash table:

>We could reduce the runtime complexity of looking up a value to O(1) using a hash map that maps a value to its index.

题解大意就是用直接遍历(暴力破解)的话就是O(n^2),但是用哈希表就是O(n)的复杂度。具体到python语言就可以使用内置的字典(dict)直接编写了。

后来看了看C++的题解，尝试写了一个C++版本的代码：

##### C++(数组)

~~~cpp
#define MAX 200002
#define OFFSET 100000

class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> answer;
        int num_id[MAX];
        memset(num_id, 0, sizeof(num_id));
        int length = nums.size();
        int rest;
        for (int i = 0; i < length; i++){
            rest = target - nums[i];
            if(num_id[rest + OFFSET]){
            //由于rest和nums都可能为负数，数组OFFSET以前表示负数
                answer.push_back(num_id[rest + OFFSET]);
                answer.push_back(i + 1);
                return answer;
            }else{
                num_id[nums[i] + OFFSET] = i + 1;
            }
        }
    }
};
~~~

##### C++(STL map)
~~~cpp
class Solution {
public:
    vector<int> twoSum(vector<int>& nums, int target) {
        vector<int> answer;
        map<int ,int> num_index;//key:num value:index
        int length = nums.size();
        int rest;
        for (int i = 0; i < length; i++){
            rest = target - nums[i];
            if(num_index[rest]){
            //由于rest和nums都可能为负数，数组OFFSET以前表示负数
                answer.push_back(num_index[rest]);
                answer.push_back(i + 1);
                return answer;
            }else{
                num_index[nums[i]] = i + 1;
            }
        }
    }
};
~~~

##### Java
(题解答案，暂时不会java)
~~~java
public int[] twoSum(int[] numbers, int target) {
	Map<Integer, Integer> map = new HashMap<>();
	for (int i = 0; i < numbers.length; i++) {
        int x = numbers[i];
        if (map.containsKey(target - x)) {
            return new int[] { map.get(target - x) + 1, i + 1 };
        }
        map.put(x, i);
	}
	throw new IllegalArgumentException("No two sum solution");
}
~~~

参考：

[[1]] http://blog.csdn.net/hcbbt/article/details/43966403  [LeetCode] 001. Two Sum (Medium) (C++/Java/Python)
