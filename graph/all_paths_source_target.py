
def all_paths_source_target(graph, source, target):
    """
    find all paths from source to target
    Args:
        graph (dict): key -> list of neighbors
    """
    def dfs(cur, path, res):
        if cur== target:
            res.append(path.copy())
            return
        for nei in graph.get(cur, []):
            if nei in path:
                continue
            path.append(nei)
            dfs(nei, path, res)
            path.pop()
    
    results=[]
    dfs(source, [source], results)
    return results

#example usage
if __name__ == "__main__":
    graph = {
        "A": ["B", "C"],
        "B": []
    }