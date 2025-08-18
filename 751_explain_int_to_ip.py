
def explain_int_to_ip_conversion():
    """详细解释 32位整数转IP地址字符串的过程"""
    
    print("=== 32位整数转IP地址字符串详解 ===\n")
    
    # 示例：IP地址 192.168.1.100
    ip_str = "192.168.1.100"
    
    # 首先展示如何从IP字符串转为32位整数
    print("1. IP字符串转32位整数过程：")
    parts = ip_str.split('.')
    print(f"IP地址: {ip_str}")
    print(f"分解为: {parts}")
    
    # 计算每个部分的贡献
    part0 = int(parts[0]) << 24  # 192 << 24
    part1 = int(parts[1]) << 16  # 168 << 16  
    part2 = int(parts[2]) << 8   # 1 << 8
    part3 = int(parts[3])        # 100
    
    print(f"\n各部分的位移计算:")
    print(f"第1个字节 {parts[0]:3s}: {int(parts[0]):3d} << 24 = {part0:>10d} (0x{part0:08X})")
    print(f"第2个字节 {parts[1]:3s}: {int(parts[1]):3d} << 16 = {part1:>10d} (0x{part1:08X})")
    print(f"第3个字节 {parts[2]:3s}: {int(parts[2]):3d} << 8  = {part2:>10d} (0x{part2:08X})")
    print(f"第4个字节 {parts[3]:3s}: {int(parts[3]):3d} << 0  = {part3:>10d} (0x{part3:08X})")
    
    num = part0 + part1 + part2 + part3
    print(f"\n最终32位整数: {num} (0x{num:08X})")
    print(f"二进制表示: {bin(num)}")
    
    # 现在解释反向转换过程
    print(f"\n" + "="*60)
    print("2. 32位整数转IP字符串过程 - 逐步解析：")
    print(f"输入整数: {num} (0x{num:08X})")
    print(f"二进制:   {num:032b}")
    print()
    
    # 分解每个字节的提取过程
    print("字节提取过程:")
    print("位置:     [31-24] [23-16] [15-8]  [7-0]")
    print(f"二进制:   {num:032b}")
    print("           └─────┘ └─────┘ └────┘ └───┘")
    print("            字节0   字节1   字节2  字节3")
    print()
    
    # 详解每个操作
    operations = [
        ("第1个字节", "num >> 24", num >> 24, "(num >> 24) & 255", (num >> 24) & 255),
        ("第2个字节", "num >> 16", num >> 16, "(num >> 16) & 255", (num >> 16) & 255),
        ("第3个字节", "num >> 8",  num >> 8,  "(num >> 8) & 255",  (num >> 8) & 255),
        ("第4个字节", "num >> 0",  num,       "num & 255",         num & 255)
    ]
    
    print("逐步计算:")
    for desc, shift_expr, shift_result, mask_expr, final_result in operations:
        print(f"\n{desc}:")
        print(f"  步骤1 - 右移: {shift_expr:12s} = {shift_result:>10d} (0x{shift_result:08X})")
        print(f"          二进制: {shift_result:032b}")
        print(f"  步骤2 - 掩码: {mask_expr:15s} = {final_result:>3d}")
        print(f"          解释: 只保留最低8位，得到 {final_result}")

def demonstrate_bit_operations():
    """演示位操作的关键概念"""
    print(f"\n" + "="*60)
    print("3. 关键位操作概念解释")
    print("="*60)
    
    print("\n右移操作 (>>) 的作用:")
    num = 0xC0A80164  # 192.168.1.100
    
    print(f"原数字: {num:>10d} (0x{num:08X})")
    print(f"二进制: {num:032b}")
    print()
    
    for shift in [24, 16, 8, 0]:
        result = num >> shift
        print(f">> {shift:2d}:   {result:>10d} (0x{result:08X}) = {result:032b}")
    
    print(f"\n按位与操作 (& 255) 的作用:")
    print("255 的二进制是: 11111111 (8个1)")
    print("& 255 的作用是只保留最低8位，清除高位")
    print()
    
    examples = [
        (num >> 24, "192"),
        (num >> 16, "168"), 
        (num >> 8, "1"),
        (num, "100")
    ]
    
    for value, expected in examples:
        masked = value & 255
        print(f"{value:>10d} & 255 = {masked:3d} (期望: {expected})")
        print(f"{value:032b}")
        print(f"{'11111111':>32s} (mask)")
        print(f"{masked:032b} (结果)")
        print()

def test_various_ips():
    """测试不同IP地址的转换"""
    print(f"\n" + "="*60)
    print("4. 测试不同IP地址")
    print("="*60)
    
    def ip_to_int(ip_str):
        parts = ip_str.split('.')
        return (int(parts[0]) << 24) + (int(parts[1]) << 16) + (int(parts[2]) << 8) + int(parts[3])
    
    def int_to_ip(num):
        return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"
    
    test_ips = [
        "0.0.0.0",
        "127.0.0.1", 
        "192.168.1.1",
        "255.255.255.255",
        "10.0.0.1",
        "172.16.0.1"
    ]
    
    print(f"{'IP地址':<18s} {'32位整数':<12s} {'十六进制':<12s} {'转换回来':<18s} {'验证'}")
    print("-" * 70)
    
    for ip in test_ips:
        num = ip_to_int(ip)
        converted_back = int_to_ip(num)
        is_correct = ip == converted_back
        status = "✓" if is_correct else "✗"
        
        print(f"{ip:<18s} {num:<12d} 0x{num:08X}      {converted_back:<18s} {status}")

def step_by_step_example():
    explain_int_to_ip_conversion()
    demonstrate_bit_operations()
    test_various_ips()

# 执行一遍
step_by_step_example()