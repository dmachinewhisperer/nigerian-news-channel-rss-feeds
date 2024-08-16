import json
import requests
import time
import argparse
from datetime import datetime
from jsonschema import validate, ValidationError

#template for schema validation
schema = {
    "type": "object",
    "properties": {
        "metadata": {"type": "object"},
        "data": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "integer"},
                    "name": {"type": "string"},
                    "base": {"type": "string"},
                    "feed": {"type": ["string", "null"]},
                    "info": {
                        "type": "object",
                        "properties": {
                            "type": {"type": "string"},
                            "reputation": {"type": "string"},
                            "status": {"type": "string"},
                            "latency": {"type": ["number", "null"]}
                        },
                        "required": ["type", "reputation", "status", "latency"]
                    }
                },
                "required": ["id", "name", "base", "feed", "info"]
            }
        }
    },
    "required": ["metadata", "data"]
}

def log(message, verbose):
    if verbose:
        print(message)

def validate_json(data, verbose):
    log("Validating schema...", verbose)
    try:
        validate(instance=data, schema=schema)
        log("Looks good.", verbose)
        log("Schema Validation Done", verbose)
        return True
    except ValidationError as e:
        print(f"JSON is not valid. Error: {e}")
        return False

def check_url(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False

def validate_links(data, verbose):
    log("Validating link states", verbose)
    live_count = 0
    stale_count = 0

    for entry in data['data']:
        #check base URL
        is_live = check_url(entry['base'])
        status = 'live' if is_live else 'stale'
        entry['info']['status'] = status
        
        if is_live:
            live_count += 1
        else:
            stale_count += 1

        #check RSS feed if it exists
        latency = None
        if entry['feed']:
            try:
                start_time = time.time()
                requests.get(entry['feed'], timeout=10)
                latency = round((time.time() - start_time) * 1000, 2)  #convert to ms
            except requests.RequestException:
                pass
        
        entry['info']['latency'] = latency
        
        log(f"Checking {entry['name']}, {entry['base']}...{status}, latency = {latency if latency is not None else 'N/A'}ms", verbose)

    #metadata
    data['metadata']['live entry count'] = live_count
    data['metadata']['all entry count'] = live_count + stale_count
    data['metadata']['last link validation'] = datetime.now().strftime("%d-%m-%y %H:%M:%S")
    latencies = [entry['info']['latency'] for entry in data['data'] if entry['info']['latency'] is not None]
    data['metadata']['avg latency'] = round(sum(latencies) / len(latencies), 2) if latencies else None

    log("Link state validation Done", verbose)
    return data

def main(verbose):
    with open('sites.json', 'r') as f:
        data = json.load(f)

    if not validate_json(data, verbose):
        return

    updated_data = validate_links(data, verbose)

    log("Updating metadata and writing files", verbose)
    with open('sites-validated.json', 'w') as f:
        json.dump(updated_data, f, indent=4)

    log("Done", verbose)
    
    #metadata
    print("\nMetadata:")
    for key, value in updated_data['metadata'].items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validator")
    parser.add_argument("-v", "--verbose", action="store_true", help="Increase output verbosity")
    args = parser.parse_args()

    main(args.verbose)