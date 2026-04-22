from concurrent.futures import thread
import pandas as pd
from ai_client import ask_deepseek
from similarity import compute_similarity

# 1. 读取 Excel 用例
df = pd.read_excel("test_cases.xlsx")

# # 2. 新增结果列
df['actual_response'] = ''
df['finish_reason'] = ''
df['total_tokens'] = 0
df['assert_result'] = ''
df['assert_detail'] = ''

# 3. 遍历执行
for index, row in df.iterrows():
    case_id = row['case_id']
    prompt = row['prompt']
    expected = row['expected_keyword'] 

    print(f"正在执行 [{case_id}] ...")

    try:
        answer, finish_reason, tokens = ask_deepseek(prompt)
        df.at[index, 'actual_response'] = answer
        df.at[index, 'finish_reason'] = finish_reason
        df.at[index, 'total_tokens'] = tokens

        similarity_score = compute_similarity(prompt, answer)
        threshold = 0.5  # 可以根据需要调整阈值
        if similarity_score > threshold:
            df.at[index, 'assert_result'] = 'PASS'
        else:
            df.at[index, 'assert_result'] = 'FAIL'
            df.at[index, 'assert_detail'] = f"相似度得分 {similarity_score:.4f}，低于阈值 {threshold}"

        df.at[index, 'similarity_score'] = similarity_score       # 将预期关键词转为字符串（兼容数字、浮点数等）
        # expected_str = str(expected)
        

    except Exception as e:
        df.at[index, 'assert_result'] = 'ERROR'
        df.at[index, 'assert_detail'] = f"发生错误: {str(e)}"

print("\n✅ 所有用例执行完毕！")

# 4. 回写结果
output_file = "test_results.xlsx"
df.to_excel(output_file, index=False)
print(f"📁 测试报告已生成：{output_file}")