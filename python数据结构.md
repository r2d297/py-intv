# 滑动窗口模版

```python
for idx, num in enumerate(nums):
	#
```

# List(动态数组)

```python
arr=[]

#追加: 
arr.append(1)

#在指定索引位置插入:  
arr.insert(2, 123)

#在头部插入:  
arr.insert(0,-1)

#删除末尾:  
arr.pop()

#删除索引位置的值:  
arr.pop(2)

#根据索引修改和access元素:  
ele=arr[2]

#根据元素值查找索引: 
idx=arr.index(123)

#动态数组的代码实现

```

# 环形数组

**代码的关键在于求模运算 `%`，也就是求余数**。当 `i` 到达数组末尾元素时，`i + 1` 和 `arr.length` 取余数又会变成 0，即会回到数组头部，这样就在逻辑上形成了一个环形数组，永远遍历不完。

## **关键点、注意开闭区间**

在我的代码中，环形数组的区间被定义为左闭右开的，即 `[start, end)` 区间包含数组元素。所以其他的方法都是以左闭右开区间为基础实现的。

那么肯定就会有读者问，为啥要左闭右开，我就是想两端都开，或者两端都闭，不行么？

在 [**滑动窗口算法核心框架**](https://labuladong.online/algo/essential-technique/sliding-window-framework/) 中定义滑动窗口的边界时也会有类似的问题，这里我也解释一下。

**理论上，你可以随意设计区间的开闭，但一般设计为左闭右开区间是最方便处理的**。

因为这样初始化 `start = end = 0` 时，区间 `[0, 0)` 中没有元素，但只要让 `end` 向右移动（扩大）一位，区间 `[0, 1)` 就包含一个元素 `0` 了。

如果你设置为两端都开的区间，那么让 `end` 向右移动一位后开区间 `(0, 1)` 仍然没有元素；如果你设置为两端都闭的区间，那么初始区间 `[0, 0]` 就已经包含了一个元素。这两种情况都会给边界处理带来不必要的麻烦，如果你非要使用的话，需要在代码中做一些特殊处理。

```python
# 长度为 5 的数组
arr = [1, 2, 3, 4, 5]
i = 0
# 模拟环形数组，这个循环永远不会结束
while i < len(arr):
    print(arr[i])
    i = (i + 1) % len(arr)
```


# Queue

```python
#使用deque实现队列
from collections import deque

queue=deque()
#入队
queue.append(1)
#查看队首元素
if queue:
	front=queue[0]
	print(f"队首元素: {front}")

#出队操作
dequeued=queue.popleft()
#检查队列是否为空
is_empty=len(queue)==0

#获取队列大小
size=len(queue)
#从左端添加
queue.appendleft(0) #从左端添加
queue.pop() #从右端删除

```

# 双端队列

| 操作 | `list` | `deque` |
| --- | --- | --- |
| append (右端添加) | ✅ O(1) | ✅ O(1) |
| pop (右端弹出) | ✅ O(1) | ✅ O(1) |
| insert(0, x) (左端添加) | ✅ O(n) | ✅ O(1) |
| pop(0) (左端弹出) | ✅ O(n) | ✅ O(1) |

如果你只是偶尔在末尾操作，用 `list` 没问题；但如果你要做 BFS、滑动窗口、频繁双端操作，强烈建议使用 `deque`。

```python
内置List可以当deque用,但是不推荐,因为性能差(list.insert(0,x)和list.pop(0)会移动整个数组),
推荐collection.deque,专为双端队列设计,添加和删除都是O(1)时间完成

from collections import deque

q = deque([1, 2, 3])
q.append(4)     # 右端添加
q.appendleft(0) # 左端添加
q.pop()         # 右端弹出
q.popleft()     # 左端弹出

#初始化
dq1=deque()
#从可迭代对象创建
dq2=deque([1,2,3,4,5])
#指定最大长度(循环队列)
dq2=deque([1,2,3], maxlen=5)
#从字符串创建
dq4=deque("hello")

#右端操作(默认端)
dq.append(4)
removed=dq.pop()

#左端操作
dq.appendleft(5)
removed=dq.popleft()

#右端批量添加
dq.extend([4,5,6])
#左端批量添加
dq.extendleft([0,-1, -2]). #注意： 逆序添加
```

# Dict哈希表

## 遍历dict所有的键

1. 直接遍历字典（最 Pythonic）

```python
d = {'a': 1, 'b': 2, 'c': 3}
for key in d:
    print(key)

```

1. 遍历 `dict.keys()` 视图

```python
for key in d.keys():
    print(key)
```

1. 转成列表再遍历（不常用，除非你要对键做切片／排序）

```python
for key in list(d):
    print(key)
```

1. 对键排序后遍历

```python
for key in sorted(d):
    print(key)

```

1. 同时要值时，用 `.items()`：

```python
for key, value in d.items():
    print(key, value)
```

### **小结**

- 推荐做法：`for key in d:` 或 `for key in d.keys():`，二者等价；
- 如果你只关心键，不要用 `for key, _ in d.items()`，因为多了解析了一遍值而已；
- 如需有序输出，可对 `d.keys()` 或 `d` 调用 `sorted()`。

# BFS模版

```python

```