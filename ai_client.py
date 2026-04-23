"""
DeepSeek API 客户端工具

该模块提供了与 DeepSeek 大语言模型交互的功能，
通过 OpenAI 兼容的 API 接口调用 DeepSeek 模型。

注意：该模块已重构，现在优先使用本地 Ollama (deepseek-r1:7b)，
仅在 Ollama 不可用时自动切换到 DeepSeek API。
如需直接使用 DeepSeek API，请使用 llm_client 模块。
"""

from llm_client import ask_llm, get_provider_info

def ask_deepseek(prompt: str,
                 temperature: float = 0.0,
                 max_tokens: int = 200,
                 seed: int = None,
                 system_prompt: str = None) -> tuple[str, str, int]:
    """
    调用 LLM 生成回答（统一接口）

    默认优先使用本地 Ollama (deepseek-r1:7b)，如果不可用则自动切换到 DeepSeek API。

    :param prompt: 用户问题或指令
    :param temperature: 随机性控制，0=确定性输出，值越大输出越随机
    :param max_tokens: 最大输出长度，控制生成内容的长度
    :param seed: 随机种子，配合 temperature=0 实现完全可复现的输出
    :param system_prompt: 系统级指令，定义 AI 行为边界和角色
    :return: (回答内容, 结束原因, Token消耗) 三元组
    """
    return ask_llm(
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        seed=seed,
        system_prompt=system_prompt
    )
