import re


string = "DATA |     HLD001_00001  | 1 | 1 | 0 | 3 | 0.00000 | 0.00000 | 0.00000 |  Small collet"

result = re.search(r"^\s*DATA\s* \| ([^|]+) \| \d+ \|", string)

if result:
    extracted_text = result.group(1).strip()
    print(extracted_text)
else:
    print("Match not found.")
