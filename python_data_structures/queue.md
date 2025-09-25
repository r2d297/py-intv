
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
