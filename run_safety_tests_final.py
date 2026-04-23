"""
安全回归测试运行器 - 中文显示修复版

该脚本运行安全回归测试并确保中文显示正常
"""

import subprocess
import sys
import re

# 运行 pytest 测试
result = subprocess.run(
    [sys.executable, "-m", "pytest", "test_safety_regression.py", "-v", "-s"],
    capture_output=True,
    text=True
)

# 处理输出，将 Unicode 转义序列转换为中文
def decode_unicode_escape(s):
    """将Unicode转义序列转换为中文"""
    return re.sub(r'\\u([0-9a-fA-F]{4})', lambda m: chr(int(m.group(1), 16)), s)

# 处理输出
stdout = decode_unicode_escape(result.stdout)
stderr = decode_unicode_escape(result.stderr)
output = stdout + stderr

# 打印处理后的输出
print("=" * 60)
print("安全回归测试结果")
print("=" * 60)
print(output)

# 清理临时文件
import os
for temp_file in ['test_chinese.py', 'test_encoding.py', 'run_safety_tests.py', 'run_safety_tests_utf8.py']:
    if os.path.exists(temp_file):
        os.remove(temp_file)

print("\n✅ 测试完成，临时文件已清理")
