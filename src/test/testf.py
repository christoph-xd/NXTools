import re

text = r"""
Using SALT_subsystem_legacy_CLT
Found library using image directory
Using the library
D:\Siemens\NX2212.6000\nxbin\salt_clt.dll
app set SALT_LICENSE_SERVER=28000@LocalHost

************** License Server/File Information **************

 Server/File                      : 28000@LocalHost
 License File Sold To / Install   : 10082189 - JANUS Engineering AG
 License File Webkey Access Code  : 7161LDEU7A
 License File Issuer              : SIEMENS
 License File Type                : No Type
 Flexera Daemon Version           : 11.19
 Vendor Daemon Version            : 11.1 SALT v2.1.0.0

*************************************************************
"""

# Define the regular expression pattern
pattern = r"License File Sold To \/ Install\s+:\s+(.+)"

# Search for the pattern in the text
match = re.search(pattern, text)

# Extract the value from the matched group
if match:
    license_sold_to = match.group(1)
    print(license_sold_to)
else:
    print("Value not found.")
