#!/bin/bash

# Specify your input file
input_file="operator-components.yaml"

# Check if the file exists
if [[ ! -f "$input_file" ]]; then
    echo "Error: File '$input_file' not found!"
    exit 1
fi

# Initialize a counter for naming each split CRD file
counter=1

# Read the input file and split only at CRDs
awk '
/^kind: CustomResourceDefinition/ {
    if (out) close(out); 
    out="crd_split_" counter ".yaml"; 
    counter++;
} 
{if (out) print > out}' "$input_file"

echo "CRD resources have been split successfully."
