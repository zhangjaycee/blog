---
layout: post
title: LeetCode第24/25题:Swap Nodes in Pairs和Reverse Nodes in k-Group总结
tags: leetcode 算法 python 链表
categories: LeetCode
---

## 题目一
>Given a linked list, swap every two adjacent nodes and return its head.

>For example,
Given 1->2->3->4, you should return the list as 2->1->4->3.

>Your algorithm should use only constant space. You may not modify the values in the list, only nodes itself can be changed.

× 大意： 给定一个链表，依次交换两个相邻节点，并返回头节点。
比如：
1->2->3->4 交换后应该为 2->1->4->3.

### 思路
~~~
交换前：
O->A->B->C->D->E
^  ^  ^  ^
p  p1 p2 p3
交换后：
O->B->A->C->D->E
^  ^  ^  ^
p  p2 p1 p3
~~~
比如我们的列表从A开始，先考虑一般情况：
我们想交换C和D。要交换C和D，我们需要将B.next指向D将C.next指向E，将D.next指向C，所以我们可以维护一个指针p进行从前往后的遍历，然后进行交换。一次交换需要涉及4个节点，所以每次交换我们又临时定义了p1,p2,p3。

* 注意：
1.因为我们交换的是p1和p2位置的节点，所以为了保证从前两个节点就开始交换，我们定义了一个哑节点O(代码中为header)；
2.当p1或者p2为空的时候，停止交换直接break,p3不用判断是否为空，因为用不到p3.next
3.可能用不到三个辅助指针，但是这样思路不容易乱。


### 代码(python)
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def swapPairs(self, head):
        """
        :type head: ListNode
        :rtype: ListNode
        """
        header = ListNode(0)
        header.next = head
        p = header
        while p.next:
            p1 = p.next
            if not p1:
                break
            p2 = p1.next
            if not p2:
                break
            p3 = p2.next
            p.next = p2
            p2.next = p1
            p1.next = p3
            p = p.next.next
        return header.next
~~~



## 题目二

>Given a linked list, reverse the nodes of a linked list k at a time and return its modified list.

>If the number of nodes is not a multiple of k then left-out nodes in the end should remain as it is.

>You may not alter the values in the nodes, only nodes itself may be changed.

>Only constant memory is allowed.

>For example,
Given this linked list: 1->2->3->4->5

>For k = 2, you should return: 2->1->4->3->5

>For k = 3, you should return: 3->2->1->4->5


* 大意： 升级上一道题，，，将交换两个点换成了没k个点反序一次。具体例子如上。

### 思路
~~~
假设k=4:
交换前：
O--->A--->B--->C--->D--->E--->F--->G
^    ^    ^    ^    ^    ^    ^    ^
pre  p1/2 p3             head
step1
O--->B--->A--->C--->D--->E--->F--->G
^    ^    ^    ^    ^    ^    ^    ^
pre  p1   p2   p3        head
step2
O--->C--->B--->A--->D--->E--->F--->G
^    ^    ^    ^    ^    ^    ^    ^
pre  p1        p2   p3   head
step3
O--->D--->C--->B--->A--->E--->F--->G
^    ^    ^    ^    ^    ^    ^    ^
pre  p1             p2   head
下一次循环

O--->D--->C--->B--->A--->E--->F--->G
^    ^    ^    ^    ^    ^    ^    ^
.                        pre
~~~
交换过程中最少需要3个指针p1、p2和pre

### 代码(python)


~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def reverseKGroup(self, head, k):
        """
        :type head: ListNode
        :type k: int
        :rtype: ListNode
        """
        if head is None or k == 1:
            return head
        dummy = ListNode(-1)
        dummy.next = head
        pre = dummy
        while head:
            for i in range(k-1):
                if head.next is None:
                    break
                head = head.next
            else:
                head = head.next
                p1 = p2 = pre.next
                for i in range(k-1):
                    p3 = p2.next
                    p2.next = p3.next
                    p3.next = p1
                    pre.next = p3
                    p1 = p3
                pre = p2
                continue
            break
        return dummy.next
~~~
