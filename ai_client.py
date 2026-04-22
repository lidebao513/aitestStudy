import os
from openai import OpenAI

def ask_deepseek(prompt: str, 
                 temperature: float = 0.0, 
                 max_tokens: int = 200,
                 seed: int = None) -> tuple[str, str, int]:
    """
    调用 DeepSeek API
    :param prompt: 用户问题
    :param temperature: 随机性控制，0=确定，1=高随机
    :param max_tokens: 最大输出长度
    :param seed: 随机种子，固定后输出可复现
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("❌ 未找到环境变量 DEEPSEEK_API_KEY")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    extra_params = {}
    if seed is not None:
        extra_params["seed"] = seed

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
        max_tokens=max_tokens,
        **extra_params
    )

    answer = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    total_tokens = response.usage.total_tokens

    return answer, finish_reason, total_tokens