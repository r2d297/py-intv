

class FibonacciTreePathFinder:
    def __init__(self, max_order=50):
        """预计算斐波那契树的节点数量"""
        self.nodes = [0] * (max_order + 1)
        self.nodes[0] = 1  # 0阶树有1个节点
        self.nodes[1] = 1  # 1阶树有1个节点
        
        for i in range(2, max_order + 1):
            self.nodes[i] = 1 + self.nodes[i-1] + self.nodes[i-2]
    
    def find_path(self, order, source, dest):
        """
        使用动态规划找到两个节点间的路径
        
        Args:
            order: 斐波那契树的阶数
            source: 源节点编号
            dest: 目标节点编号
            
        Returns:
            路径字符串，"U"表示向上，"L"表示向左，"R"表示向右
        """
        if source == dest:
            return ""
        
        # 找到两个节点到根的路径
        source_path = self.find_path_to_root(order, source)
        dest_path = self.find_path_to_root(order, dest)
        
        # 移除公共前缀（到LCA的路径）
        lca_depth = 0
        min_len = min(len(source_path), len(dest_path))
        
        while (lca_depth < min_len and 
               source_path[lca_depth] == dest_path[lca_depth]):
            lca_depth += 1
        
        # 构造最终路径
        # 从source到LCA：剩余路径长度的"U"
        # 从LCA到dest：剩余路径
        up_moves = "U" * (len(source_path) - lca_depth)
        down_moves = "".join(dest_path[lca_depth:])
        
        return up_moves + down_moves
    
    def find_path_to_root(self, order, target):
        """
        找到从根节点到目标节点的路径
        利用斐波那契树的递归性质快速定位
        """
        if order <= 1:
            return []  # 0阶或1阶树只有根节点
        
        if target == 0:
            return []  # 已经是根节点
        
        # 左子树的大小（(order-2)阶斐波那契树的节点数）
        left_subtree_size = self.nodes[order-2] if order >= 2 else 0
        
        if target <= left_subtree_size:
            # 目标在左子树中
            # 递归到左子树，调整目标编号
            sub_path = self.find_path_to_root(order-2, target-1)
            return ["L"] + sub_path
        else:
            # 目标在右子树中
            # 递归到右子树，调整目标编号
            adjusted_target = target - left_subtree_size - 1
            sub_path = self.find_path_to_root(order-1, adjusted_target)
            return ["R"] + sub_path
    
    def get_subtree_info(self, order, node):
        """获取节点的子树信息（用于调试）"""
        if order <= 1:
            return f"Node {node} is a leaf (order {order})"
        
        left_size = self.nodes[order-2] if order >= 2 else 0
        
        if node == 0:
            return f"Node {node} is root of order-{order} tree"
        elif node <= left_size:
            return f"Node {node} is in left subtree (order-{order-2})"
        else:
            return f"Node {node} is in right subtree (order-{order-1})"

# 测试和演示
def test_fibonacci_tree():
    finder = FibonacciTreePathFinder()
    
    # 测试用例1：order=5, source=5, dest=7
    print("=== 测试用例1 ===")
    order = 5
    source = 5
    dest = 7
    
    print(f"斐波那契树阶数: {order}")
    print(f"各阶节点数: {[finder.nodes[i] for i in range(order+1)]}")
    print(f"总节点数: {finder.nodes[order]}")
    print()
    
    # 分析节点位置
    print("节点位置分析:")
    print(finder.get_subtree_info(order, source))
    print(finder.get_subtree_info(order, dest))
    print()
    
    # 找到路径
    result = finder.find_path(order, source, dest)
    print(f"从节点 {source} 到节点 {dest} 的路径: '{result}'")
    
    # 详细路径分析
    source_path = finder.find_path_to_root(order, source)
    dest_path = finder.find_path_to_root(order, dest)
    print(f"源节点到根的路径: {source_path}")
    print(f"目标节点到根的路径: {dest_path}")
    
    print("\n" + "="*50)
    
    # 更多测试用例
    test_cases = [
        (5, 3, 6, "UURL"),  # 预期结果
        (4, 1, 7, "URL"),
        (3, 2, 4, "ULR"),
        (5, 0, 14, "RRR"),  # 根到最右叶子
    ]
    
    print("更多测试用例:")
    for order, src, dst, expected in test_cases:
        if dst < finder.nodes[order]:  # 确保节点存在
            actual = finder.find_path(order, src, dst)
            status = "✓" if actual == expected else "✗"
            print(f"{status} Order {order}: {src}→{dst} = '{actual}' (期望: '{expected}')")

# 算法复杂度分析
def analyze_complexity():
    print("\n=== 算法复杂度分析 ===")
    print("时间复杂度: O(order) - 每次递归减少阶数")
    print("空间复杂度: O(order) - 递归栈深度和预计算数组")
    print("预计算复杂度: O(max_order) - 只需要一次")
    print()
    print("优势:")
    print("1. 避免了O(n)的完整树遍历")
    print("2. 利用数学性质直接'跳跃'到目标区域")
    print("3. 递归深度只与阶数相关，而非节点总数")
    print("4. 可以处理非常大的斐波那契树而无需构建实际树结构")

if __name__ == "__main__":
    test_fibonacci_tree()
    analyze_complexity()

# 进阶：可视化斐波那契树结构
def visualize_fibonacci_tree(order, max_nodes=20):
    """可视化小规模斐波那契树的结构"""
    finder = FibonacciTreePathFinder()
    
    if finder.nodes[order] > max_nodes:
        print(f"树太大({finder.nodes[order]}个节点)，跳过可视化")
        return
    
    print(f"\n=== {order}阶斐波那契树结构可视化 ===")
    
    def print_tree_structure(curr_order, offset=0, prefix=""):
        if curr_order <= 1:
            print(f"{prefix}叶子[{offset}]")
            return offset + 1
        
        print(f"{prefix}根[{offset}] (order-{curr_order})")
        
        # 左子树
        left_offset = print_tree_structure(curr_order-2, offset+1, prefix+"├─L:")
        
        # 右子树  
        right_offset = print_tree_structure(curr_order-1, left_offset, prefix+"└─R:")
        
        return right_offset
    
    print_tree_structure(order)
    print(f"总节点数: {finder.nodes[order]}")

# 运行可视化
if __name__ == "__main__":
    for order in [2, 3, 4]:
        visualize_fibonacci_tree(order)
