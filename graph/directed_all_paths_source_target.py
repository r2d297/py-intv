
def all_paths_directed(graph, source, target):
    """
    在有向图中找到从source到target的所有路径
    
    Args:
        graph: Dict[int, List[int]] - 邻接表表示的有向图
        source: int - 起始节点
        target: int - 目标节点
    
    Returns:
        List[List[int]] - 所有从source到target的路径
    """
    results = []
    
    def dfs(current, path):
        # 到达目标节点，记录当前路径
        if current == target:
            results.append(path.copy())  # 重要：使用copy()避免引用问题
            return
        
        # 遍历当前节点的所有邻居
        for neighbor in graph.get(current, []):
            # 避免环路：如果邻居已在当前路径中，跳过
            if neighbor in path:
                continue
            
            # 回溯算法：添加邻居到路径，递归探索，然后移除
            path.append(neighbor)
            dfs(neighbor, path)
            path.pop()  # 回溯：移除刚添加的节点
    
    # 从source开始DFS，初始路径包含source
    dfs(source, [source])
    return results


# 测试代码和示例
if __name__ == "__main__":
    # 测试例1：简单有向图
    directed_graph1 = {
        0: [1, 2],
        1: [3],
        2: [1, 3],
        3: []
    }
    
    print("测试1 - 有向图 0→3 的所有路径:")
    paths1 = all_paths_directed(directed_graph1, 0, 3)
    for i, path in enumerate(paths1, 1):
        print(f"  路径{i}: {' → '.join(map(str, path))}")
    print(f"总共找到 {len(paths1)} 条路径\n")
    
    # 测试例2：有环的有向图
    directed_graph2 = {
        0: [1],
        1: [2, 3],
        2: [1, 4],  # 2→1 形成环
        3: [4],
        4: []
    }
    
    print("测试2 - 有环有向图 0→4 的所有路径:")
    paths2 = all_paths_directed(directed_graph2, 0, 4)
    for i, path in enumerate(paths2, 1):
        print(f"  路径{i}: {' → '.join(map(str, path))}")
    print(f"总共找到 {len(paths2)} 条路径\n")
    
    # 测试例3：无路径情况
    directed_graph3 = {
        0: [1],
        1: [2],
        2: [],
        3: [4],  # 3和4是孤立的
        4: []
    }
    
    print("测试3 - 无路径情况 0→4:")
    paths3 = all_paths_directed(directed_graph3, 0, 4)
    if paths3:
        for i, path in enumerate(paths3, 1):
            print(f"  路径{i}: {' → '.join(map(str, path))}")
    else:
        print("  没有找到从0到4的路径")
    print(f"总共找到 {len(paths3)} 条路径\n")
    
    # 测试例4：复杂图
    directed_graph4 = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['E', 'F'],
        'D': ['G'],
        'E': ['G'],
        'F': ['G'],
        'G': []
    }
    
    print("测试4 - 字符节点有向图 A→G 的所有路径:")
    paths4 = all_paths_directed(directed_graph4, 'A', 'G')
    for i, path in enumerate(paths4, 1):
        print(f"  路径{i}: {' → '.join(path)}")
    print(f"总共找到 {len(paths4)} 条路径")
