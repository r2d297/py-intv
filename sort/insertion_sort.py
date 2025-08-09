def insertion_sort(arr):
    """插入排序
    
    基本思想：
    1. 将数组分为已排序区间和未排序区间
    2. 初始时已排序区间只有第一个元素
    3. 每次从未排序区间取出一个元素，插入到已排序区间的正确位置
    
    时间复杂度：
    - 最好情况：O(n) - 数组已经有序
    - 最坏情况：O(n²) - 数组逆序
    - 平均情况：O(n²)
    
    🔍 关键理解：while循环结束后j的位置 
    情况分析
    当while循环while j >= 0 and arr_copy[j] > key:结束时，有两种可能：
        j < 0：说明key比所有已排序元素都小
        arr_copy[j] <= key：找到了合适位置
    
    空间复杂度：O(1) - 原地排序
    
    Args:
        arr: List[int] - 待排序的数组
    
    Returns:
        List[int] - 排序后的数组
    """

    arr_copy = arr.copy()
    n = len(arr)
    
    #从第二个元素开始(下标1), 因为第一个元素默认已经排序
    for i in range(1,n):
        #当前要插入的元素
        key = arr_copy[i]
        #已经排序区间的最后一个位置
        j = i-1
        
        #在已经排序区间中找到合适的插入位置
        #将所有大于key的元素向右移动一位
        while j>=0 and arr_copy[j]  > key:
            arr_copy[j+1] = arr_copy[j]
            j-=1
        
        arr_copy[j+1]=key
    
    return arr_copy



def insertion_sort_optimized(arr):
    """
    优化版插入排序：使用二分查找找插入位置
    时间复杂度：O(n log n) for 查找 + O(n²) for 移动 = O(n²)
    但是比较次数大大减少
    """
    import bisect
    
    arr_copy = arr.copy()
    
    for i in range(1, len(arr_copy)):
        key = arr_copy[i]
        # 使用二分查找找到插入位置
        pos = bisect.bisect_left(arr_copy[:i], key)
        # 移动元素
        arr_copy[pos+1:i+1] = arr_copy[pos:i]
        # 插入元素
        arr_copy[pos] = key
    
    return arr_copy

def insertion_sort_recursive(arr, n=None):
    """
    递归版本的插入排序
    """
    if n is None:
        arr = arr.copy()
        n = len(arr)
    
    # 基础情况：只有一个元素或没有元素
    if n <= 1:
        return arr
    
    # 递归排序前n-1个元素
    insertion_sort_recursive(arr, n-1)
    
    # 将第n个元素插入到正确位置
    last = arr[n-1]
    j = n-2
    
    while j >= 0 and arr[j] > last:
        arr[j+1] = arr[j]
        j -= 1
    
    arr[j+1] = last
    
    return arr


if __name__ == "__main__":
    test_arrays = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 2, 4, 6, 1, 3],
        [1],  # 单元素
        [],   # 空数组
        [3, 3, 3, 3],  # 重复元素
        [1, 2, 3, 4, 5],  # 已排序
        [5, 4, 3, 2, 1],  # 逆序
    ]
    
    print("🔄 插入排序算法测试")
    print("=" * 60)
    
    for i, arr in enumerate(test_arrays, 1):
        print(f"\n测试用例 {i}:")
        print(f"原数组: {arr}")
        sorted_arr = insertion_sort(arr)
        print(f"排序后: {sorted_arr}")
        print(f"验证: {'✅' if sorted_arr == sorted(arr) else '❌'}")
    
    # 详细过程演示
    print("\n" + "=" * 60)
    print("📝 详细排序过程演示")
    print("=" * 60)
    demo_array = [64, 34, 25, 12, 22]
    insertion_sort(demo_array)
       