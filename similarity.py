import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import jieba

warnings.filterwarnings('ignore', message="The parameter 'token_pattern' will not be used")

vectorizer = TfidfVectorizer(
    tokenizer=jieba.lcut,
    token_pattern=None
)

def compute_similarity(text1: str, text2: str) -> float:
    try:
        tfidf_matrix = vectorizer.fit_transform([text1, text2])
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return float(similarity)
    except Exception as e:
        print(f"计算相似度时出错: {e}")
        return 0.0