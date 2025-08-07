
def all_paths_undirected(graph, source, target):
    """
    在无向图中找到从source到target的所有路径
    
    Args:
        graph: Dict[int, List[int]] - 邻接表表示的无向图
        source: int - 起始节点
        target: int - 目标节点
    
    Returns:
        List[List[int]] - 所有从source到target的路径
    """
    results = []
    
    def dfs(current, path, parent):
        # 到达目标节点，记录当前路径
        if current == target:
            results.append(path.copy())  # 重要：使用copy()避免引用问题
            return
        
        # 遍历当前节点的所有邻居
        for neighbor in graph.get(current, []):
            # 避免立即回到父节点（无向图特有）
            if neighbor == parent:
                continue
            
            # 避免环路：如果邻居已在当前路径中，跳过
            if neighbor in path:
                continue
            
            # 回溯算法：添加邻居到路径，递归探索，然后移除
            path.append(neighbor)
            dfs(neighbor, path, current)  # 当前节点成为下一层的父节点
            path.pop()  # 回溯：移除刚添加的节点
    
    # 从source开始DFS，初始路径包含source，初始parent为-1（表示无父节点）
    dfs(source, [source], -1)
    return results


# 性能优化版本（使用set代替list的in操作）
def all_paths_undirected_optimized(graph, source, target):
    """
    无向图路径查找的性能优化版本
    使用set来提高visited检查的效率
    """
    results = []
    
    def dfs(current, path, visited, parent):
        if current == target:
            results.append(path.copy())
            return
        
        for neighbor in graph.get(current, []):
            if neighbor == parent or neighbor in visited:
                continue
            
            path.append(neighbor)
            visited.add(neighbor)
            dfs(neighbor, path, visited, current)
            path.pop()
            visited.remove(neighbor)
    
    dfs(source, [source], {source}, -1)
    return results


# 测试代码和示例
if __name__ == "__main__":
    # 测试例1：经典4节点无向图
    undirected_graph1 = {
        0: [1, 2],
        1: [0, 2, 3],  # 无向图：每条边都是双向的
        2: [0, 1, 3],
        3: [1, 2]
    }
    
    print("测试1 - 经典无向图 0→3 的所有路径:")
    paths1 = all_paths_undirected(undirected_graph1, 0, 3)
    for i, path in enumerate(paths1, 1):
        print(f"  路径{i}: {' - '.join(map(str, path))}")
    print(f"总共找到 {len(paths1)} 条路径")
    print("预期: 4条路径 [0,1,3], [0,1,2,3], [0,2,1,3], [0,2,3]\n")
    
    # 测试例2：更复杂的网格状无向图
    grid_graph = {
        0: [1, 3],
        1: [0, 2, 4],
        2: [1, 5],
        3: [0, 4, 6],
        4: [1, 3, 5, 7],
        5: [2, 4, 8],
        6: [3, 7],
        7: [4, 6, 8],
        8: [5, 7]
    }
    
    print("测试2 - 3x3网格图 0→8 的所有路径:")
    paths2 = all_paths_undirected(grid_graph, 0, 8)
    for i, path in enumerate(paths2, 1):
        print(f"  路径{i}: {' - '.join(map(str, path))}")
    print(f"总共找到 {len(paths2)} 条路径\n")
    
    # 测试例3：线性链状图
    chain_graph = {
        0: [1],
        1: [0, 2],
        2: [1, 3],
        3: [2, 4],
        4: [3]
    }
    
    print("测试3 - 链状图 0→4 的所有路径:")
    paths3 = all_paths_undirected(chain_graph, 0, 4)
    for i, path in enumerate(paths3, 1):
        print(f"  路径{i}: {' - '.join(map(str, path))}")
    print(f"总共找到 {len(paths3)} 条路径（应该只有1条）\n")
    
    # 测试例4：字符节点图
    char_graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D'],
        'C': ['A', 'D', 'E'],
        'D': ['B', 'C', 'E'],
        'E': ['C', 'D']
    }
    
    print("测试4 - 字符节点图 A→E 的所有路径:")
    paths4 = all_paths_undirected(char_graph, 'A', 'E')
    for i, path in enumerate(paths4, 1):
        print(f"  路径{i}: {' - '.join(path)}")
    print(f"总共找到 {len(paths4)} 条路径\n")
    
    # 性能对比测试
    print("性能对比测试 - 使用相同的图:")
    
    import time
    
    # 标准版本
    start = time.time()
    paths_standard = all_paths_undirected(undirected_graph1, 0, 3)
    time_standard = time.time() - start
    
    # 优化版本
    start = time.time()
    paths_optimized = all_paths_undirected_optimized(undirected_graph1, 0, 3)
    time_optimized = time.time() - start
    
    print(f"标准版本: {len(paths_standard)} 条路径, 用时: {time_standard:.6f}秒")
    print(f"优化版本: {len(paths_optimized)} 条路径, 用时: {time_optimized:.6f}秒")
    print(f"结果一致: {paths_standard == paths_optimized}")
    
    # 展示错误用法的对比
    print("\n" + "="*50)
    print("错误示例：用有向图算法处理无向图")
    
    def all_paths_directed(graph, source, target):
        """有向图算法（错误地用于无向图）"""
        results = []
        def dfs(cur, path):
            if cur == target:
                results.append(path.copy())
                return
            for nei in graph.get(cur, []):
                if nei in path:
                    continue
                path.append(nei)
                dfs(nei, path)
                path.pop()
        dfs(source, [source])
        return results
    
    wrong_paths = all_paths_directed(undirected_graph1, 0, 3)
    correct_paths = all_paths_undirected(undirected_graph1, 0, 3)
    
    print(f"❌ 错误方法找到: {len(wrong_paths)} 条路径")
    print(f"✅ 正确方法找到: {len(correct_paths)} 条路径")
    print("差异说明：有向图算法无法正确处理无向图的双向边特性")
