from sortedcontainers import SortedDict

class MaxStack:
    class Node:
        def __init__(self, val):
            self.val=val
            self.prev=None
            self.next=None

    def __init__(self):
        self.head= self.Node(0)
        self.tail= self.Node(0)
        self.head.next= self.tail
        self.tail.prev= self.head
        self.map = SortedDict()    # 值 -> [节点]

    def _add_node(self, node):
        prev = self.tail.prev
        prev.next=node
        node.prev=prev
        node.next=self.tail
        self.tail.prev = node

    def _remove_node(self, node):
        prev, nxt = node.prev, node.next
        prev.next, nxt.prev = nxt, prev    


    def push(self, x: int) -> None:
        node = self.Node(x)
        self._add_node(node)
        if x not in self.map:
            self.map[x] = []
        self.map[x].append(node)

    def pop(self) -> int:
        node = self.tail.prev
        self._remove_node(node)
        nodes_list = self.map[node.val]
        nodes_list.pop()
        if not nodes_list:
            del self.map[node.val]
        return node.val

    def top(self) -> int:
        return self.tail.prev.val

    def peekMax(self) -> int:
        return self.map.peekitem(-1)[0]

    def popMax(self) -> int:
        max_val, nodes_list = self.map.peekitem(-1)
        node = nodes_list.pop()
        if not nodes_list:
            del self.map[max_val]
        self._remove_node(node)
        return max_val


# 测试用例
def test_max_stack():
    # 测试基本功能
    stack = MaxStack()

    # 测试 push 和 top
    stack.push(5)
    assert stack.top() == 5

    stack.push(1)
    assert stack.top() == 1

    stack.push(5)
    assert stack.top() == 5

    # 测试 peekMax
    assert stack.peekMax() == 5

    # 测试 popMax
    assert stack.popMax() == 5  # 应该弹出最后一个5
    assert stack.top() == 1
    assert stack.peekMax() == 5  # 还有一个5

    # 测试 pop
    stack.pop()
    assert stack.top() == 5
    assert stack.peekMax() == 5

    print("基本测试通过!")

def test_max_stack_complex():
    # 测试复杂场景
    stack = MaxStack()

    # 添加多个元素
    stack.push(1)
    stack.push(3)
    stack.push(2)
    stack.push(3)
    stack.push(1)

    assert stack.peekMax() == 3
    assert stack.popMax() == 3  # 弹出最后一个3
    assert stack.top() == 1
    assert stack.peekMax() == 3  # 还有一个3

    stack.pop()  # 弹出1
    assert stack.top() == 2

    assert stack.popMax() == 3  # 弹出剩下的3
    assert stack.top() == 2
    assert stack.peekMax() == 2

    print("复杂测试通过!")

def test_max_stack_edge_cases():
    # 测试边界情况
    stack = MaxStack()

    # 单个元素
    stack.push(42)
    assert stack.top() == 42
    assert stack.peekMax() == 42
    assert stack.popMax() == 42

    # 重新添加元素
    stack.push(10)
    stack.push(20)
    stack.push(10)

    # 连续popMax
    assert stack.popMax() == 20
    assert stack.popMax() == 10  # 弹出最后一个10
    assert stack.top() == 10

    print("边界测试通过!")

if __name__ == "__main__":
    test_max_stack()
    test_max_stack_complex()
    test_max_stack_edge_cases()
    print("所有测试通过!")
        