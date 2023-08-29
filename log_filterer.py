import json
from fuzzywuzzy import fuzz

def read_jsonl(filename):
    with open(filename, 'r') as f:
        for line in f:
            yield json.loads(line)

def write_jsonl(data, filename):
    with open(filename, 'w') as f:
        for entry in data:
            f.write(json.dumps(entry) + '\n')

def is_similar(str1, str2, threshold=90):
    return fuzz.ratio(str1, str2) > threshold

def main():
    input_file = 'production_logs.jsonl'
    output_file = 'filtered_logs.jsonl'
    
    logs = list(read_jsonl(input_file))
    unique_logs = []
    seen_messages = []

    for log in logs:
        message = log["message"]
        if not any(is_similar(message, seen_msg) for seen_msg in seen_messages):
            unique_logs.append(log)
            seen_messages.append(message)
    
    write_jsonl(unique_logs, output_file)
    print(f"Finished writing unique logs to {output_file}")

if __name__ == "__main__":
    main()
