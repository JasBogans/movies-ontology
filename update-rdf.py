import requests
import re

# URL of the RDF file
url = "https://raw.githubusercontent.com/JasBogans/movies-ontology/main/ontology.rdf"

# New base URI
new_base_uri = "https://raw.githubusercontent.com/JasBogans/movies-ontology/main/ontology"

# Download the file
response = requests.get(url)
content = response.text

# Define the old URI pattern
old_uri_pattern = r"http://www\.ime\.usp\.br/~renata/FOAF-modified"

# Function to replace URIs
def replace_uri(match):
    old_uri = match.group(0)
    # Remove the FOAF-modified part and add '#' if needed
    new_uri = new_base_uri
    if old_uri.endswith("FOAF-modified"):
        return new_uri
    return f"{new_uri}#{old_uri.split('FOAF-modified')[-1]}"

# Replace all occurrences of the old URI
updated_content = re.sub(old_uri_pattern, replace_uri, content)

# Update the xml:base attribute
updated_content = re.sub(
    r'xml:base="http://www\.ime\.usp\.br/~renata/FOAF-modified"',
    f'xml:base="{new_base_uri}"',
    updated_content
)

# Update the default namespace
updated_content = re.sub(
    r'xmlns="http://www\.ime\.usp\.br/~renata/FOAF-modified"',
    f'xmlns="{new_base_uri}#"',
    updated_content
)

# Update custom namespace if it exists
updated_content = re.sub(
    r'xmlns:renata="http://www\.ime\.usp\.br/~renata/"',
    f'xmlns:renata="{new_base_uri}/"',
    updated_content
)

# Update comments
updated_content = re.sub(
    r'<!-- http://www\.ime\.usp\.br/~renata/FOAF-modified([a-zA-Z]+) -->',
    lambda m: f'<!-- {new_base_uri}#{m.group(1)} -->',
    updated_content
)

# Save the updated content to a new file
with open("updated_ontology.rdf", "w", encoding="utf-8") as f:
    f.write(updated_content)

print("Updated RDF file has been saved as 'updated_ontology.rdf'")