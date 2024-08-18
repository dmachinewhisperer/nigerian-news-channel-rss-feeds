import json
import csv

with open('../sites-validated.json', 'r') as file:
    json_data = json.load(file)

#flatten the data
flattened_data = []
for entry in json_data['data']:
    flattened_entry = {
        'id': entry['id'],
        'name': entry['name'],
        'base': entry['base'],
        'feed': entry['feed'],
        'type': entry['info']['type'],
        'reputation': entry['info']['reputation'],
        'status': entry['info']['status'],
        'latency': entry['info']['latency']
    }
    flattened_data.append(flattened_entry)

#write flattened data to a new CSV file
with open('../sites.csv', 'w', newline='') as csvfile:
    fieldnames = ['id', 'name', 'base', 'feed', 'type', 'reputation', 'status', 'latency']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(flattened_data)

print("Data has been successfully flattened and saved to 'sites.csv'.")
