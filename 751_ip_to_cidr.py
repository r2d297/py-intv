from typing import List

def ipToCIDR(self, ip: str, n: int) -> list[str]:
    """
    LeetCode 751 - IP to CIDR
    
    给定起始IP地址和需要覆盖的IP数量，返回最少的CIDR块列表
    
    核心思想：
    1. 将IP转换为整数便于计算
    2. 使用贪心算法，每次创建最大可能的CIDR块
    3. 最大块大小由两个因素限制：
    - 对齐约束：start & (-start) 
    - 剩余IP数量：n
    """
    
    def ip_to_int(ip_str):
        """将IP字符串转换为32位整数"""
        parts = ip_str.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16)+ (int(parts[2]) << 8) + int(parts[3])
    
    def int_to_ip(num):
        """将32位整数转换为IP字符串"""
        return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"
    
    def get_max_block_size(start, remaining):
        """
        计算从start开始能创建的最大CIDR块大小
        受两个因素限制：
        1. 对齐约束：start & (-start) - lowbit操作
        2. 剩余数量：remaining
        """
        # Find the largest block size we can use
        # This is limited by two factors:
        # 1. Alignment: how many addresses can start at 'start' position
        # 2. Remaining count: we can't exceed n addresses            
        if start == 0:
        # Special case: if start is 0, we can have very large blocks
        # Find the largest power of 2 that doesn't exceed n
            max_size_by_alignment = 1 << (n.bit_length() - 1) if n > 0 else 1
        else:
            # 找到start的最大2的幂因子（对齐约束）
            # The alignment constraint: start & (-start) gives us the largest power of 2
            # that divides start, which determines the max block size at this position
            max_size_by_alignment = start & (-start) if start > 0 else 1
        
        # 找到小于等于remaining的最大2的幂,Find the largest power of 2 that doesn't exceed n
        max_size_by_remaining = 1 << (remaining.bit_length() - 1) if remaining > 0 else 1
        
        # 取两者的最小值,The actual block size is the minimum of alignment constraint and count constraint
        return min(max_size_by_alignment, max_size_by_remaining)
    
    # 将起始IP转换为整数
    start = ip_to_int(ip)
    result = []
    
    # 贪心算法：每次创建最大可能的CIDR块
    while n > 0:
        # 计算当前能创建的最大块大小
        block_size = get_max_block_size(start, n)
        
        # 计算CIDR前缀长度（/xx）,calculate the prefix length,if block size is 2^k, then prefix length is 32-k
        prefix_length = 32 - (block_size.bit_length() - 1)
        
        # 创建CIDR表示
        cidr_block = f"{int_to_ip(start)}/{prefix_length}"
        result.append(cidr_block)
        
        # 更新状态
        start += block_size
        n -= block_size
    
    return result

# Test with the provided examples
def test_examples():
    # Example 1
    ip1, n1 = "255.0.0.7", 10
    result1 = ipToCIDR(ip1, n1)
    print(f"Example 1: {result1}")
    # Expected: ["255.0.0.7/32","255.0.0.8/29","255.0.0.16/32"]
    
    # Example 2
    ip2, n2 = "117.145.102.62", 8
    result2 = ipToCIDR(ip2, n2)
    print(f"Example 2: {result2}")
    # Expected: ["117.145.102.62/31","117.145.102.64/30","117.145.102.68/31"]

# Run tests
#test_examples()


# Let's also trace through Example 1 step by step to understand the algorithm
def trace_example1():
    print("\nTracing Example 1: ip='255.0.0.7', n=10")
    
    def ip_to_int(ip_str):
        parts = ip_str.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])
    
    def int_to_ip(num):
        return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"
    
    start = ip_to_int("255.0.0.7")
    n = 10
    step = 1
    
    print(f"Starting IP as integer: {start} (binary: {bin(start)})")
    
    while n > 0:
        print(f"\nStep {step}:")
        print(f"  Current start: {int_to_ip(start)} ({start}), remaining: {n}")
        print(f"  Binary of start: {bin(start)}")
        
        if start == 0:
            max_size_by_alignment = n
        else:
            max_size_by_alignment = start & (-start)
        
        block_size = min(max_size_by_alignment, n)
        prefix_len = 32 - (block_size.bit_length() - 1)
        
        print(f"  Max size by alignment: {max_size_by_alignment}")
        print(f"  Block size: {block_size}")
        print(f"  Prefix length: {prefix_len}")
        print(f"  CIDR block: {int_to_ip(start)}/{prefix_len}")
        
        start += block_size
        n -= block_size
        step += 1

trace_example1()
