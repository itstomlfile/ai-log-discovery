import gensim
import json
import re

def tokenize_log(log):
    """
    Tokenize a log entry into words, numbers, and special characters.
    """
    return re.findall(r'\w+|\S', log)

def log_to_vector(log, model):
    """
    Convert a log entry into an embedding using a pretrained Word2Vec or FastText model.
    If a word/token from the log does not exist in the model's vocabulary, it's skipped.
    Returns the average vector of all tokens in the log.
    """
    tokens = tokenize_log(log)
    tokens = [token for token in tokens if token in model.wv]

    if not tokens:
        return [0] * model.vector_size

    vector = sum([model.wv[token] for token in tokens]) / len(tokens)
    return vector

def read_logs(filename):
    """
    Read and return log messages from the provided filename.
    """
    logs = []
    with open(filename, 'r') as file:
        for line in file:
            log_entry = json.loads(line)
            message = log_entry.get("message", "")
            logs.append(message)
    return logs

def train_word2vec_model(logs):
    """
    Train a Word2Vec model on the provided logs.
    """
    tokenized_logs = [tokenize_log(log) for log in logs]
    model = gensim.models.Word2Vec(sentences=tokenized_logs, vector_size=100, window=5, min_count=1, workers=4)
    model.train(tokenized_logs, total_examples=len(tokenized_logs), epochs=10)
    return model

# Define model file name
model_filename = "processed_logs.model"

# Try to load the pretrained model or train a new one
try:
    model = gensim.models.Word2Vec.load(model_filename)
except FileNotFoundError:
    print("Model not found. Training a new model on the provided logs...")
    logs = read_logs("production_logs.jsonl")
    model = train_word2vec_model(logs)
    model.save(model_filename)
    print(f"Model saved as {model_filename}")


def process_logs(input_filename, output_filename, model):
    """
    Process logs from input file and write vectorized representation to output file.
    """
    logs = read_logs(input_filename)
    with open(output_filename, 'w') as outfile:
        for message in logs:
            vector = log_to_vector(message, model)

            # Write the vector representation to the output file
            outfile.write(json.dumps({"message": message, "vector": vector.tolist()}) + '\n')


# Process logs and write vectorized representation
process_logs("production_logs.jsonl", "vectorized_logs.jsonl", model)
