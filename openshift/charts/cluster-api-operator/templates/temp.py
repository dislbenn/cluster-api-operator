import os
import yaml

# Specify your input file
input_file = "operator-components.yaml"
crd_dir = "crds"
resources_dir = "resources"

# Check if the file exists
if not os.path.isfile(input_file):
    print(f"Error: File '{input_file}' not found!")
    exit(1)

# Create directories if they do not exist
os.makedirs(crd_dir, exist_ok=True)
os.makedirs(resources_dir, exist_ok=True)

# Read the input file and split only at CRDs
with open(input_file, 'r') as file:
    documents = file.read().split('---')  # Split on the YAML document separator

    for doc in documents:
        doc = doc.strip()  # Remove leading and trailing whitespace
        if not doc:
            continue  # Skip empty documents

        # Load the YAML document
        try:
            resource = yaml.safe_load(doc)
        except yaml.YAMLError as e:
            print(f"Error parsing YAML document: {e}")
            continue

        # Determine the resource type
        if isinstance(resource, dict):
            kind = resource.get('kind')
            # Check if the kind is CustomResourceDefinition
            if kind == 'CustomResourceDefinition':
                # Extract the CRD name for the output file
                crd_name = resource['metadata']['name']
                output_file = os.path.join(crd_dir, f"{crd_name}.yaml")
                with open(output_file, 'w') as output:
                    yaml.dump(resource, output, default_flow_style=False)
                print(f"Created CRD: {output_file}")
            else:
                # For other resources
                resource_name = resource['metadata']['name']
                output_file = os.path.join(resources_dir, f"{resource_name}.yaml")
                with open(output_file, 'w') as output:
                    yaml.dump(resource, output, default_flow_style=False)
                print(f"Created Resource: {output_file}")

print("Resources have been split into 'crds' and 'resources' directories successfully.")
