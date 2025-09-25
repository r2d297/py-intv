# Python 并发编程：条件变量与信号量详解

## 条件变量 (Condition Variables)

### 基本概念
条件变量用于线程间的**等待/通知**机制。当某个条件不满足时，线程可以等待；当条件改变时，可以通知等待的线程。

### 核心API
```python
import threading

condition = threading.Condition()
# 或者
lock = threading.Lock()
condition = threading.Condition(lock)  # 使用自定义锁

# 基本操作
with condition:
    while not some_condition:
        condition.wait()        # 等待条件满足
    # 执行业务逻辑
    
condition.notify()              # 唤醒一个等待线程
condition.notify_all()          # 唤醒所有等待线程
```

### 例子1：生产者-消费者模型
```python
import threading
import time
import random
from collections import deque

class ProducerConsumer:
    def __init__(self, max_size=5):
        self.buffer = deque()
        self.max_size = max_size
        self.condition = threading.Condition()
        
    def producer(self, name, items):
        for item in items:
            with self.condition:
                # 等待缓冲区不满
                while len(self.buffer) >= self.max_size:
                    print(f"[{name}] 缓冲区满，等待...")
                    self.condition.wait()
                
                # 生产物品
                self.buffer.append(item)
                print(f"[{name}] 生产: {item}, 缓冲区: {list(self.buffer)}")
                
                # 通知消费者
                self.condition.notify_all()
            
            time.sleep(random.uniform(0.1, 0.5))
    
    def consumer(self, name):
        while True:
            with self.condition:
                # 等待缓冲区不空
                while not self.buffer:
                    print(f"[{name}] 缓冲区空，等待...")
                    self.condition.wait()
                
                # 消费物品
                item = self.buffer.popleft()
                print(f"[{name}] 消费: {item}, 缓冲区: {list(self.buffer)}")
                
                # 通知生产者
                self.condition.notify_all()
            
            time.sleep(random.uniform(0.2, 0.8))

# 使用示例
def demo_producer_consumer():
    pc = ProducerConsumer(max_size=3)
    
    # 启动生产者线程
    producer1 = threading.Thread(
        target=pc.producer, 
        args=("生产者1", [f"商品{i}" for i in range(5)])
    )
    producer2 = threading.Thread(
        target=pc.producer, 
        args=("生产者2", [f"产品{i}" for i in range(3)])
    )
    
    # 启动消费者线程
    consumer1 = threading.Thread(target=pc.consumer, args=("消费者1",), daemon=True)
    consumer2 = threading.Thread(target=pc.consumer, args=("消费者2",), daemon=True)
    
    consumer1.start()
    consumer2.start()
    producer1.start()
    producer2.start()
    
    producer1.join()
    producer2.join()
    time.sleep(2)  # 让消费者处理完剩余物品

demo_producer_consumer()
```

### 例子2：等待特定条件
```python
import threading
import time

class EventWaiter:
    def __init__(self):
        self.condition = threading.Condition()
        self.data_ready = False
        self.result = None
    
    def data_processor(self):
        """处理数据的线程"""
        print("数据处理器启动，准备数据中...")
        time.sleep(3)  # 模拟耗时的数据处理
        
        with self.condition:
            self.result = "处理完成的数据"
            self.data_ready = True
            print("数据处理完成，通知等待的线程")
            self.condition.notify_all()
    
    def wait_for_data(self, worker_name):
        """等待数据的工作线程"""
        print(f"[{worker_name}] 等待数据准备...")
        
        with self.condition:
            while not self.data_ready:
                print(f"[{worker_name}] 数据还没准备好，继续等待...")
                self.condition.wait()
            
            print(f"[{worker_name}] 获得数据: {self.result}")
            return self.result

# 使用示例
def demo_event_waiter():
    waiter = EventWaiter()
    
    # 启动数据处理线程
    processor = threading.Thread(target=waiter.data_processor)
    
    # 启动多个等待线程
    waiters = []
    for i in range(3):
        worker = threading.Thread(
            target=waiter.wait_for_data, 
            args=(f"工作者{i+1}",)
        )
        waiters.append(worker)
    
    # 启动所有线程
    for worker in waiters:
        worker.start()
    
    time.sleep(1)  # 让等待者先启动
    processor.start()
    
    # 等待所有线程完成
    processor.join()
    for worker in waiters:
        worker.join()

demo_event_waiter()
```

