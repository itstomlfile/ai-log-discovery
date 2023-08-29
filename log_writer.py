import json
import random
from datetime import datetime

# Constants
NUM_EXECUTIONS = 100000
LOG_FILE = "production_logs.jsonl"

def validate_file(file_name, file_size, num_lines, file_data):
    """
    Simulated file validation function.
    Returns a status string based on various checks.
    """
    valid_extensions = [".txt", ".csv", ".json"]
    extension = file_name.split('.')[-1] if '.' in file_name else ""
    
    if extension not in valid_extensions:
        return "INVALID_EXTENSION"
    
    if not file_name.startswith("data_"):
        return "INVALID_NAME_CONVENTION"
    
    if file_size < 5 * 1024 or file_size > 10 * 1024 * 1024:  # 5KB to 10MB
        return "INVALID_FILE_SIZE"
    
    if num_lines < 50 or num_lines > 10000:
        return "INVALID_LINE_COUNT"
    
    if "HEADER" not in file_data or "FOOTER" not in file_data:
        return "MISSING_DATA_FIELDS"
    
    return "VALID"

def log_message(message, log_type="INFO"):
    """
    Create a log message in JSON format.
    """
    log = {
        "timestamp": datetime.now().isoformat(),
        "type": log_type,
        "message": message
    }
    return log

def main():
    with open(LOG_FILE, "w") as log_file:
        for _ in range(NUM_EXECUTIONS):
            file_name = f"data_{random.randint(1, 5000)}.{random.choice(['txt', 'csv', 'json', 'xml'])}"
            file_size = random.randint(1, 15 * 1024 * 1024)  # 1B to 15MB
            num_lines = random.randint(1, 15000)
            file_data = random.choice(["HEADER", "DATA", "FOOTER", "JUNK"])

            validation_result = validate_file(file_name, file_size, num_lines, file_data)
            
            if validation_result == "VALID":
                log_file.write(json.dumps(log_message(f"'{file_name}' is valid.")) + "\n")
            else:
                log_file.write(json.dumps(log_message(f"Validation failed for '{file_name}': {validation_result}", "ERROR")) + "\n")
            
            # Occasionally log some other random operational messages.
            if random.random() < 0.05:  # 5% chance
                log_file.write(json.dumps(log_message("Connection to database re-established.")) + "\n")
            elif random.random() < 0.02:  # 2% chance
                log_file.write(json.dumps(log_message("Server health is optimal.")) + "\n")
            elif random.random() < 0.01:  # 1% chance
                log_file.write(json.dumps(log_message("Unexpected shutdown detected!", "ERROR")) + "\n")

if __name__ == "__main__":
    main()
