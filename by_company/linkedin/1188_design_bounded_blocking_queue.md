# 线程安全有界阻塞队列实现说明

## 问题要求
实现一个线程安全的有界阻塞队列，支持多个生产者和消费者线程同时操作。

实现一个线程安全的有界阻塞队列，该队列具有指定容量的构造函数、向队列前端添加元素的enqueue方法（如果队列已满则阻塞线程）、从队列后端移除元素的dequeue方法（如果队列为空则阻塞线程）以及返回队列当前元素数量的size方法。在多线程环境下，生产者线程调用enqueue方法，消费者线程调用dequeue方法，size方法在每个测试用例后调用，要求避免使用内置的有界阻塞队列实现。

## 关键点
有界阻塞队列需要在构造时指定最大容量。
enqueue方法用于向队列前端添加元素，队列满时会阻塞调用线程。
dequeue方法用于从队列后端移除元素，队列为空时会阻塞调用线程。
size方法返回队列中当前元素的数量。
实现需要保证线程安全，适用于多线程并发访问。
生产者线程只调用enqueue方法，消费者线程只调用dequeue方法。
每个测试用例结束后都会调用size方法以检查队列状态。
不允许使用内置的有界阻塞队列实现，需要自行实现。
enqueue的调用次数总是大于等于dequeue的调用次数。

## 核心方法
- `BoundedBlockingQueue(int capacity)`: 初始化指定容量的队列
- `enqueue(int element)`: 队列满时阻塞，直到有空间可插入
- `dequeue()`: 队列空时阻塞，直到有元素可取出
- `size()`: 返回当前队列元素个数

## 设计要点

### 1. 数据结构
- 使用数组或链表存储元素
- 维护队头、队尾指针
- 记录当前元素个数

### 2. 线程同步机制
**互斥锁 (Mutex/Lock)**：
- 保护队列的数据结构，确保同一时间只有一个线程能修改队列

**条件变量 (Condition Variable)**：
- `notFull`: 队列未满条件，生产者等待
- `notEmpty`: 队列非空条件，消费者等待

### 3. 阻塞逻辑
**enqueue 流程**：
1. 获取锁
2. 如果队列已满，等待 `notFull` 条件
3. 插入元素，更新队列状态
4. 通知等待 `notEmpty` 的消费者线程
5. 释放锁

**dequeue 流程**：
1. 获取锁
2. 如果队列为空，等待 `notEmpty` 条件
3. 取出元素，更新队列状态
4. 通知等待 `notFull` 的生产者线程
5. 释放锁

### 4. 关键实现细节
- 使用 `while` 循环检查条件（防止虚假唤醒）
- 正确的锁获取和释放顺序
- 条件变量的 `wait` 会自动释放锁并在被唤醒时重新获取
- `notify/signal` 唤醒等待的线程

## 示例执行过程
以容量为2的队列为例：
```
enqueue(1) -> 队列: [1], 通知消费者
dequeue()  -> 返回1, 队列: [], 通知生产者  
dequeue()  -> 队列空，消费者阻塞等待
enqueue(0) -> 队列: [0], 唤醒阻塞的消费者，返回0
enqueue(2) -> 队列: [2]
enqueue(3) -> 队列: [2,3], 已满
enqueue(4) -> 队列满，生产者阻塞等待
dequeue()  -> 返回2, 队列: [3], 唤醒阻塞的生产者，插入4
```

## 注意事项
- 多线程环境下操作顺序不确定，相同输入可能有多种合法输出
- 必须处理线程间的竞争条件和死锁风险
- 条件检查使用 `while` 而非 `if`（避免虚假唤醒）
- 确保异常情况下锁能正确释放



## solution 1: 使用condition variables
# LeetCode 1188 - 设计有界阻塞队列最优解

```

import threading
from collections import deque

class BoundedBlockingQueue(object):
    
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.queue = deque()
        self.lock = threading.Lock()
        # 使用两个条件变量分别处理满和空的情况
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)
    
    def enqueue(self, element: int) -> None:
        with self.not_full:
            # 如果队列满了，等待直到有空间
            while len(self.queue) >= self.capacity:
                self.not_full.wait()
            
            # 添加元素到队列末尾
            self.queue.append(element)
            
            # 通知等待的消费者线程
            self.not_empty.notify()
    
    def dequeue(self) -> int:
        with self.not_empty:
            # 如果队列为空，等待直到有元素
            while len(self.queue) == 0:
                self.not_empty.wait()
            
            # 从队列头部取出元素
            element = self.queue.popleft()
            
            # 通知等待的生产者线程
            self.not_full.notify()
            
            return element
    
    def size(self) -> int:
        with self.lock:
            return len(self.queue)

```

## 解决方案详解

### 核心设计思路
1. **数据结构**：使用 `collections.deque` 作为底层队列，支持高效的两端操作
2. **线程同步**：使用两个条件变量分别处理"队列未满"和"队列非空"的条件
3. **阻塞机制**：通过 `wait()` 和 `notify()` 实现线程间的阻塞和唤醒

### 关键技术点

**1. 条件变量设计**
- `not_full`: 生产者等待队列有空间时使用
- `not_empty`: 消费者等待队列有元素时使用
- 两者共享同一个锁，避免死锁

**2. 使用 `while` 循环检查条件**
```python
while len(self.queue) >= self.capacity:
    self.not_full.wait()
```
防止虚假唤醒（spurious wakeup），确保条件真正满足

**3. 正确的通知机制**
- `enqueue` 后通知 `not_empty`（告知消费者有新元素）
- `dequeue` 后通知 `not_full`（告知生产者有空间）

