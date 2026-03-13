import re
import json5

file_path = "amazontesting_raw.txt"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Extract the JS object assigned to dataToReturn
match = re.search(r'var\s+dataToReturn\s*=\s*({[\s\S]*?})\s*;', content)

if not match:
    print("dataToReturn not found")
    exit()

json_text = match.group(1)
json_text = re.sub(r'"\s*\+\s*"', '', json_text)
json_text = re.sub(r',(\s*[}\]])', r'\1', json_text)
json_text = json_text.replace("\n", " ")
data = json5.loads(json_text)

print("Parsed successfully")
print(data["dimensions"])
print(data["dimensionValuesDisplayData"])