import pytest
from ai_client import ask_deepseek

def test_temperature_zero_consistency():
    """验证 temperature=0 时回答高度一致"""
    prompt = "1+1等于几？只回答数字"
    ans1,_,_ =ask_deepseek(prompt ,temperature= 0.0, max_tokens=20)
    ans2,_,_ =ask_deepseek(prompt ,temperature= 0.0, max_tokens=20)
    assert ans1.strip() == ans2.strip(),f"回答不一致：'{ans1}' vs '{ans2}'"

def test_seed_reproducibility():
    """验证固定 seed 后输出可复现"""
    prompt = "说一个水果名字"
    seed = 42
    ans1,_,_ =ask_deepseek(prompt ,seed=seed, max_tokens=20,temperature= 0.0)
    ans2,_,_ =ask_deepseek(prompt ,seed=seed, max_tokens=20,temperature= 0.0)
    assert ans1 == ans2,"相同seed 但输出不同"

def test_max_tokens_truncation():
    """验证 max_tokens 过小导致截断"""
    prompt = "写一首关于春天的短诗"
    ans ,finish_reason ,tokens = ask_deepseek(prompt ,max_tokens=5 ,temperature= 0.0)
    assert finish_reason == "length",f" 预期截断，但 finish_reason = {finish_reason}"
    assert tokens <= 15,f"token消耗异常 {tokens}"