## 信号量 (Semaphore)

### 基本概念
信号量用于控制同时访问**有限资源**的线程数量。它维护一个内部计数器，`acquire()` 时递减，`release()` 时递增。

### 核心API
```python
import threading

# 创建信号量，允许最多 n 个线程同时访问
semaphore = threading.Semaphore(n)

# 使用方式1：显式获取和释放
semaphore.acquire()     # 获取资源，计数-1
try:
    # 使用资源
    pass
finally:
    semaphore.release() # 释放资源，计数+1

# 使用方式2：上下文管理器（推荐）
with semaphore:
    # 使用资源
    pass
```

### 例子1：数据库连接池
```python
import threading
import time
import random

class DatabaseConnectionPool:
    def __init__(self, pool_size=3):
        self.pool_size = pool_size
        self.semaphore = threading.Semaphore(pool_size)
        self.connections = [f"连接{i+1}" for i in range(pool_size)]
        self.available_connections = list(self.connections)
        self.lock = threading.Lock()  # 保护连接列表
    
    def get_connection(self, user):
        print(f"[{user}] 请求数据库连接...")
        
        # 获取连接许可
        self.semaphore.acquire()
        
        # 从连接池获取连接
        with self.lock:
            connection = self.available_connections.pop()
        
        print(f"[{user}] 获得连接: {connection}")
        return connection
    
    def release_connection(self, user, connection):
        print(f"[{user}] 释放连接: {connection}")
        
        # 归还连接到池中
        with self.lock:
            self.available_connections.append(connection)
        
        # 释放信号量许可
        self.semaphore.release()
    
    def execute_query(self, user, query):
        connection = self.get_connection(user)
        try:
            print(f"[{user}] 执行查询: {query}")
            time.sleep(random.uniform(1, 3))  # 模拟查询耗时
            print(f"[{user}] 查询完成")
        finally:
            self.release_connection(user, connection)

# 使用示例
def demo_connection_pool():
    pool = DatabaseConnectionPool(pool_size=2)
    
    def user_task(user_id):
        user = f"用户{user_id}"
        queries = [f"SELECT * FROM table_{i}" for i in range(2)]
        
        for query in queries:
            pool.execute_query(user, query)
            time.sleep(random.uniform(0.5, 1))
    
    # 启动5个用户线程（超过连接池大小）
    threads = []
    for i in range(5):
        thread = threading.Thread(target=user_task, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

demo_connection_pool()
```

### 例子2：限流器
```python
import threading
import time
from datetime import datetime

class RateLimiter:
    def __init__(self, max_requests_per_second=3):
        self.semaphore = threading.Semaphore(max_requests_per_second)
        self.max_requests = max_requests_per_second
        
    def make_request(self, user, api_name):
        # 获取请求许可
        acquired = self.semaphore.acquire(blocking=False)
        
        if not acquired:
            print(f"[{user}] 请求 {api_name} 被限流，请稍后重试")
            return False
        
        try:
            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
            print(f"[{user}] {timestamp} 调用 {api_name}")
            
            # 模拟API处理时间
            time.sleep(random.uniform(0.1, 0.5))
            
            print(f"[{user}] {api_name} 调用完成")
            return True
            
        finally:
            # 1秒后释放许可（模拟每秒限流）
            def release_later():
                time.sleep(1)
                self.semaphore.release()
            
            threading.Thread(target=release_later, daemon=True).start()

# 使用示例
def demo_rate_limiter():
    limiter = RateLimiter(max_requests_per_second=2)
    
    def user_requests(user_id):
        user = f"用户{user_id}"
        apis = ["getUserInfo", "getOrders", "getPayments", "getNotifications"]
        
        for api in apis:
            limiter.make_request(user, api)
            time.sleep(random.uniform(0.1, 0.3))
    
    # 多个用户同时发起请求
    threads = []
    for i in range(3):
        thread = threading.Thread(target=user_requests, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    for thread in threads:
        thread.join()

demo_rate_limiter()
```

