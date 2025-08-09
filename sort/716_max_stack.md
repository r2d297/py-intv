**双向链表 + SortedDict** 是怎么配合实现最优 Max Stack 的：  

```
双向链表 (维护栈顺序，O(1) 插入/删除任意节点)
HEAD <-> [5] <-> [1] <-> [5] <-> TAIL
           ^              ^
           |              |
SortedDict (按值排序，value → 节点列表)
{
  1: [Node(1)],
  5: [Node(5-第1个), Node(5-第2个)]
}
```

**push(x)**  
1. 用双向链表 `_add_node` 把新节点插到尾部 → 得到最新的栈顶  
2. 在 `SortedDict` 中，把这个值的节点追加到 value 对应的列表末尾  

**pop()**  
1. 从双向链表尾部取节点并删除  
2. 从 `SortedDict` 中删除这个节点（列表末尾弹出），空了就删掉那一条记录  

**peekMax()**  
- `SortedDict.peekitem(-1)` 直接返回最大键（因为它是有序的，末尾就是最大值）  

**popMax()**  
1. 从 `SortedDict.peekitem(-1)` 取到最大值 `max_val`  
2. 在节点列表中取出最后一个节点（最新的那一个 max）  
3. `_remove_node` 从链表中 O(1) 删除它  
4. 如果节点列表空了，删掉那条 value  

这样：  
- 链表保证了 O(1) 拿到栈顶、删除任意节点  
- SortedDict 保证了 O(log n) 找最大值并定位到对应节点  
- 删除最大值所需的链表节点引用已经在 `SortedDict` 里存着，所以可以 O(1) 精确删除  

要不要我直接在你现在这个空的 `MaxStack` 类里，把这个最优实现帮你填好，并改成可以直接在 LeetCode 上提交的版本？这样你直接 Ctrl+C / Ctrl+V 就能 AC。