import os
import json
import requests

# Step 1: Read the content of 'rulesets.txt'
rulesets_file = '../rule/rulesets.txt'
try:
    with open(rulesets_file, 'r', encoding='utf-8') as file:
        rulesets_content = file.readlines()
except FileNotFoundError:
    print(f"File '{rulesets_file}' not found. Please upload the file.")
    raise

# Step 2: Extract URLs from the content
urls = [line.split(',')[1].strip() for line in rulesets_content if ',' in line and not line.startswith(';')]

# Step 3: Create the directory to store downloaded files
temp_rules_dir = 'temp_rules'
os.makedirs(temp_rules_dir, exist_ok=True)

# Step 4: Function to parse individual rule files
def parse_rules(file_content):
    rule_types = ['domain', 'domain_keyword', 'domain_suffix', 'ip_cidr']
    rules = {rule_type: [] for rule_type in rule_types}
    
    for line in file_content.splitlines():
        line = line.strip()
        if line.startswith('#') or not line:
            continue
        
        # Split the line based on comma
        parts = line.split(',')
        rule_type = parts[0].lower()
        domain_or_ip = parts[1]

        # Store relevant types
        if rule_type in rules:
            rules[rule_type].append(domain_or_ip)
    
    return rules

# Step 5: Download the files, parse them, and convert to JSON
for url in urls:
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Save the content to the temp_rules directory
            file_name = os.path.join(temp_rules_dir, os.path.basename(url))
            with open(file_name, 'w', encoding='utf-8') as f:
                f.write(response.text)
            
            # Parse the content
            parsed_rules = parse_rules(response.text)
            
            # Format the rules into JSON
            rules_json = {
                "version": 2,
                "rules": [
                    {
                    "domain": parsed_rules['domain'],
                    "domain_keyword": parsed_rules['domain_keyword'],
                    "domain_suffix": parsed_rules['domain_suffix'],
                    "ip_cidr": parsed_rules['ip_cidr']
                    }
                ]
            }
            
            # Save the JSON file
            json_output_file = os.path.join(temp_rules_dir, os.path.basename(url).replace('.list', '.json'))
            with open(json_output_file, 'w', encoding='utf-8') as json_file:
                json.dump(rules_json, json_file, indent=2)
            
            print(f"JSON file generated: {json_output_file}")
        else:
            print(f"Failed to download file from {url}")
    except Exception as e:
        print(f"Error processing {url}: {e}")


