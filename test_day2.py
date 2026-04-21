import os
import sys
from typing import AnyStr
from dotenv import load_dotenv
from openai import OpenAI


sys.stdout.reconfigure(encoding='utf-8')
load_dotenv()

def test_deepseek_basic():
    api_key = os.getenv("DEEPSEEK_API_KEY")

    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY环境变量未设置")

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )
        
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": "你好,请介绍下你自己"}
        ]
    )
    answer = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    total_tokens = response.usage.total_tokens

    assert len(answer) > 0, "模型返回为空"
    assert finish_reason == "stop", "模型返回非预期结束" 
    assert total_tokens > 0, "模型返回的token数为0"
    assert 5<=total_tokens<=500, "模型返回的token数不在预期范围内"
    print(f"✅ 所有断言通过！")
    print(f"   - 回答长度: {len(answer)} 字符")
    print(f"   - Token 消耗: {total_tokens}")
    print(f"   - 回答摘要: {answer[:80]}...")

if __name__ == '__main__':
    test_deepseek_basic()
