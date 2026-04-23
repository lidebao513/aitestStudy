"""
统一 LLM 客户端

该模块提供了与多种大语言模型交互的功能，支持：
1. 本地 Ollama (deepseek-r1:7b) - 优先使用
2. DeepSeek API - 作为 Ollama 不可用时的备选方案

配置优先级：
- OLLAMA_BASE_URL: Ollama 服务地址，默认为 http://localhost:11434
- OLLAMA_MODEL: Ollama 模型名称，默认为 deepseek-r1:7b
- DEEPSEEK_API_KEY: DeepSeek API 密钥（仅在使用 DeepSeek API 时需要）
"""

import os
import httpx
from typing import Optional

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:7b")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")

LLM_TIMEOUT = 300.0


def check_ollama_available() -> bool:
    """
    检查 Ollama 服务是否可用

    :return: True 如果 Ollama 服务正在运行且可访问
    """
    try:
        response = httpx.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=LLM_TIMEOUT)
        return response.status_code == 200
    except Exception:
        return False


def call_ollama(prompt: str,
                temperature: float = 0.0,
                max_tokens: int = 200,
                seed: Optional[int] = None,
                system_prompt: Optional[str] = None) -> tuple[str, str, int]:
    """
    调用本地 Ollama 模型

    :param prompt: 用户问题或指令
    :param temperature: 随机性控制，0=确定性输出
    :param max_tokens: 最大输出长度
    :param seed: 随机种子，配合 temperature=0 实现可复现输出
    :param system_prompt: 系统级指令
    :return: (回答内容, 结束原因, Token消耗) 三元组
    """
    from openai import OpenAI

    client = OpenAI(
        api_key="ollama",
        base_url=OLLAMA_BASE_URL + "/v1",
        timeout=LLM_TIMEOUT
    )

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    extra_params = {}
    if seed is not None:
        extra_params["seed"] = seed
    if temperature > 0:
        extra_params["temperature"] = temperature

    response = client.chat.completions.create(
        model=OLLAMA_MODEL,
        messages=messages,
        max_tokens=max_tokens,
        **extra_params
    )

    message = response.choices[0].message
    answer = message.content or ""
    if not answer and hasattr(message, 'reasoning') and message.reasoning:
        answer = message.reasoning
    finish_reason = response.choices[0].finish_reason or "stop"
    total_tokens = response.usage.total_tokens if response.usage else 0

    return answer, finish_reason, total_tokens


def call_deepseek_api(prompt: str,
                      temperature: float = 0.0,
                      max_tokens: int = 200,
                      seed: Optional[int] = None,
                      system_prompt: Optional[str] = None) -> tuple[str, str, int]:
    """
    调用 DeepSeek API

    :param prompt: 用户问题或指令
    :param temperature: 随机性控制，0=确定性输出
    :param max_tokens: 最大输出长度
    :param seed: 随机种子，配合 temperature=0 实现可复现输出
    :param system_prompt: 系统级指令
    :return: (回答内容, 结束原因, Token消耗) 三元组
    """
    from openai import OpenAI

    if not DEEPSEEK_API_KEY:
        raise ValueError("❌ 未找到环境变量 DEEPSEEK_API_KEY")

    client = OpenAI(
        api_key=DEEPSEEK_API_KEY,
        base_url="https://api.deepseek.com",
        timeout=LLM_TIMEOUT
    )

    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    extra_params = {}
    if seed is not None:
        extra_params["seed"] = seed

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
        **extra_params
    )

    answer = response.choices[0].message.content
    finish_reason = response.choices[0].finish_reason
    total_tokens = response.usage.total_tokens

    return answer, finish_reason, total_tokens


def ask_llm(prompt: str,
            temperature: float = 0.0,
            max_tokens: int = 200,
            seed: Optional[int] = None,
            system_prompt: Optional[str] = None,
            prefer_local: bool = True) -> tuple[str, str, int]:
    """
    统一的 LLM 调用接口，自动选择 Ollama 或 DeepSeek API

    默认优先使用本地 Ollama (deepseek-r1:7b)，如果不可用则自动切换到 DeepSeek API。

    :param prompt: 用户问题或指令
    :param temperature: 随机性控制，0=确定性输出，值越大输出越随机
    :param max_tokens: 最大输出长度，控制生成内容的长度
    :param seed: 随机种子，配合 temperature=0 实现完全可复现的输出
    :param system_prompt: 系统级指令，定义 AI 行为边界和角色
    :param prefer_local: 是否优先使用本地 Ollama，默认为 True
    :return: (回答内容, 结束原因, Token消耗) 三元组
    """
    if prefer_local and check_ollama_available():
        try:
            return call_ollama(
                prompt=prompt,
                temperature=temperature,
                max_tokens=max_tokens,
                seed=seed,
                system_prompt=system_prompt
            )
        except Exception as e:
            print(f"⚠️ Ollama 调用失败: {e}")
            print(f"🔄 切换到 DeepSeek API...")

    if DEEPSEEK_API_KEY:
        return call_deepseek_api(
            prompt=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            seed=seed,
            system_prompt=system_prompt
        )
    else:
        raise ValueError("❌ Ollama 不可用且未找到 DEEPSEEK_API_KEY 环境变量")


def get_provider_info() -> dict:
    """
    获取当前可用的 LLM 提供者信息

    :return: 包含提供者信息的字典
    """
    ollama_ok = check_ollama_available()
    deepseek_ok = bool(DEEPSEEK_API_KEY)

    if ollama_ok:
        primary = "Ollama"
        primary_model = OLLAMA_MODEL
    else:
        primary = "DeepSeek API"
        primary_model = "deepseek-chat"

    return {
        "ollama_available": ollama_ok,
        "deepseek_api_available": deepseek_ok,
        "primary_provider": primary,
        "primary_model": primary_model,
        "ollama_base_url": OLLAMA_BASE_URL,
        "ollama_model": OLLAMA_MODEL
    }
