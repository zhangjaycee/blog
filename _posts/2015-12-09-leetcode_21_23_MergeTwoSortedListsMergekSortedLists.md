---
layout: post
title: LeetCode第21/23题:Merge Two Sorted Lists和Merge k Sorted Lists总结 
tags: leetcode 算法 python list 归并 排序
categories: LeetCode
---


## 题目一
> Merge two sorted linked lists and return it as a new list. The new list should be made by splicing together the nodes of the first two lists.

* 大意：合并两个列表，返回一个新的列表，新的列表要把前边给定的两个列表链接起来。

### 思路：
其实就是把两个有序列表变成一个有序列表，只要维护两个指针，分别将当前最小的数复制到第三个列表中，然后将相应指针后移即可。道理很简单。

需要注意到是，python中，如果一个变量等于一个列表(比如，list1为一个列表，定义a1 = list1)，则这个变量(a1)其实类似c中的指针的概念(a1和list1等价，都是“指针”)，并不是拷贝了这个列表(如要实现拷贝复制，可以写a1 = list1[:])。
对于本题，这样的语法其实产生了两种写法，（见下边小节)。对于本题，两种写法都对，第一种写法比较简洁，但是却改变了原来的l1和l2列表，因为p3指针赋值的时候，直接用了l1或者l2的节点，那么下一次赋值的时候，便改变了这个节点的next指针。第二种写法采用了oj所定义的ListNode类的构造函数，直接用符合要求的l1或者l2的节点的val值创建一个新的node链接在l3后边，所以不改变原先的l1和l2列表。
所以，具体用哪一种，要根据知己需求定。

#### 代码1(python)
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeTwoLists(self, l1, l2):
<!--more-->
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        p1 = l1
        p2 = l2
        l3 = ListNode(0)
        p3 = l3
        while l1 and l2:
            if l1.val < l2.val:
                p3.next = l1
                l1 = l1.next
            else:
                p3.next = l2
                l2 = l2.next
            p3 = p3.next
        p3.next = l1 if not l2 else l2
        return l3.next
~~~
#### 代码2(python)
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeTwoLists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        p1 = l1
        p2 = l2
        l3 = ListNode(0)
        p3 = l3
        while l1 and l2:
            if l1.val < l2.val:
                p3.next = ListNode(l1.val)
                p3 = p3.next
                l1 = l1.next
            else:
                p3.next = ListNode(l2.val)
                p3 = p3.next
                l2 = l2.next
        if not l1 and not l2:
            return l3.next
        elif not l1:
            while l2:
                p3.next = ListNode(l2.val)
                p3 = p3.next
                l2 = l2.next
            return l3.next
        else:
            while l1:
                p3.next = ListNode(l1.val)
                p3 = p3.next
                l1 = l1.next
            return l3.next
~~~

## 题目二
> Merge k sorted linked lists and return it as one sorted list. Analyze and describe its complexity.

* 大意：明显是前一道题的升级版，这次是合并k个已排序列表到一个列表。

### 思路0：
其实，这个就是一个归并排序，和归并排序不同的是，归并排序开始我们需要假设所有顺序都是乱的，我们假定每一个数都是一个list，然后逐步减少list数目，加长每一个list长度，而这道题，相当于已经进行到一半的归并排序。
不过，这没有关系，因为归并是递归实现的，我们玩全可以按照归并的方法，做这道题，而且正好用到了上一个题的代码。

#### 代码：（Python）
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        if not lists:
            return None
        if len(lists) == 1:
            return lists[0]
        mid = len(lists) / 2
        left = self.mergeKLists(lists[:mid])
        right = self.mergeKLists(lists[mid:])
        return self.merge2Lists(left, right)

    def merge2Lists(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        l3 = ListNode(0)
        p3 = l3
        while l1 and l2:
            if l1.val < l2.val:
                p3.next = l1
                l1 = l1.next
            else:
                p3.next = l2
                l2 = l2.next
            p3 = p3.next
        p3.next = l1 if not l2 else l2
        return l3.next
~~~
> 参考：
> 《百度百科 归并排序》( http://baike.baidu.com/link?url=V2OlIM61x3mTzbnICxp-CK5GD6CfSz1JHy4KWHLpcRbgd6LO8Nz9oYobdtF58Lat6-BfiB8F1NH2P49QW0vW9_ )


### 思路1：
用堆排序，用到了python的heapq这个数据结构。

#### 代码(python):
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        ret, heap = [], []
        for li in lists:
            while li:
                heapq.heappush(heap, li.val)
                li = li.next
        while heap:
            ret.append(heapq.heappop(heap))
        return ret
~~~


### 思路2：
用python的排序，直接将所有列表的所有数放在一个列表中，然后直接用sorted()排序。
个人感觉：虽然投机取巧，但是速度一点也不慢，实际解决问题却最快速实用。

#### 代码(Python):
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def mergeKLists(self, lists):
        """
        :type lists: List[ListNode]
        :rtype: ListNode
        """
        ret = []
        for lst in lists:
            while lst:
                ret.append(lst.val)
                lst = lst.next
        return sorted(ret)

~~~



