import os
from openai import OpenAI

def ask_deepseek(prompt: str, model: str = "deepseek-chat") -> tuple[str, str, int]:
    """
    调用 DeepSeek API，返回 (回答内容, 结束原因, 总Token数)
    """
    api_key = os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("未找到环境变量 DEEPSEEK_API_KEY，请先设置")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    total_tokens = response.usage.total_tokens

    return answer, finish_reason, total_tokens