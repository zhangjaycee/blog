## 题目
> There are two sorted arrays nums1 and nums2 of size m and n respectively. Find the median of the two sorted arrays. The overall run time complexity should be O(log (m+n)).

## 大意
有两个排好序的数组nums1和nums2，分别长m和n.找出两个数列的中值，复杂度应该为O(log (m+n)).

## 思路
这道题虽然知道应该是分治的思路，我没有做出来，找了一下discuss里面的题解，看了一下，打算**把有关的分治书上好好看过之后在回顾之后再更新下这道题**。
这里贴出discuss的两个帖子链接，这两个是discuss里面顶的最多了两篇。第一篇思路比较正常，翻译了下。第二篇的思路更是很巧妙的避开了奇偶数的讨论，但不知道是否具有普适性。

### Python:
我的**错误代码**如下：（仅作纪念）
~~~python
#错误代码
class Solution(object):
    def findMedianSortedArrays(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: float
        """
        if len(nums1) == 1 and len(nums2) == 1:
            return (float)(nums2[0] + nums1[0])/2;
        elif len(nums1) == 0 and len(nums2) == 1:
            return nums2[0]
        elif len(nums1) == 1 and len(nums2) == 0:
            return nums1[0]
        print "len(nums1)=",len(nums1),"   len(nums2)=",len(nums2)
        i1 = len(nums1)//2
        i2 = len(nums2)//2
        print "i1=",i1,"   i2=",i2
        if (nums1[i1] > nums2[i2]):
            return self.findMedianSortedArrays(nums1[i1:], nums2[:i2])
        else:
            return self.findMedianSortedArrays(nums1[i2:], nums2[:i1])
~~~

#### 参考：
原文：《[share my o(log(min(m,n)) solution with explanation](https://leetcode.com/discuss/15790/share-my-o-log-min-m-n-solution-with-explanation)》
翻译：
> * 已知一个长度为m的数组A，我们可以把它拆分成两部分：
~~~
{ A[0], A[1], ... , A[i - 1] } | { A[i], A[i + 1], ... , A[m - 1] }
~~~
右边的所有元素都比左边的元素大。
左边有*i*个元素，右边有*m - 1*个元素。
一共可以有*m+1*中拆分的办法。(i = 0 ~ m)
当*i = 0*时，左半部分有*0*个元素，右半部份有*m*个元素；
当*i = m*时，左半部分有*m*个元素，右半部份有*0*个元素。

> * 对于数组B，我们可以同理拆成：
~~~
{ B[0], B[1], ... , B[j - 1] } | { B[j], B[j + 1], ... , B[n - 1] }
~~~
左边有*k*个元素，右边有*n-j*个元素。

> * 将A的左边和B的左边放到同一个集合中(取名"LeftSet")
将A的右边和B的右边放到同一个集合中(取名"RightSet")
~~~
            LeftPart           |            RightPart 
{ A[0], A[1], ... , A[i - 1] } | { A[i], A[i + 1], ... , A[m - 1] }
{ B[0], B[1], ... , B[j - 1] } | { B[j], B[j + 1], ... , B[n - 1] }
~~~
> * 如果我们能够保证：
~~~
1) LeftPart的长度 == RightPart的长度 (或者RightPart的长度 + 1)
2) RightPart的所有元素都比LeftPart的任一元素大
~~~
那么我们就已经把{A, B}中所有的元素，分成了长度相等的两个部分，并且其中一部分的元素总是比另一部分的元素大。这样的话，中值(median)就能较容易地找到了

> * 为了保证这两点，我们只需要保证：
~~~
1) i + j == m -i + n - j(或: m - i +n -j + 1)，要是n >= m，那么我们只需要设置: 
       i = 0 ~ m, j = (m + n + 1) / 2 - i
2) B[j - 1] <= A[i] 且 A[i - 1] <= B[j]，要是考虑迟到边缘值，其实我们需要保证的是：
       (j \== 0 or i == m or B[j - 1] <= A[i]) and (i \== 0 or j == n or A[i - 1] <= B[j])
~~~
>* 所以，我们要去做的就是：
*取i从0到m，找出符合上述两点要求的i值ix和对应的j值jx*

>* 我们可以用二分查找来找出它，怎么做呢？
1) 如果 B[j0 - 1] > A[i0]，那么"ix" 就肯定不在[0, i0]中，为什么呢？
因为如果 ix < i0, 那么jx = (m + n + 1) / 2 -ix > j0, 那么 B[jx -1] >= B[j0 - 1] > A[i0] >= A[ix]，这和条件2是有冲突的！所以ix是不能比i0小的。
2) 如果 A[i0 - 1] > B[j0]，那么"ix"就肯定不在[i0, m]中。
（证明同上）

> * 所以我们就可以按下边的步骤进行二分搜索：
1) 设置 imin, imax = 0, m,然后开始在[imin, imax]中搜索
2) `i = (imin + imax) / 2; j = (m + n +1) / 2 - i`
3) if B[j - 1] > A[i]: 在[i + 1, imax]中继续搜索;
   elif A[i - 1] > B[j]: 在[imin, i - 1]中继续搜索;
   else: bingo!这就是我们要找的i了!
> * 当我们找到ix时，中值(median)就是：
~~~python
max(A[i - 1], B[j - 1]) #(m + n)为奇数
~~~
或：
~~~python
(max(A[i - 1], B[j - 1]) + min(A[i], B[j])) / 2 #(m + n)为偶数
~~~

> * 代码如下：（Python）
~~~python
def median(A, B):
    m, n = len(A), len(B)
    if m > n:
        A, B, m, n = B, A, n, m
    imin, imax, half_len = 0, m, (m + n + 1) / 2
    while imin <= imax:
        i = (imin + imax) / 2
        j = half_len - i
        if j > 0 and i < m and B[j - 1] > A[i]:
            imin = i + 1
        elif i > 0 and j < n and A[i - 1] > B[j]:
            imax = i - 1
        else:
            if i == 0:
                num1 = B[j - 1]
            elif j == 0:
                num1 = A[i - 1]
            else:
                num1 = max(A[i - 1], B[j - 1])
            if (m + n) % 2 == 1:
                return num1
            if i == m:
                num2 = B[j]
            elif j == n:
                num2 = A[i]
            else:
                num2 = min(A[i], B[j])
            return (num1 + num2) / 2.0
~~~

### C++

#### 参考：
(《[Very concise O(log(min(M,N))) iterative solution with detailed explanation](https://leetcode.com/discuss/41621/very-concise-iterative-solution-with-detailed-explanation)》的代码)
~~~cpp
 double findMedianSortedArrays(vector<int>& nums1, vector<int>& nums2) {
    int N1 = nums1.size();
    int N2 = nums2.size();
    if (N1 < N2) return findMedianSortedArrays(nums2, nums1);   // Make sure A2 is the shorter one.

    if (N2 == 0) return ((double)nums1[(N1-1)/2] + (double)nums1[N1/2])/2;  // If A2 is empty

    int lo = 0, hi = N2 * 2;
    while (lo <= hi) {
        int mid2 = (lo + hi) / 2;   // Try Cut 2 
        int mid1 = N1 + N2 - mid2;  // Calculate Cut 1 accordingly

        double L1 = (mid1 == 0) ? INT_MIN : nums1[(mid1-1)/2];  // Get L1, R1, L2, R2 respectively
        double L2 = (mid2 == 0) ? INT_MIN : nums2[(mid2-1)/2];
        double R1 = (mid1 == N1 * 2) ? INT_MAX : nums1[(mid1)/2];
        double R2 = (mid2 == N2 * 2) ? INT_MAX : nums2[(mid2)/2];

        if (L1 > R2) lo = mid2 + 1;     // A1's lower half is too big; need to move C1 left (C2 right)
        else if (L2 > R1) hi = mid2 - 1;    // A2's lower half too big; need to move C2 left.
        else return (max(L1,L2) + min(R1, R2)) / 2; // Otherwise, that's the right cut.
    }
    return -1;
} 
~~~















