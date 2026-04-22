from ai_client import ask_deepseek

prompt = "请用一个简短的词语描述天空的颜色（只输出词语，不要解释）"

print("=== Temperature 实验 ===\n")

for temp in [0.0, 0.5, 1.0, 1.5]:
    print(f"Temperature = {temp}:")
    for i in range(3):  # 每个温度跑3次，观察一致性
        ans, _, _ = ask_deepseek(prompt, temperature=temp, max_tokens=20)
        print(f"  第{i+1}次: {ans.strip()}")
    print()
'''
Temperature 控制模型输出的 “脑洞大小”。

0.0：几乎每次回答都一样（可复现）。

1.0 以上：回答变幻莫测（像有随机 Bug）。
测试视角映射：temperature=0.0 相当于一个 稳定接口，适合做回归测试；高温度适合做探索性测试或压力测试。
'''