import os
import pandas as pd
import requests
import numpy as np
import pickle
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.cluster import AffinityPropagation
from sklearn.metrics.pairwise import cosine_similarity
from tqdm import tqdm

class RuleProcessor:
    def __init__(self, input_filename, response_filename, embedding_filename):
        self.input_filename = input_filename
        self.response_filename = response_filename
        self.embedding_filename = embedding_filename

    def read_data(self):
        self.df = pd.read_csv(self.input_filename)

    def check_responses(self):
        try:
            return pd.read_csv(self.response_filename)
        except FileNotFoundError:
            return pd.DataFrame(columns=['RuleContent', 'Response'])
    def ask_openai_common(self, prompt):
        api_key = os.getenv("OPENAI_API_KEY")
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        data = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        response = requests.post('https://api.openai.com/v1/chat/completions', headers=headers, json=data)
        response_json = response.json()
        if 'choices' not in response_json:
            return ''
        return response_json['choices'][0]['message']['content']

    def get_embeddings(self, text):
        api_key = os.getenv("OPENAI_API_KEY")
        response = requests.post(
            "https://api.openai.com/v1/embeddings",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "text-embedding-3-large",
                "input": text
            }
        )
        response_json = response.json()
        return response_json['data'][0]['embedding']
    def check_embeddings(self):
        try:
            with open(self.embedding_filename, 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return {}

    def process_rules(self):
        self.read_data()
        try:
            responses_df = pd.read_csv(self.response_filename)
            with open(self.embedding_filename, 'rb') as f:
                embeddings = pickle.load(f)
        except FileNotFoundError:
            responses_df = pd.DataFrame(columns=['RuleContent', 'Response'])
            embeddings = {}

        for _, row in tqdm(self.df.iterrows(), total=self.df.shape[0], desc="Processing rules"):
            rule_content = row['RuleContent']
            if rule_content in embeddings:
                continue  # Skip processing if already done
            response = responses_df[responses_df['RuleContent'] == rule_content]['Response'].iloc[0] if rule_content in responses_df['RuleContent'].values else ''
            if not response:
                prompt = f"{rule_content} Use 1-2 sentences to tell me what this rule/invariant needs to be verified. Do not involve specific function names or contract names."
                response = self.ask_openai_common(prompt)
                responses_df = responses_df.append({'RuleContent': rule_content, 'Response': response}, ignore_index=True)
            embeddings[rule_content] = self.get_embeddings(response) if response else np.zeros(3072)

        responses_df.to_csv(self.response_filename, index=False)
        with open(self.embedding_filename, 'wb') as f:
            pickle.dump(embeddings, f)

        embedding_list = list(embeddings.values())
        similarity_matrix = cosine_similarity(embedding_list)

        # Clustering
        clustering = AffinityPropagation(damping=0.5, preference=-75, random_state=5)
        labels = clustering.fit_predict(similarity_matrix)

        # Visualizing Clusters
        pca = PCA(n_components=2)
        X_r = pca.fit_transform(embedding_list)
        unique_clusters = np.unique(labels)
        colors = plt.cm.tab20(np.linspace(0, 1, len(unique_clusters)))
        lw = 2

        for cluster_id, color in zip(unique_clusters, colors):
            plt.scatter(X_r[labels == cluster_id, 0], X_r[labels == cluster_id, 1],
                        color=color, alpha=0.8, lw=lw, label=f'Cluster {cluster_id}')

        plt.legend(loc='best', shadow=False, scatterpoints=1, title='Clusters')
        # plt.title('Affinity Propagation Clustering of Rules')
        plt.xlabel('PCA Dimension 1')
        plt.ylabel('PCA Dimension 2')
        plt.savefig('rule_classification/category_of_spec/cluster_visualization.pdf')  # Save the figure to a file
        plt.show()


        # Creating the results DataFrame
        result_df = pd.DataFrame({
            'RuleContent': list(embeddings.keys()),
            'Response': [responses_df[responses_df['RuleContent'] == rc]['Response'].iloc[0] for rc in embeddings.keys()],
            'ClusterLabel': labels
        })

        result_df.to_csv('rule_classification/category_of_spec/processed_cluster.csv', index=False)
        return labels


# Example usage
processor = RuleProcessor('rule_classification/category_of_spec/combied_output_train_all_with_functionality.csv', 
                          'rule_classification/category_of_spec/combied_output_train_all_with_functionality_responses.csv', 
                          'rule_classification/category_of_spec/embeddings.pkl')
cluster_labels = processor.process_rules()
print(cluster_labels)
