from ai_client import ask_deepseek

prompt = "推荐一个适合周末的户外活动"

print("=== Seed 实验 (temperature=0.8) ===\n")

# 固定种子 123
seed = 123
for i in range(3):
    ans, _, _ = ask_deepseek(prompt, temperature=0.8, max_tokens=50, seed=seed)
    print(f"第{i+1}次 (seed={seed}): {ans[:40]}...")

print("\n--- 更换种子为 456 ---")
ans2, _, _ = ask_deepseek(prompt, temperature=0.8, max_tokens=50, seed=456)
print(f"seed=456: {ans2[:40]}...")

'''
测试价值：在自动化回归测试中，我们可以 固定 Seed，让每次运行的 AI 输出完全一致，从而用精确断言（如字符串比对）替代模糊的相似度断言。
'''