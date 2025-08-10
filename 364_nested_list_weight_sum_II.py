from typing import List

class NestedInteger:
    def __init__(self, value=None):
        """
        If value is not specified, initializes an empty list.
        Otherwise initializes a single integer equal to value.
        """
        if value is None:
            self._data = []
        elif isinstance(value, int):
            self._data = value
        else:
            raise TypeError("value should be an integer or None.")

    def isInteger(self):
        """Return True if this NestedInteger holds a single integer."""
        return isinstance(self._data, int)

    def add(self, elem):
        """Set this NestedInteger to hold a nested list and adds a NestedInteger elem to it."""
        if self.isInteger():
            self._data = [NestedInteger(self._data)]
        self._data.append(elem)

    def setInteger(self, value):
        """Set this NestedInteger to hold a single integer."""
        self._data = value

    def getInteger(self):
        """Return the single integer if it holds one, else return None."""
        return self._data if self.isInteger() else None

    def getList(self):
        """Return the nested list if it holds one, else return None."""
        return self._data if not self.isInteger() else None


def build_nested_integer(data):
    """Helper function to build NestedInteger from Python list/int"""
    if isinstance(data, int):
        return NestedInteger(data)
    ni = NestedInteger()
    for item in data:
        ni.add(build_nested_integer(item))
    return ni

class Solution:
    """
    BFS 累加原理：

    level_sum 是累积的，不会重置
    每轮把当前 level_sum 加到 res
    越早进入 level_sum 的数字，被累加次数越多
    累加次数分析：

    数字 1：第1轮加入，被累加3次（第1、2、3轮都加到res）→ 1×3 = 3
    数字 4：第2轮加入，被累加2次（第2、3轮加到res）→ 4×2 = 8
    数字 6：第3轮加入，被累加1次（第3轮加到res）→ 6×1 = 6
    总和：3 + 8 + 6 = 17 ✓
    这就是 BFS 单遍算法的精妙之处：通过累积 level_sum 和逐轮相加，自然实现了反向深度加权！
    """
    
    def depthSumInverse(self, nestedList: List[NestedInteger]) -> int:
        res, level_sum = 0, 0
        while nestedList:
            next_level = []
            
            for n in nestedList:
                if n.isInteger():
                    level_sum += n.getInteger()
                else:
                    next_level.extend(n.getList())
            nestedList = next_level
            res += level_sum
        return res


# test
if __name__ == "__main__":
    solution = Solution()
    
    # 测试例子 1: [[1,1], 2, [1,1]]
    print("测试例子 1: [[1,1], 2, [1,1]]")
    test1_data = [[1,1], 2, [1,1]]
    test1_nested = [build_nested_integer(item) for item in test1_data]
    result1 = solution.depthSumInverse(test1_nested)
    print(f"输入: {test1_data}")
    print(f"输出: {result1}")
    print()
    
    # 测试例子 2: [1, [4, [6]]]
    print("测试例子 2: [1, [4, [6]]]")
    test2_data = [1, [4, [6]]]
    test2_nested = [build_nested_integer(item) for item in test2_data]
    result2 = solution.depthSumInverse(test2_nested)
    print(f"输入: {test2_data}")
    print(f"输出: {result2}")
    print()
    
    # 详细步骤演示（例子2）
    print("=== 详细步骤演示 (例子2) ===")
    test2_nested_demo = [build_nested_integer(item) for item in test2_data]
    
    res, level_sum = 0, 0
    round_num = 1
    nestedList = test2_nested_demo
    
    while nestedList:
        print(f"第 {round_num} 轮:")
        print(f"  当前层元素数量: {len(nestedList)}")
        next_level = []
        integers_in_level = []
        
        for n in nestedList:
            if n.isInteger():
                value = n.getInteger()
                level_sum += value
                integers_in_level.append(value)
            else:
                next_level.extend(n.getList())
        
        if integers_in_level:
            print(f"  发现整数: {integers_in_level}")
        print(f"  level_sum: {level_sum}")
        
        nestedList = next_level
        res += level_sum
        print(f"  res += level_sum → res = {res}")
        print()
        
        round_num += 1
    
    print(f"最终结果: {res}")