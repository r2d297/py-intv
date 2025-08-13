from typing import List



def ipToCIDR(ip:str, n:int) -> List[str]:
    def ip_to_int(ip_str):
        #convert IP string to 32-bit integer
        parts = ip_str.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16)+ (int(parts[2]) << 8) + int(parts[3])
    
    def int_to_ip(num):
        #convert 32-bit integer to IP string
        return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"

    start = ip_to_int(ip)
    res = []
    
    while n > 0:
        # Find the largest block size we can use
        # This is limited by two factors:
        # 1. Alignment: how many addresses can start at 'start' position
        # 2. Remaining count: we can't exceed n addresses

        if start == 0:
            # Special case: if start is 0, we can have very large blocks
            # Find the largest power of 2 that doesn't exceed n
            max_size_by_alignment = 1 << (n.bit_length() - 1) if n > 0 else 1
        else:
            # The alignment constraint: start & (-start) gives us the largest power of 2
            # that divides start, which determines the max block size at this position
            max_size_by_alignment = start & (-start)

        # Find the largest power of 2 that doesn't exceed n
        max_size_by_count = 1 << (n.bit_length() - 1) if n > 0 else 1

        # The actual block size is the minimum of alignment constraint and count constraint
        block_size = min(max_size_by_alignment, max_size_by_count)


        # calculate the prefix length
        # if block size is 2^k, then prefix length is 32-k
        prefix_len = 32 - (block_size.bit_length() - 1)

        # generate the CIDR block
        res.append(f"{int_to_ip(start)}/{prefix_len}")

        # update the state
        start += block_size
        n -= block_size
        
    return res

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
