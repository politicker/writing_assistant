import csv
import json

def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"{m.role}: {m.content[0].text.value}")
    print()

def show_json(obj):
    # Convert JSON string to a Python dictionary
    parsed_json = json.loads(obj.model_dump_json())
    # Pretty print the JSON
    print(json.dumps(parsed_json, indent=4, sort_keys=True))

def csv_to_json(csv_file, jsonl_file):
    with open(csv_file, mode='r', encoding='utf-8') as csvf, open(jsonl_file, mode='w', encoding='utf-8') as jsonlf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            jsonlf.write(json.dumps(row) + '\n')

