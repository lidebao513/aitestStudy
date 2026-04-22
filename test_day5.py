import numpy as np
import ollama  # 导入 ollama 库，替代 sentence_transformers

# --- 任务 5.1 (保持不变) ---
vec = np.array([1, 2, 3])
print(f"向量: {vec}")
print(f"向量形状: {vec.shape}")
print(f"向量长度: {np.linalg.norm(vec):.4f}")  # 这里修正了之前代码中 ':.4f' 的位置

# --- 任务 5.2 & 5.3 (改造为 Ollama 实现) ---

# 模型名称，确保你已经在终端执行了 ollama pull shaw/dmeta-embedding-zh
model_name = "shaw/dmeta-embedding-zh"

# 1. 定义一个函数，用于获取文本的向量
def get_embedding_ollama(text):
    """使用 Ollama 的 dmeta-embedding-zh 模型将文本转换为向量"""
    try:
        response = ollama.embed(model=model_name, input=text)
        embedding = response['embeddings'][0]
        return np.array(embedding)  # 确保返回的是 NumPy 数组，方便后续计算
    except Exception as e:
        print(f"调用 Ollama 时发生错误: {e}")
        return None

# 2. 定义测试文本
text = "AI测试工程师"
text_a = "我喜欢吃苹果"
text_b = "我喜欢吃香蕉"
text_c = "今天天气真好"

# 3. 获取向量表示
emb = get_embedding_ollama(text)
emb_a = get_embedding_ollama(text_a)
emb_b = get_embedding_ollama(text_b)
emb_c = get_embedding_ollama(text_c)

# 打印向量信息（任务 5.2）
if emb is not None:
    print(f"\n文本: '{text}'")
    print(f"向量维度: {emb.shape[0]}")  # 预期输出：1024 维
    print(f"向量前5个值: {emb[:5]}")

# 4. 定义手动余弦相似度计算函数（任务 5.3 核心）
def cosine_similarity_manual(vec1, vec2):
    """手动实现余弦相似度计算"""
    dot_product = np.dot(vec1, vec2)
    norm1 = np.linalg.norm(vec1)
    norm2 = np.linalg.norm(vec2)
    if norm1 == 0 or norm2 == 0:
        return 0.0  # 处理零向量除零错误
    return dot_product / (norm1 * norm2)

# 5. 计算并打印相似度
if emb_a is not None and emb_b is not None and emb_c is not None:
    sim_ab = cosine_similarity_manual(emb_a, emb_b)
    sim_ac = cosine_similarity_manual(emb_a, emb_c)
    print(f"\n句子A vs 句子B 相似度: {sim_ab:.4f}") # 预期是一个较高的值
    print(f"句子A vs 句子C 相似度: {sim_ac:.4f}") # 预期是一个较低的值


# ===== 任务 5.4：模拟 AI 测试断言 =====
print("\n" + "=" * 40)
print("任务 5.4：AI 测试断言模拟")
print("=" * 40)

# 模拟一个测试用例
expected_answer = "2"
actual_answer = "1 + 1 等于 2"

# 获取向量
emb_expected = get_embedding_ollama(expected_answer)
emb_actual = get_embedding_ollama(actual_answer)

if emb_expected is not None and emb_actual is not None:
    similarity = cosine_similarity_manual(emb_expected, emb_actual)
    threshold = 0.5  # 相似度阈值

    print(f"预期答案: '{expected_answer}'")
    print(f"实际回答: '{actual_answer}'")
    print(f"语义相似度: {similarity:.4f}")

    if similarity >= threshold:
        print("✅ 断言通过：回答与预期语义一致")
    else:
        print("❌ 断言失败：回答与预期偏差过大")

# ===== 任务 5.5：NumPy 统计分析 =====
print("\n" + "=" * 40)
print("任务 5.5：Bad Case 统计与模型漂移监控")
print("=" * 40)

# 1. 模拟一批 Bad Case 的相似度分数（值越低说明回答越差）
bad_case_scores = np.array([0.12, 0.08, 0.35, 0.21, 0.05])
print(f"\nBad Case 相似度样本: {bad_case_scores}")
print(f"  均值: {np.mean(bad_case_scores):.4f}")
print(f"  标准差: {np.std(bad_case_scores):.4f}")
print(f"  最低分: {np.min(bad_case_scores):.4f}")

# 2. 模型漂移简易监控：对比基线相似度分布和新数据分布
np.random.seed(42)  # 固定随机种子，让结果可复现
baseline = np.random.normal(0.75, 0.1, 1000)   # 上线初期的相似度分布（均值0.75）
current = np.random.normal(0.68, 0.12, 1000)   # 最近的相似度分布（均值0.68）

print(f"\n基线相似度均值: {np.mean(baseline):.4f}")
print(f"当前相似度均值: {np.mean(current):.4f}")

if np.mean(current) < np.mean(baseline) - 0.05:
    print("⚠️ 警告：当前模型相似度均值显著下降，可能存在效果漂移，建议排查！")
else:
    print("✅ 模型相似度分布稳定，无明显漂移。")