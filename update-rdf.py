import requests
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom

# URL of the RDF file
url = "https://raw.githubusercontent.com/JasBogans/movies-ontology/main/ontology.rdf"

# New base URI
new_base_uri = "https://raw.githubusercontent.com/JasBogans/movies-ontology/main/ontology"

# Download the file
response = requests.get(url)
content = response.text

# Parse the XML
ET.register_namespace('', f"{new_base_uri}#")
ET.register_namespace('rdf', "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
ET.register_namespace('owl', "http://www.w3.org/2002/07/owl#")
ET.register_namespace('xml', "http://www.w3.org/XML/1998/namespace")
ET.register_namespace('xsd', "http://www.w3.org/2001/XMLSchema#")
ET.register_namespace('rdfs', "http://www.w3.org/2000/01/rdf-schema#")
ET.register_namespace('vs', "http://www.w3.org/2003/06/sw-vocab-status/ns#")
ET.register_namespace('wot', "http://xmlns.com/wot/0.1/")
ET.register_namespace('foaf', "http://xmlns.com/foaf/0.1/")
ET.register_namespace('dc', "http://purl.org/dc/elements/1.1/")

root = ET.fromstring(content)

# Update xml:base
root.set('{http://www.w3.org/XML/1998/namespace}base', new_base_uri)

# Function to update URIs
def update_uri(uri):
    if uri.startswith("http://www.ime.usp.br/~renata/FOAF-modified"):
        return f"{new_base_uri}#{uri.split('FOAF-modified')[-1]}"
    return uri

# Update all URIs in the XML
for elem in root.iter():
    for attr in list(elem.attrib.keys()):
        if isinstance(elem.attrib[attr], str) and elem.attrib[attr].startswith("http://www.ime.usp.br/~renata/FOAF-modified"):
            elem.set(attr, update_uri(elem.attrib[attr]))

# Convert the ElementTree to a string
xml_str = ET.tostring(root, encoding="unicode", method="xml")

# Pretty print the XML
dom = minidom.parseString(xml_str)
pretty_xml = dom.toprettyxml(indent="  ")

# Remove empty lines
pretty_xml = '\n'.join([line for line in pretty_xml.split('\n') if line.strip()])

# Save the updated content to a new file
with open("updated_ontology.rdf", "w", encoding="utf-8") as f:
    f.write(pretty_xml)

print("Updated RDF file has been saved as 'updated_ontology.rdf'")