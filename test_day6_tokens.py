from ai_client import ask_deepseek

prompt = "请用一段话介绍中国长城"

print("==============MAX Token 边界值测试===================")
for limit in [10,30,100]:
    ans, finish_reason,tokens = ask_deepseek(prompt ,max_tokens=limit ,temperature= 0.0)
    print(f"限制 {limit} tokens | 实际消耗: {tokens} | 结束原因: {finish_reason}")
    print(f"回答: {ans[:50]}...\n") 

    '''
    测试场景：在你的自动化用例中，应增加对 finish_reason 的断言，当预期是完整回答时，必须要求 finish_reason="stop"。
    '''
