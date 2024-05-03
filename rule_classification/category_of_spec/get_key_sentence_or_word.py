import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.luhn import LuhnSummarizer

def extract_keywords_tfidf(texts):
    # 初始化TF-IDF Vectorizer
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(texts)
    feature_names = vectorizer.get_feature_names_out()
    
    # 汇总每个词的TF-IDF分数
    tfidf_scores = tfidf_matrix.sum(axis=0).A1
    importance = dict(zip(feature_names, tfidf_scores))
    
    # 按TF-IDF分数降序排序
    important_words = sorted(importance.items(), key=lambda x: x[1], reverse=True)
    return important_words[:10]  # 返回前5个最重要的词

def extract_summary(text):
    parser = PlaintextParser.from_string(text, Tokenizer('english'))
    summarizer = LuhnSummarizer()
    summary = summarizer(parser.document, 3)  # 提取3个关键句
    return ' '.join([sentence._text for sentence in summary])

def main():
    # 读取CSV文件
    df = pd.read_csv('rule_classification/category_of_spec/processed_cluster.csv')  # 请替换为你的文件路径
    
    # 按ClusterLabel分组
    grouped = df.groupby('ClusterLabel')
    
    # 对每个聚类处理
    for label, group in grouped:
        responses = group['Response'].tolist()
        combined_text = ' '.join(responses)
        
        print(f"Cluster {label}:")
        print("Top 5 TF-IDF Keywords:", extract_keywords_tfidf(responses))
        
        # 使用sumy提取关键句
        print("Luhn Summary:")
        print(extract_summary(combined_text))
        print("\n")

if __name__ == '__main__':
    main()
