import pandas as pd
import spacy
from sklearn.cluster import AffinityPropagation
from sklearn.metrics import pairwise_distances

# 加载spaCy模型
nlp = spacy.load('en_core_web_sm')

# 加载数据
df = pd.read_csv('src/vector_db/basic_data/processed_name.csv')

# 提取需要的列
texts = df['cleaned_name'].values

# 生成嵌入向量
embeddings = [nlp(text).vector for text in texts]

# 计算相似度矩阵，这里使用余弦相似度
similarity_matrix = 1 - pairwise_distances(embeddings, metric='cosine')

# 执行Affinity Propagation聚类
clustering = AffinityPropagation(affinity='precomputed', damping=0.5)
labels = clustering.fit_predict(similarity_matrix)

# 将聚类结果添加到原始DataFrame中
df['cluster'] = labels

# 输出聚类结果
print(df[['SpecHash', 'cleaned_name', 'cluster']])
df.to_csv('src/vector_db/category_of_spec/processed_cluster.csv', index=False)
