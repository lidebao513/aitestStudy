import pandas as pd

df = pd.read_excel("test_cases.xlsx")

print(df)
print(df.columns.tolist())
print(df.iloc[0])
print("\n===== 逐行遍历用例 =====")
for index, row in df.iterrows():
    case_id =row['case_id']
    prompt = row['prompt']
    expected = row['expected_keyword']
    print(f"{case_id} 问题 {prompt} 预期关键字 {expected}")

    test_case = df.to_dict('records')

    print(f"共有{len(test_case)}条用例")
    print(f"第一条用例数据{test_case[0]}")