### 时间复杂度
- **enqueue/dequeue**: O(1) - deque的append和popleft都是常数时间
- **size**: O(1) - 直接返回长度

### 空间复杂度
- O(capacity) - 队列最多存储capacity个元素

### 线程安全保证
- 所有操作都在适当的锁保护下进行
- 使用条件变量确保线程能正确阻塞和唤醒
- 避免了竞态条件和死锁问题

这个实现是最优的，因为它：
- 使用了高效的数据结构（deque）
- 正确处理了多线程同步
- 避免了忙等待，真正实现了阻塞
- 代码简洁且易于理解

### 复杂度分析
# 有界阻塞队列时间空间复杂度详细分析

## 时间复杂度分析

### 单操作复杂度（无竞争情况）

| 操作 | 时间复杂度 | 说明 |
|------|------------|------|
| `enqueue()` | **O(1)** | deque.append() 是常数时间 |
| `dequeue()` | **O(1)** | deque.popleft() 是常数时间 |
| `size()` | **O(1)** | len() 对 deque 是常数时间 |

### 详细分解

**enqueue() 操作**：
```python
def enqueue(self, element: int) -> None:
    with self.not_full:                    # O(1) - 获取锁
        while len(self.queue) >= self.capacity:  # O(1) - 长度检查
            self.not_full.wait()           # 阻塞时间（非算法复杂度）
        self.queue.append(element)         # O(1) - deque 尾部插入
        self.not_empty.notify()            # O(1) - 通知一个等待线程
```

**dequeue() 操作**：
```python
def dequeue(self) -> int:
    with self.not_empty:                   # O(1) - 获取锁
        while len(self.queue) == 0:        # O(1) - 长度检查
            self.not_empty.wait()          # 阻塞时间（非算法复杂度）
        element = self.queue.popleft()     # O(1) - deque 头部删除
        self.not_full.notify()             # O(1) - 通知一个等待线程
        return element
```

### 多线程环境下的复杂度考量

**1. 锁竞争成本**
- **无竞争**：O(1) - 快速路径获取锁
- **有竞争**：取决于操作系统调度，但不影响算法复杂度

**2. 阻塞等待时间**
```python
# 这不是算法复杂度，而是业务逻辑
while len(self.queue) >= self.capacity:
    self.not_full.wait()  # 可能等待任意长时间
```
- 阻塞时间 ≠ 算法时间复杂度
- 算法复杂度关注的是**非阻塞情况下**的计算步骤

**3. 通知成本**
- `notify()`: O(1) - 只唤醒一个等待线程
- `notify_all()`: O(k)，其中 k 是等待线程数（我们用的是前者）

## 空间复杂度分析

### 主要存储开销

| 组件 | 空间复杂度 | 说明 |
|------|------------|------|
| `self.queue` | **O(capacity)** | 存储最多 capacity 个元素 |
| `self.lock` | **O(1)** | 单个锁对象 |
| `self.not_full` | **O(1)** | 条件变量对象 |
| `self.not_empty` | **O(1)** | 条件变量对象 |
| 其他变量 | **O(1)** | capacity 等基本类型 |

**总空间复杂度：O(capacity)**

### deque 的内存特性
```python
from collections import deque

# deque 内部使用双端队列，每个块存储多个元素
# 空间效率比 list 更好，因为：
# 1. 不需要预分配大量连续内存
# 2. 支持高效的两端操作
# 3. 内存按需分配
```

## 性能对比分析

### vs 基于数组的循环队列
```python
# 数组实现
class ArrayQueue:
    def __init__(self, capacity):
        self.buffer = [None] * capacity  # O(capacity) 预分配
        self.head = 0
        self.tail = 0
        self.size = 0
```

| 特性 | deque实现 | 数组实现 |
|------|-----------|----------|
| 内存预分配 | 按需分配 | 预分配全部 |
| 空间效率 | 更好 | 较差（可能浪费） |
| 缓存局部性 | 一般 | 更好 |
| 实现复杂度 | 简单 | 需要处理环形索引 |

### vs 基于链表的队列
```python
class LinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0
```

| 特性 | deque实现 | 链表实现 |
|------|-----------|----------|
| 时间复杂度 | O(1) | O(1) |
| 空间开销 | 较小 | 每个节点额外指针开销 |
| 内存连续性 | 部分连续 | 完全不连续 |

## 最坏情况分析

### 时间复杂度最坏情况
- **单线程顺序操作**：所有操作都是 O(1)
- **高竞争多线程**：虽然锁竞争增加延迟，但算法复杂度仍然是 O(1)

### 空间复杂度最坏情况
- **队列满载**：O(capacity) - 这也是唯一的情况
- **大量阻塞线程**：线程栈空间不计入数据结构复杂度

## 实际性能考量

### 关键性能因素
1. **内存分配**：deque 的分块分配比 list 的重新分配更高效
2. **锁粒度**：使用细粒度的条件变量而非粗粒度的全局锁
3. **上下文切换**：阻塞/唤醒的系统调用开销
4. **缓存效应**：deque 的内存布局对 CPU 缓存较友好

### 优化空间
```python
# 可能的优化方向（但会增加复杂度）
class OptimizedQueue:
    def __init__(self, capacity):
        # 使用无锁数据结构（如环形缓冲区 + CAS）
        # 但实现复杂度大大增加
        pass
```

## 结论

**时间复杂度**：所有操作均为 **O(1)** amortized
**空间复杂度**：**O(capacity)**

这个实现在简洁性和性能之间取得了很好的平衡，是面试和生产环境的最优选择。