### 例子3：资源池管理
```python
import threading
import time
import random

class ResourcePool:
    def __init__(self, resources):
        self.resources = list(resources)
        self.semaphore = threading.Semaphore(len(resources))
        self.lock = threading.Lock()
        self.available = list(resources)
        self.in_use = {}  # 记录资源使用情况
    
    def acquire_resource(self, user):
        print(f"[{user}] 请求资源...")
        
        # 等待资源可用
        self.semaphore.acquire()
        
        # 获取具体资源
        with self.lock:
            if not self.available:
                raise RuntimeError("信号量与资源池不同步!")
            
            resource = self.available.pop(0)
            self.in_use[resource] = user
            
        print(f"[{user}] 获得资源: {resource}")
        return resource
    
    def release_resource(self, user, resource):
        print(f"[{user}] 释放资源: {resource}")
        
        with self.lock:
            if resource not in self.in_use:
                raise ValueError(f"资源 {resource} 未在使用中")
            
            del self.in_use[resource]
            self.available.append(resource)
        
        # 释放信号量
        self.semaphore.release()
    
    def get_status(self):
        with self.lock:
            return {
                'available': list(self.available),
                'in_use': dict(self.in_use)
            }

# 使用示例
def demo_resource_pool():
    # 创建有限资源池（比如GPU、打印机等）
    pool = ResourcePool(['GPU-1', 'GPU-2', 'GPU-3'])
    
    def worker_task(worker_id):
        worker = f"工作者{worker_id}"
        
        # 申请资源
        resource = pool.acquire_resource(worker)
        
        try:
            # 使用资源执行任务
            work_time = random.uniform(2, 5)
            print(f"[{worker}] 使用 {resource} 执行任务 ({work_time:.1f}秒)")
            time.sleep(work_time)
            
            print(f"[{worker}] 任务完成")
            
        finally:
            # 释放资源
            pool.release_resource(worker, resource)
    
    # 启动多个工作者（超过资源数量）
    threads = []
    for i in range(6):
        thread = threading.Thread(target=worker_task, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    # 监控资源使用情况
    def monitor():
        while any(t.is_alive() for t in threads):
            status = pool.get_status()
            print(f"资源状态 - 可用: {status['available']}, 使用中: {status['in_use']}")
            time.sleep(1)
    
    monitor_thread = threading.Thread(target=monitor, daemon=True)
    monitor_thread.start()
    
    for thread in threads:
        thread.join()
    
    print("所有任务完成")

demo_resource_pool()
```

## 条件变量 vs 信号量对比

| 特性 | 条件变量 (Condition) | 信号量 (Semaphore) |
|------|---------------------|-------------------|
| **用途** | 等待特定条件满足 | 控制资源访问数量 |
| **核心机制** | wait/notify | acquire/release |
| **计数特性** | 无内置计数 | 维护资源计数 |
| **使用场景** | 复杂条件判断 | 资源池管理 |
| **阻塞行为** | 条件不满足时阻塞 | 资源不足时阻塞 |

## 最佳实践

### 1. 条件变量使用要点
```python
# ✅ 正确：使用 while 循环检查条件
with condition:
    while not some_condition():
        condition.wait()
    # 执行业务逻辑

# ❌ 错误：使用 if 可能遇到虚假唤醒
with condition:
    if not some_condition():  # 可能被虚假唤醒
        condition.wait()
```

### 2. 避免死锁
```python
# ✅ 正确：统一的锁获取顺序
def transfer(from_account, to_account, amount):
    # 按地址排序获取锁，避免死锁
    first, second = sorted([from_account, to_account], key=lambda x: id(x))
    
    with first.condition:
        with second.condition:
            # 执行转账
            pass

# ❌ 错误：不同的锁获取顺序可能死锁
```

### 3. 超时处理
```python
import threading

def wait_with_timeout(condition, predicate, timeout=5):
    with condition:
        end_time = time.time() + timeout
        while not predicate():
            remaining = end_time - time.time()
            if remaining <= 0:
                raise TimeoutError("等待超时")
            condition.wait(timeout=remaining)
```

### 4. 信号量使用模式
```python
# ✅ 推荐：使用上下文管理器
def use_resource(semaphore):
    with semaphore:
        # 使用资源
        pass

# ✅ 手动管理（需要 try/finally）
def use_resource_manual(semaphore):
    semaphore.acquire()
    try:
        # 使用资源
        pass
    finally:
        semaphore.release()
```

条件变量适合**复杂的等待/通知**场景，而信号量适合**资源数量控制**。选择合适的同步原语可以让并发代码更清晰、更高效。