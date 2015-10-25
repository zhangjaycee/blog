
## 题目
> You are given two linked lists representing two non-negative numbers. The digits are stored in reverse order and each of their nodes contain a single digit. Add the two numbers and return it as a linked list.

>Input: (2 -> 4 -> 3) + (5 -> 6 -> 4)
Output: 7 -> 0 -> 8

**大意**：给出两个从低位到高位排列链表形式的多位数，相加后按原格式输出。

## 分析
感觉这道题还是比较简单的，除了有的语法有点不熟悉查了下书以外，还都是挺顺利的。
编写时，只要注意进位的判断和退出的条件就可以了，代码如下：

### Python

~~~python
# Definition for singly-linked list.
#class ListNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        answer = ListNode(0)
        pa = answer
        p1 = l1
        p2 = l2
        c = 0
        while(True):
            if p1 != None :
                val1 = p1.val
                p1 = p1.next
            else:
                val1 = 0
            if p2 != None :
                val2 = p2.val
                p2 = p2.next
            else:
                val2 = 0
            sum = val1 + val2 + c
            pa.val = sum % 10
            c = sum / 10
            if p1 == None and p2 == None and c == 0:
                return answer
            else:
                pa.next = ListNode(0)
                pa = pa.next
~~~

### C++

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
    ListNode * addTwoNumbers(ListNode* l1, ListNode* l2) {
        int sum = 0;
        int c = 0;
        int val1,val2;
        ListNode * answer = new ListNode(0);
        ListNode * p1 = l1;
        ListNode * p2 = l2;
        ListNode * pa = answer;
        while(p1 != NULL || p2 != NULL || c != 0 ){
            if(p1 == NULL){
                val1 = 0;
            }else{
                val1 = p1->val;
                p1 = p1->next;
            }
            if(p2 == NULL){
                val2 = 0;
            }else{
                val2 = p2->val;
                p2 = p2->next;
            }
            sum = val1 + val2 + c;
            pa->val = sum % 10;
            c = sum / 10;
            if(p1 == NULL && p2 == NULL && c == 0){
                break;
            }else{
                pa->next = new ListNode(0);
                pa = pa->next;
            }
        }
        return answer;
    }
};
~~~
