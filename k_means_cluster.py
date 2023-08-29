import json
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer

def read_logs_from_file(filename):
    logs = []
    with open(filename, "r") as file:
        for line in file:
            logs.append(json.loads(line))
    return logs

def cluster_logs(logs, num_clusters=10):
    log_messages = [entry['message'] for entry in logs]
    
    # Convert log messages to TF-IDF vectors
    vectorizer = TfidfVectorizer(max_df=0.85)
    tfidf_matrix = vectorizer.fit_transform(log_messages)
    
    # Cluster the logs using K-means algorithm
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)
    
    clustered_logs = {}
    for i, label in enumerate(kmeans.labels_):
        if label not in clustered_logs:
            clustered_logs[label] = []
        clustered_logs[label].append(logs[i]['message'])
    
    return clustered_logs

def extract_unique_logs(clustered_logs):
    return [log_entries[0] for log_entries in clustered_logs.values()]

def write_logs_to_file(logs, filename):
    with open(filename, "w") as outfile:
        for log_message in logs:
            json.dump({"message": log_message}, outfile)
            outfile.write('\n')

if __name__ == "__main__":
    input_filename = "vectorized_logs.jsonl"
    output_filename = "unique_logs.jsonl"
    
    logs = read_logs_from_file(input_filename)
    clustered_logs = cluster_logs(logs)
    unique_logs = extract_unique_logs(clustered_logs)
    write_logs_to_file(unique_logs, output_filename)