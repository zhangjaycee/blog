# leetcode 19 Remove Nth Node From End of List

## 题目
>Given a linked list, remove the nth node from the end of list and return its head.

>For example,

>   Given linked list: 1->2->3->4->5, and n = 2.

>   After removing the second node from the end, the linked list becomes 1->2->3->5.
>Note:
Given n will always be valid.
Try to do this in one pass.

* 大意：给定一个链表和一个数n，从一个链表中删去从后变数的第n个节点，比如1->2->3->4->5,  n = 2.处理完后为1->2->3->5.。注意给定的n都是有效的，尝试用一遍遍历完成。

## 思路0
python投机取巧的做法，将链表遍历转为数组，直接删除第-n个元素（注意因为从后数第一个节点index为-1，则后数第n个节点index为-n）

代码：(python)
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """
        p = head
        l = []
        while p.next != None:
            l.append(p.val)
            p = p.next
        l.append(p.val)
        del l[-n]
        return l
~~~




##思路1
题设是单链表，不方便从后遍历。而从前边遍历判断是尾节点的方法只能是当前指向的节点的next节点是NULL。我们如果定义两个指针，分别指针，第一个指向第0个节点，第二个指针第n个节点，两个指针同时向后遍历，当尾节点的时候，第一个指针所指向的节点正好是从后数第n+1个节点，这时只要将第一个指针的.next修正为.next.next即可。
特殊情况是，注意到题设n总是有效的，所以如果第n个(从0开始数)节点不存在，则一定是链表只存在n个节点，只需要删除第0个节点即可（返回head.next）。
```
比如n=3：
开始第一次循环后：
n0->n1->n2->n3->......n(n-3)->n(n-2)->n(n-1)->n(n)
^           ^
遍历后：
n0->n1->n2->n3->......n(n-3)->n(n-2)->n(n-1)->n(n)
                        ^                      ^
此时只需要删除第一个指针后边的元素即可。
```
代码(python)
~~~python
# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def removeNthFromEnd(self, head, n):
        """
        :type head: ListNode
        :type n: int
        :rtype: ListNode
        """
        p1 = p2 = head
        for i in range(n):
            p2 = p2.next
        if not p2:
            return p1.next
        while p2.next:
            p1 = p1.next
            p2 = p2.next
        p1.next = p1.next.next
        return head
~~~
代码(c++)
~~~cpp
/**
 * Definition for singly-linked list.
 * struct ListNode {
 *     int val;
 *     ListNode *next;
 *     ListNode(int x) : val(x), next(NULL) {}
 * };
 */
class Solution {
public:
    ListNode* removeNthFromEnd(ListNode* head, int n) {
        ListNode * p1 = head;
        ListNode * p2 = head;
        for(int i = 0; i < n; i++) {
            p2 = p2->next;
        }
        if(!p2) {
            return head->next;
        }
        while(p2->next) {
            p1 = p1->next;
            p2 = p2->next;
        }
        p1->next = p1->next->next;
        return head;
    }
};
~~~


> 参考:
> 《3 short Python solutions》(https://leetcode.com/discuss/37149/3-short-python-solutions)

