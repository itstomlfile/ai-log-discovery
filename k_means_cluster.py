import json
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

# Load logs from file
def load_logs(file_name):
    logs = []
    with open(file_name, 'r') as file:
        for line in file:
            logs.append(json.loads(line))
    return logs

logs = load_logs("vectorized_logs.jsonl")

# Extract vectors for clustering
vectors = [log['vector'] for log in logs]

# Determine the optimal number of clusters using silhouette score
best_k = 2
best_score = -1

for k in range(2, 11):  # Searching for best k in range 2 to 10
    kmeans = KMeans(n_clusters=k, random_state=42).fit(vectors)
    silhouette_avg = silhouette_score(vectors, kmeans.labels_)
    if silhouette_avg > best_score:
        best_score = silhouette_avg
        best_k = k

print(f"Optimal number of clusters: {best_k}")

# Cluster data with best_k
kmeans = KMeans(n_clusters=best_k, random_state=42).fit(vectors)

# Assign logs to clusters
clustered_logs = {}
for i, label in enumerate(kmeans.labels_):
    if label not in clustered_logs:
        clustered_logs[label] = []
    clustered_logs[label].append(logs[i]['message'])


# Print clustered logs
for cluster, log_entries in clustered_logs.items():
    print(f"Cluster {cluster}:")
    for entry in log_entries:
        print(f"  - {entry}")
    print("\n")
